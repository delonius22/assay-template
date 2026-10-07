"""Ticket rules. List order is build order and dependencies point only
backward, so dependency cycles cannot exist (I15)."""
from ..domain.models import USER_STORY, TicketPlan
from .common import GWT


def plan_problems(plan: TicketPlan, feature_ids: set[str], prd_ids: set[str]) -> list[str]:
    """Problems with a ticket plan.

       Expected outcome: no cycles (I15), right-sized tickets, and every requirement covered.
    """
    problems = []
    n = len(plan.tickets)
    for i, t in enumerate(plan.tickets,1):
      w = f"Ticket {i} ('{t.title[:40]}'): "
      if t.feature_id not in feature_ids:
         problems.append(w + f"unknown feature {t.feature_id}; valid: {sorted(feature_ids)}")
      if t.type == "Ticket" and not USER_STORY.match(t.user_story.strip()):
         problems.append(w + "user_story must read 'As a…, I want…, so that…'")
      if t.type == "Spike" and (not t.question or not t.timebox):
         problems.append(w + "a spike needs a question and a timebox")
      if t.type == "Enabler" and not t.unblocks:
         problems.append(w + "an enabler must list the later tickets it unblocks")
      if t.type == "Ticket" and not t.requirements:
         problems.append(w + "trace at least one FR- or NFR- ID")
      if bad := [r for r in t.requirements if r not in prd_ids]:
         problems.append(w + f"requirements {bad} are not in the PRD")
      if t.type == "Ticket":
         ac = t.acceptance_criteria
         if not (3 <= len(ac) <= 7):
               problems.append(w + f"{len(ac)} acceptance criteria; use 3 to 7")
         for k, c in enumerate(ac, 1):
               if not GWT.match(c):
                  problems.append(w + f"criterion {k} is not Given/When/Then")
      if t.type in {"Spike", "Enabler"} and not t.acceptance_criteria:
         problems.append(w + "state the deliverable as at least one acceptance criterion")
      if any(d < 1 or d >= i for d in t.depends_on):
         problems.append(w + "depends_on may point only to EARLIER tickets (list order is build order)")
      if any(u <= i or u > n for u in t.unblocks):
         problems.append(w + "unblocks may point only to LATER tickets")
      if t.size == "L":
         problems.append(w + "size L is too large for one ticket; split it")

    covered = {r for t in plan.tickets for r in t.requirements} | {u.id for u in plan.uncovered}
    if missing := sorted(r for r in prd_ids if r not in covered):
        problems.append(f"No ticket covers {missing}. Add tickets or list them in uncovered with a reason.")
    return problems
