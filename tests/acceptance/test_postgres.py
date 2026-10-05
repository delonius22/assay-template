"""Stop mid-session, restart the app with fresh connections, and resume.
Runs only when ASSAY_TEST_DATABASE_URL points at a Postgres database."""

import os
import uuid

import pytest

from assay.api.app import create_app
from assay.llm.call import Limits
from tests.support.fakes import fake_model, make_settings
from tests.support.script import script

URL = os.environ.get("ASSAY_TEST_DATABASE_URL")
pytestmark = pytest.mark.skipif(not URL, reason="set ASSAY_TEST_DATABASE_URL to run")


def make(tmp_path):
    """Test helper: make."""
    from fastapi.testclient import TestClient

    model = fake_model(script)
    return TestClient(
        create_app(
            make_settings(tmp_path, database_url=URL),
            get_model=lambda r: model,
            background=False,
            limits=Limits(sleep=lambda s: None),
        )
    )


def test_session_survives_a_restart(tmp_path):
    """Session survives a restart.

    Spec: S7.2 | Traces to: I6
    Expected outcome: after a restart with fresh connections the session waits on the same pause.
    """
    slug = f"pg-{uuid.uuid4().hex[:8]}"
    with make(tmp_path) as c:
        c.post("/api/sessions", json={"slug": slug, "title": "Alerts", "mode": 1})
        r = c.post(f"/api/sessions/{slug}/reply", json={"text": "Customers overdraw."})
        assert r.json()["pending"]["kind"] == "dod_question"
    # New app, new connection pool: simulates the user stopping and the server restarting.
    with make(tmp_path) as c:
        st = c.get(f"/api/sessions/{slug}").json()
        assert st["status"] == "waiting" and st["pending"]["kind"] == "dod_question"
        r = c.post(f"/api/sessions/{slug}/reply", json={"text": "None supplied."})
        assert r.json()["pending"]["kind"] in ("approval", "dod_question")
