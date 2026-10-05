"""Write the tickets CSV: each story, then each feature followed by its tickets.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C4 Traceable documents. The CSV is the handoff a tracker agent
imports. This file owns its rows and columns; it never decides what tickets exist.

Why this comes now: State exists (step 17). The markdown renderer (step 19) embeds
this CSV in the agent prompt.

Build order: Step 18 of 33.
Previous: src/assay/graph/state.py (step 17), which defines AssayState, the session
saved after every step.
Next: src/assay/render/markdown.py (step 19), which writes every markdown artifact,
the PDF, and the tracker prompt.

Build these in order:
    1. story_title: the smallest piece.
    2. dod_cell: independent.
    3. top_priority: independent.
    4. rows: combines the helpers above.
    5. to_csv: the last step.

Depends on:
    assay.domain.models: DodItem, PRDCore, Ticket. The rows' sources.
    Standard library: csv, io, re.
    Third-party: none.

Depended on by:
    assay.render.markdown: the CSV file and the prompt that embeds it.

Spec coverage: S6.5 | Traces to: C6
"""

import csv
import io
import re

from assay.domain.models import DodItem, PRDCore, Ticket

SPEC_SECTIONS: dict[str, str] = {  # S6.5: spec section names
    "modules": "3.1 Modules",
    "interfaces": "3.2 Interfaces",
    "data": "3.3 Data",
    "key_flows": "3.4 Key flows",
    "integrations": "3.5 Integrations",
    "security": "4 Security",
    "nfr_design": "5 Non-functional design",
    "observability": "6 Observability",
    "rollout": "7 Rollout",
    "testing": "8 Testing",
}
COLUMNS: list[str] = [  # S6.5: the CSV contract
    "Level",
    "ID",
    "Parent ID",
    "Title",
    "Description",
    "Acceptance Criteria",
    "Definition of Done",
    "Requirements",
    "Spec Sections",
    "Priority",
    "Size",
    "Type",
    "Depends On",
    "Unblocks",
    "Sources",
]
RANK: dict[str, int] = {"Must have": 0, "Should have": 1, "Could have": 2, "Won't have": 3}  # S6.5


def story_title(text: str) -> str:
    """Return a short title from a story's goal clause.

    Problem piece: C4: readable story titles in the tracker.

    Why it matters: A tracker title of 'As a retail customer, I want...' is
                    unreadable in lists; the goal clause is the title people
                    recognise.

    What: 'As a customer, I want low-balance alerts, so that...' becomes
          'Low-balance alerts'. Called as story_title(text: str) and returns str.

    Spec: S6.5 | Ticket: 07 | Traces to: C6

    Build steps:
    1. Task: Take the text between 'I want' (dropping a following 'to') and 'so
             that', or the whole text when that clause is missing, and capitalise
             its first letter.
       Expected outcome: 'As an agent, I want to view settings so that I can help.'
                         becomes 'View settings'.
    """
    raise NotImplementedError("S6.5: story_title")


def dod_cell(items: list[DodItem]) -> str:
    """Return one Definition of Done checklist cell.

    Problem piece: C4 and C6: each row carries its quality bar.

    Why it matters: A tracker agent copies cells verbatim; one line per item with
                    its evidence keeps the checklist usable there.

    What: One line per item: '[ ] <id> <statement> (evidence: <evidence>)'. Called
          as dod_cell(items: list[DodItem]) and returns str.

    Spec: S6.5 | Ticket: 07 | Traces to: C6

    Build steps:
    1. Task: Write one '[ ] <id> <statement> (evidence: <evidence>)' line per item.
       Expected outcome: Two items give two lines.
    """
    raise NotImplementedError("S6.5: dod_cell")


def top_priority(priorities: list[str]) -> str:
    """Return the highest MoSCoW priority in a list.

    Problem piece: C4: a story and feature priority derived from its requirements.

    Why it matters: A feature is as urgent as its most urgent requirement. Without
                    it, a feature containing one must-have requirement could be
                    scheduled after features that contain none.

    What: The priority with the lowest RANK, or empty text for an empty list. Called
          as top_priority(priorities: list[str]) and returns str.

    Spec: S6.5 | Ticket: 07 | Traces to: C6

    Build steps:
    1. Task: Return the priority with the lowest RANK, or empty text for no
             priorities.
       Expected outcome: Should have and Must have give Must have.
    """
    raise NotImplementedError("S6.5: top_priority")


def rows(
    core: PRDCore, fr_ids: list[str], tickets: list[Ticket], dod: dict[str, list[DodItem]]
) -> list[dict[str, str]]:
    """Return the CSV rows in hierarchy order.

    Problem piece: C4: the hierarchy a tracker agent rebuilds from Parent ID.

    Why it matters: A tracker agent creates items top-down, so each story must come
                    before its features and each feature before its tickets. Tickets
                    stay in build order so the CSV doubles as the plan.

    What: A Story row, then for each of its features a Feature row followed by that
          feature's Ticket rows. DoD attaches by level; priorities derive from
          requirements.

    Spec: S6.5 | Ticket: 07 | Traces to: C6, I15

    Build steps:
    1. Task: Group each feature's FR IDs and priorities.
       Expected outcome: F-01 lists FR-01 and FR-02.
    2. Task: Write each story row: Level Story, its ID, no parent, title from the
             goal clause, the full story text, story-level DoD, and the top priority
             of all its features' requirements.
       Expected outcome: The first row is the S-01 story.
    3. Task: After each story, write each feature row (parent the story,
             feature-level DoD, its FR IDs and top priority), then that feature's
             tickets in list order.
       Think about: Why must tickets keep list order?
       Expected outcome: Rows run S-01, F-01, T-001, T-002, F-02, T-003.
    4. Task: Fill each ticket row: description is the user story, or 'Question: <q>
             Timebox: <t>' for a spike, or 'Enabler. Unblocks <ids>.' for an
             enabler, plus a Notes line when present; criteria numbered one per
             line; ticket-level DoD; requirements, spec section names, priority,
             size, type, dependency and unblock IDs, and sources.
       Expected outcome: A spike row's description starts with 'Question:'.
    """
    raise NotImplementedError("S6.5: rows")


def to_csv(rows_: list[dict[str, str]]) -> str:
    r"""Return CSV text with every column, multi-line cells quoted.

    Problem piece: C4: a file every spreadsheet and importer reads.

    Why it matters: Criteria and DoD cells contain line breaks; only a proper CSV
                    writer quotes them so importers keep rows intact.

    What: A header of COLUMNS, then one line per row with missing cells empty and
          '\n' line endings.

    Spec: S6.5 | Ticket: 07 | Traces to: C1

    Build steps:
    1. Task: Write the COLUMNS header, then each row with missing cells empty, using
             '\n' line endings and standard CSV quoting.
       Think about: Why must quoting be left to a CSV writer?
       Expected outcome: A cell with two lines reads back as one cell.
    """
    raise NotImplementedError("S6.5: to_csv")
