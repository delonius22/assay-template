"""Single nodes and routers, called directly (S5.1 to S5.10)."""
from types import SimpleNamespace

import pytest

from assay.domain.models import LogEntry
from assay.graph.context import AppContext
from assay.graph.nodes import dod, intake, prd, spec, tickets
from assay.graph.state import AssayState, log_view
from assay.rules.intake import failures, gate
from langgraph.store.memory import InMemoryStore
from tests.support.fakes import fake_model, make_settings
from tests.support.script import script


def state(**kw) -> AssayState:
    return AssayState(**{"slug": "t", "title": "T", "pm": "PM", "mode": 1, **kw})


def test_routers_read_state_only():
    assert intake.route_mode(state(mode=3)) == "brief_check"
    assert intake.after_gate(state(agenda=[])) == "prd"
    assert intake.after_gate(state(agenda=["x"], stage="Definition of Done")) == "dod_think"
    assert intake.after_gate(state(agenda=["x"], stage="Intake")) == "grill_think"
    assert prd.after_review(state(review_error="no")) == "prd_review_ask"
    assert spec.after_seams(state(seams_feedback="redo")) == "seams"
    assert tickets.after_ticket_review(state(ticket_feedback="")) == "export_tickets"
    assert dod.after_dod(state(dod_phase="done")) == "intake_gate_node"


def test_gate_reports_open_blocking_question():
    q = LogEntry(id="Q-001", type="Q", title="Disclosure?", area="Regulation", detail="", source="x",
                 priority="Blocking", owner="Compliance", status="Open")
    assert any("blocking questions still open: Q-001" in f for f in failures(gate([q], True)))


def test_log_view_shows_typed_flags():
    from assay.domain.ids import add_entries
    from assay.domain.models import NewEntry
    log = add_entries([], [NewEntry(type="D", area="Scope", title="Joint holders", detail="d", source="PM",
                                    scope_side="out")])
    assert "scope:out" in log_view(state(log=log))


def test_grill_think_assigns_ids_and_writes_files(tmp_path):
    model = fake_model(lambda kind, n: script(kind, 3))
    c = AppContext(settings=make_settings(tmp_path), store=InMemoryStore(), get_model=lambda r: model)
    out = intake.grill_think(state(), SimpleNamespace(context=c))
    assert out["log"][0].id == "D-001" and out["pending"] is None
    assert (c.folder(state()) / "session-log.md").exists()


def test_missing_context_names_the_cause():
    with pytest.raises(RuntimeError) as exc:            # NotImplementedError is a RuntimeError too
        intake.setup(state(), SimpleNamespace(context=None))
    assert not isinstance(exc.value, NotImplementedError), f"stub {exc.value} is not built yet"
    assert "Pass context=AppContext" in str(exc.value)
