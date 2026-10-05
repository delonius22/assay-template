"""Wire every node and edge of the workflow.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C3 Gated progress. The order of steps and the gates between
them are edges. This file owns the wiring; nodes own behaviour.

Why this comes now: Every node exists (21 to 26).

Build order: Step 27 of 33.
Previous: src/assay/graph/nodes/tickets.py (step 26), which runs the ticket stage.
Next: src/assay/api/auth.py (step 28), which reads the signed-in user from the SSO
header.

Build these in order:
    1. build_graph: the only function.

Depends on:
    assay.graph.context: AppContext. The context schema.
    assay.graph.state: AssayState. The state schema.
    assay.graph.nodes: dod, intake, prd, spec, tickets. Every node and router.
    Standard library: none.
    Third-party: langgraph.

Depended on by:
    assay.api.app: compiles the graph at startup.

Spec coverage: S5.11 | Traces to: I5, I7
"""

from langgraph.graph import END, START, StateGraph

from assay.graph.context import AppContext
from assay.graph.nodes import dod, intake, prd, spec, tickets
from assay.graph.state import AssayState


def build_graph() -> StateGraph[AssayState, AppContext, AssayState, AssayState]:
    """Return the uncompiled workflow graph.

    Problem piece: C3: every stage reachable only through its gate.

    Why it matters: Writing every transition explicitly makes the flow reviewable on
                    one screen by people who never read the nodes, and makes
                    skipping a gate impossible.

    What: A graph over AssayState with AppContext as its context schema, every node
          registered by its function name, and the edges listed in the steps.

    Spec: S5.11 | Ticket: 02 | Traces to: I5, I7

    Build steps:
    1. Task: Register all 23 nodes by name: intake (setup, explore, confirm_map_ask,
             brief_check, brief_fix_ask, write_questionnaire, await_answers_ask,
             read_responses, reconcile, grill_think, grill_ask, intake_gate_node),
             dod (dod_think, dod_ask), prd (prd, prd_review_ask, stamp_approval),
             spec (seams, seams_ask, spec), tickets (tickets, ticket_review_ask,
             export_tickets).
       Expected outcome: The compiled graph has 25 nodes including start and end.
    2. Task: Wire intake: start to setup; setup routes by mode; explore to
             confirm_map_ask to grill_think; brief_check routes to brief_fix_ask
             (which returns to brief_check) or write_questionnaire, then
             await_answers_ask, read_responses (back to waiting or on to reconcile),
             and reconcile (back to waiting or to the gate); grill_think routes to
             grill_ask (which returns) or the gate; the gate routes to prd,
             grill_think, or dod_think.
       Expected outcome: A mode 1 session pauses first at grill_ask.
    3. Task: Wire the rest: dod_think routes to dod_ask (which returns), itself, or
             the gate; prd to prd_review_ask, which routes to prd, itself, or
             stamp_approval; stamp_approval to seams to seams_ask, which routes to
             seams or spec; spec to tickets to ticket_review_ask, which routes to
             tickets or export_tickets; export_tickets to end.
       Think about: Which edges make it impossible to export unreviewed tickets?
       Expected outcome: A full scripted session pauses at question, dod_question,
                         approval, seams, ticket_review in order.
    """
    raise NotImplementedError("S5.11: build_graph")
