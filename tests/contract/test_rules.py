"""Rules as pure functions: no models, no graph."""
from assay.domain.ids import add_entries, assign_tickets
from assay.domain.models import NewEntry, TicketPlan
from assay.rules import common, intake, tickets
from tests.support.script import script


def entry(**kw):
    return NewEntry(**{"type": "D", "title": "t", "detail": "d", "source": "PM", **kw})


def test_gate_checks_typed_flags_not_words():
    # The words say "out of scope", but no scope_side flag: the gate is not fooled.
    log = add_entries([], [entry(area="Scope", title="Joint holders are out of scope", scope_side="in")])
    failed = intake.failures(intake.gate(log, dod_agreed=True))
    assert any(f.startswith("Scope in and scope out") for f in failed)


def test_gate_passes_on_full_scripted_intake():
    log = add_entries([], [NewEntry(**x) for x in script("GrillTurn", 3)["recorded"]])
    assert intake.failures(intake.gate(log, dod_agreed=True)) == []
    assert intake.failures(intake.gate(log, dod_agreed=False)) == [
        "Team Definition of Done exists, and initiative additions are agreed: Definition of Done not agreed yet"]


def test_entries_must_carry_gate_flags():
    problems = intake.entry_problems([entry(area="Scope"), entry(area="Journeys"),
                                      entry(type="Q", area="Data")])
    assert len(problems) == 3


def test_compliance_claims_catch_reworded_assertions():
    assert common.compliance_claims("The design conforms to Reg E.")
    assert not common.compliance_claims("Reg E applicability: Compliance to confirm.")


def test_ticket_order_is_build_order_so_no_cycles():
    plan = TicketPlan(**script("TicketPlan", 2))
    plan.tickets[0].depends_on = [2]          # points forward: rejected
    problems = tickets.plan_problems(plan, {"F-01", "F-02"}, {"FR-01", "FR-02", "FR-03", "NFR-01"})
    assert any("EARLIER" in p for p in problems)


def test_ticket_plan_must_cover_every_fr():
    plan = TicketPlan(**script("TicketPlan", 1))
    problems = tickets.plan_problems(plan, {"F-01", "F-02"}, {"FR-01", "FR-02", "FR-03", "NFR-01"})
    assert any("FR-03" in p for p in problems)


def test_positions_become_ids():
    ts = assign_tickets(TicketPlan(**script("TicketPlan", 2)))
    assert [t.id for t in ts] == ["T-001", "T-002", "T-003", "T-004"]
    assert ts[3].depends_on_ids == ["T-003"]


def test_ticket_plan_must_cover_nfrs_too():
    plan = TicketPlan(**script("TicketPlan", 2))
    plan.tickets[0].requirements = ["FR-01"]          # drop NFR-01
    problems = tickets.plan_problems(plan, {"F-01", "F-02"}, {"FR-01", "FR-02", "FR-03", "NFR-01"})
    assert any("NFR-01" in p for p in problems)


def test_size_l_is_rejected():
    plan = TicketPlan(**script("TicketPlan", 2))
    plan.tickets[0].size = "L"
    assert any("size L" in p for p in tickets.plan_problems(plan, {"F-01", "F-02"},
                                                            {"FR-01", "FR-02", "FR-03", "NFR-01"}))
