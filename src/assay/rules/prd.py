"""Check the PRD's stories, features, requirements, and narrative.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C4 Traceable documents. Every PRD claim must trace to a
recorded source. This file checks structure and sources; it never writes the PRD.

Why this comes now: Shared rules exist (step 4); the PRD follows the DoD.

Build order: Step 7 of 33.
Previous: src/assay/rules/dod.py (step 6), which holds the Definition of Done rules.
Next: src/assay/rules/spec.py (step 8), which holds the spec coverage rule.

Build these in order:
    1. core_problems: the traceable core.
    2. narrative_problems: the prose part.

Depends on:
    assay.domain.models: PRDCore, PRDNarrative, USER_STORY. The PRD shapes and story
    wording.
    assay.rules.common: compliance_claims. No compliance assertions.
    Standard library: none.
    Third-party: none.

Depended on by:
    assay.llm.agents: the agent validators. assay.graph.nodes: the stage gates.

Spec coverage: S3.4 | Traces to: I3, I4
"""

from assay.domain.models import USER_STORY, PRDCore, PRDNarrative
from assay.rules.common import compliance_claims


def core_problems(core: PRDCore, known_ids: set[str]) -> list[str]:
    """Return problems with the PRD's stories, features, and requirements.

    Problem piece: C4: a PRD whose every requirement is sourced and placed.

    Why it matters: An approver signs requirements believing each rests on something
                    people said. A requirement citing an invented ID, or a feature
                    with no requirement, breaks that belief silently; numbering
                    errors break the IDs every later stage cites.

    What: Checks story wording and numbering, feature numbering across stories,
          requirement features and sources, features without requirements, and
          compliance claims.

    Spec: S3.4 | Ticket: 05 | Traces to: I3, I4

    Build steps:
    1. Task: Check each story reads 'As a..., I want..., so that...' (the USER_STORY
             pattern) and stories run S-01, S-02 in order.
       Expected outcome: A story 'Low-balance alerts' produces a wording problem.
    2. Task: Check features run F-01, F-02 in order across all stories, every
             requirement names a real feature, and every feature has a functional
             requirement.
       Think about: Why must numbering continue across stories?
       Expected outcome: Restarting F-01 under the second story produces a problem.
    3. Task: Check every requirement's sources are known IDs, naming the unknown
             ones, then add compliance problems.
       Expected outcome: A source D-999 produces a problem naming D-999.
    """
    raise NotImplementedError("S3.4: core_problems")


def narrative_problems(nar: PRDNarrative, known_ids: set[str]) -> list[str]:
    """Return problems with the PRD narrative.

    Problem piece: C4: objectives sourced, prose free of compliance claims.

    Why it matters: Objectives are the success an approver signs for; an unsourced
                    objective is a wish. The narrative is also where compliance
                    language tends to creep in, because it is written as persuasive
                    prose.

    What: Flags objectives with unknown sources and any compliance assertion. Called
          as narrative_problems(nar: PRDNarrative, known_ids: set[str]) and returns
          list[str].

    Spec: S3.4 | Ticket: 05 | Traces to: I3, I4

    Build steps:
    1. Task: Flag each objective whose source is unknown, then add compliance
             problems.
       Expected outcome: An objective citing D-999 produces a problem.
    """
    raise NotImplementedError("S3.4: narrative_problems")
