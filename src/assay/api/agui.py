"""Serve Assay over AG-UI: runs as events, pauses as standard interrupts.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C7 Live, standard interaction. Any AG-UI client, CopilotKit
included, can start a session, watch each step, and act on each pause. This file
translates runs and replies to and from AG-UI; it never runs workflow logic.

Why this comes now: The runner publishes progress (29). The app (31) mounts this
endpoint.

Build order: Step 30 of 33.
Previous: src/assay/api/runner.py (step 29), which runs sessions in the background
and publishes each run's progress.
Next: src/assay/api/app.py (step 31), which serves the REST API and the AG-UI
endpoint.

Build these in order:
    1. AnswerReply: first reply shape.
    2. DecisionReply: second reply shape.
    3. BriefReply: third reply shape.
    4. ContinueReply: fourth reply shape.
    5. SessionView: the snapshot shape.
    6. interrupt_for: the first mapping.
    7. resume_value: the reverse mapping.
    8. session_view: used in every snapshot.
    9. start_from_props: before run_events can stream a new session.
    10. check_service_call: every AG-UI call passes this first.
    11. run_events: the heart of the endpoint.
    12. encode_stream: the last step before the route.

Depends on:
    assay.api.runner: BusyError, Runner, RunProgress. Driving runs and receiving
    progress.
    assay.domain.models: Brief, now. Briefs in forwarded props and timestamps.
    assay.graph.state: AssayState. New sessions.
    assay.settings: Settings. The service token and user header.
    Standard library: asyncio, hmac, re, collections.abc, typing.
    Third-party: ag-ui-protocol, langgraph, pydantic.

Depended on by:
    assay.api.app: the /agui route.

Spec coverage: S9.2, S9.3, S9.4, S9.5, S9.6, S9.7 | Traces to: I7, I12, I17, I18
"""

import asyncio
import hmac
import re
from collections.abc import AsyncIterator, Mapping
from typing import Literal

from ag_ui.core import (
    BaseEvent,
    Interrupt,
    ResumeEntry,
    RunAgentInput,
    RunErrorEvent,
    RunFinishedEvent,
    RunStartedEvent,
    StateSnapshotEvent,
    StepFinishedEvent,
    StepStartedEvent,
)
from ag_ui.encoder import EventEncoder
from langgraph.store.base import BaseStore
from pydantic import BaseModel, Field, ValidationError

from assay.api.runner import BusyError, Runner, RunProgress
from assay.domain.models import Brief, now
from assay.graph.state import AssayState
from assay.settings import Settings


class AnswerReply(BaseModel):
    """The reply to a question pause.

    Problem piece: C6 and C7: what a client sends to answer.

    Why it matters: Each pause kind has one reply shape; its schema travels with the
                    interrupt so clients can validate before sending (I18).

    What: The answer text.

    Spec: S9.2 | Ticket: — | Traces to: —
    """

    text: str = Field(min_length=1)


class DecisionReply(BaseModel):
    """The reply to an approval or review pause.

    Problem piece: C6 and C7: approve or request changes.

    Why it matters: Approval, seams, and ticket review all decide between approving
                    and changing.

    What: A decision and optional change text.

    Spec: S9.2 | Ticket: — | Traces to: —
    """

    decision: Literal["approve", "changes"]
    text: str = ""


class BriefReply(BaseModel):
    """The reply to a brief-fix pause.

    Problem piece: C6 and C7: the PM's corrected brief.

    Why it matters: Only the PM fixes the brief; the reply carries the whole brief.

    What: The corrected brief.

    Spec: S9.2 | Ticket: — | Traces to: —
    """

    brief: Brief


class ContinueReply(BaseModel):
    """The reply to a waiting pause.

    Problem piece: C6 and C7: continue when answers are in.

    Why it matters: Waiting for answers needs only a signal, not content.

    What: No fields.

    Spec: S9.2 | Ticket: — | Traces to: —
    """


REPLY_MODELS: dict[str, type[BaseModel]] = {  # S9.2: pause kind -> reply shape
    "question": AnswerReply,
    "dod_question": AnswerReply,
    "map_review": AnswerReply,
    "brief_fix": BriefReply,
    "await_answers": ContinueReply,
    "approval": DecisionReply,
    "seams": DecisionReply,
    "ticket_review": DecisionReply,
}
SERVICE_TOKEN_HEADER = "X-Assay-Service-Token"  # S9.6
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{2,39}$")  # S9.5: same rule as S8.3


class SessionView(BaseModel):
    """What a client sees in each state snapshot.

    Problem piece: C7: progress without exposing the whole session.

    Why it matters: The full state includes logs and drafts; clients need only what
                    the page shows.

    What: Slug, title, mode, PM, stage, files, agenda, and questionnaire round.

    Spec: S9.4 | Ticket: — | Traces to: —
    """

    slug: str
    title: str
    mode: int
    pm: str
    stage: str
    files: list[str] = Field(default_factory=list)
    agenda: list[str] = Field(default_factory=list)
    q_round: int = 0


def interrupt_for(pause: Mapping[str, object], interrupt_id: str) -> Interrupt:
    """Return the AG-UI interrupt for one pause.

    Problem piece: C7: every pause as a standard interrupt (D12).

    Why it matters: CopilotKit renders standard interrupts and resolves them by ID.
                    The ID must stay the same when a pause is re-sent, so it reuses
                    LangGraph's own interrupt ID; the schema lets the client
                    validate replies.

    What: An Interrupt whose ID is the LangGraph interrupt ID, reason the pause
          kind, message a short line, response schema the reply model's JSON schema,
          and metadata the pause's other fields.

    Spec: S9.2 | Ticket: 12 | Traces to: I18

    Build steps:
    1. Task: Use the LangGraph interrupt ID as the ID and the pause's kind as the
             reason.
       Think about: Why must re-sending a pause keep its ID?
       Expected outcome: The same pause re-sent has the same ID.
    2. Task: Set the message to the question text when there is one, else a short
             phrase for the kind; set the response schema from the kind's reply
             model; put every other pause field in metadata.
       Expected outcome: An approval interrupt's schema requires 'decision'.
    """
    raise NotImplementedError("S9.2: interrupt_for")


def resume_value(
    entries: list[ResumeEntry], pause: Mapping[str, object], interrupt_id: str, user: str
) -> dict[str, object]:
    """Validate a client's resume entry and convert it to the resume value contract.

    Problem piece: C6 and C7: only valid replies reach the graph (I18).

    Why it matters: A client rendering a form from the schema is not a guarantee;
                    the payload comes from outside and must be validated on the
                    server before it resumes a session.

    What: Finds the entry for the open interrupt, validates its payload against the
          kind's reply model, and returns the resume value with keys text, user,
          decision, and brief.

    Spec: S9.3 | Ticket: 12 | Traces to: I18, I12

    Raises:
        ValueError: no entry for the open interrupt, or a payload that does not
        match its reply model.

    Build steps:
    1. Task: Find the entry whose interrupt ID matches the open pause; refuse when
             none does.
       Expected outcome: An entry for an unknown interrupt ID is refused.
    2. Task: Open question (spec silent): what a 'cancelled' resume entry should do
             to an Assay session.
       Expected outcome: Resolve with the spec owner before implementing; logged as
                         OQ-1 in BUILD_ORDER.md.
    3. Task: Validate the payload against the kind's reply model, refusing with the
             validation errors.
       Expected outcome: An approval payload without 'decision' is refused.
    4. Task: Return text, the user, decision, and brief (as plain data) from the
             validated reply, leaving fields the reply lacks empty.
       Expected outcome: An AnswerReply becomes a value with text and user.
    """
    raise NotImplementedError("S9.3: resume_value")


def session_view(slug: str, values: Mapping[str, object]) -> SessionView:
    """Return the client's view of a session.

    Problem piece: C7: progress the page can show.

    Why it matters: Snapshots must reveal only what the page needs, never drafts or
                    logs. Sending the whole state would leak draft text and log
                    entries to every browser that watches a session.

    What: A SessionView from the saved values. Called as session_view(slug: str,
          values: Mapping[str, object]) and returns SessionView.

    Spec: S9.4 | Ticket: 12 | Traces to: I12

    Build steps:
    1. Task: Build a SessionView from the slug and the saved values' title, mode,
             PM, stage, files, agenda, and round, with empty defaults.
       Expected outcome: A snapshot never contains the log.
    """
    raise NotImplementedError("S9.4: session_view")


def start_from_props(
    runner: Runner, store: BaseStore, thread_id: str, props: Mapping[str, object], user: str
) -> None:
    """Create a session from an AG-UI run on a new thread.

    Problem piece: C7: sessions start from any AG-UI client.

    Why it matters: A CopilotKit client starts a session by opening a thread; the
                    same validation as the REST endpoint must apply so neither path
                    is weaker.

    What: Validates the thread ID as a slug and the forwarded title, mode, brief,
          and PM; registers the session; starts it.

    Spec: S9.5 | Ticket: 12 | Traces to: I12

    Raises:
        ValueError: a bad slug, a missing title, a mode outside 1 to 3, or mode 3
        without a brief.

    Build steps:
    1. Task: Validate the thread ID with the SLUG pattern and the forwarded title
             (at least 3 characters), mode (1 to 3), and brief (required for mode 3,
             validated as a Brief).
       Expected outcome: Mode 3 without a brief is refused.
    2. Task: Register the session in the store's 'sessions' namespace with title,
             creator, and time, then start it with the PM defaulting to the user.
       Expected outcome: The session appears in the session list.
    """
    raise NotImplementedError("S9.5: start_from_props")


def check_service_call(headers: Mapping[str, str], settings: Settings) -> str:
    """Accept a call only from the Node service; return the user it vouches for.

    Problem piece: C7: browsers never reach Python directly (I17).

    Why it matters: The Node service authenticates users through SSO; Python trusts
                    its user header only when the call proves it came from that
                    service. A constant-time comparison avoids leaking the token
                    through timing.

    What: Compares the service token header with the configured token in constant
          time and returns the user header.

    Spec: S9.6 | Ticket: 13 | Traces to: I17

    Raises:
        PermissionError: no token configured, a wrong token, or no user header.

    Build steps:
    1. Task: Refuse when no service token is configured or the header's token
             differs, comparing in constant time.
       Think about: Why does ordinary string equality leak information?
       Expected outcome: A wrong token is refused.
    2. Task: Return the user from the configured user header, refusing when it is
             empty.
       Expected outcome: A correct token with a user returns that user.
    """
    raise NotImplementedError("S9.6: check_service_call")


async def run_events(
    runner: Runner, store: BaseStore, run_input: RunAgentInput, user: str
) -> AsyncIterator[BaseEvent]:
    """Translate one run into AG-UI events.

    Problem piece: C7: live steps and standard pauses.

    Why it matters: The client sees progress as it happens instead of polling. The
                    run itself belongs to the runner, so a disconnect stops only the
                    stream, never the step (S8.2).

    What: Run started; then the session is started, resumed, or (when waiting with
          no resume) its open interrupt re-sent; step events and snapshots stream as
          progress arrives; run finished with an interrupt or success outcome, or
          run error.

    Spec: S9.4, S9.5 | Ticket: 12 | Traces to: I7, I18

    Build steps:
    1. Task: Emit run started with the thread and run IDs, then subscribe to the
             session's progress before starting anything.
       Think about: Why subscribe before starting?
       Expected outcome: The first step event is never missed.
    2. Task: Decide the action: a new thread starts a session from the forwarded
             props; a waiting session with resume entries resumes with the validated
             value; a waiting session without them re-sends its open interrupt and
             finishes without running anything.
       Expected outcome: Re-requesting a waiting session runs no step.
    3. Task: Emit step started and step finished for each progress event, and a
             state snapshot of the session view after each finished step, waiting
             for queue items without blocking the event loop.
       Expected outcome: Each node produces a start, a finish, and a snapshot.
    4. Task: When the run ends, emit run finished with outcome 'interrupt' and the
             interrupt for the new pause, or 'success' when finished; on error emit
             run error with the message; always unsubscribe.
       Expected outcome: A run reaching a pause ends with outcome interrupt.
    """
    raise NotImplementedError("S9.4: run_events")


async def encode_stream(events: AsyncIterator[BaseEvent], accept: str | None) -> AsyncIterator[str]:
    """Encode events for the client's accepted content type.

    Problem piece: C7: a stream any AG-UI client reads.

    Why it matters: AG-UI clients accept server-sent events by default; the
                    protocol's encoder handles the format so the endpoint never
                    hand-writes it.

    What: Each event encoded by the AG-UI encoder for the accept header, in order.
          Awaited as encode_stream(events: AsyncIterator[BaseEvent], accept: str |
          None) and returns AsyncIterator[str].

    Spec: S9.7 | Ticket: 12 | Traces to: I7

    Build steps:
    1. Task: Encode each event with the protocol's encoder for the given accept
             header and yield it.
       Expected outcome: Each event arrives as one 'data:' line.
    """
    raise NotImplementedError("S9.7: encode_stream")
