"""The web API end to end with a scripted model and SQLite persistence."""

import csv
import io

from fastapi.testclient import TestClient

from assay.api.app import create_app
from assay.llm.call import Limits
from tests.support.fakes import fake_model, make_settings
from tests.support.script import script


def client(tmp_path):
    """Test helper: client."""
    model = fake_model(script)
    app = create_app(
        make_settings(tmp_path),
        get_model=lambda r: model,
        background=False,
        limits=Limits(sleep=lambda s: None),
    )
    return TestClient(app)


def answer(c, slug, user="jordan", **body):
    """Test helper: answer."""
    return c.post(f"/api/sessions/{slug}/reply", json=body, headers={"X-Forwarded-User": user})


def test_full_session_over_http_ends_with_csv_and_prompt(tmp_path):
    """Full session over http ends with csv and prompt.

    Spec: S8.3, S8.5 | Traces to: I8
    Expected outcome: a full session over HTTP ends done; the CSV starts Story, Feature, Ticket; a non-approver's approval gets 403.
    """
    with client(tmp_path) as c:
        assert c.get("/").status_code == 200
        r = c.post(
            "/api/sessions", json={"slug": "alerts", "title": "Low-Balance Alerts", "mode": 1}
        )
        assert r.status_code == 201 and r.json()["pending"]["kind"] == "question"
        assert (
            answer(c, "alerts", text="Customers overdraw.").json()["pending"]["kind"]
            == "dod_question"
        )
        assert answer(c, "alerts", text="None supplied.").json()["pending"]["kind"] == "approval"
        assert (
            answer(c, "alerts", user="jordan", decision="approve").status_code == 403
        )  # not an approver
        assert (
            answer(c, "alerts", user="dana", decision="approve").json()["pending"]["kind"]
            == "seams"
        )
        assert (
            answer(c, "alerts", user="priya", decision="approve").json()["pending"]["kind"]
            == "ticket_review"
        )
        done = answer(c, "alerts", decision="approve").json()
        assert done["status"] == "done" and done["stage"] == "Done"

        rows = list(
            csv.DictReader(io.StringIO(c.get("/api/sessions/alerts/files/tickets.csv").text))
        )
        assert [x["Level"] for x in rows][:3] == ["Story", "Feature", "Ticket"]
        assert "```csv" in c.get("/api/sessions/alerts/files/agent-prompt.md").text
        assert c.get("/api/sessions/alerts/files/prd.pdf").content[:4] == b"%PDF"
        assert c.get("/api/sessions/alerts/files/..%2Fsecrets").status_code == 404
        usage = c.get("/api/sessions/alerts/usage").json()["total"]
        assert usage["calls"] > 0 and usage["cache_hit_rate"] == 0.8
        assert c.get("/api/sessions").json()[0]["slug"] == "alerts"


def test_developers_answer_the_questionnaire_in_the_browser(tmp_path):
    """Developers answer the questionnaire in the browser.

    Spec: S8.4 | Traces to: I12
    Expected outcome: unknown question IDs get 422; a valid sheet is saved under the respondent.
    """
    with client(tmp_path) as c:
        brief = {
            "ask": "Alert on low balance",
            "why": "Complaints up 18%",
            "outcome": "42 to 34 per 1,000 by June",
        }
        assert (
            c.post(
                "/api/sessions",
                json={"slug": "alerts-m3", "title": "Alerts", "mode": 3, "brief": brief},
            ).status_code
            == 201
        )
        q = c.get("/api/sessions/alerts-m3/questionnaire").json()
        assert [x["id"] for x in q["questions"]] == ["Q-01", "Q-02"]
        bad = c.post(
            "/api/sessions/alerts-m3/responses",
            json={"role": "Dev", "answers": [{"question_id": "Q-99", "response": "Confirm"}]},
            headers={"X-Forwarded-User": "priya"},
        )
        assert bad.status_code == 422
        ok = c.post(
            "/api/sessions/alerts-m3/responses",
            json={
                "role": "Lead Developer",
                "answers": [{"question_id": "Q-02", "response": "Correct", "text": "Seven years"}],
            },
            headers={"X-Forwarded-User": "priya"},
        )
        assert ok.json()["respondent"] == "priya"
        assert c.get("/api/sessions/alerts-m3/responses").json()[0]["respondent"] == "priya"
        nxt = answer(c, "alerts-m3", text="continue").json()
        assert nxt["pending"]["kind"] == "question"


def test_rejects_bad_input(tmp_path):
    """Rejects bad input.

    Spec: S8.3 | Traces to: I12
    Expected outcome: a bad slug and mode 3 without a brief get 422; an unknown session gets 404.
    """
    with client(tmp_path) as c:
        assert (
            c.post(
                "/api/sessions", json={"slug": "Bad Slug", "title": "x" * 5, "mode": 1}
            ).status_code
            == 422
        )
        assert (
            c.post("/api/sessions", json={"slug": "m3x", "title": "Alerts", "mode": 3}).status_code
            == 422
        )
        assert c.get("/api/sessions/nope").status_code == 404
