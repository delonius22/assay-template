"""Definition of Done rules."""
from ..domain.models import DodItem, DodItemDraft
from .common import vague_words


def draft_problems(items: list[DodItemDraft]) -> list[str]:
    """Problems with individual DoD items."""
    p = []
    for it in items:
      if vague := vague_words(it.statement):
          p.append(f"'{it.statement}' uses vague words {vague}. Make it verifiable.")
      if it.verified_by.strip().lower() in ("team", "the team", "everyone"):
          p.append(f"'{it.statement}': verified_by must name a role.")
      if len(it.statement.split()) > 18:
          p.append(f"'{it.statement}' is long; keep the statement short and move detail to how_verified.")
    return p


def team_problems(items: list[DodItem]) -> list[str]:
    """Problems with a whole team standard. Expected outcome: empty means the standard can be saved."""
    p = draft_problems(items)
    n_ticket = sum(1 for i in items if i.level == "ticket")
    if n_ticket == 0:
        p.append("No ticket-level items: every ticket needs a quality bar.")
    if n_ticket > 12:
        p.append(f"{n_ticket} ticket-level items; above 12, people stop reading. Move some to feature level or automate them.")
    return p
