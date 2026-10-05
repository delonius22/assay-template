"""Definition of Done rules."""
from ..domain.models import DodItem, DodItemDraft
from .common import vague_words


def draft_problems(items: list[DodItemDraft]) -> list[str]:
    """Problems with individual DoD items.

    Spec: S3.3 | Ticket: 04 | Traces to: I1

    Build steps:
    1. Task: For each `it`, if `vague := vague_words(it.statement)`, add
       `f"'{it.statement}' uses vague words {vague}. Make it verifiable."`.
       Expected outcome: unverifiable wording is rejected.
    2. Task: If `it.verified_by.strip().lower() in ("team", "the team", "everyone")`, add
       `f"'{it.statement}': verified_by must name a role."`.
       Expected outcome: every item has an owner.
    3. Task: If `len(it.statement.split()) > 18`, add
       `f"'{it.statement}' is long; keep the statement short and move detail to how_verified."`.
       Expected outcome: statements stay scannable.
    4. Task: Return the problems.
       Expected outcome: empty means every item passes.
    """
    raise NotImplementedError("S3.3")


def team_problems(items: list[DodItem]) -> list[str]:
    """Problems with a whole team standard.

    Spec: S3.3 | Ticket: 04 | Traces to: I1

    Build steps:
    1. Task: Start with `p = draft_problems(items)`.
       Expected outcome: item-level problems included.
    2. Task: Count `n_ticket = sum(1 for i in items if i.level == "ticket")`.
       Expected outcome: the number of checks every ticket must pass.
    3. Task: If `n_ticket == 0`, add "No ticket-level items: every ticket needs a quality bar.";
       if `n_ticket > 12`, add f"{n_ticket} ticket-level items; above 12, people stop reading. Move some to feature level or automate them."
       Expected outcome: the standard stays usable.
    4. Task: Return `p`.
       Expected outcome: empty means the standard can be saved.
    """
    raise NotImplementedError("S3.3")
