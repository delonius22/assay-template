"""Every ID is assigned here, by code. Models count and number unreliably,
and IDs must stay stable because people and trackers refer to them (I2)."""

from .models import (DodItem, DodTurn, LogEntry, NewEntry, PRDCore, Questionnaire, Ticket,
                     TicketPlan)

LEVEL_LETTER = {"ticket": "T", "feature": "F", "story": "S", "release": "R"}


def add_entries(log: list[LogEntry], new: list[NewEntry], supersedes: list[str] = ()) -> list[LogEntry]:
    """Append entries with fresh IDs; mark superseded entries, never delete them."""
    out = [e.model_copy() for e in log]
    added = []
    for e in new:
        n = sum(1 for x in out if x.type == e.type) + 1
        entry = LogEntry(id=f"{e.type}-{n:03d}", **e.model_dump())
        out.append(entry)
        added.append(entry.id)
    for old in supersedes:
        for e in out:
            if e.id == old:
                e.superseded_by = sorted(set(e.superseded_by + added))
    return out



def live(log: list[LogEntry]) -> list[LogEntry]:
    """Entries that have not been superseded."""
    return [e for e in log if not e.superseded_by]


def question_ids(q: Questionnaire, round_no: int) -> list[str]:
    """IDs for the primary questions of one round."""

    prefix = "Q-" if round_no == 1 else "Q-F"
    return [f"{prefix}{i:02d}" for i in range(1, len(q.questions) + 1)]


def all_answerable_ids(q: Questionnaire, round_no: int) -> list[str]:
    """Every ID a respondent may answer: questions, follow-ups, and (round 1) confirmations."""

    ids = question_ids(q, round_no)
    follow = [f"{qid}{chr(97 + j)}" for qid, it in zip(ids, q.questions) for j in range(len(it.follow_ups))]
    conf = [f"K-{i:02d}" for i in range(1, len(q.confirmations) + 1)] if round_no == 1 else []
    return ids + follow + conf


def apply_dod_turn(items: list[DodItem], retired: list[str], turn: DodTurn,
                   additions: bool) -> tuple[list[DodItem], list[str]]:
    """Withdraw and add Definition of Done items without ever reusing an ID."""

    prefix = "DOD-A" if additions else "DOD-"
    retired.extend([i.id for i in items if i.id in turn.remove])
    kept = [i for i in items if i.id not in turn.remove]
    for d in turn.agreed:
        stem = f"{prefix}{LEVEL_LETTER[d.level]}"
        n = sum(1 for u in [i.id for i in kept] + retired if u.startswith(stem)) + 1
        kept.append(DodItem(id=f"{stem}{n:02d}", **d.model_dump()))
    return kept, retired


def requirement_ids(core: PRDCore) -> tuple[list[str], list[str]]:
    """FR-01… and NFR-01… in list order."""
    fr = [f"FR-{i:02d}" for i in range(1, len(core.functional) + 1)]
    nfr = [f"NFR-{i:02d}" for i in range(1, len(core.non_functional) + 1)]
    return fr, nfr
    


def assign_tickets(plan: TicketPlan) -> list[Ticket]:
    """T-001… in list order (the build order); 1-based positions become IDs."""
    ids = [f"T-{i:03d}" for i in range(1, len(plan.tickets) + 1)]
    tickets = [
        Ticket(
            id=tid,
            **t.model_dump(),
            depends_on_ids=[ids[d - 1] for d in t.depends_on],
            unblocks_ids=[ids[u - 1] for u in t.unblocks],
        )
        for tid, t in zip(ids, plan.tickets)
    ]
    return tickets
