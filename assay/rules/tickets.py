"""Ticket rules. List order is build order and dependencies point only
backward, so dependency cycles cannot exist (I15)."""
from ..domain.models import USER_STORY, TicketPlan
from .common import GWT


def plan_problems(plan: TicketPlan, feature_ids: set[str], prd_ids: set[str]) -> list[str]:
    """Problems with a ticket plan.

    Spec: S3.6 | Ticket: 07 | Traces to: I1, I15

    Build steps:
    1. Task: Let `n = len(plan.tickets)`; iterate `for i, t in enumerate(plan.tickets, 1)` with
       prefix `w = f"Ticket {i} ('{t.title[:40]}'): "`.
       Expected outcome: every message names the ticket.
    2. Task: Add `w + f"unknown feature {t.feature_id}; valid: {sorted(feature_ids)}"` when
       `t.feature_id not in feature_ids`; add `w + "user_story must read 'As a…, I want…, so that…'"` when
       `t.type == "Ticket" and not USER_STORY.match(t.user_story.strip())`.
       Expected outcome: tickets belong to approved features and say who benefits.
    3. Task: Spikes need `t.question and t.timebox` ("a spike needs a question and a timebox");
       enablers need `t.unblocks` ("an enabler must list the later tickets it unblocks");
       tickets and enablers need `t.requirements` ("trace at least one FR- or NFR- ID");
       any `r` in `t.requirements` not in `prd_ids` gives w + f"requirements {bad} are not in the PRD".
       Expected outcome: every item is traceable.
    4. Task: For `t.type == "Ticket"`: require `3 <= len(ac) <= 7` (w + f"{len(ac)} acceptance criteria; use 3 to 7")
       and `GWT.match(c)` for each criterion `c` (w + f"criterion {k} is not Given/When/Then");
       for spikes and enablers require at least one criterion
       (w + "state the deliverable as at least one acceptance criterion").
       Expected outcome: every ticket can be proven done.
    5. Task: Add w + "depends_on may point only to EARLIER tickets (list order is build order)" when
       `any(d < 1 or d >= i for d in t.depends_on)`; add w + "unblocks may point only to LATER tickets" when
       `any(u <= i or u > n for u in t.unblocks)`; add w + "size L is too large for one ticket; split it" when
       `t.size == "L"`. Then build `covered = {r for t in plan.tickets for r in t.requirements} | {u.id for u in plan.uncovered}`
       and add f"No ticket covers {missing}. Add tickets or list them in uncovered with a reason." when
       `missing := sorted(r for r in prd_ids if r not in covered)` (FR and NFR, decision D5). Return the problems.
       Expected outcome: no cycles (I15), right-sized tickets, and every requirement covered.
    """
    raise NotImplementedError("S3.6")
