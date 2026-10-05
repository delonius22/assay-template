"""Agree test seams with developers, then write the spec.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C4 Traceable documents and C6 People decide. Developers
confirm seams before the spec is written. This file owns that loop.

Why this comes now: The PRD is approved (24).

Build order: Step 25 of 33.
Previous: src/assay/graph/nodes/prd.py (step 24), which runs the PRD stage and its
approval.
Next: src/assay/graph/nodes/tickets.py (step 26), which runs the ticket stage.

Build these in order:
    1. prd_brief: the shared prompt piece.
    2. seams: the stage's first node.
    3. seams_ask: the pause after the step above.
    4. after_seams: a pure router.
    5. spec: after seams are confirmed.

Depends on:
    assay.graph.context: AppContext, ctx.
    assay.graph.state: AssayState.
    assay.graph.nodes.shared: files, glossary_text, reply.
    assay.llm.agents: agent. Seams and spec agents.
    assay.render.markdown: spec.
    Standard library: none.
    Third-party: langgraph (Runtime, interrupt).

Depended on by:
    assay.graph.build.
    assay.graph.nodes.tickets: prd_brief.

Spec coverage: S5.9 | Traces to: I1
"""

from langgraph.runtime import Runtime
from langgraph.types import interrupt

from assay.graph.context import AppContext, ctx
from assay.graph.nodes.shared import files, glossary_text, reply
from assay.graph.state import AssayState
from assay.llm.agents import agent
from assay.render import markdown as md


def prd_brief(s: AssayState) -> str:
    """Return the approved stories, features, and numbered requirements as prompt text.

    Problem piece: C4: later agents see exactly what was approved.

    Why it matters: The spec and ticket agents must work from the approved structure
                    and real requirement IDs, not a summary.

    What: The stories as data, then one line per requirement: '<id>: <text> (feature
          <F>)' or '<id>: [<area>] <text>'.

    Spec: S5.9 | Ticket: 06 | Traces to: I3

    Build steps:
    1. Task: Write the stories as data, then each functional requirement with its ID
             and feature and each non-functional one with its ID and area.
       Expected outcome: The text contains 'FR-01:' and 'NFR-01:'.
    """
    raise NotImplementedError("S5.9: prd_brief")


def seams(s: AssayState, runtime: Runtime[AppContext]) -> dict[str, object]:
    """Propose test seams.

    Problem piece: C6: testable work from the start.

    Why it matters: Seams decide how every ticket is tested; earlier feedback must
                    shape a new proposal. Without feedback in the prompt, the agent
                    would propose the same rejected seams again.

    What: Runs the seams agent with the PRD brief and any feedback; sets stage
          'Spec'. Called as seams(s: AssayState, runtime: Runtime[AppContext]) and
          returns dict[str, object].

    Spec: S5.9 | Ticket: 06 | Traces to: I1

    Build steps:
    1. Task: Run the seams agent on the PRD brief plus earlier feedback (or 'none')
             and return the seams and stage 'Spec'.
       Expected outcome: Feedback text appears in the prompt.
    """
    raise NotImplementedError("S5.9: seams")


def seams_ask(s: AssayState) -> dict[str, object]:
    """Pause for a person (seams) and record the reply.

    Problem piece: C6: developers confirm seams.

    Why it matters: Wrong seams make every ticket hard to test. Only developers know
                    which boundaries their test setup can actually reach, so they
                    must confirm them.

    What: Pauses with kind 'seams'; on resume returns empty feedback on approval,
          otherwise the reply text (or 'Propose different seams.').

    Spec: S5.9 | Ticket: 06 | Traces to: I7

    Build steps:
    1. Task: Pause with an interrupt of kind 'seams' carrying the proposed seams,
             and nothing else in this node.
       Think about: What would rerun on resume if this node also called a model?
       Expected outcome: Resuming runs no model call.
    2. Task: Turn the resume value into empty feedback on approval, otherwise the
             reply text (or 'Propose different seams.').
       Expected outcome: Corrections produce feedback; approval clears it.
    """
    raise NotImplementedError("S5.9: seams_ask")


def after_seams(s: AssayState) -> str:
    """Return the next node's name.

    Problem piece: C6: re-propose until confirmed.

    Why it matters: Only confirmed seams reach the spec. Writing the spec against
                    unconfirmed seams would make every ticket's tests hard to write.

    What: Reads state only and returns the next node: seams when there is feedback,
          otherwise spec.

    Spec: S5.9 | Ticket: 06 | Traces to: I5

    Build steps:
    1. Task: Choose the next node: seams when there is feedback, otherwise spec.
       Think about: Why must a router never read files or call anything?
       Expected outcome: Feedback routes back to seams.
    """
    raise NotImplementedError("S5.9: after_seams")


def spec(s: AssayState, runtime: Runtime[AppContext]) -> dict[str, object]:
    """Write the spec.

    Problem piece: C4: the design tickets are cut from.

    Why it matters: Coverage is checked inside the agent call, so a written spec
                    already covers every requirement.

    What: Runs the spec agent with the PRD brief, agreed seams, map, and glossary;
          writes spec.md; sets stage 'Tickets'.

    Spec: S5.9 | Ticket: 06 | Traces to: I1

    Build steps:
    1. Task: Run the spec agent on the PRD brief, agreed seams, current-state map or
             'n/a', and glossary.
       Expected outcome: The spec covers every requirement.
    2. Task: Write spec.md and return the spec, stage 'Tickets', and files.
       Expected outcome: spec.md is listed in files.
    """
    raise NotImplementedError("S5.9: spec")
