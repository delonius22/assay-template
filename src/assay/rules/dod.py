"""Check Definition of Done items and the team standard.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C6 People decide. A quality bar works only if every item is
verifiable and owned. This file checks items; it never stores them.

Why this comes now: Shared rules exist (step 4); the DoD stage follows intake.

Build order: Step 6 of 33.
Previous: src/assay/rules/intake.py (step 5), which holds the intake entry rules and
the 11-item exit gate.
Next: src/assay/rules/prd.py (step 7), which holds the PRD rules.

Build these in order:
    1. draft_problems: item-level checks first.
    2. team_problems: builds on draft_problems.

Depends on:
    assay.domain.models: DodItem, DodItemDraft. The items checked.
    assay.rules.common: vague_words. Rejects unverifiable wording.
    Standard library: none.
    Third-party: none.

Depended on by:
    assay.llm.agents: the agent validators. assay.graph.nodes: the stage gates.

Spec coverage: S3.3 | Traces to: I1
"""

from assay.domain.models import DodItem, DodItemDraft
from assay.rules.common import vague_words


def draft_problems(items: list[DodItemDraft]) -> list[str]:
    """Return problems with individual Definition of Done items.

    Problem piece: C6: each check is verifiable, owned, and short.

    Why it matters: An item nobody can verify gets ticked without looking, and an
                    item owned by 'the team' is owned by nobody. Rejecting both at
                    agreement time keeps the standard real.

    What: Flags vague wording, 'team' or 'everyone' as verifier, and statements over
          18 words. Called as draft_problems(items: list[DodItemDraft]) and returns
          list[str].

    Spec: S3.3 | Ticket: 04 | Traces to: I1

    Build steps:
    1. Task: Flag vague words with: '<statement>' uses vague words <list>. Make it
             verifiable.
       Expected outcome: 'Code is clean' produces one problem.
    2. Task: Flag a verifier of 'team', 'the team', or 'everyone', and any statement
             over 18 words.
       Think about: Where should the detail of a long statement go instead?
       Expected outcome: A 19-word statement produces one problem.
    """
    raise NotImplementedError("S3.3: draft_problems")


def team_problems(items: list[DodItem]) -> list[str]:
    """Return problems with a whole team standard.

    Problem piece: C6: a standard every ticket can meet and people still read.

    Why it matters: A standard with no ticket-level item gives tickets no quality
                    bar; one with dozens is skimmed. Both make the DoD decorative.

    What: Item problems, plus none or more than 12 ticket-level items. Called as
          team_problems(items: list[DodItem]) and returns list[str].

    Spec: S3.3 | Ticket: 04 | Traces to: I1

    Build steps:
    1. Task: Include every item problem, then flag zero ticket-level items and more
             than 12.
       Expected outcome: A standard with 13 ticket-level items produces a problem.
    """
    raise NotImplementedError("S3.3: team_problems")
