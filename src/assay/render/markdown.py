"""Write every markdown artifact, and the PDF and prompt, from typed state.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C4 Traceable documents. People and tools read files, not
state. This file fills templates from state and writes them; it never reads them
back (D2).

Why this comes now: State (17) and CSV rows (18) exist; workflow nodes (21 to 26)
call these writers.

Build order: Step 19 of 33.
Previous: src/assay/render/csv_export.py (step 18), which writes the tickets CSV
rows.
Next: src/assay/graph/context.py (step 20), which defines AppContext, the run-time
dependencies injected into every node.

Build these in order:
    1. template_env: every writer uses it.
    2. write: every writer uses it.
    3. intake: the first files a session writes.
    4. glossary: independent.
    5. questionnaire: mode 3.
    6. dod: the DoD stage.
    7. prd: the PRD stage.
    8. spec: the spec stage.
    9. tickets: the last writer.

Depends on:
    assay.domain.ids: live, question_ids. Current entries and question numbering.
    assay.domain.models: DodItem, GlossaryTerm. Items and terms written.
    assay.graph.state: AssayState. The source of every file.
    assay.render.csv_export: SPEC_SECTIONS, rows, to_csv. The tickets CSV.
    assay.rules.intake: gate. The exit gate printed in intake.md.
    assay.vendor.pdfrender: render_pdf. The vendored PDF renderer (D15).
    Standard library: datetime, pathlib.
    Third-party: jinja2.

Depended on by:
    assay.graph.nodes: every file a session produces.

Spec coverage: S6.1, S6.2, S6.3, S6.4, S6.6 | Traces to: C1, C6, D2
"""

from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from assay.domain.ids import live, question_ids
from assay.domain.models import DodItem, GlossaryTerm
from assay.graph.state import AssayState
from assay.render.csv_export import SPEC_SECTIONS, rows, to_csv
from assay.rules.intake import gate
from assay.vendor.pdfrender import render_pdf

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"  # S6.1: content files
MODES: dict[int, str] = {1: "1 Greenfield", 2: "2 Existing system", 3: "3 Brief + questionnaire"}
LEVELS: list[tuple[str, str]] = [  # S6.2: DoD level headings, in order
    ("ticket", "Ticket level"),
    ("feature", "Feature level"),
    ("story", "Story level"),
    ("release", "Release level"),
]


def template_env() -> Environment:
    """Return the template environment with its filters.

    Problem piece: C4: one definition of every output format.

    Why it matters: Templates are the only definition of each file's layout. Strict
                    undefined variables make a missing field fail loudly instead of
                    printing blanks into a PRD, and whitespace control must not join
                    table rows onto one line.

    What: An environment over TEMPLATES with strict undefined, block trimming off,
          trailing newlines kept, and the filters cell, yamlsafe, section_name, and
          count.

    Spec: S6.1 | Ticket: 02 | Traces to: C1

    Build steps:
    1. Task: Load templates from TEMPLATES with strict undefined variables, without
             trimming blocks, keeping the trailing newline.
       Think about: Why does block trimming break tables?
       Expected outcome: A rendered table keeps one row per line.
    2. Task: Add four filters: cell replaces '|' with '/' and line breaks with
             spaces; yamlsafe wraps text in double quotes with inner double quotes
             turned to single; section_name maps a spec key through SPEC_SECTIONS;
             count writes '<n> <one>' or '<n> <many>' (default <one> plus 's').
       Expected outcome: count of 1 story writes '1 story'; of 2 writes '2 stories'.
    """
    raise NotImplementedError("S6.1: template_env")


def write(path: Path, text: str) -> str:
    """Write text with one trailing newline, creating folders; return the file name.

    Problem piece: C4: files always written the same way.

    Why it matters: Every writer needs the same folder creation and trailing
                    newline; one helper keeps them identical.

    What: Creates parent folders, writes the text with exactly one trailing newline,
          returns the name. Called as write(path: Path, text: str) and returns str.

    Spec: S6.1 | Ticket: 02 | Traces to: C1

    Build steps:
    1. Task: Create the parent folders, write the text trimmed of trailing
             whitespace plus one newline as UTF-8, and return the file name.
       Expected outcome: Writing twice leaves identical files.
    """
    raise NotImplementedError("S6.1: write")


def intake(s: AssayState, folder: Path) -> list[str]:
    """Write intake.md and session-log.md.

    Problem piece: C2 and C3: the gate and the record, on disk.

    Why it matters: A PM checks progress in intake.md and an auditor reads the
                    session log; both must match state after every step.

    What: Renders intake.md with the gate and session-log.md from state; returns
          both names. Called as intake(s: AssayState, folder: Path) and returns
          list[str].

    Spec: S6.1 | Ticket: 02 | Traces to: I5

    Build steps:
    1. Task: Compute the gate from the log and whether the DoD is done, render
             intake.md.j2 with it and MODES, render session-log.md.j2, and return
             both names.
       Expected outcome: intake.md shows every gate item ticked or with its reason.
    """
    raise NotImplementedError("S6.1: intake")


def glossary(terms: list[GlossaryTerm], root: Path, team: str) -> None:
    """Write the shared glossary file.

    Problem piece: C4: the team's terms in one readable file.

    Why it matters: The glossary is shared by every session, so it lives at the
                    artifacts root, not in one session's folder.

    What: Renders glossary.md.j2 into glossary.md at the root. Called as
          glossary(terms: list[GlossaryTerm], root: Path, team: str) and returns
          None.

    Spec: S6.1 | Ticket: 02 | Traces to: C1

    Build steps:
    1. Task: Render glossary.md.j2 with the terms and team name into glossary.md at
             the root.
       Expected outcome: Terms appear sorted by name.
    """
    raise NotImplementedError("S6.1: glossary")


def questionnaire(s: AssayState, folder: Path, form_url: str) -> str:
    """Write the printable questionnaire for the current round.

    Problem piece: C6: a copy of what developers answer.

    Why it matters: Developers answer in the browser, but a printable copy helps
                    reviews and records what was asked.

    What: Writes questionnaire.md (round 1) or questionnaire-followup.md (round 2);
          returns the name. Called as questionnaire(s: AssayState, folder: Path,
          form_url: str) and returns str.

    Spec: S6.2 | Ticket: 08 | Traces to: C1

    Build steps:
    1. Task: Number the current round's questions, choose the file name for the
             round, render questionnaire.md.j2 with question and ID pairs and the
             form URL, and return the name.
       Expected outcome: Round 2 writes questionnaire-followup.md.
    """
    raise NotImplementedError("S6.2: questionnaire")


def dod(items: list[DodItem], path: Path, heading: str) -> str:
    """Write a Definition of Done file.

    Problem piece: C6: the quality bar people read.

    Why it matters: The team standard and each initiative's additions are read by
                    people outside the app. Grouping items under their level shows
                    reviewers at a glance which checks apply to every ticket and
                    which only once per release.

    What: Renders dod.md.j2 grouped by LEVELS under the heading; returns the name.
          Called as dod(items: list[DodItem], path: Path, heading: str) and returns
          str.

    Spec: S6.2 | Ticket: 04 | Traces to: C1

    Build steps:
    1. Task: Render dod.md.j2 with the items, heading, and LEVELS to the path, and
             return the name.
       Expected outcome: Items appear under their level headings.
    """
    raise NotImplementedError("S6.2: dod")


def prd(s: AssayState, folder: Path) -> list[str]:
    """Write prd.md and prd.pdf.

    Problem piece: C4: the document approvers sign.

    Why it matters: The PDF is what gets signed; the markdown is what reviewers
                    diff. Both come from one rendering so they never disagree.

    What: Renders prd.md.j2 with front matter, writes it, renders the PDF from the
          same text; returns both names.

    Spec: S6.3 | Ticket: 05 | Traces to: I3

    Build steps:
    1. Task: Prepare the template inputs: feature-to-story lookup, live entries
             split into assumptions, risks, and open questions (not closed),
             requirement and ID pairs, and today's date.
       Expected outcome: Closed questions are absent from the PRD.
    2. Task: Render prd.md.j2, write prd.md, render prd.pdf from the same text with
             the vendored renderer, and return both names.
       Think about: Why render the PDF from the written text, not separately?
       Expected outcome: The PDF shows Approved once approved_by is set.
    """
    raise NotImplementedError("S6.3: prd")


def spec(s: AssayState, folder: Path) -> str:
    """Write spec.md.

    Problem piece: C4: the design developers read.

    Why it matters: Developers read the spec as a document; the coverage table
                    proves every requirement is designed.

    What: Renders spec.md.j2 with the spec and seams; returns the name. Called as
          spec(s: AssayState, folder: Path) and returns str.

    Spec: S6.4 | Ticket: 06 | Traces to: C1

    Build steps:
    1. Task: Render spec.md.j2 with the state, spec, and seams to spec.md, and
             return the name.
       Expected outcome: spec.md lists every coverage row.
    """
    raise NotImplementedError("S6.4: spec")


def tickets(s: AssayState, folder: Path) -> list[str]:
    """Write tickets.csv and agent-prompt.md.

    Problem piece: C4: the handoff to the tracker agent.

    Why it matters: The tracker agent needs the CSV and instructions together;
                    embedding the CSV in the prompt makes the handoff a single file.

    What: Writes the CSV with DoD by level, then the prompt embedding it with story,
          feature, and ticket counts.

    Spec: S6.6 | Ticket: 07 | Traces to: C1, C6

    Build steps:
    1. Task: Group the team and additions DoD items by level, build the CSV text
             from the rows, and write tickets.csv exactly as generated.
       Expected outcome: The CSV's first row is the header.
    2. Task: List each feature's ticket IDs in order, count stories, features, and
             tickets, render agent-prompt.md.j2 with the CSV embedded, and return
             both names.
       Expected outcome: The prompt contains a csv code block and '1 story, 2
                         features, 4 tickets'.
    """
    raise NotImplementedError("S6.6: tickets")
