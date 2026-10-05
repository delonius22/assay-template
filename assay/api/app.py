"""FastAPI app.

    uvicorn --factory assay.api.app:create_app --workers 1     (or: assay serve)

Route wiring, the 501 handler, and startup are complete. Each route calls a
handler below; the handlers are stubbed (S8.3 to S8.5). Until persistence
(S7.2) is built, the server still starts and every API call answers 501
naming the missing S-ID (decision D7).
"""
import logging
import re
from contextlib import asynccontextmanager
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Literal

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, JSONResponse
from pydantic import BaseModel, Field

from ..domain.ids import question_ids
from ..domain.models import Answer, Brief, ResponseSheet, now
from ..graph.build import build_graph
from ..graph.context import AppContext
from ..graph.state import AssayState
from ..settings import Settings, load_settings, missing_config
from ..store.persistence import Persistence, open_persistence
from .auth import user_from
from .runner import Busy, Runner

STATIC = Path(__file__).resolve().parent / "static"
SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{2,39}$")
log = logging.getLogger("assay.api")


class NewSession(BaseModel):
    slug: str
    title: str = Field(min_length=3)
    mode: Literal[1, 2, 3]
    brief: Brief | None = None
    pm: str = Field("", description="Product manager; defaults to the signed-in user")


class Reply(BaseModel):
    text: str = ""
    decision: Literal["approve", "changes"] | None = None
    brief: Brief | None = None


class Responses(BaseModel):
    role: str
    answers: list[Answer]
    comments: str = ""


@dataclass
class Services:
    """Everything the handlers need. Filled at startup. (Complete.)"""
    settings: Settings
    persistence: Persistence | None = None
    runner: Runner | None = None
    graph: Any = None
    test_model: Any = None


def ready(svc: Services) -> Runner:
    """The runner, or a 501 naming persistence when it is not built yet. (Complete.)"""
    if svc.runner is None:
        raise NotImplementedError("S7.2")
    return svc.runner


def values(svc: Services, slug: str) -> dict:
    """Saved state of one session, or 404. (Complete.)"""
    v = ready(svc).app.get_state(Runner.config(slug)).values
    if not v:
        raise HTTPException(404, f"No session '{slug}'.")
    return v


# ------------------------------------------------------------------ handlers (S8.3)
def handle_me(svc: Services, user: str) -> dict:
    """Spec: S8.3 | Ticket: 02 | Traces to: I8

    Build steps:
    1. Task: Return `{"user": user, "approver": not svc.settings.approvers or user in svc.settings.approvers,
       "missing_config": [] if svc.test_model else missing_config(svc.settings),
       "backend": svc.persistence.backend if svc.persistence else "none"}`.
       Expected outcome: the UI knows who is signed in and whether they can approve.
    """
    raise NotImplementedError("S8.3")


def handle_list(svc: Services) -> list[dict]:
    """Spec: S8.3 | Ticket: 02 | Traces to: I6

    Build steps:
    1. Task: `items = svc.persistence.store.search(("sessions",), limit=500)`.
       Expected outcome: the session registry.
    2. Task: Return `sorted([{**i.value, **ready(svc).status(i.key)} for i in items],
       key=lambda r: r.get("created_at", ""), reverse=True)`.
       Expected outcome: newest first, each with live status.
    """
    raise NotImplementedError("S8.3")


def handle_create(svc: Services, body: NewSession, user: str) -> dict:
    """Spec: S8.3 | Ticket: 02 | Traces to: I12

    Build steps:
    1. Task: If `not SLUG.match(body.slug)` raise `HTTPException(422, "Slug: 3 to 40 lowercase letters, digits, or hyphens.")`;
       if `svc.persistence.store.get(("sessions",), body.slug)` raise `HTTPException(409, f"Session '{body.slug}' already exists.")`;
       if `body.mode == 3 and not body.brief` raise `HTTPException(422, "Mode 3 needs the ask, the why, and the outcome.")`.
       Expected outcome: bad input fails at the boundary.
    2. Task: `svc.persistence.store.put(("sessions",), body.slug, {"title": body.title, "created_by": user, "created_at": now()})`.
       Expected outcome: the session appears in the list.
    3. Task: `ready(svc).start(AssayState(slug=body.slug, title=body.title, pm=body.pm or user, mode=body.mode,
       brief=body.brief, created_by=user))`; return `ready(svc).status(body.slug)`.
       Expected outcome: the first step runs; the UI polls status.
    """
    raise NotImplementedError("S8.3")


def handle_get(svc: Services, slug: str) -> dict:
    """Spec: S8.3 | Ticket: 02 | Traces to: I6

    Build steps:
    1. Task: `st = ready(svc).status(slug)`; if `st["status"] == "missing"` raise `HTTPException(404, f"No session '{slug}'.")`.
       Expected outcome: unknown slugs are 404.
    2. Task: Return `st`.
       Expected outcome: status, pending pause, files.
    """
    raise NotImplementedError("S8.3")


def handle_reply(svc: Services, slug: str, body: Reply, user: str) -> dict:
    """Spec: S8.3 | Ticket: 02, 05 | Traces to: I8, I12

    Build steps:
    1. Task: `st = ready(svc).status(slug)`; if `st["status"] != "waiting"` raise
       `HTTPException(409, f"Session is {st['status']}, not waiting for an answer.")`.
       Expected outcome: answers only land on a pause.
    2. Task: If `st["pending"]["kind"] == "approval" and body.decision == "approve" and svc.settings.approvers and
       user not in svc.settings.approvers`, raise `HTTPException(403, "Only a named approver can approve the PRD.")`.
       Expected outcome: I8 enforced at the boundary (the node checks again).
    3. Task: `value = {"text": body.text, "user": user, "decision": body.decision,
       "brief": body.brief.model_dump() if body.brief else None}`; call `ready(svc).resume(slug, value)`,
       mapping `Busy` to `HTTPException(409, "This session is already working on a step.")`; return `ready(svc).status(slug)`.
       Expected outcome: the resume value contract in SPECS ## Data shapes.
    """
    raise NotImplementedError("S8.3")


def handle_retry(svc: Services, slug: str) -> dict:
    """Spec: S8.3 | Ticket: 02 | Traces to: I6

    Build steps:
    1. Task: Call `ready(svc).retry(slug)`, mapping `Busy` to `HTTPException(409, "This session is already working on a step.")`.
       Expected outcome: continues from the last saved step.
    2. Task: Return `ready(svc).status(slug)`.
       Expected outcome: the UI shows working.
    """
    raise NotImplementedError("S8.3")


# ------------------------------------------------------------------ handlers (S8.4)
def handle_questionnaire(svc: Services, slug: str) -> dict:
    """Spec: S8.4 | Ticket: 08 | Traces to: I12

    Build steps:
    1. Task: `v = values(svc, slug)`; `q, rnd = v.get("questionnaire"), v.get("q_round", 0)`; if `not q` raise
       `HTTPException(404, "This session has no questionnaire.")`.
       Expected outcome: only mode 3 sessions have one.
    2. Task: `ids = question_ids(q, rnd)`; return `{"title": v["title"], "round": rnd, "brief": v.get("brief"),
       "questions": [{"id": qid, **item.model_dump(), "follow_ups": [{"id": f"{qid}{chr(97 + j)}", **f.model_dump()}
       for j, f in enumerate(item.follow_ups)]} for qid, item in zip(ids, q.questions)],
       "confirmations": [{"id": f"K-{i:02d}", **c.model_dump()} for i, c in enumerate(q.confirmations, 1)] if rnd == 1 else []}`.
       Expected outcome: the form the developer page renders.
    """
    raise NotImplementedError("S8.4")


def handle_submit(svc: Services, slug: str, body: Responses, user: str) -> dict:
    """Spec: S8.4 | Ticket: 08 | Traces to: I12

    Build steps:
    1. Task: `v = values(svc, slug)`; `rnd, valid = v.get("q_round", 0), set(v.get("q_ids", []))`; if `not rnd` raise
       `HTTPException(409, "No questionnaire is open for this session.")`.
       Expected outcome: answers only while a round is open.
    2. Task: If `bad := [a.question_id for a in body.answers if a.question_id not in valid]` raise
       `HTTPException(422, f"Unknown question IDs: {bad}")`.
       Expected outcome: responses are validated at the boundary.
    3. Task: `sheet = ResponseSheet(respondent=user, role=body.role, round=rnd, answers=body.answers, comments=body.comments)`;
       `svc.persistence.store.put(("responses", slug, f"r{rnd}"), user, sheet.model_dump())`;
       return `{"saved": True, "round": rnd, "respondent": user}`.
       Expected outcome: one record per developer per round; resubmitting replaces it.
    """
    raise NotImplementedError("S8.4")


def handle_responses(svc: Services, slug: str) -> list[dict]:
    """Spec: S8.4 | Ticket: 08 | Traces to: I12

    Build steps:
    1. Task: `v = values(svc, slug)`; `items = svc.persistence.store.search(("responses", slug, f"r{v.get('q_round', 0)}"), limit=500)`.
       Expected outcome: this round's responses.
    2. Task: Return `[{"respondent": i.value["respondent"], "role": i.value["role"], "submitted_at": i.value["submitted_at"]} for i in items]`.
       Expected outcome: who answered, never what (the PM sees content in the log).
    """
    raise NotImplementedError("S8.4")


# ------------------------------------------------------------------ handlers (S8.5)
def handle_download(svc: Services, slug: str, name: str) -> FileResponse:
    """Spec: S8.5 | Ticket: 07 | Traces to: I12

    Build steps:
    1. Task: `v = values(svc, slug)`; if `name not in v.get("files", [])` raise
       `HTTPException(404, f"'{name}' is not a file of this session.")`.
       Expected outcome: only the session's own generated files; no path traversal.
    2. Task: `path = svc.settings.artifacts_dir / "initiatives" / slug / name`; if `not path.exists()` raise
       `HTTPException(404, f"'{name}' has not been generated.")`.
       Expected outcome: missing files are 404, not 500.
    3. Task: Return `FileResponse(path, filename=f"{slug}-{name}")`.
       Expected outcome: a named download.
    """
    raise NotImplementedError("S8.5")


def handle_usage(svc: Services, slug: str) -> dict:
    """Spec: S8.5 | Ticket: 10 | Traces to: A2

    Build steps:
    1. Task: `calls = [i.value for i in svc.persistence.store.search(("calls", slug), limit=10_000)]`.
       Expected outcome: every model call record for the session.
    2. Task: `total = {k: sum(c.get(k, 0) for c in calls) for k in ("input_tokens", "cache_read_tokens", "output_tokens",
       "rejections", "transient_retries")}`; `total["calls"] = len(calls)`;
       `total["cache_hit_rate"] = round(total["cache_read_tokens"] / total["input_tokens"], 3) if total["input_tokens"] else 0.0`.
       Expected outcome: the numbers that prove caching works (A2).
    3. Task: Return `{"total": total, "calls": sorted(calls, key=lambda c: c["started_at"])}`.
       Expected outcome: totals plus the call log.
    """
    raise NotImplementedError("S8.5")


# ------------------------------------------------------------------ app factory (complete)
def startup_settings() -> Settings:
    """load_settings(), or development defaults while S1.1 is not built yet. (Complete.)"""
    try:
        return load_settings()
    except NotImplementedError:
        log.warning("Settings not built yet (S1.1); using development defaults.")
        return Settings(artifacts_dir=Path("./data").resolve(), database_url="",
                        sqlite_path=Path("./data/assay.sqlite").resolve(), gateway_url="", gateway_key="",
                        gateway_headers={}, models={}, timeout_s=120, cache_mode="explicit", retry_attempts=5,
                        retry_base_s=1.0, retry_cap_s=30, max_steps=40, max_output_retries=3, code_roots=(),
                        user_header="X-Forwarded-User", dev_user="dev", approvers=frozenset(),
                        team_name="Delivery team")


def create_app(settings: Settings | None = None, get_model=None, background: bool = True,
               persistence: Persistence | None = None, limits=None) -> FastAPI:
    svc = Services(settings=settings or startup_settings(), test_model=get_model)

    @asynccontextmanager
    async def lifespan(_app: FastAPI):
        try:
            p = persistence or open_persistence(svc.settings)
        except NotImplementedError as exc:
            log.warning("Persistence not built yet (%s); API calls will answer 501.", exc)
            yield
            return
        context = AppContext(settings=svc.settings, store=p.store, get_model=get_model, limits=limits)
        graph = build_graph().compile(checkpointer=p.checkpointer, store=p.store)
        svc.persistence, svc.graph = p, graph
        svc.runner = Runner(graph, context, background=background)
        yield
        if persistence is None:
            p.close()

    api = FastAPI(title="Assay", lifespan=lifespan)

    @api.exception_handler(NotImplementedError)
    async def not_built(_request: Request, exc: NotImplementedError):
        return JSONResponse(status_code=501, content={"detail": f"Not implemented yet: {exc}"})

    def user(request: Request) -> str:
        return user_from(request, svc.settings.user_header, svc.settings.dev_user)

    @api.get("/", response_class=HTMLResponse)
    @api.get("/s/{slug}", response_class=HTMLResponse)
    @api.get("/q/{slug}", response_class=HTMLResponse)
    def page(slug: str = ""):
        return HTMLResponse((STATIC / "index.html").read_text(encoding="utf-8"))

    @api.get("/api/me")
    def me(request: Request):
        return handle_me(svc, user(request))

    @api.get("/api/sessions")
    def list_sessions(request: Request):
        user(request)
        return handle_list(svc)

    @api.post("/api/sessions", status_code=201)
    def create(body: NewSession, request: Request):
        return handle_create(svc, body, user(request))

    @api.get("/api/sessions/{slug}")
    def get_session(slug: str, request: Request):
        user(request)
        return handle_get(svc, slug)

    @api.post("/api/sessions/{slug}/reply")
    def reply(slug: str, body: Reply, request: Request):
        return handle_reply(svc, slug, body, user(request))

    @api.post("/api/sessions/{slug}/retry")
    def retry(slug: str, request: Request):
        user(request)
        return handle_retry(svc, slug)

    @api.get("/api/sessions/{slug}/questionnaire")
    def questionnaire(slug: str, request: Request):
        user(request)
        return handle_questionnaire(svc, slug)

    @api.post("/api/sessions/{slug}/responses", status_code=201)
    def respond(slug: str, body: Responses, request: Request):
        return handle_submit(svc, slug, body, user(request))

    @api.get("/api/sessions/{slug}/responses")
    def responses(slug: str, request: Request):
        user(request)
        return handle_responses(svc, slug)

    @api.get("/api/sessions/{slug}/files/{name}")
    def download(slug: str, name: str, request: Request):
        user(request)
        return handle_download(svc, slug, name)

    @api.get("/api/sessions/{slug}/usage")
    def usage(slug: str, request: Request):
        user(request)
        return handle_usage(svc, slug)

    return api
