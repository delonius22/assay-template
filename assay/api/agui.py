"""AG-UI protocol layer (S9): maps the runner's step progress onto an event stream.

Build these in order (from the build order in src/assay/api/agui.py):
    AnswerReply, DecisionReply, BriefReply, ContinueReply, SessionView,
    interrupt_for, resume_value, session_view, start_from_props,
    check_service_call, run_events, encode_stream

Spec coverage: S9.1-S9.7. The runner publishes one RunProgress per node and one
terminal event per run; this module turns that into AG-UI events (run/step/
state) and pauses the run as standard AG-UI interrupts, so the Node service can
render and resume it without knowing Assay's shapes.
"""
import asyncio
import hmac
import queue
import re
from typing import Any

from ag_ui.core import (
    Interrupt,
    RunAgentInput,
    RunErrorEvent,
    RunFinishedEvent,
    RunFinishedInterruptOutcome,
    RunFinishedSuccessOutcome,
    RunStartedEvent,
    StateSnapshotEvent,
    StepFinishedEvent,
    StepStartedEvent,
)
from ag_ui.encoder import EventEncoder
from pydantic import BaseModel, Field, ValidationError

from ..domain.models import Brief, now
from ..settings import Settings
from .runner import RunProgress

SERVICE_TOKEN_HEADER = "X-Assay-Service-Token"
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{2,39}$")


class AnswerReply(BaseModel):
    """A question-kind resume (grill, map, seams, ticket, brief-fix, DoD)."""

    text: str = Field(min_length=1)


class DecisionReply(BaseModel):
    """An approval-kind resume: a decision plus optional text/brief."""

    decision: str
    text: str = ""
    brief: Brief | None = None


class BriefReply(BaseModel):
    """A mode-3 resume that must carry the brief."""

    brief: Brief


class ContinueReply(BaseModel):
    """A 'continue without a fixed input' resume (await_answers)."""


# Which reply shape validates a resume for each pause kind (S9.3).
REPLY_MODELS: dict[str, type[BaseModel]] = {
    "question": AnswerReply,
    "map_review": AnswerReply,
    "brief_fix": AnswerReply,
    "await_answers": ContinueReply,
    "dod_question": AnswerReply,
    "approval": DecisionReply,
    "seams": DecisionReply,
    "ticket_review": DecisionReply,
}


class SessionView(BaseModel):
    """The part of a session the AG-UI client needs (never the raw log)."""

    slug: str
    title: str
    mode: int
    pm: str
    stage: str
    files: list[str]
    agenda: list[str]
    q_round: int


def _message_for(pause: dict) -> str:
    """The interrupt's human message: the question when present, else a phrase."""
    q = pause.get("question") or pause.get("challenge") or ""
    if q:
        return str(q)
    return {
        "approval": "Approve the PRD or send it back.",
        "seams": "Review the seams.",
        "ticket_review": "Review the ticket plan.",
    }.get(str(pause.get("kind")), "Assay needs input to continue.")


def interrupt_for(pause: dict, interrupt_id: str) -> Interrupt:
    """Build the AG-UI interrupt for an open Assay pause.

    Spec: S9.2 | Traces to: I18

    Build steps:
    1. Task: Set the interrupt ID to the one Assay already has for the pause;
       when Assay re-sends the same pause, it uses the same ID.
       Expected outcome: the client can match a resume to an interrupt.
    2. Task: Set the reason to the pause's kind, its message to the question or a short
       phrase for the other kinds, and its response schema to the matching reply model's
       JSON schema.
       Expected outcome: the client renders the right input.
    3. Task: Put every other pause field in metadata.
       Expected outcome: nothing from the pause is lost.
    """
    kind = str(pause.get("kind", ""))
    schema = REPLY_MODELS.get(kind)
    return Interrupt(
        id=interrupt_id,
        reason=kind,
        message=_message_for(pause),
        response_schema=schema.model_json_schema() if schema else None,
        metadata={k: v for k, v in pause.items() if k != "kind"},
    )


def _field(entry: Any, name: str, default: Any = None) -> Any:
    if isinstance(entry, dict):
        return entry.get(name, default)
    return getattr(entry, name, default)


def resume_value(entries, pause: dict, interrupt_id: str, user: str) -> dict:
    """Validate a resume against the pause's reply model and return the resume value.

    Spec: S9.3 | Traces to: I18, I12

    Build steps:
    1. Task: Find the entry for the open interrupt; refuse when none does.
       Expected outcome: resumes name the interrupt they answer.
    2. Task: Treat a `cancelled` status as the open question about cancel semantics:
       resolve with the spec owner before implementing; logged as OQ-1 in BUILD_ORDER.md.
       Expected outcome: no invented cancel behavior.
    3. Task: Validate the payload against the reply model for the pause's kind; refuse when
       the payload is missing what the model requires.
       Expected outcome: a bad answer does not resume the run.
    4. Task: Return the resume value with keys `text`, `user`, `decision`, and `brief`.
       Expected outcome: the runner's resume contract.
    """
    kind = pause.get("kind")
    match = next((e for e in (entries or []) if _field(e, "interrupt_id") == interrupt_id), None)
    if match is None:
        raise ValueError(f"no resume entry for interrupt {interrupt_id!r}")
    if _field(match, "status", "resolved") == "cancelled":
        raise ValueError("cancel is not defined for an Assay pause (OQ-1)")
    model = REPLY_MODELS.get(kind)
    if model is None:
        raise ValueError(f"unknown pause kind {kind!r}")
    try:
        reply = model.model_validate(_field(match, "payload", {}) or {})
    except ValidationError as exc:
        raise ValueError(str(exc)) from exc
    brief = getattr(reply, "brief", None)
    return {
        "text": getattr(reply, "text", "") or "",
        "user": user,
        "decision": getattr(reply, "decision", None),
        "brief": brief.model_dump() if brief is not None else None,
    }


def session_view(slug: str, values: dict | None) -> SessionView:
    """Convert saved session values into the SessionView the client renders.

    Spec: S9.4 | Traces to: I12

    Build steps:
    1. Task: Take slug, title, mode, PM, stage, files, agenda, and the question round from
       the values.
       Expected outcome: enough to render the session list and header.
    2. Task: Never include the raw session log.
       Expected outcome: the snapshot stays small.
    """
    values = values or {}
    return SessionView(
        slug=slug,
        title=str(values.get("title") or ""),
        mode=int(values.get("mode") or 1),
        pm=str(values.get("pm") or ""),
        stage=str(values.get("stage") or ""),
        files=list(values.get("files") or []),
        agenda=list(values.get("agenda") or []),
        q_round=int(values.get("q_round") or 0),
    )


def start_from_props(runner, store, thread_id: str, props: dict, user: str) -> None:
    """Start a new session from the forwarded props.

    Spec: S9.5 | Traces to: I12

    Build steps:
    1. Task: Read title, mode, PM (defaulting to the user), and optional brief from the
       props; raise ValueError when title is missing, mode is not 1 to 3, or mode 3 has no
       brief.
       Expected outcome: a bad start is refused before it runs.
    2. Task: Register the session in the store's `sessions` namespace with title, creator,
       and time; start the runner with the initial state.
       Expected outcome: the session exists and is working.
    """
    props = props or {}
    title = str(props.get("title") or "")
    mode = int(props.get("mode") or 0)
    pm = str(props.get("pm") or user)
    brief_in = props.get("brief")
    if not title:
        raise ValueError("props need a title")
    if not 1 <= mode <= 3:
        raise ValueError("mode must be 1, 2, or 3")
    brief = None
    if brief_in is not None:
        brief = Brief.model_validate(brief_in)
    if mode == 3 and brief is None:
        raise ValueError("mode 3 needs a brief")
    store.put(("sessions",), thread_id, {"title": title, "created_by": user, "created_at": now()})
    runner.start(_initial_state(thread_id, title, mode, pm, brief, user))


def _initial_state(thread_id, title, mode, pm, brief, user):
    from ..graph.state import AssayState  # local: avoid a heavy import cycle at module load
    return AssayState(slug=thread_id, title=title, mode=mode, pm=pm, brief=brief, created_by=user)


def check_service_call(headers, settings: Settings) -> str:
    """Check that the caller is the Node service and return the acting user.

    Spec: S9.6 | Traces to: I17

    Build steps:
    1. Task: Compare the `X-Assay-Service-Token` header to the settings' service token in
       constant time; raise PermissionError on a missing or wrong token.
       Expected outcome: only the service can run AG-UI runs.
    2. Task: Read the user header from the settings; raise PermissionError when it is empty.
       Expected outcome: every run records an acting user.
    """
    configured = settings.service_token
    provided = headers.get(SERVICE_TOKEN_HEADER, "") if configured else ""
    if not configured or not provided or not hmac.compare_digest(provided, configured):
        raise PermissionError("bad service token")
    user = (headers.get(settings.user_header, "") or "").strip()
    if not user:
        raise PermissionError("missing user header")
    return user


def _pending_interrupts(runner, slug: str):
    """The open pauses from the checkpoint, as (LangGraph id, pause dict) pairs."""
    snap = runner.app.get_state(runner.config(slug))
    out = []
    for task in snap.tasks:
        for item in task.interrupts:
            out.append((item.id, item.value))
    return out


async def _progress(runner, q):
    """Yield the runner's progress events for a thread, never blocking the loop."""
    while True:
        try:
            ev = await asyncio.to_thread(q.get, timeout=60)
        except queue.Empty:
            break
        yield ev
        if isinstance(ev, RunProgress) and ev.kind == "ended":
            break


async def run_events(runner, store, run_input: RunAgentInput, user: str):
    """Emit the AG-UI events for one run, resuming or starting as the request says.

    Spec: S9.4, S9.5 | Traces to: I7, I18

    Build steps:
    1. Task: Emit the run started event, then subscribe to the runner's progress events.
       Expected outcome: the first step event is never missed.
    2. Task: Decide the action: a new thread starts a session from the forwarded props; a
       waiting session with resume entries resumes with the validated value; a waiting
       session without them re-sends its open interrupt and finishes without running
       anything.
       Expected outcome: one request maps to exactly one Assay action.
    3. Task: Emit step started and step finished for each progress event, and a state
       snapshot of the session view after each finished step, waiting for queue items
       without blocking the event loop.
       Expected outcome: the client renders progress live.
    4. Task: When the run ends, emit run finished with the outcome: an interrupt for a
       pause (with the interrupt's ID and schema), a success when the agenda is done, or
       run error when the step raised.
       Expected outcome: the client knows exactly how to continue.
    5. Task: Always unsubscribe from the runner when the stream closes.
       Expected outcome: no subscriber leak.
    """
    thread = run_input.thread_id
    props = run_input.forwarded_props or {}
    resume_entries = run_input.resume or []

    yield RunStartedEvent(thread_id=thread, run_id=run_input.run_id)
    q = runner.subscribe(thread)
    try:
        values = (runner.app.get_state(runner.config(thread)).values) or {}
        pending = _pending_interrupts(runner, thread)
        try:
            if not values:
                start_from_props(runner, store, thread, props, user)
            elif pending and resume_entries:
                value = resume_value(resume_entries, pending[0][1], pending[0][0], user)
                runner.resume(thread, value)
            elif pending:
                yield RunFinishedEvent(
                    thread_id=thread, run_id=run_input.run_id,
                    outcome=RunFinishedInterruptOutcome(
                        type="interrupt",
                        interrupts=[interrupt_for(pending[0][1], pending[0][0])]),
                )
                return
            else:
                yield RunFinishedEvent(
                    thread_id=thread, run_id=run_input.run_id,
                    outcome=RunFinishedSuccessOutcome(type="success"))
                return
        except ValueError as exc:
            yield RunErrorEvent(message=str(exc))
            return

        outcome, error = "finish", None
        async for ev in _progress(runner, q):
            if not isinstance(ev, RunProgress):
                continue
            if ev.kind == "step_started":
                yield StepStartedEvent(step_name=ev.node)
            elif ev.kind == "step_finished":
                yield StepFinishedEvent(step_name=ev.node)
                cur = (runner.app.get_state(runner.config(thread)).values) or {}
                yield StateSnapshotEvent(snapshot=session_view(thread, cur).model_dump())
            elif ev.kind == "ended":
                outcome, error = ev.outcome, ev.error
                break

        pending2 = _pending_interrupts(runner, thread)
        if outcome == "error" or error:
            yield RunErrorEvent(message=str(error) or "the run ended with an error")
        elif pending2:
            iid, pause = pending2[0]
            yield RunFinishedEvent(
                thread_id=thread, run_id=run_input.run_id,
                outcome=RunFinishedInterruptOutcome(
                    type="interrupt", interrupts=[interrupt_for(pause, iid)]))
        else:
            yield RunFinishedEvent(
                thread_id=thread, run_id=run_input.run_id,
                outcome=RunFinishedSuccessOutcome(type="success"))
    finally:
        runner.unsubscribe(thread, q)


def encode_stream(events, accept: str | None):
    """Wrap an async event iterator as an SSE stream (one data line per event).

    Spec: S9.7 | Traces to: I7

    Build steps:
    1. Task: Build an EventEncoder honoring the Accept header, and yield one encoded data
       line per event.
       Expected outcome: the response is a server-sent-event stream.
    """
    encoder = EventEncoder(accept=accept or None)

    async def gen():
        async for ev in events:
            yield encoder.encode(ev)

    return gen()
