"""Intake: log-entry rules and the exit gate, checked on typed fields only."""
from calendar import c
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
   """Problems for entries missing the typed flags the gate depends on."""
   p = []
   for e in entries:
      if e.type == "Q" and (not e.priority or not e.owner):
         p.append(f"Open question '{e.title}' needs a priority and an owner.")
      if e.area == "Scope" and e.type in ("D", "A") and e.scope_side is None:
         p.append(f"Scope entry '{e.title}' needs scope_side: 'in' or 'out'.")
      if e.area == "Journeys" and e.type in ("D", "A") and e.journey_path is None:
         p.append(f"Journey entry '{e.title}' needs journey_path: 'happy' or 'failure'.")
      if e.area == "Regulation" and not e.owner:
         p.append(f"Regulation entry '{e.title}' needs an owner (Compliance, Legal, Risk, InfoSec).")
   return p


def gate(log: list[LogEntry], dod_agreed: bool) -> list[GateItem]:
   """The 11-item intake exit gate, from typed fields only."""
   regulation_entries = [entry for entry in live(log) if entry.area == "Regulation"]
   open_blocking_ids = [entry.id for entry in live(log) if entry.type =="Q" and entry.priority == "Blocking" and entry.status in (None, "Open","Parked")]


   def decided(area:str) -> list[LogEntry]:
      return [e for e in live(log) if e.area == area and e.type in ("D", "A")]

   checks = [
      (bool(decided("Problem")), "no decision or assumption about the problem"),
    (bool(decided("Users")), "users and affected parties not recorded"),
    (
        any(entry.metric for entry in decided("Outcome")),
        "no outcome with a measure, baseline, and target",
    ),
    (
        {"in", "out"} <= {entry.scope_side for entry in decided("Scope")},
        "need at least one in-scope and one out-of-scope entry",
    ),
    (
        any(entry.journey_path == "failure" for entry in decided("Journeys")),
        "no failure path recorded",
    ),
    (bool(decided("Data")), "data and its sensitivity not recorded"),
    (
        bool(decided("Non-functional")),
        "non-functional needs not recorded",
    ),
    (
        bool(regulation_entries) and all(entry.owner for entry in regulation_entries),
        "regulatory areas missing or without owners",
    ),
    (
        any(entry.covers_rollback for entry in decided("Rollout")),
        "no rollback approach recorded",
    ),
    (
        not open_blocking_ids,
        "blocking questions still open: " + ", ".join(open_blocking_ids),
    ),
    (dod_agreed, "Definition of Done not agreed yet"),
   ]

   return [
      GateItem(label, ok, "" if ok else why)
      for label, (ok, why) in zip(GATE_LABELS, checks)]
      

def failures(items: list[GateItem]) -> list[str]:
    """Failed gate items as 'label: why' lines."""
    return [f"{i.label}: {i.why}" for i in items if not i.ok]
