"""Check intake entries and decide whether intake is complete.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C3 Gated progress. The PRD may be written only when intake
covers every area. This file owns the entry flags and the exit gate, checked on
typed fields; it never asks questions.

Why this comes now: Shared rules exist (step 4). The intake gate is the first gate a
session meets.

Build order: Step 5 of 33.
Previous: src/assay/rules/common.py (step 4), which holds the shared text rules:
compliance claims, single questions, vague words.
Next: src/assay/rules/dod.py (step 6), which holds the Definition of Done rules.

Build these in order:
    1. GateItem: the result type gate returns.
    2. entry_problems: used while recording.
    3. gate: the gate itself.
    4. failures: formats gate output.

Depends on:
    assay.domain.ids: live. Only current entries count.
    assay.domain.models: LogEntry, NewEntry. The entries checked.
    Standard library: typing.
    Third-party: none.

Depended on by:
    assay.llm.agents: the agent validators. assay.graph.nodes: the stage gates.
    assay.render.markdown: prints the gate.

Spec coverage: S3.2 | Traces to: I5
"""

from typing import NamedTuple

from assay.domain.ids import live
from assay.domain.models import LogEntry, NewEntry

GATE_LABELS: list[str] = [  # S3.2: the exit gate, in order
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
    """One exit-gate item and its result.

    Problem piece: C3: a gate result a person can act on.

    Why it matters: A pass or fail alone does not tell a PM what to do next; each
                    failed item carries its reason.

    What: Label, pass flag, and reason.

    Spec: S3.2 | Ticket: — | Traces to: —
    """

    label: str
    ok: bool
    why: str


def entry_problems(entries: list[NewEntry]) -> list[str]:
    """Return problems for entries missing the flags the gate depends on.

    Problem piece: C3: entries carry the typed facts the gate checks.

    Why it matters: The gate reads flags, not wording, so an entry recorded without
                    its flag can never satisfy the gate. Checking at recording time
                    makes the agent fix it while the answer is fresh, instead of the
                    gate failing later for an invisible reason.

    What: Open questions need a priority and owner; scope decisions and assumptions
          need a side; journey decisions and assumptions need a path; regulation
          entries need an owner.

    Spec: S3.2 | Ticket: 03 | Traces to: I5

    Build steps:
    1. Task: Flag open questions without a priority or owner: Open question
             '<title>' needs a priority and an owner.
       Expected outcome: A question with no owner produces that problem.
    2. Task: Flag scope and journey decisions or assumptions missing scope_side or
             journey_path, naming the allowed values 'in' or 'out' and 'happy' or
             'failure'.
       Expected outcome: A scope decision with no side produces a problem naming in
                         or out.
    3. Task: Flag regulation entries without an owner, naming Compliance, Legal,
             Risk, InfoSec.
       Expected outcome: A regulation entry without an owner produces a problem.
    """
    raise NotImplementedError("S3.2: entry_problems")


def gate(log: list[LogEntry], dod_agreed: bool) -> list[GateItem]:
    """Return the 11 exit-gate items, checked on typed fields only.

    Problem piece: C3: the single decision that intake is done.

    Why it matters: Word-matching lets phrasing pass the gate: 'Out of scope: none'
                    contains the right words and proves nothing. Reading the typed
                    flags makes the gate test what was actually decided, which is
                    the only thing a PRD can safely rest on.

    What: Takes the log and whether the DoD is agreed; returns one GateItem per
          GATE_LABELS entry.

    Spec: S3.2 | Ticket: 03 | Traces to: I5

    Build steps:
    1. Task: Consider only live entries, and treat an area as decided when it has a
             decision or assumption.
       Expected outcome: A superseded decision never satisfies an item.
    2. Task: Check each item from typed fields: problem, users, data, and
             non-functional areas decided; an outcome with a metric; scope with both
             an 'in' and an 'out' side; a journey with a failure path; every
             regulation entry owned; a rollout entry that covers rollback; no open
             or parked blocking question; the DoD agreed.
       Think about: Why must scope require both sides, not just any scope entry?
       Expected outcome: A scope entry worded 'out of scope' but flagged 'in' fails
                         the scope item.
    3. Task: Give each failed item a reason a PM can act on, listing open blocking
             question IDs.
       Expected outcome: An open blocking Q-001 fails with 'blocking questions still
                         open: Q-001'.
    """
    raise NotImplementedError("S3.2: gate")


def failures(items: list[GateItem]) -> list[str]:
    """Return failed gate items as 'label: reason' lines.

    Problem piece: C3: gaps the grill agent works through.

    Why it matters: The grill agent receives gaps as text; one consistent line per
                    gap keeps that agenda clear.

    What: Returns one line per failed item, empty when the gate passes. Called as
          failures(items: list[GateItem]) and returns list[str].

    Spec: S3.2 | Ticket: 03 | Traces to: I5

    Build steps:
    1. Task: Return 'label: reason' for each failed item, in gate order.
       Expected outcome: A fully passing gate returns no lines.
    """
    raise NotImplementedError("S3.2: failures")
