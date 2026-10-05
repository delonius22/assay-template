"""Serve the REST API and the AG-UI endpoint.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C6 People decide and C7 Live, standard interaction. People
reach Assay through the Next.js service, which calls these endpoints. This file owns
routes, validation at the boundary, and startup; behaviour lives in the runner and
the graph.

Why this comes now: Identity (28), the runner (29), and the AG-UI translation (30)
exist.

Build order: Step 31 of 33.
Previous: src/assay/api/agui.py (step 30), which serves Assay over the AG-UI
protocol.
Next: src/assay/cli.py (step 32), which provides the command line.

Build these in order:
    1. NewSession: request bodies first.
    2. Reply: second body.
    3. Responses: third body.
    4. Services: the handlers' context.
    5. handle_me: the simplest handler.
    6. handle_list: lists sessions.
    7. handle_create: starts sessions.
    8. handle_get: reads status.
    9. handle_reply: resumes sessions.
    10. handle_retry: recovers sessions.
    11. handle_questionnaire: serves the form.
    12. handle_submit: saves answers.
    13. handle_responses: lists respondents.
    14. handle_download: serves files.
    15. handle_usage: reports usage.
    16. create_app: the last piece; wires everything.

Depends on:
    assay.api.agui: check_service_call, encode_stream, run_events. The AG-UI route.
    assay.api.auth: user_from. Identity for REST routes.
    assay.api.runner: BusyError, Runner. Driving sessions.
    assay.domain.ids: question_ids. Questionnaire numbering.
    assay.domain.models: Answer, Brief, ResponseSheet, now. Request bodies and
    records.
    assay.graph.build: build_graph. The workflow.
    assay.graph.context: AppContext. Built at startup.
    assay.graph.state: AssayState. New sessions.
    assay.settings: Settings, load_settings, missing_config. Configuration.
    assay.store.persistence: Persistence, open_persistence. Storage.
    Standard library: logging, re, contextlib, dataclasses, pathlib, typing.
    Third-party: fastapi, pydantic, ag-ui-protocol.

Depended on by:
    assay.cli: serves it with uvicorn's factory mode.

Spec coverage: S8.3, S8.4, S8.5, S9.7 | Traces to: I8, I12, I17
"""

import logging
import re
from contextlib import asynccontextmanager
from dataclasses import dataclass
from typing import Literal

from ag_ui.core import RunAgentInput
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse
from pydantic import BaseModel, Field

from assay.api.agui import check_service_call, encode_stream, run_events
from assay.api.auth import user_from
from assay.api.runner import BusyError, Runner
from assay.domain.ids import question_ids
from assay.domain.models import Answer, Brief, ResponseSheet, now
from assay.graph.build import build_graph
from assay.graph.context import AppContext
from assay.graph.state import AssayState
from assay.settings import Settings, load_settings, missing_config
from assay.store.persistence import Persistence, open_persistence

SLUG = re.compile(r"^[a-z0-9][a-z0-9-]{2,39}$")  # S8.3
log = logging.getLogger("assay.api")


class NewSession(BaseModel):
    """The body that starts a session.

    Problem piece: C6: a PM starts a session.

    Why it matters: Validating the body at the boundary stops a malformed session
                    ever being created (I12).

    What: Slug, title, mode, optional brief, and optional PM.

    Spec: S8.3 | Ticket: — | Traces to: —
    """

    slug: str
    title: str = Field(min_length=3)
    mode: Literal[1, 2, 3]
    brief: Brief | None = None
    pm: str = ""


class Reply(BaseModel):
    """The body that answers a pause.

    Problem piece: C6: a person replies.

    Why it matters: One body shape serves every pause kind over REST.

    What: Text, decision, and optional brief.

    Spec: S8.3 | Ticket: — | Traces to: —
    """

    text: str = ""
    decision: Literal["approve", "changes"] | None = None
    brief: Brief | None = None


class Responses(BaseModel):
    """The body a developer submits for a questionnaire round.

    Problem piece: C6: developers answer.

    Why it matters: Answers are validated against the session's question IDs before
                    saving.

    What: Role, answers, and comments.

    Spec: S8.4 | Ticket: — | Traces to: —
    """

    role: str
    answers: list[Answer]
    comments: str = ""


@dataclass
class Services:
    """Everything the handlers need, filled at startup.

    Problem piece: C5 and C6: one bundle passed to every handler.

    Why it matters: Handlers stay plain functions that tests can call; startup fills
                    this once.

    What: Settings, persistence, runner, compiled graph, and an optional test model
          factory.

    Spec: S8.3 | Ticket: — | Traces to: —
    """

    settings: Settings
    persistence: Persistence | None = None
    runner: Runner | None = None
    graph: object = None
    test_model: object = None


def handle_me(svc: Services, user: str) -> dict[str, object]:
    """Return who is signed in and whether they may approve.

    Problem piece: C6: the UI knows what this person may do.

    Why it matters: Disabling Approve for non-approvers stops the UI inviting an
                    action the server refuses. The page asks this once at load, so
                    it must be cheap and must never expose configuration values,
                    only their names.

    What: User, approver flag (anyone when no approvers are configured), missing
          configuration (empty with a test model), and the storage backend name.

    Spec: S8.3 | Ticket: 02 | Traces to: I8

    Build steps:
    1. Task: Return the user, whether they may approve, missing configuration unless
             a test model is set, and the backend name or 'none'.
       Expected outcome: A non-approver sees approver false.
    """
    raise NotImplementedError("S8.3: handle_me")


def handle_list(svc: Services) -> list[dict[str, object]]:
    """Return every session with its live status, newest first.

    Problem piece: C5 and C6: a PM finds their sessions.

    Why it matters: Status comes from the checkpoint so it is correct after
                    restarts. Reading status from memory instead would show finished
                    sessions as working after a restart, and the PM would retry work
                    already done.

    What: Each registered session merged with its status, sorted by creation time
          descending. Called as handle_list(svc: Services) and returns
          list[dict[str, object]].

    Spec: S8.3 | Ticket: 02 | Traces to: I6

    Build steps:
    1. Task: Merge each registered session with its runner status and sort by
             creation time, newest first.
       Expected outcome: The newest session is listed first.
    """
    raise NotImplementedError("S8.3: handle_list")


def handle_create(svc: Services, body: NewSession, user: str) -> dict[str, object]:
    """Validate and start a new session.

    Problem piece: C6: a PM starts a session; bad input fails at the boundary.

    Why it matters: A malformed or duplicate session would corrupt the list and
                    checkpoints. Validating here, before the runner sees anything,
                    means no half-created session ever exists in the store or the
                    checkpoints.

    What: Refuses a bad slug (422), a duplicate (409), or mode 3 without a brief
          (422); registers and starts the session; returns its status.

    Spec: S8.3 | Ticket: 02 | Traces to: I12

    Raises:
        HTTPException: 409 or 422 as above.

    Build steps:
    1. Task: Refuse a slug not matching SLUG with 422 'Slug: 3 to 40 lowercase
             letters, digits, or hyphens.', an existing slug with 409, and mode 3
             without a brief with 422.
       Expected outcome: A duplicate slug gets 409.
    2. Task: Register the session, start it with the PM defaulting to the user, and
             return its status.
       Expected outcome: The response shows the first pause or 'working'.
    """
    raise NotImplementedError("S8.3: handle_create")


def handle_get(svc: Services, slug: str) -> dict[str, object]:
    """Return one session's status.

    Problem piece: C5: status on demand.

    Why it matters: The REST path mirrors what AG-UI streams, for clients that
                    cannot stream. Without it, a client that cannot hold a stream
                    open would have no way to learn whether a session is waiting for
                    it.

    What: The status, or 404 for an unknown slug. Called as handle_get(svc:
          Services, slug: str) and returns dict[str, object].

    Spec: S8.3 | Ticket: 02 | Traces to: I6

    Raises:
        HTTPException: 404.

    Build steps:
    1. Task: Return the status, refusing an unknown session with 404.
       Expected outcome: An unknown slug gets 404.
    """
    raise NotImplementedError("S8.3: handle_get")


def handle_reply(svc: Services, slug: str, body: Reply, user: str) -> dict[str, object]:
    """Answer a pause over REST.

    Problem piece: C6: replies attributed and authorised.

    Why it matters: Approval is checked here and again in the node (I8); a session
                    not waiting must not be resumed.

    What: Refuses unless waiting (409); refuses approval by a non-approver (403);
          resumes with text, user, decision, and brief.

    Spec: S8.3 | Ticket: 02, 05 | Traces to: I8, I12

    Raises:
        HTTPException: 403 or 409.

    Build steps:
    1. Task: Refuse with 409 unless the session is waiting, and with 403 'Only a
             named approver can approve the PRD.' for an approval by a non-approver
             when approvers are configured.
       Expected outcome: A non-approver's approval gets 403.
    2. Task: Resume with text, user, decision, and brief, mapping BusyError to 409,
             and return the status.
       Expected outcome: The status shows the next pause.
    """
    raise NotImplementedError("S8.3: handle_reply")


def handle_retry(svc: Services, slug: str) -> dict[str, object]:
    """Continue a session from its last saved step.

    Problem piece: C5: recover after an error.

    Why it matters: Retry must never run two steps at once. After a crash, retry is
                    the only way forward that keeps every completed step, so it must
                    refuse rather than race a running step.

    What: Retries, mapping BusyError to 409; returns the status. Called as
          handle_retry(svc: Services, slug: str) and returns dict[str, object].

    Spec: S8.3 | Ticket: 02 | Traces to: I6

    Raises:
        HTTPException: 409.

    Build steps:
    1. Task: Retry the session, mapping BusyError to 409, and return the status.
       Expected outcome: Retrying a stopped session continues it.
    """
    raise NotImplementedError("S8.3: handle_retry")


def handle_questionnaire(svc: Services, slug: str) -> dict[str, object]:
    """Return the current round's questionnaire for the form.

    Problem piece: C6: developers see what to answer.

    Why it matters: The form needs IDs for questions, follow-ups, and confirmations,
                    numbered exactly as reconciliation expects. If the form numbered
                    questions differently from the server, a developer's correction
                    would be saved against the wrong question.

    What: Title, round, brief, questions with IDs and lettered follow-ups, and round
          1 confirmations; 404 without a questionnaire.

    Spec: S8.4 | Ticket: 08 | Traces to: I12

    Raises:
        HTTPException: 404.

    Build steps:
    1. Task: Refuse with 404 when the session has no questionnaire.
       Expected outcome: A mode 1 session gets 404.
    2. Task: Return the title, round, brief, each question with its ID and lettered
             follow-ups, and K-numbered confirmations in round 1 only.
       Expected outcome: Round 2 returns no confirmations.
    """
    raise NotImplementedError("S8.4: handle_questionnaire")


def handle_submit(svc: Services, slug: str, body: Responses, user: str) -> dict[str, object]:
    """Save one developer's answers for the open round.

    Problem piece: C6: answers saved per developer.

    Why it matters: Answers come from browsers, so IDs must be checked against the
                    session's list (I12); one record per developer per round lets
                    them resubmit.

    What: Refuses without an open round (409) or with unknown IDs (422); saves under
          ('responses', slug, 'r<round>') keyed by the user.

    Spec: S8.4 | Ticket: 08 | Traces to: I12

    Raises:
        HTTPException: 409 or 422.

    Build steps:
    1. Task: Refuse with 409 when no round is open and with 422 naming unknown
             question IDs.
       Expected outcome: Q-99 is refused.
    2. Task: Save a ResponseSheet for the user and round, replacing any earlier one,
             and return saved, round, and respondent.
       Expected outcome: Resubmitting replaces the earlier sheet.
    """
    raise NotImplementedError("S8.4: handle_submit")


def handle_responses(svc: Services, slug: str) -> list[dict[str, object]]:
    """Return who has answered the open round.

    Problem piece: C6: the PM sees who answered.

    Why it matters: The PM decides when to continue; seeing respondents, not
                    content, keeps answers private until reconciled.

    What: Respondent, role, and submission time for each sheet in the round. Called
          as handle_responses(svc: Services, slug: str) and returns list[dict[str,
          object]].

    Spec: S8.4 | Ticket: 08 | Traces to: I12

    Build steps:
    1. Task: Return respondent, role, and submission time for each sheet in the
             current round.
       Expected outcome: One submission lists one respondent.
    """
    raise NotImplementedError("S8.4: handle_responses")


def handle_download(svc: Services, slug: str, name: str) -> FileResponse:
    """Return one of a session's generated files.

    Problem piece: C4: the PRD, CSV, and prompt reach people.

    Why it matters: Building a path from the URL alone allows traversal; only files
                    the session lists may be served (I12).

    What: Refuses names not in the session's files or not yet written (404); returns
          the file named '<slug>-<name>'.

    Spec: S8.5 | Ticket: 07 | Traces to: I12

    Raises:
        HTTPException: 404.

    Build steps:
    1. Task: Refuse with 404 any name not in the session's file list, and any listed
             file not yet written.
       Think about: Why is checking the list safer than checking the path?
       Expected outcome: '../secrets' gets 404.
    2. Task: Return the file from the session folder with the download name
             '<slug>-<name>'.
       Expected outcome: tickets.csv downloads as '<slug>-tickets.csv'.
    """
    raise NotImplementedError("S8.5: handle_download")


def handle_usage(svc: Services, slug: str) -> dict[str, object]:
    """Return a session's model usage and cache-hit rate.

    Problem piece: C1: proof that caching and the rules work.

    Why it matters: The cache-hit rate is how an operator verifies the gateway
                    honours caching (A2). Without these numbers nobody can tell
                    whether a slow, expensive session is a caching failure or simply
                    a long conversation.

    What: Totals of input, cached, and output tokens, rejections, and retries; call
          count; cache-hit rate rounded to 3 places; and the calls by start time.

    Spec: S8.5 | Ticket: 10 | Traces to: A2

    Build steps:
    1. Task: Total the call records' counters, count the calls, and compute cached
             input tokens divided by input tokens rounded to 3 places (0 when no
             input).
       Expected outcome: 800 cached of 1000 input gives 0.8.
    2. Task: Return the totals and the calls sorted by start time.
       Expected outcome: The first call is listed first.
    """
    raise NotImplementedError("S8.5: handle_usage")


def create_app(
    settings: Settings | None = None,
    get_model: object = None,
    background: bool = True,
    persistence: Persistence | None = None,
    limits: object = None,
) -> FastAPI:
    """Build the FastAPI app with every route.

    Problem piece: C6 and C7: one app serving REST and AG-UI.

    Why it matters: Tests inject settings, a fake model, inline runs, and storage;
                    production loads everything at startup. The AG-UI route must
                    refuse anything not from the Node service (I17).

    What: An app whose startup opens persistence, builds the context and compiled
          graph, and creates the runner; whose shutdown closes storage it opened;
          and whose routes call the handlers.

    Spec: S8.3, S9.7 | Ticket: 02, 12 | Traces to: I17

    Build steps:
    1. Task: Create the services from the given or loaded settings; at startup open
             persistence (or use the given one), build the context, compile the
             graph with its checkpointer and store, and create the runner; at
             shutdown close persistence only if this app opened it. Expose the
             services on the app's state as 'services' so tests and tools can reach
             the runner.
       Expected outcome: After startup, the app's state holds the services with a
                         runner.
    2. Task: Add REST routes, each resolving the user first: GET /api/me, GET and
             POST /api/sessions, GET /api/sessions/{slug}, POST
             /api/sessions/{slug}/reply and /retry, GET
             /api/sessions/{slug}/questionnaire, GET and POST
             /api/sessions/{slug}/responses (POST returns 201), GET
             /api/sessions/{slug}/files/{name}, and GET /api/sessions/{slug}/usage.
       Expected outcome: POST /api/sessions returns 201.
    3. Task: Add POST /agui: check the service call (403 on refusal), then stream
             the encoded run events for the request's run input and accept header.
       Think about: Why must this route ignore the SSO header path the REST routes
                    use?
       Expected outcome: A call without the service token gets 403.
    """
    raise NotImplementedError("S8.3: create_app")
