"""Agree the team Definition of Done once, then initiative additions.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C6 People decide. The team standard is agreed once and shared;
each initiative may add items. This file owns that loop.

Why this comes now: Intake nodes (22) exist; the gate sends sessions here when only
the DoD is missing.

Build order: Step 23 of 33.
Previous: src/assay/graph/nodes/intake.py (step 22), which runs intake: setup, the
three modes, the grill loop, and the gate.
Next: src/assay/graph/nodes/prd.py (step 24), which runs the PRD stage and its
approval.

Build these in order:
    1. dod_think: the loop's thinking half.
    2. dod_ask: the pause after the step above.
    3. after_dod: a pure router.

Depends on:
    assay.domain.ids: apply_dod_turn. Item IDs.
    assay.domain.models: Turn. Answers.
    assay.graph.context: AppContext, ctx.
    assay.graph.state: AssayState, log_view.
    assay.graph.nodes.shared: files, reply.
    assay.llm.agents: agent. The DoD agent.
    assay.render.markdown: dod. The DoD files.
    assay.rules.dod: draft_problems, team_problems.
    Standard library: none.
    Third-party: langgraph (Runtime, interrupt).

Depended on by:
    assay.graph.build.

Spec coverage: S5.7 | Traces to: I2, I5
"""

from langgraph.runtime import Runtime
from langgraph.types import interrupt

from assay.domain.ids import apply_dod_turn
from assay.domain.models import Turn
from assay.graph.context import AppContext, ctx
from assay.graph.nodes.shared import files, reply
from assay.graph.state import AssayState, log_view
from assay.llm.agents import agent
from assay.render import markdown as md
from assay.rules import dod as dod_rules

TEAM_SESSION = (  # S5.7
    "Session type: TEAM STANDARD, shared by every initiative. Start by asking for the bank's "
    "mandated SDLC or control standard."
)
ADDITIONS_SESSION = (  # S5.7
    "Session type: ADDITIONS for this initiative only, on top of the team standard. Propose "
    "additions triggered by the intake log; propose none if nothing warrants it."
)


def dod_think(s: AssayState, runtime: Runtime[AppContext]) -> dict[str, object]:
    """Run one Definition of Done turn; when done, check and save.

    Problem piece: C6: a verifiable, owned quality bar.

    Why it matters: The team standard is shared by every later session, so it is
                    checked as a whole before saving; additions belong to this
                    initiative only. Items keep IDs that are never reused (I2).

    What: Calls the DoD agent, applies the turn to team items or additions, and when
          done either loops with problems or saves: team items to the shared store
          and file (phase becomes 'additions'), additions to the session folder
          (phase becomes 'done').

    Spec: S5.7 | Ticket: 04 | Traces to: I2, I5

    Build steps:
    1. Task: Build the dynamic prompt from TEAM_SESSION (team phase) or
             ADDITIONS_SESSION plus the log view, the items agreed so far, any
             checker problems, and the last question and answer with its user.
       Expected outcome: The additions prompt contains the intake log.
    2. Task: Run the DoD agent and apply its turn to the team items or additions,
             keeping retired IDs; return the pending question when not done.
       Expected outcome: A new team item is DOD-T01.
    3. Task: When done, check the items (whole-standard rules for the team, item
             rules for additions) and loop back with any problems.
       Think about: Why check the team standard as a whole?
       Expected outcome: A team standard with no ticket item loops back.
    4. Task: Save the team standard to the shared store and to
             definition-of-done.md, moving to 'additions'; or write dod-additions.md
             when there are additions, moving to 'done'. Clear the transcript.
       Expected outcome: After additions, the phase is 'done'.
    """
    raise NotImplementedError("S5.7: dod_think")


def dod_ask(s: AssayState) -> dict[str, object]:
    """Pause for a person (dod_question) and record the reply.

    Problem piece: C6: the PM answers each DoD question.

    Why it matters: The pause lives alone so resuming never re-runs the agent (I7).
                    Keeping the pause alone in its node means resuming never repeats
                    the DoD agent's call (I7).

    What: Pauses with kind 'dod_question'; on resume returns a Turn with the
          answering user, with the pending question cleared.

    Spec: S5.7 | Ticket: 04 | Traces to: I7

    Build steps:
    1. Task: Pause with an interrupt of kind 'dod_question' carrying the challenge,
             question, recommended answer, and reason, and nothing else in this
             node.
       Think about: What would rerun on resume if this node also called a model?
       Expected outcome: Resuming runs no model call.
    2. Task: Turn the resume value into a Turn with the answering user, with the
             pending question cleared.
       Expected outcome: The answer is recorded with the answering user.
    """
    raise NotImplementedError("S5.7: dod_ask")


def after_dod(s: AssayState) -> str:
    """Return the next node's name.

    Problem piece: C3: finish the DoD, then re-check the gate.

    Why it matters: Checker problems and the switch to additions both loop to
                    dod_think. Getting this wrong either loops forever on a finished
                    standard or skips the additions an initiative needs.

    What: Reads state only and returns the next node: dod_ask while a question is
          pending, intake_gate_node when the phase is 'done', otherwise dod_think.

    Spec: S5.7 | Ticket: 04 | Traces to: I5

    Build steps:
    1. Task: Choose the next node: dod_ask while a question is pending,
             intake_gate_node when the phase is 'done', otherwise dod_think.
       Think about: Why must a router never read files or call anything?
       Expected outcome: Phase 'done' routes to intake_gate_node.
    """
    raise NotImplementedError("S5.7: after_dod")
