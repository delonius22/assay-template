"""The whole graph with a scripted model, in-memory checkpoints and store."""
import csv
import io

import pytest
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langgraph.types import Command

from assay.domain.models import Brief, ResponseSheet, Answer
from assay.graph.build import build_graph
from assay.graph.context import AppContext
from assay.graph.state import AssayState
from assay.llm.call import Limits
from assay.store.persistence import serializer
from tests.support.fakes import fake_model, make_settings
from tests.support.script import script


@pytest.fixture
def env(tmp_path):
    store = InMemoryStore()
    model = fake_model(script)
    ctx = AppContext(settings=make_settings(tmp_path), store=store, get_model=lambda r: model,
                     limits=Limits(sleep=lambda s: None))
    app = build_graph().compile(checkpointer=InMemorySaver(serde=serializer()), store=store)
    return app, ctx, model, tmp_path / "data"


ANSWERS = {"question": {"text": "Customers overdraw.", "user": "jordan"},
           "dod_question": {"text": "None supplied.", "user": "jordan"},
           "approval": {"decision": "approve", "user": "dana"},
           "seams": {"decision": "approve", "user": "priya"},
           "ticket_review": {"decision": "approve", "user": "jordan"}}


def drive(app, ctx, cfg, first):
    r, kinds = app.invoke(first, cfg, context=ctx), []
    while r.get("__interrupt__"):
        kind = r["__interrupt__"][0].value["kind"]
        kinds.append(kind)
        r = app.invoke(Command(resume=ANSWERS[kind]), cfg, context=ctx)
    return r, kinds


def test_mode1_end_to_end_story_feature_ticket(env):
    app, ctx, model, data = env
    cfg = {"configurable": {"thread_id": "alerts"}}
    r, kinds = drive(app, ctx, cfg, AssayState(slug="alerts", title="Low-Balance Alerts", pm="jordan", mode=1))
    assert kinds == ["question", "dod_question", "approval", "seams", "ticket_review"]
    assert r["stage"] == "Done" and r["approved_by"] == "dana"

    # Rules rejected the three planted mistakes, and retries fixed them.
    assert any("exactly one question" in x for x in model.rejections)
    assert any("D-999" in x for x in model.rejections)
    assert any("FR-03" in x for x in model.rejections)

    rows = list(csv.DictReader(io.StringIO((data / "initiatives/alerts/tickets.csv").read_text())))
    assert [(x["Level"], x["ID"], x["Parent ID"]) for x in rows] == [
        ("Story", "S-01", ""), ("Feature", "F-01", "S-01"), ("Ticket", "T-001", "F-01"),
        ("Ticket", "T-002", "F-01"), ("Feature", "F-02", "S-01"), ("Ticket", "T-003", "F-02"),
        ("Ticket", "T-004", "F-02")]
    assert rows[0]["Title"] == "Low-balance alerts"
    assert "DOD-T01" in rows[2]["Definition of Done"] and "DOD-F01" in rows[1]["Definition of Done"]
    assert "DOD-S01" in rows[0]["Definition of Done"]
    assert rows[6]["Depends On"] == "T-003" and rows[5]["Type"] == "Spike"

    prompt = (data / "initiatives/alerts/agent-prompt.md").read_text()
    assert "```csv" in prompt and "T-004" in prompt and "F-02 Alert delivery" in prompt
    for f in ["prd.pdf", "prd.md", "spec.md", "intake.md", "session-log.md", "tickets.csv", "agent-prompt.md"]:
        assert f in r["files"], f
    assert "- [ ]" not in (data / "initiatives/alerts/intake.md").read_text()
    assert (data / "definition-of-done.md").exists() and (data / "glossary.md").exists()

    # Every model call was logged with its cache hits.
    calls = [i.value for i in ctx.store.search(("calls", "alerts"), limit=100)]
    assert calls and all(c["cache_read_tokens"] > 0 for c in calls)


def test_second_initiative_reuses_the_team_dod(env):
    app, ctx, model, _ = env
    drive(app, ctx, {"configurable": {"thread_id": "a"}}, AssayState(slug="a", title="First", pm="j", mode=1))
    team = ctx.team_dod()
    assert [i.id for i in team] == ["DOD-T01", "DOD-T02", "DOD-F01", "DOD-S01"]
    assert any("TEAM STANDARD" in p for k, p in model.prompts if k == "DodTurn")
    model.prompts.clear()
    drive(app, ctx, {"configurable": {"thread_id": "b"}}, AssayState(slug="b", title="Second", pm="j", mode=1))
    dod_prompts = [p for k, p in model.prompts if k == "DodTurn"]
    assert dod_prompts and all("ADDITIONS" in p and "TEAM STANDARD" not in p for p in dod_prompts)
    assert [i.id for i in app.get_state({"configurable": {"thread_id": "b"}}).values["dod_team"]] == \
        [i.id for i in team]


def test_non_approver_cannot_approve(env):
    app, ctx, _, _ = env
    cfg = {"configurable": {"thread_id": "x"}}
    r = app.invoke(AssayState(slug="x", title="X", pm="j", mode=1), cfg, context=ctx)
    while r["__interrupt__"][0].value["kind"] != "approval":
        r = app.invoke(Command(resume=ANSWERS[r["__interrupt__"][0].value["kind"]]), cfg, context=ctx)
    r = app.invoke(Command(resume={"decision": "approve", "user": "mallory"}), cfg, context=ctx)
    pending = r["__interrupt__"][0].value
    assert pending["kind"] == "approval" and "not an approver" in pending["error"]


def test_mode3_questionnaire_through_web_form_responses(env):
    app, ctx, model, data = env
    cfg = {"configurable": {"thread_id": "m3"}}
    brief = Brief(ask="Alert customers on low balance", why="Complaints up 18%",
                  outcome="Overdrafts from 42 to 34 per 1,000 by June 2027")
    r = app.invoke(AssayState(slug="m3", title="Alerts", pm="j", mode=3, brief=brief), cfg, context=ctx)
    assert r["__interrupt__"][0].value["kind"] == "await_answers"
    # Continue with no answers: told to share the link, still waiting.
    r = app.invoke(Command(resume={"text": "continue", "user": "j"}), cfg, context=ctx)
    assert "No new responses" in r["__interrupt__"][0].value["note"]
    sheet = ResponseSheet(respondent="priya", role="Lead Developer", round=1,
                          answers=[Answer(question_id="Q-02", response="Correct", text="Seven years")])
    ctx.store.put(("responses", "m3", "r1"), "priya", sheet.model_dump())
    r = app.invoke(Command(resume={"text": "continue", "user": "j"}), cfg, context=ctx)
    state = app.get_state(cfg).values
    assert any(e.title == "Thresholds kept seven years" for e in state["log"])
    assert model.calls["Reconciliation"] == 1
    assert r["__interrupt__"][0].value["kind"] == "question"   # gate gaps go to the PM, live


def test_ticket_review_changes_recut_the_tickets(env):
    app, ctx, model, _ = env
    cfg = {"configurable": {"thread_id": "rv"}}
    r = app.invoke(AssayState(slug="rv", title="Review", pm="j", mode=1), cfg, context=ctx)
    while r["__interrupt__"][0].value["kind"] != "ticket_review":
        r = app.invoke(Command(resume=ANSWERS[r["__interrupt__"][0].value["kind"]]), cfg, context=ctx)
    review = r["__interrupt__"][0].value
    assert [t["id"] for t in review["tickets"]] == ["T-001", "T-002", "T-003", "T-004"]
    before = model.calls["TicketPlan"]
    r = app.invoke(Command(resume={"decision": "changes", "text": "Split T-001", "user": "j"}), cfg, context=ctx)
    assert r["__interrupt__"][0].value["kind"] == "ticket_review"        # re-cut, reviewed again
    assert model.calls["TicketPlan"] == before + 1
    assert any("Split T-001" in p for k, p in model.prompts if k == "TicketPlan")
    assert "tickets.csv" not in app.get_state(cfg).values["files"]     # nothing exported unreviewed
