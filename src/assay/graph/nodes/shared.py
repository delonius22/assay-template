"""Hold helpers several workflow stages use.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C6 People decide. Replies, file lists, and intake files are
handled the same way in every stage. This file owns those helpers.

Why this comes now: Context (20), state (17), and the markdown writer (19) exist;
every node file imports these.

Build order: Step 21 of 33.
Previous: src/assay/graph/context.py (step 20), which defines AppContext, the
run-time dependencies injected into every node.
Next: src/assay/graph/nodes/intake.py (step 22), which runs intake: setup, the three
modes, the grill loop, and the gate.

Build these in order:
    1. reply: the smallest helper.
    2. write_intake: used after every intake change.
    3. files: used by every node that writes files.
    4. glossary_text: used by agent prompts.

Depends on:
    assay.graph.context: AppContext. Settings and folders.
    assay.graph.state: AssayState. The session.
    assay.render.markdown: intake, glossary. Intake files and the glossary.
    Standard library: none.
    Third-party: none.

Depended on by:
    Every node module.

Spec coverage: S5.3, S6.1 | Traces to: I12
"""

from assay.graph.context import AppContext
from assay.graph.state import AssayState
from assay.render import markdown as md


def reply(value: object) -> tuple[str, str]:
    """Split a resume value into answer text and user.

    Problem piece: C6: every reply attributed to a person.

    Why it matters: Resume values arrive from the web app as a mapping with the SSO
                    user; scripts and tests send plain text. Both must work, and an
                    unknown user must be marked as such.

    What: From a mapping: its trimmed 'text' and its 'user' or 'unknown'. From
          anything else: its trimmed text and 'unknown'.

    Spec: S5.3 | Ticket: 02 | Traces to: I12

    Build steps:
    1. Task: Return the trimmed text and user from a mapping, or the trimmed text
             and 'unknown' otherwise.
       Expected outcome: A mapping with user 'dana' returns 'dana'.
    """
    raise NotImplementedError("S5.3: reply")


def write_intake(s: AssayState, c: AppContext) -> list[str]:
    """Rewrite intake files so disk matches state.

    Problem piece: C4: the files a PM and auditor read stay current.

    Why it matters: Files written only at the end would be stale or missing if a
                    session stops; rewriting after each change keeps them true at
                    every pause.

    What: Writes intake.md and session-log.md, and the glossary when the session has
          terms; returns the two names.

    Spec: S6.1 | Ticket: 02 | Traces to: C1

    Build steps:
    1. Task: Write the intake files into the session folder and, when the session
             has glossary terms, the shared glossary; return the intake file names.
       Expected outcome: After a grill turn, session-log.md lists the new entries.
    """
    raise NotImplementedError("S6.1: write_intake")


def files(s: AssayState, *names: str) -> list[str]:
    """Return the session's files plus new names, sorted and without blanks.

    Problem piece: C4: downloads list exactly what was generated.

    Why it matters: Downloads are allowed only for listed files (I12), so the list
                    must grow by union and never contain blanks.

    What: The union of existing and new non-empty names, sorted. Called as files(s:
          AssayState) and returns list[str].

    Spec: S5.3 | Ticket: 02 | Traces to: I12

    Build steps:
    1. Task: Return the sorted union of the existing names and the non-empty new
             names.
       Expected outcome: Adding 'prd.md' twice lists it once.
    """
    raise NotImplementedError("S5.3: files")


def glossary_text(s: AssayState) -> str:
    """Return the glossary as prompt lines.

    Problem piece: C4: agents use the shared vocabulary.

    Why it matters: Agents only use terms they are shown; one line per term keeps
                    prompts short. Agents drift into their own vocabulary when the
                    agreed terms are not in front of them on every call.

    What: '- <term>: <definition>' per term, or '(no glossary yet)'. Called as
          glossary_text(s: AssayState) and returns str.

    Spec: S5.3 | Ticket: 02 | Traces to: C1

    Build steps:
    1. Task: Write one '- <term>: <definition>' line per term, or '(no glossary
             yet)' when empty.
       Expected outcome: Two terms give two lines.
    """
    raise NotImplementedError("S5.3: glossary_text")
