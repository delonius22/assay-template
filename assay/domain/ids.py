"""Every ID is assigned here, by code. Models count and number unreliably,
and IDs must stay stable because people and trackers refer to them (I2)."""
from .models import (DodItem, DodTurn, LogEntry, NewEntry, PRDCore, Questionnaire, Ticket,
                     TicketPlan)

LEVEL_LETTER = {"ticket": "T", "feature": "F", "story": "S", "release": "R"}


def add_entries(log: list[LogEntry], new: list[NewEntry], supersedes: list[str] = ()) -> list[LogEntry]:
    """Append entries with fresh IDs; mark superseded entries, never delete them.

    Spec: S2.1 | Ticket: 01 | Traces to: I2

    Build steps:
    1. Task: Copy the log: `out = [e.model_copy() for e in log]`.
       Expected outcome: the caller's list is not mutated.
    2. Task: For each `e` in `new`, count existing entries of its type:
       `n = sum(1 for x in out if x.type == e.type) + 1`, then build
       `entry = LogEntry(id=f"{e.type}-{n:03d}", **e.model_dump())`, append it, and add its id to `added`.
       Expected outcome: IDs like D-001, D-002, Q-001, numbered per type across the whole log.
    3. Task: For each `old` in `supersedes`, find the entry with `e.id == old` and set
       `e.superseded_by = sorted(set(e.superseded_by + added))`.
       Expected outcome: replaced entries stay in the log, marked.
    4. Task: Return `out`.
       Expected outcome: the full log with new entries appended.
    """
    raise NotImplementedError("S2.1")


def live(log: list[LogEntry]) -> list[LogEntry]:
    """Entries that have not been superseded.

    Spec: S2.2 | Ticket: 01 | Traces to: I2

    Build steps:
    1. Task: Return `[e for e in log if not e.superseded_by]`.
       Expected outcome: only current entries, original order kept.
    """
    raise NotImplementedError("S2.2")


def question_ids(q: Questionnaire, round_no: int) -> list[str]:
    """IDs for the primary questions of one round.

    Spec: S2.3 | Ticket: 08 | Traces to: I2

    Build steps:
    1. Task: Set `prefix = "Q-" if round_no == 1 else "Q-F"`.
       Expected outcome: round one uses Q-01…, the follow-up round Q-F01….
    2. Task: Return `[f"{prefix}{i:02d}" for i in range(1, len(q.questions) + 1)]`.
       Expected outcome: one ID per question in list order.
    """
    raise NotImplementedError("S2.3")


def all_answerable_ids(q: Questionnaire, round_no: int) -> list[str]:
    """Every ID a respondent may answer: questions, follow-ups, and (round 1) confirmations.

    Spec: S2.3 | Ticket: 08 | Traces to: I2, I12

    Build steps:
    1. Task: Get `ids = question_ids(q, round_no)`.
       Expected outcome: primary question IDs.
    2. Task: Build `follow = [f"{qid}{chr(97 + j)}" for qid, it in zip(ids, q.questions) for j in range(len(it.follow_ups))]`.
       Expected outcome: follow-up IDs like Q-01a, Q-01b.
    3. Task: Build `conf = [f"K-{i:02d}" for i in range(1, len(q.confirmations) + 1)]` only when `round_no == 1`, else `[]`.
       Expected outcome: confirmations never collide across rounds.
    4. Task: Return `ids + follow + conf`.
       Expected outcome: the full allowlist the questionnaire endpoint validates against.
    """
    raise NotImplementedError("S2.3")


def apply_dod_turn(items: list[DodItem], retired: list[str], turn: DodTurn,
                   additions: bool) -> tuple[list[DodItem], list[str]]:
    """Withdraw and add Definition of Done items without ever reusing an ID.

    Spec: S2.4 | Ticket: 04 | Traces to: I2

    Build steps:
    1. Task: Set `prefix = "DOD-A" if additions else "DOD-"`.
       Expected outcome: team items DOD-T01…, additions DOD-AT01….
    2. Task: Extend `retired` with `[i.id for i in items if i.id in turn.remove]` and keep
       `kept = [i for i in items if i.id not in turn.remove]`.
       Expected outcome: withdrawn IDs are remembered.
    3. Task: For each draft `d` in `turn.agreed`: `stem = f"{prefix}{LEVEL_LETTER[d.level]}"`;
       `n = sum(1 for u in [i.id for i in kept] + retired if u.startswith(stem)) + 1`;
       append `DodItem(id=f"{stem}{n:02d}", **d.model_dump())` to `kept`.
       Expected outcome: numbering counts kept AND retired IDs, so none is reused.
    4. Task: Return `(kept, retired)`.
       Expected outcome: the new item list and the updated retired list.
    """
    raise NotImplementedError("S2.4")


def requirement_ids(core: PRDCore) -> tuple[list[str], list[str]]:
    """FR-01… and NFR-01… in list order.

    Spec: S2.5 | Ticket: 05 | Traces to: I2

    Build steps:
    1. Task: Build `fr = [f"FR-{i:02d}" for i in range(1, len(core.functional) + 1)]`.
       Expected outcome: one ID per functional requirement.
    2. Task: Build `nfr = [f"NFR-{i:02d}" for i in range(1, len(core.non_functional) + 1)]`.
       Expected outcome: one ID per non-functional requirement.
    3. Task: Return `(fr, nfr)`.
       Expected outcome: IDs aligned by position with the requirement lists.
    """
    raise NotImplementedError("S2.5")


def assign_tickets(plan: TicketPlan) -> list[Ticket]:
    """T-001… in list order (the build order); 1-based positions become IDs.

    Spec: S2.6 | Ticket: 07 | Traces to: I2, I15

    Build steps:
    1. Task: Build `ids = [f"T-{i:03d}" for i in range(1, len(plan.tickets) + 1)]`.
       Expected outcome: one ID per ticket.
    2. Task: For each `(tid, t)` in `zip(ids, plan.tickets)`, build
       `Ticket(id=tid, **t.model_dump(), depends_on_ids=[ids[d - 1] for d in t.depends_on],
       unblocks_ids=[ids[u - 1] for u in t.unblocks])`.
       Expected outcome: positions are 1-based, so position 3 maps to `ids[2]` = T-003.
    3. Task: Return the list of Ticket.
       Expected outcome: positions were validated by S3.6 before this runs.
    """
    raise NotImplementedError("S2.6")
