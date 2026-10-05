"""AG-UI endpoint (S9): runs as events, pauses as standard interrupts."""

import json
import queue

from fastapi.testclient import TestClient

from assay.api.app import create_app
from assay.api.runner import RunProgress
from assay.llm.call import Limits
from tests.support.fakes import fake_model, make_settings
from tests.support.script import script

HEADERS = {
    "X-Assay-Service-Token": "svc-token",
    "X-Forwarded-User": "jordan",
    "Accept": "text/event-stream",
}


def client(tmp_path):
    """Build an app with a scripted model, inline runs, and SQLite in a temporary folder."""
    model = fake_model(script)
    return TestClient(
        create_app(
            make_settings(tmp_path),
            get_model=lambda r: model,
            background=False,
            limits=Limits(sleep=lambda s: None),
        )
    )


def run(c, thread, **extra):
    """POST one AG-UI run and return its decoded events."""
    body = {
        "threadId": thread,
        "runId": f"run-{thread}-{len(extra)}",
        "state": {},
        "messages": [],
        "tools": [],
        "context": [],
        "forwardedProps": extra.pop("props", {}),
        **extra,
    }
    r = c.post("/agui", json=body, headers=HEADERS)
    assert r.status_code == 200, r.text
    return [json.loads(l[5:]) for l in r.text.splitlines() if l.startswith("data:")]


def test_new_thread_ends_with_first_question_interrupt(tmp_path):
    """A new thread starts a session and ends with the first question as an interrupt.

    Spec: S9.2, S9.4, S9.5 | Traces to: I7, I18
    Expected outcome: events run RUN_STARTED, step events, a snapshot, then RUN_FINISHED with
    outcome "interrupt" whose reason is "question" and whose schema requires "text".
    """
    with client(tmp_path) as c:
        ev = run(c, "alerts", props={"title": "Low-Balance Alerts", "mode": 1})
        kinds = [e["type"] for e in ev]
        assert kinds[0] == "RUN_STARTED" and kinds[-1] == "RUN_FINISHED"
        assert "STEP_STARTED" in kinds and "STEP_FINISHED" in kinds and "STATE_SNAPSHOT" in kinds
        outcome = ev[-1]["outcome"]
        assert outcome["type"] == "interrupt" and outcome["interrupts"][0]["reason"] == "question"
        assert "text" in outcome["interrupts"][0]["responseSchema"]["required"]


def test_waiting_session_resends_same_interrupt(tmp_path):
    """Re-requesting a waiting session re-sends its interrupt without running a step.

    Spec: S9.4 | Traces to: I7
    Expected outcome: the second run has no STEP_STARTED and the same interrupt ID.
    """
    with client(tmp_path) as c:
        first = run(c, "alerts", props={"title": "Low-Balance Alerts", "mode": 1})
        again = run(c, "alerts")
        assert "STEP_STARTED" not in [e["type"] for e in again]
        assert (
            again[-1]["outcome"]["interrupts"][0]["id"]
            == first[-1]["outcome"]["interrupts"][0]["id"]
        )


def test_resume_with_invalid_payload_is_refused(tmp_path):
    """A resume payload that does not match the pause's schema is refused.

    Spec: S9.3 | Traces to: I18
    Expected outcome: the run ends with RUN_ERROR and the session still waits on the same question.
    """
    with client(tmp_path) as c:
        first = run(c, "alerts", props={"title": "Low-Balance Alerts", "mode": 1})
        iid = first[-1]["outcome"]["interrupts"][0]["id"]
        bad = run(
            c,
            "alerts",
            resume=[{"interruptId": iid, "status": "resolved", "payload": {"wrong": 1}}],
        )
        assert bad[-1]["type"] == "RUN_ERROR"
        good = run(
            c,
            "alerts",
            resume=[{"interruptId": iid, "status": "resolved", "payload": {"text": "Overdrafts."}}],
        )
        assert good[-1]["outcome"]["interrupts"][0]["reason"] == "dod_question"


def test_call_without_service_token_is_refused(tmp_path):
    """Only the Node service may call the AG-UI endpoint.

    Spec: S9.6 | Traces to: I17
    Expected outcome: a call without the service token gets HTTP 403.
    """
    with client(tmp_path) as c:
        r = c.post(
            "/agui",
            json={
                "threadId": "x",
                "runId": "r",
                "state": {},
                "messages": [],
                "tools": [],
                "context": [],
                "forwardedProps": {},
            },
            headers={"X-Forwarded-User": "jordan"},
        )
        assert r.status_code == 403


def test_events_are_encoded_for_sse(tmp_path):
    """Events stream as server-sent events.

    Spec: S9.7 | Traces to: I7
    Expected outcome: every non-empty line of the response starts with "data:".
    """
    with client(tmp_path) as c:
        body = {
            "threadId": "sse",
            "runId": "r",
            "state": {},
            "messages": [],
            "tools": [],
            "context": [],
            "forwardedProps": {"title": "Alerts", "mode": 1},
        }
        text = c.post("/agui", json=body, headers=HEADERS).text
        assert all(l.startswith("data:") for l in text.splitlines() if l.strip())


def test_runner_publishes_step_events(tmp_path):
    """The runner publishes a start and finish per node and how the run ended.

    Spec: S9.1 | Traces to: I7
    Expected outcome: a subscriber sees step_started and step_finished events and a final
    'ended' event with outcome 'pause'.
    """
    with client(tmp_path) as c:
        runner = c.app.state.services.runner if hasattr(c.app.state, "services") else None
        assert runner is not None, "create_app must expose its services on app.state.services"
        q = runner.subscribe("pub")
        c.post("/api/sessions", json={"slug": "pub", "title": "Publish", "mode": 1})
        seen = []
        while True:
            try:
                seen.append(q.get_nowait())
            except queue.Empty:
                break
        kinds = [e.kind for e in seen if isinstance(e, RunProgress)]
        assert "step_started" in kinds and "step_finished" in kinds
        assert seen[-1].kind == "ended" and seen[-1].outcome == "pause"
