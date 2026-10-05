"""Write the PRD, render it, and get sign-off from a named approver.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C4 Traceable documents and C6 People decide. The PRD is
written from the log, rendered, and approved. This file owns that loop; rules run
inside the agent call.

Why this comes now: The DoD stage (23) is done when the gate passes into the PRD.

Build order: Step 24 of 33.
Previous: src/assay/graph/nodes/dod.py (step 23), which runs the Definition of Done
stage.
Next: src/assay/graph/nodes/spec.py (step 25), which runs the spec stage.

Build these in order:
    1. prd: the stage's writer.
    2. prd_review_ask: the pause after the writer.
    3. after_review: a pure router.
    4. stamp_approval: after approval.

Depends on:
    assay.domain.ids: requirement_ids.
    assay.graph.context: AppContext, ctx.
    assay.graph.state: AssayState, log_view.
    assay.graph.nodes.shared: files, glossary_text, reply.
    assay.llm.agents: agent. The PRD core and narrative agents.
    assay.render.markdown: prd.
    Standard library: datetime.
    Third-party: langgraph (Runtime, interrupt).

Depended on by:
    assay.graph.build.

Spec coverage: S5.8 | Traces to: I3, I8
"""

from datetime import date

from langgraph.runtime import Runtime
from langgraph.types import interrupt

from assay.domain.ids import requirement_ids
from assay.graph.context import AppContext, ctx
from assay.graph.nodes.shared import files, glossary_text, reply
from assay.graph.state import AssayState, log_view
from assay.llm.agents import agent
from assay.render import markdown as md


def prd(s: AssayState, runtime: Runtime[AppContext]) -> dict[str, object]:
    """Write and render the PRD.

    Problem piece: C4: a sourced PRD approvers can sign.

    Why it matters: Writing the core and the narrative separately keeps each output
                    small enough for the rules to check; both share one cached
                    prefix. The document ID is set once and kept across versions.

    What: Runs the core then the narrative agent, numbers requirements, sets the
          document ID if new, renders markdown and PDF, and moves to 'PRD review'.

    Spec: S5.8 | Ticket: 05 | Traces to: I3, I4

    Build steps:
    1. Task: Build the dynamic prompt from the title, brief, log view as citable
             IDs, questionnaire IDs, glossary, and any reviewer feedback.
       Expected outcome: Reviewer feedback appears in the prompt.
    2. Task: Run the core agent, then the narrative agent with the core appended,
             and number the requirements.
       Expected outcome: Requirements are FR-01 onward.
    3. Task: Keep an existing document ID or create 'PRD-<year>-<SLUG>' (slug
             upper-case, first 16 characters), render the PRD, and return the parts,
             IDs, cleared feedback, stage 'PRD review', and files.
       Expected outcome: prd.pdf is listed in files.
    """
    raise NotImplementedError("S5.8: prd")


def prd_review_ask(s: AssayState, runtime: Runtime[AppContext]) -> dict[str, object]:
    """Pause for PRD review; only a named approver may approve.

    Problem piece: C6: sign-off means something (I8).

    Why it matters: The API also refuses non-approvers, but the node checks again so
                    no path can approve without authority. Changes produce a new
                    version so approved text never changes silently.

    What: Pauses with kind 'approval'. An approval by a non-approver sets a review
          error; by an approver records approved_by. Changes set feedback and bump
          the minor version.

    Spec: S5.8 | Ticket: 05 | Traces to: I7, I8

    Build steps:
    1. Task: Pause with kind 'approval' carrying the version, the file names prd.pdf
             and prd.md, and any review error.
       Expected outcome: Resuming runs no model call.
    2. Task: For an approval: when approvers are configured and the user is not one,
             return the error '<user> is not an approver. Approvers: <sorted
             list>.'; otherwise record approved_by.
       Think about: Why check approval here as well as in the API?
       Expected outcome: A non-approver's approval is refused.
    3. Task: For changes: set the feedback (or 'Revise the PRD.'), clear approval,
             and bump the minor version.
       Expected outcome: Changes to version 0.1 produce 0.2.
    """
    raise NotImplementedError("S5.8: prd_review_ask")


def after_review(s: AssayState) -> str:
    """Return the next node's name.

    Problem piece: C6: refused approval asks again; changes rewrite.

    Why it matters: Each review outcome has exactly one next step. Each outcome must
                    have exactly one next step, or an approval could be lost or a
                    change request ignored.

    What: Reads state only and returns the next node: prd_review_ask when there is a
          review error, prd when there is feedback, otherwise stamp_approval.

    Spec: S5.8 | Ticket: 05 | Traces to: I5

    Build steps:
    1. Task: Choose the next node: prd_review_ask when there is a review error, prd
             when there is feedback, otherwise stamp_approval.
       Think about: Why must a router never read files or call anything?
       Expected outcome: An approval routes to stamp_approval.
    """
    raise NotImplementedError("S5.8: after_review")


def stamp_approval(s: AssayState, runtime: Runtime[AppContext]) -> dict[str, object]:
    """Re-render the PRD so it shows Approved.

    Problem piece: C4: the signed artifact says it is approved.

    Why it matters: The PDF printed before approval says 'For review'; the approved
                    copy must say Approved. A signed PDF that still says 'For
                    review' would contradict the audit trail of who approved it.

    What: Re-renders the PRD and moves to stage 'Spec'. Called as stamp_approval(s:
          AssayState, runtime: Runtime[AppContext]) and returns dict[str, object].

    Spec: S5.8 | Ticket: 05 | Traces to: I8

    Build steps:
    1. Task: Re-render the PRD from state and return stage 'Spec' and the files.
       Expected outcome: The PDF's status reads Approved.
    """
    raise NotImplementedError("S5.8: stamp_approval")
