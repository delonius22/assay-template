"""Cut tickets, have a person review them, then export the CSV and prompt.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C4 Traceable documents and C6 People decide. Tickets are cut,
reviewed by a person (D4), and exported. This file owns that loop.

Why this comes now: The spec exists (25).

Build order: Step 26 of 33.
Previous: src/assay/graph/nodes/spec.py (step 25), which runs the spec stage.
Next: src/assay/graph/build.py (step 27), which wires every node and edge of the
workflow.

Build these in order:
    1. tickets: the stage's writer.
    2. ticket_review_ask: the pause after the step above.
    3. after_ticket_review: a pure router.
    4. export_tickets: the last node.

Depends on:
    assay.domain.ids: assign_tickets.
    assay.graph.context: AppContext, ctx.
    assay.graph.state: AssayState.
    assay.graph.nodes.shared: files, reply.
    assay.graph.nodes.spec: prd_brief.
    assay.llm.agents: agent. The ticket agent.
    assay.render.markdown: tickets.
    Standard library: none.
    Third-party: langgraph (Runtime, interrupt).

Depended on by:
    assay.graph.build.

Spec coverage: S5.10 | Traces to: I7, I15
"""

from langgraph.runtime import Runtime
from langgraph.types import interrupt

from assay.domain.ids import assign_tickets
from assay.graph.context import AppContext, ctx
from assay.graph.nodes.shared import files, reply
from assay.graph.nodes.spec import prd_brief
from assay.graph.state import AssayState
from assay.llm.agents import agent
from assay.render import markdown as md


def tickets(s: AssayState, runtime: Runtime[AppContext]) -> dict[str, object]:
    """Cut tickets for every feature in build order.

    Problem piece: C4: a reviewed, traceable backlog.

    Why it matters: Review feedback must reach the re-cut, and the DoD is attached
                    automatically so the agent must not repeat it in criteria.

    What: Runs the ticket agent, assigns ticket IDs, and returns the tickets,
          uncovered requirements, cleared feedback, and stage 'Tickets'.

    Spec: S5.10 | Ticket: 07 | Traces to: I15

    Build steps:
    1. Task: Build the dynamic prompt from the PRD brief, the spec as data, the DoD
             items with a note that they are attached automatically, and any
             reviewer feedback.
       Expected outcome: Reviewer feedback appears in the prompt.
    2. Task: Run the ticket agent, assign IDs, and return the tickets, uncovered
             list, cleared feedback, and stage 'Tickets'.
       Expected outcome: Tickets are numbered T-001 onward.
    """
    raise NotImplementedError("S5.10: tickets")


def ticket_review_ask(s: AssayState) -> dict[str, object]:
    """Pause for a person (ticket_review) and record the reply.

    Problem piece: C6: nothing is exported unreviewed (D4).

    Why it matters: The rules check structure, not whether a slice is truly end to
                    end; a person must look.

    What: Pauses with kind 'ticket_review'; on resume returns empty feedback on
          approval, otherwise the reply text (or 'Revise the tickets.').

    Spec: S5.10 | Ticket: 07 | Traces to: I7

    Build steps:
    1. Task: Pause with an interrupt of kind 'ticket_review' carrying each ticket's
             ID, title, feature, type, size, and dependency IDs, plus the uncovered
             requirements, and nothing else in this node.
       Think about: What would rerun on resume if this node also called a model?
       Expected outcome: Resuming runs no model call.
    2. Task: Turn the resume value into empty feedback on approval, otherwise the
             reply text (or 'Revise the tickets.').
       Expected outcome: Changes produce feedback; approval clears it.
    """
    raise NotImplementedError("S5.10: ticket_review_ask")


def after_ticket_review(s: AssayState) -> str:
    """Return the next node's name.

    Problem piece: C6: re-cut until approved.

    Why it matters: Export happens only after approval. Exporting before approval
                    would hand a tracker agent tickets nobody has looked at (D4).

    What: Reads state only and returns the next node: tickets when there is
          feedback, otherwise export_tickets.

    Spec: S5.10 | Ticket: 07 | Traces to: I5

    Build steps:
    1. Task: Choose the next node: tickets when there is feedback, otherwise
             export_tickets.
       Think about: Why must a router never read files or call anything?
       Expected outcome: Approval routes to export_tickets.
    """
    raise NotImplementedError("S5.10: after_ticket_review")


def export_tickets(s: AssayState, runtime: Runtime[AppContext]) -> dict[str, object]:
    """Write tickets.csv and agent-prompt.md.

    Problem piece: C4: the handoff to the tracker agent.

    Why it matters: The session is only complete when the handoff files exist for
                    download. Writing the files last, after approval, means the CSV
                    a tracker agent sees is always the reviewed one.

    What: Writes the CSV and prompt and sets stage 'Done'. Called as
          export_tickets(s: AssayState, runtime: Runtime[AppContext]) and returns
          dict[str, object].

    Spec: S5.10 | Ticket: 07 | Traces to: C1

    Build steps:
    1. Task: Write the tickets files and return stage 'Done' and the files.
       Expected outcome: tickets.csv and agent-prompt.md are listed in files.
    """
    raise NotImplementedError("S5.10: export_tickets")
