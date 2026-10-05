"""Check that the spec covers exactly the PRD's requirements.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C4 Traceable documents. Every requirement needs design. This
file checks coverage and module traces; it never designs.

Why this comes now: Shared rules exist (step 4); the spec follows the PRD.

Build order: Step 8 of 33.
Previous: src/assay/rules/prd.py (step 7), which holds the PRD rules.
Next: src/assay/rules/tickets.py (step 9), which holds the ticket plan rules.

Build these in order:
    1. problems: the only spec rule.

Depends on:
    assay.domain.models: Spec. The spec checked.
    assay.rules.common: compliance_claims. No compliance assertions.
    Standard library: none.
    Third-party: none.

Depended on by:
    assay.llm.agents: the agent validators. assay.graph.nodes: the stage gates.

Spec coverage: S3.5 | Traces to: I1, I4
"""

from assay.domain.models import Spec
from assay.rules.common import compliance_claims


def problems(spec: Spec, prd_ids: set[str]) -> list[str]:
    """Return coverage and trace problems with a spec.

    Problem piece: C4: no requirement without design, no design without a
                   requirement.

    Why it matters: A requirement missing from the coverage table is one nobody
                    builds; a module serving an unknown ID is design nobody asked
                    for. Both are cheap to catch here and expensive after tickets
                    are cut.

    What: Flags missing and extra coverage IDs, modules serving unknown IDs, and
          compliance claims. Called as problems(spec: Spec, prd_ids: set[str]) and
          returns list[str].

    Spec: S3.5 | Ticket: 06 | Traces to: I1

    Build steps:
    1. Task: Compare covered IDs with the PRD IDs in both directions, naming missing
             and extra IDs.
       Expected outcome: A spec omitting FR-02 produces a problem naming FR-02.
    2. Task: Flag modules that serve IDs not in the PRD, then add compliance
             problems.
       Expected outcome: A module serving FR-99 produces a problem.
    """
    raise NotImplementedError("S3.5: problems")
