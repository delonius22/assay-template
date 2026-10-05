"""Ticket 01: settings and code-assigned IDs (S1.1, S1.2, S2.1 to S2.6)."""

from assay.domain.ids import (
    add_entries,
    all_answerable_ids,
    apply_dod_turn,
    assign_tickets,
    live,
    question_ids,
    requirement_ids,
)
from assay.domain.models import (
    Confirmation,
    DodItemDraft,
    DodTurn,
    FollowUp,
    NewEntry,
    PRDCore,
    QItem,
    Questionnaire,
    TicketPlan,
)
from assay.settings import load_settings, missing_config
from tests.support.script import script


def test_settings_defaults_and_per_role_fallback(monkeypatch):
    """Settings defaults and per role fallback.

    Spec: S1.1 | Traces to: I9
    Expected outcome: a role without its own model uses the default; approvers are trimmed.
    """
    for k in list(__import__("os").environ):
        if k.startswith("ASSAY_"):
            monkeypatch.delenv(k)
    monkeypatch.setenv("ASSAY_MODEL", "gw/default")
    monkeypatch.setenv("ASSAY_MODEL_PRD", "gw/strong")
    monkeypatch.setenv("ASSAY_APPROVERS", "dana, lee ,")
    s = load_settings()
    assert s.models["prd"] == "gw/strong" and s.models["grill"] == "gw/default"
    assert (
        s.approvers == frozenset({"dana", "lee"})
        and s.cache_mode == "explicit"
        and s.retry_attempts == 5
    )
    assert s.user_header == "X-Forwarded-User" and s.code_roots == ()


def test_missing_config_names_never_values(monkeypatch):
    """Missing config names never values.

    Spec: S1.2 | Traces to: I9
    Expected outcome: missing settings are named and the key's value never appears.
    """
    monkeypatch.setenv("ASSAY_GATEWAY_KEY", "super-secret-value")
    monkeypatch.delenv("ASSAY_GATEWAY_URL", raising=False)
    monkeypatch.setenv("ASSAY_MODEL", "")
    missing = missing_config(load_settings())
    assert "ASSAY_GATEWAY_URL" in missing and "ASSAY_MODEL or ASSAY_MODEL_GRILL" in missing
    assert not any("super-secret-value" in m for m in missing)


def entry(t="D", **kw):
    """Test helper: entry."""
    return NewEntry(
        **{"type": t, "title": "x", "area": "Problem", "detail": "d", "source": "PM", **kw}
    )


def test_log_ids_number_per_type_and_supersede_without_deleting():
    """Log ids number per type and supersede without deleting.

    Spec: S2.1, S2.2 | Traces to: I2
    Expected outcome: IDs number per type and superseded entries stay, marked.
    """
    log = add_entries([], [entry(), entry("A"), entry()])
    assert [e.id for e in log] == ["D-001", "A-001", "D-002"]
    log = add_entries(log, [entry()], supersedes=["D-001"])
    assert [e.id for e in log] == ["D-001", "A-001", "D-002", "D-003"]
    assert log[0].superseded_by == ["D-003"] and [e.id for e in live(log)] == [
        "A-001",
        "D-002",
        "D-003",
    ]


def test_question_ids_by_round():
    """Question ids by round.

    Spec: S2.3 | Traces to: I2
    Expected outcome: round 1 numbers Q-01 with follow-ups and K-01; round 2 has no K IDs.
    """
    item = QItem(
        text="Where?",
        owner_role="Developer",
        priority="Important",
        why_it_matters="x",
        proposed_answer="y",
        reason="z",
        area="Data",
        follow_ups=[FollowUp(condition="c", text="t")],
    )
    q = Questionnaire(
        summary="s", questions=[item, item], confirmations=[Confirmation(statement="s", source="f")]
    )
    assert question_ids(q, 1) == ["Q-01", "Q-02"] and question_ids(q, 2) == ["Q-F01", "Q-F02"]
    assert all_answerable_ids(q, 1) == ["Q-01", "Q-02", "Q-01a", "Q-02a", "K-01"]
    assert "K-01" not in all_answerable_ids(q, 2)


def test_withdrawn_dod_ids_are_never_reused():
    """Withdrawn dod ids are never reused.

    Spec: S2.4 | Traces to: I2
    Expected outcome: withdrawing DOD-T01 then adding gives DOD-T02.
    """
    d = DodItemDraft(
        level="ticket",
        statement="Reviewer approved the merge",
        category="c",
        how_verified="h",
        evidence="e",
        verified_by="Reviewer",
        source="s",
    )
    items, retired = apply_dod_turn([], [], DodTurn(agreed=[d]), additions=False)
    items, retired = apply_dod_turn(
        items, retired, DodTurn(remove=["DOD-T01"], agreed=[d]), additions=False
    )
    assert [i.id for i in items] == ["DOD-T02"] and retired == ["DOD-T01"]
    extra, _ = apply_dod_turn([], [], DodTurn(agreed=[d]), additions=True)
    assert extra[0].id == "DOD-AT01"


def test_requirement_and_ticket_ids():
    """Requirement and ticket ids.

    Spec: S2.5, S2.6 | Traces to: I2
    Expected outcome: requirements number FR-01 and NFR-01; ticket positions become T-IDs.
    """
    fr, nfr = requirement_ids(PRDCore(**script("PRDCore", 2)))
    assert fr == ["FR-01", "FR-02", "FR-03"] and nfr == ["NFR-01"]
    ts = assign_tickets(TicketPlan(**script("TicketPlan", 2)))
    assert [t.id for t in ts] == ["T-001", "T-002", "T-003", "T-004"]
    assert ts[1].depends_on_ids == ["T-001"] and ts[3].depends_on_ids == ["T-003"]
