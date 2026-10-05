"""Rules as pure functions: no models, no graph."""

from assay.domain.ids import add_entries, assign_tickets
from assay.domain.models import NewEntry, TicketPlan
from assay.rules import common, intake, tickets
from tests.support.script import script


def entry(**kw):
    """Test helper: entry."""
    return NewEntry(**{"type": "D", "title": "t", "detail": "d", "source": "PM", **kw})


def test_gate_checks_typed_flags_not_words():
    # The words say "out of scope", but no scope_side flag: the gate is not fooled.
    """Gate checks typed flags not words.

    Spec: S3.2 | Traces to: I5
    Expected outcome: scope wording with the 'in' flag fails the scope item.
    """
    log = add_entries(
        [], [entry(area="Scope", title="Joint holders are out of scope", scope_side="in")]
    )
    failed = intake.failures(intake.gate(log, dod_agreed=True))
    assert any(f.startswith("Scope in and scope out") for f in failed)


def test_gate_passes_on_full_scripted_intake():
    """Gate passes on full scripted intake.

    Spec: S3.2 | Traces to: I5
    Expected outcome: a full scripted intake passes except for the DoD item.
    """
    log = add_entries([], [NewEntry(**x) for x in script("GrillTurn", 3)["recorded"]])
    assert intake.failures(intake.gate(log, dod_agreed=True)) == []
    assert intake.failures(intake.gate(log, dod_agreed=False)) == [
        "Team Definition of Done exists, and initiative additions are agreed: Definition of Done not agreed yet"
    ]


def test_entries_must_carry_gate_flags():
    """Entries must carry gate flags.

    Spec: S3.2 | Traces to: I5
    Expected outcome: three entries missing flags produce three problems.
    """
    problems = intake.entry_problems(
        [entry(area="Scope"), entry(area="Journeys"), entry(type="Q", area="Data")]
    )
    assert len(problems) == 3


def test_compliance_claims_catch_reworded_assertions():
    """Compliance claims catch reworded assertions.

    Spec: S3.1 | Traces to: I4
    Expected outcome: 'conforms to' is flagged; 'Compliance to confirm' is not.
    """
    assert common.compliance_claims("The design conforms to Reg E.")
    assert not common.compliance_claims("Reg E applicability: Compliance to confirm.")


def test_ticket_order_is_build_order_so_no_cycles():
    """Ticket order is build order so no cycles.

    Spec: S3.6 | Traces to: I15
    Expected outcome: a dependency on a later ticket is rejected.
    """
    plan = TicketPlan(**script("TicketPlan", 2))
    plan.tickets[0].depends_on = [2]  # points forward: rejected
    problems = tickets.plan_problems(plan, {"F-01", "F-02"}, {"FR-01", "FR-02", "FR-03", "NFR-01"})
    assert any("EARLIER" in p for p in problems)


def test_ticket_plan_must_cover_every_fr():
    """Ticket plan must cover every fr.

    Spec: S3.6 | Traces to: I15
    Expected outcome: a plan missing FR-03 is rejected.
    """
    plan = TicketPlan(**script("TicketPlan", 1))
    problems = tickets.plan_problems(plan, {"F-01", "F-02"}, {"FR-01", "FR-02", "FR-03", "NFR-01"})
    assert any("FR-03" in p for p in problems)


def test_positions_become_ids():
    """Positions become ids.

    Spec: S2.6 | Traces to: I15
    Expected outcome: positions convert to T-001 to T-004 and T-003 dependencies.
    """
    ts = assign_tickets(TicketPlan(**script("TicketPlan", 2)))
    assert [t.id for t in ts] == ["T-001", "T-002", "T-003", "T-004"]
    assert ts[3].depends_on_ids == ["T-003"]


def test_ticket_plan_must_cover_nfrs_too():
    """Ticket plan must cover nfrs too.

    Spec: S3.6 | Traces to: I15
    Expected outcome: dropping NFR-01 from every ticket is rejected.
    """
    plan = TicketPlan(**script("TicketPlan", 2))
    plan.tickets[0].requirements = ["FR-01"]  # drop NFR-01
    problems = tickets.plan_problems(plan, {"F-01", "F-02"}, {"FR-01", "FR-02", "FR-03", "NFR-01"})
    assert any("NFR-01" in p for p in problems)


def test_size_l_is_rejected():
    """Size l is rejected.

    Spec: S3.6 | Traces to: I15
    Expected outcome: a size L ticket is rejected.
    """
    plan = TicketPlan(**script("TicketPlan", 2))
    plan.tickets[0].size = "L"
    assert any(
        "size L" in p
        for p in tickets.plan_problems(
            plan, {"F-01", "F-02"}, {"FR-01", "FR-02", "FR-03", "NFR-01"}
        )
    )
