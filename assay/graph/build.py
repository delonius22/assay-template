"""The workflow: wiring only (S5.11, shipped complete per D6; verify with the
end-to-end test). Nodes live in graph/nodes/.

    app = build_graph().compile(checkpointer=..., store=...)
    app.invoke(state_or_command, config, context=AppContext(...))
"""
from langgraph.graph import END, START, StateGraph

from .context import AppContext
from .nodes import dod, intake, prd, spec, tickets
from .state import AssayState


def build_graph() -> StateGraph:
    """Register every node and edge. Complete; verify with the end-to-end flow test.

    Spec: S5.11 | Ticket: 02 | Traces to: I5, I7
    """
    g = StateGraph(AssayState, context_schema=AppContext)
    for fn in [intake.setup, intake.explore, intake.confirm_map_ask, intake.brief_check,
               intake.brief_fix_ask, intake.write_questionnaire, intake.await_answers_ask,
               intake.read_responses, intake.reconcile, intake.grill_think, intake.grill_ask,
               intake.intake_gate_node, dod.dod_think, dod.dod_ask, prd.prd, prd.prd_review_ask,
               prd.stamp_approval, spec.seams, spec.seams_ask, spec.spec, tickets.tickets,
               tickets.ticket_review_ask, tickets.export_tickets]:
        g.add_node(fn.__name__, fn)

    # Intake: pick the mode.
    g.add_edge(START, "setup")
    g.add_conditional_edges("setup", intake.route_mode, ["grill_think", "explore", "brief_check"])
    # Mode 2: map the code, developers correct it, then grill.
    g.add_edge("explore", "confirm_map_ask")
    g.add_edge("confirm_map_ask", "grill_think")
    # Mode 3: brief, questionnaire, web-form responses, reconcile (one follow-up round at most).
    g.add_conditional_edges("brief_check", intake.after_brief, ["brief_fix_ask", "write_questionnaire"])
    g.add_edge("brief_fix_ask", "brief_check")
    g.add_edge("write_questionnaire", "await_answers_ask")
    g.add_edge("await_answers_ask", "read_responses")
    g.add_conditional_edges("read_responses", intake.after_read, ["await_answers_ask", "reconcile"])
    g.add_conditional_edges("reconcile", intake.after_reconcile, ["await_answers_ask", "intake_gate_node"])
    # Grill loop and the intake gate.
    g.add_conditional_edges("grill_think", intake.after_grill, ["grill_ask", "intake_gate_node"])
    g.add_edge("grill_ask", "grill_think")
    g.add_conditional_edges("intake_gate_node", intake.after_gate, ["prd", "grill_think", "dod_think"])
    # Definition of Done.
    g.add_conditional_edges("dod_think", dod.after_dod, ["dod_ask", "dod_think", "intake_gate_node"])
    g.add_edge("dod_ask", "dod_think")
    # PRD and sign-off.
    g.add_edge("prd", "prd_review_ask")
    g.add_conditional_edges("prd_review_ask", prd.after_review, ["prd", "prd_review_ask", "stamp_approval"])
    g.add_edge("stamp_approval", "seams")
    # Spec.
    g.add_edge("seams", "seams_ask")
    g.add_conditional_edges("seams_ask", spec.after_seams, ["seams", "spec"])
    g.add_edge("spec", "tickets")
    # Tickets: cut, review (D4), export.
    g.add_edge("tickets", "ticket_review_ask")
    g.add_conditional_edges("ticket_review_ask", tickets.after_ticket_review, ["tickets", "export_tickets"])
    g.add_edge("export_tickets", END)
    return g
