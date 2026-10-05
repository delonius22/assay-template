"""Assign every identifier in the system, by code.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C2 Recorded understanding. People and trackers refer to items
by ID, so IDs must be sequential, stable, and never reused. This file owns numbering
and nothing else; it never decides what is recorded.

Why this comes now: The models (step 2) define what gets an ID. Rules (steps 4 to 9)
and every workflow step need IDs to exist before they can cite or check them.

Build order: Step 3 of 33.
Previous: src/assay/domain/models.py (step 2), which defines the typed models every
agent returns and every rule checks.
Next: src/assay/rules/common.py (step 4), which holds the shared text rules:
compliance claims, single questions, vague words.

Build these in order:
    1. add_entries: the most used numbering rule.
    2. live: a filter over add_entries' output.
    3. question_ids: all_answerable_ids builds on it.
    4. all_answerable_ids: extends question_ids.
    5. apply_dod_turn: uses LEVEL_LETTER.
    6. requirement_ids: independent of the others.
    7. assign_tickets: the last ID rule; S3.6 checks positions first.

Depends on:
    assay.domain.models: DodItem, DodTurn, LogEntry, NewEntry, PRDCore,
    Questionnaire, Ticket, TicketPlan. The shapes being numbered.
    Standard library: collections.abc.
    Third-party: none.

Depended on by:
    assay.rules.intake: live entries. assay.graph.nodes: every recorded entry,
    questionnaire, DoD turn, requirement, and ticket. assay.render.markdown: live
    entries and question IDs.

Spec coverage: S2.1, S2.2, S2.3, S2.4, S2.5, S2.6 | Traces to: I2, I15
"""

from collections.abc import Sequence

from assay.domain.models import (
    DodItem,
    DodTurn,
    LogEntry,
    NewEntry,
    PRDCore,
    Questionnaire,
    Ticket,
    TicketPlan,
)

LEVEL_LETTER: dict[str, str] = {"ticket": "T", "feature": "F", "story": "S", "release": "R"}  # S2.4


def add_entries(
    log: list[LogEntry], new: list[NewEntry], supersedes: Sequence[str] = ()
) -> list[LogEntry]:
    """Append entries with fresh IDs and mark superseded entries.

    Problem piece: C2: every new decision, assumption, risk, question, or correction
                   gets a lasting ID.

    Why it matters: Every PRD line cites these IDs, so a reused or renumbered ID
                    silently changes what an approved document means. Numbering per
                    type across the whole log, and marking replaced entries instead
                    of deleting them, keeps every citation pointing at the same
                    thing forever (I2).

    What: Takes the current log, new entries, and IDs they replace. Returns a new
          log with the entries appended as <type>-NNN and replaced entries marked;
          the input is not changed.

    Spec: S2.1 | Ticket: 01 | Traces to: I2

    Build steps:
    1. Task: Copy the log so the caller's list is never changed.
       Expected outcome: The original log is identical after the call.
    2. Task: Give each new entry the next number for its type, counted across the
             whole log, as three digits: D-001, D-002, A-001.
       Think about: Why count the whole log and not just this batch?
       Expected outcome: Two calls that each add one decision produce D-001 then
                         D-002.
    3. Task: Mark every superseded entry with the IDs that replace it, without
             removing it.
       Expected outcome: A superseded entry stays in the log and lists its
                         replacements.
    """
    raise NotImplementedError("S2.1: add_entries")


def live(log: list[LogEntry]) -> list[LogEntry]:
    """Return the entries that have not been superseded.

    Problem piece: C2: the current view of what was decided.

    Why it matters: Gates and documents must act on current decisions only. Counting
                    a superseded entry would let an outdated answer satisfy the gate
                    or appear in the PRD.

    What: Takes a log; returns its entries with no replacements, in original order.
          Called as live(log: list[LogEntry]) and returns list[LogEntry].

    Spec: S2.2 | Ticket: 01 | Traces to: I2

    Build steps:
    1. Task: Keep only entries that list no replacements, preserving order.
       Expected outcome: A superseded entry is absent; every other entry keeps its
                         position.
    """
    raise NotImplementedError("S2.2: live")


def question_ids(q: Questionnaire, round_no: int) -> list[str]:
    """Return the IDs of one round's primary questions.

    Problem piece: C2: questions developers can cite in their answers.

    Why it matters: Developers answer by ID, and the follow-up round must never
                    reuse round one's IDs or an answer could be applied to the wrong
                    question.

    What: Round 1 gives Q-01, Q-02, and so on; round 2 gives Q-F01, Q-F02. Called as
          question_ids(q: Questionnaire, round_no: int) and returns list[str].

    Spec: S2.3 | Ticket: 08 | Traces to: I2

    Build steps:
    1. Task: Number the questions in list order with two digits, prefixed Q- in
             round 1 and Q-F in round 2.
       Expected outcome: Two round-2 questions are numbered Q-F01 and Q-F02.
    """
    raise NotImplementedError("S2.3: question_ids")


def all_answerable_ids(q: Questionnaire, round_no: int) -> list[str]:
    """Return every ID a respondent may answer in one round.

    Problem piece: C2 and C6: the allowlist submitted answers are checked against.

    Why it matters: Answers arrive from browsers, so their question IDs must be
                    checked against a known list (I12). Follow-ups and confirmations
                    need IDs too, and confirmations exist only in round 1.

    What: Primary IDs, then follow-ups as the question ID plus a letter (Q-01a),
          then confirmations K-01 and on, the last only in round 1.

    Spec: S2.3 | Ticket: 08 | Traces to: I2, I12

    Build steps:
    1. Task: Start from the primary question IDs and add each question's follow-ups,
             lettered a, b, c in order.
       Expected outcome: A question with one follow-up adds Q-01a.
    2. Task: Add K-01, K-02 for confirmations in round 1 only.
       Think about: What would collide if confirmations were numbered again in round
                    2?
       Expected outcome: Round 2 contains no K IDs.
    """
    raise NotImplementedError("S2.3: all_answerable_ids")


def apply_dod_turn(
    items: list[DodItem], retired: list[str], turn: DodTurn, additions: bool
) -> tuple[list[DodItem], list[str]]:
    """Withdraw and add Definition of Done items without reusing an ID.

    Problem piece: C2 and C6: a quality standard whose item IDs stay stable.

    Why it matters: Tickets list DoD items by ID. If a withdrawn item's number were
                    reused, an old ticket would suddenly point at a different check.
                    Remembering retired IDs prevents that.

    What: Takes current items, retired IDs, one turn, and whether these are
          initiative additions. Returns the new items and the updated retired list.

    Spec: S2.4 | Ticket: 04 | Traces to: I2

    Build steps:
    1. Task: Remove the turn's withdrawn items and remember their IDs as retired.
       Expected outcome: A withdrawn item is absent and its ID is in the retired
                         list.
    2. Task: Give each agreed item the next number for its level: DOD-<letter>NN for
             the team standard, DOD-A<letter>NN for additions, counting both kept
             and retired IDs.
       Think about: Why must retired IDs count when choosing the next number?
       Expected outcome: Withdrawing DOD-T01 then adding an item gives DOD-T02.
    """
    raise NotImplementedError("S2.4: apply_dod_turn")


def requirement_ids(core: PRDCore) -> tuple[list[str], list[str]]:
    """Return FR and NFR IDs for a PRD core.

    Problem piece: C2 and C4: requirement IDs the spec and tickets trace to.

    Why it matters: The spec's coverage table and every ticket cite requirement IDs,
                    so they must be assigned once, in order, by code.

    What: FR-01 onward for functional requirements and NFR-01 onward for
          non-functional ones. Called as requirement_ids(core: PRDCore) and returns
          tuple[list[str], list[str]].

    Spec: S2.5 | Ticket: 05 | Traces to: I2

    Build steps:
    1. Task: Number functional requirements FR-01 onward and non-functional ones
             NFR-01 onward, in list order.
       Expected outcome: Three functional and one non-functional give FR-01 to FR-03
                         and NFR-01.
    """
    raise NotImplementedError("S2.5: requirement_ids")


def assign_tickets(plan: TicketPlan) -> list[Ticket]:
    """Number tickets in build order and turn positions into ticket IDs.

    Problem piece: C2 and C4: tickets a tracker can import with stable IDs.

    Why it matters: The plan refers to other tickets by position because a model
                    cannot be trusted with IDs. Converting positions to IDs in code
                    keeps dependencies correct; positions are 1-based, and an
                    off-by-one would link the wrong ticket.

    What: T-001 onward in list order, with depends_on and unblocks positions
          converted to IDs. Called as assign_tickets(plan: TicketPlan) and returns
          list[Ticket].

    Spec: S2.6 | Ticket: 07 | Traces to: I2, I15

    Build steps:
    1. Task: Give each ticket T-NNN in list order.
       Expected outcome: Four tickets are T-001 to T-004.
    2. Task: Convert each 1-based dependency and unblock position into the matching
             ticket ID.
       Think about: Which ticket does position 3 name?
       Expected outcome: A ticket depending on position 3 lists T-003.
    """
    raise NotImplementedError("S2.6: assign_tickets")
