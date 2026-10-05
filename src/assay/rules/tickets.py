"""Check a ticket plan.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C4 Traceable documents. Tickets must be traceable, testable,
right-sized, and in build order. This file checks a plan; it never cuts tickets.

Why this comes now: IDs (step 3) and shared rules (step 4) exist; tickets are the
last document.

Build order: Step 9 of 33.
Previous: src/assay/rules/spec.py (step 8), which holds the spec coverage rule.
Next: src/assay/llm/caching.py (step 10), which builds cache-friendly messages and
reads token usage.

Build these in order:
    1. plan_problems: the only ticket rule.

Depends on:
    assay.domain.models: TicketPlan, USER_STORY. The plan and story wording.
    assay.rules.common: GWT. The acceptance-criterion shape.
    Standard library: none.
    Third-party: none.

Depended on by:
    assay.llm.agents: the agent validators. assay.graph.nodes: the stage gates.

Spec coverage: S3.6 | Traces to: I1, I15
"""

from assay.domain.models import USER_STORY, TicketPlan
from assay.rules.common import GWT


def plan_problems(plan: TicketPlan, feature_ids: set[str], prd_ids: set[str]) -> list[str]:
    """Return every problem with a ticket plan.

    Problem piece: C4: a backlog where every ticket traces, tests, fits, and can be
                   built in order.

    Why it matters: A ticket a tester cannot verify is never provably done; one
                    depending on a later ticket creates a cycle; an uncovered
                    requirement is silently dropped. List order is build order, so
                    checking that dependencies point backward rules out cycles
                    entirely (I15).

    What: Names each problem with the ticket's position and title: unknown feature,
          story wording, spike and enabler fields, traces, criteria, dependency
          direction, size, and coverage of every FR and NFR.

    Spec: S3.6 | Ticket: 07 | Traces to: I1, I15

    Build steps:
    1. Task: Prefix every problem with the ticket's 1-based position and the first
             40 characters of its title, and flag an unknown feature.
       Expected outcome: A ticket for F-09 produces 'Ticket 1 (...): unknown feature
                         F-09'.
    2. Task: Check type-specific fields: tickets need a user story; spikes need a
             question and a timebox; enablers need later tickets to unblock; tickets
             and enablers need at least one requirement, and every requirement must
             be in the PRD.
       Expected outcome: A spike without a timebox produces a problem.
    3. Task: Check criteria: tickets need 3 to 7, each Given/When/Then (the GWT
             pattern); spikes and enablers need at least one.
       Expected outcome: A ticket with 2 criteria produces a problem.
    4. Task: Check dependencies point only to earlier positions and unblocks only to
             later ones, and reject size L.
       Think about: Why does checking direction remove the need for cycle detection?
       Expected outcome: A ticket depending on itself produces a problem.
    5. Task: Check every FR and NFR in the PRD is covered by a ticket or listed as
             uncovered.
       Expected outcome: Dropping NFR-01 from every ticket produces 'No ticket
                         covers ['NFR-01']'.
    """
    raise NotImplementedError("S3.6: plan_problems")
