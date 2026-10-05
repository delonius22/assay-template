"""Intake: log-entry rules and the exit gate, checked on typed fields only."""
from typing import NamedTuple

from ..domain.ids import live
from ..domain.models import LogEntry, NewEntry

GATE_LABELS = [
    "Problem stated from the customer's or business's point of view",
    "Primary users and affected parties named",
    "Target outcome stated, with at least one measurable success measure",
    "Scope in and scope out written down",
    "Main user journeys walked end to end, including failure paths",
    "Data involved and its sensitivity identified",
    "Non-functional needs covered: availability, performance, security, audit, accessibility",
    "Regulatory and control areas identified, each with an owner",
    "Rollout and rollback approach discussed",
    "Every Blocking open question answered or accepted as a named risk",
    "Team Definition of Done exists, and initiative additions are agreed",
]


class GateItem(NamedTuple):
    label: str
    ok: bool
    why: str


def entry_problems(entries: list[NewEntry]) -> list[str]:
    """Problems for entries missing the typed flags the gate depends on.

    Spec: S3.2 | Ticket: 03 | Traces to: I5

    Build steps:
    1. Task: For each `e` with `e.type == "Q"` and (`not e.priority` or `not e.owner`), add
       `f"Open question '{e.title}' needs a priority and an owner."`.
       Expected outcome: every open question is owned and prioritised.
    2. Task: For each decision or assumption (`e.type in ("D", "A")`) with `e.area == "Scope"` and
       `e.scope_side is None`, add `f"Scope entry '{e.title}' needs scope_side: 'in' or 'out'."`.
       Expected outcome: scope entries carry their side.
    3. Task: Same for `e.area == "Journeys"` and `e.journey_path is None`:
       `f"Journey entry '{e.title}' needs journey_path: 'happy' or 'failure'."`.
       Expected outcome: journey entries carry their path.
    4. Task: For each `e.area == "Regulation"` with `not e.owner`, add
       `f"Regulation entry '{e.title}' needs an owner (Compliance, Legal, Risk, InfoSec)."`.
       Expected outcome: regulatory areas always have an owner.
    5. Task: Return the problems list.
       Expected outcome: empty means every entry is gate-ready.
    """
    raise NotImplementedError("S3.2")


def gate(log: list[LogEntry], dod_agreed: bool) -> list[GateItem]:
    """The 11-item intake exit gate, from typed fields only.

    Spec: S3.2 | Ticket: 03 | Traces to: I5

    Build steps:
    1. Task: Let `entries = live(log)` and define `decided(area)` as the entries with
       `e.area == area and e.type in ("D", "A")`.
       Expected outcome: superseded entries never count.
    2. Task: Compute eleven booleans, in GATE_LABELS order:
       Problem: `bool(decided("Problem"))`; Users: `bool(decided("Users"))`;
       Outcome: `any(e.metric for e in decided("Outcome"))`;
       Scope: `{"in", "out"} <= {e.scope_side for e in decided("Scope")}`;
       Journeys: `any(e.journey_path == "failure" for e in decided("Journeys"))`;
       Data: `bool(decided("Data"))`; Non-functional: `bool(decided("Non-functional"))`;
       Regulation: `reg = [e for e in entries if e.area == "Regulation"]`, ok when `bool(reg) and all(e.owner for e in reg)`;
       Rollout: `any(e.covers_rollback for e in decided("Rollout"))`;
       Blocking: no entry with `e.type == "Q" and e.priority == "Blocking" and e.status in (None, "Open", "Parked")`;
       DoD: `dod_agreed`.
       Expected outcome: each check reads fields, never wording.
    3. Task: Pair each boolean with its reason when false: "no decision or assumption about the problem",
       "users and affected parties not recorded", "no outcome with a measure, baseline, and target",
       "need at least one in-scope and one out-of-scope entry", "no failure path recorded",
       "data and its sensitivity not recorded", "non-functional needs not recorded",
       "regulatory areas missing or without owners", "no rollback approach recorded",
       "blocking questions still open: " + ", ".join(the open IDs), "Definition of Done not agreed yet".
       Expected outcome: a reason a PM can act on.
    4. Task: Return `[GateItem(label, ok, why) for label, (ok, why) in zip(GATE_LABELS, checks)]`.
       Expected outcome: eleven items in label order.
    """
    raise NotImplementedError("S3.2")


def failures(items: list[GateItem]) -> list[str]:
    """Failed gate items as 'label: why' lines.

    Spec: S3.2 | Ticket: 03 | Traces to: I5

    Build steps:
    1. Task: Return `[f"{i.label}: {i.why}" for i in items if not i.ok]`.
       Expected outcome: empty means the gate passes.
    """
    raise NotImplementedError("S3.2")
