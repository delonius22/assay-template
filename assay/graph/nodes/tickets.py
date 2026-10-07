"""Tickets: cut them, have a person review them (D4), then export the CSV and prompt."""
from langgraph.runtime import Runtime
from langgraph.types import interrupt

from ...domain.ids import assign_tickets
from ...llm import agents as A
from ...render import markdown as md
from ..context import AppContext, ctx
from ..state import AssayState
from .shared import files, reply
from .spec import prd_brief


def tickets(s: AssayState, runtime: Runtime[AppContext]):
    """Cut tickets for every feature in build order.

    Spec: S5.10 | Ticket: 07 | Traces to: I15

    Build steps:
    1. Task: `dod = "\\n".join(f"{i.id} [{i.level}] {i.statement}" for i in s.dod_team + s.dod_additions)`.
       Expected outcome: the agent knows the DoD is attached separately.
    2. Task: Build `dynamic` from `prd_brief(s)`, f"Spec (sections keyed by name):\\n{s.spec.model_dump_json(indent=1)}",
       f"Definition of Done (attached automatically; do not repeat it in criteria):\\n{dod}", and
       f"Reviewer feedback to address:\\n{s.ticket_feedback}" when present.
       Expected outcome: review feedback reaches the re-cut.
    3. Task: `plan = ctx(runtime).run(A.TICKETS, dynamic, s)`.
       Expected outcome: a plan passing S3.6, including FR and NFR coverage (D5).
    4. Task: Return `{"tickets": assign_tickets(plan), "uncovered": plan.uncovered, "ticket_feedback": "", "stage": "Tickets"}`.
       Expected outcome: code-assigned IDs T-001…; the review pause comes next.
    """
    dod = "\n".join(f"{i.id} [{i.level}] {i.statement}" for i in s.dod_team + s.dod_additions)
    dynamic = "\n\n".join([
        prd_brief(s),
        f"Spec (sections keyed by name):\n{s.spec.model_dump_json(indent=1)}",
        f"Definition of Done (attached automatically; do not repeat it in criteria):\n{dod}",
    ] + ([f"Reviewer feedback to address:\n{s.ticket_feedback}"] if s.ticket_feedback else []))
    plan = ctx(runtime).run(A.TICKETS, dynamic, s)
    return {"tickets": assign_tickets(plan), "uncovered": plan.uncovered,
            "ticket_feedback": "", "stage": "Tickets"}


def ticket_review_ask(s: AssayState):
    """Pause for a person to review the tickets before export (D4).

    Spec: S5.10 | Ticket: 07 | Traces to: I7

    Build steps:
    1. Task: `value = interrupt({"kind": "ticket_review", "tickets": [t.model_dump(include={"id", "title", "feature_id",
       "type", "size", "depends_on_ids"}) for t in s.tickets], "uncovered": [u.model_dump() for u in s.uncovered]})`;
       `text, _ = reply(value)`.
       Expected outcome: the PM sees every ticket and every uncovered requirement.
    2. Task: `approved = isinstance(value, dict) and value.get("decision") == "approve"`; return
       `{"ticket_feedback": "" if approved else (text or "Revise the tickets.")}`.
       Expected outcome: changes re-cut the tickets.
    """
    value = interrupt({"kind": "ticket_review",
                       "tickets": [t.model_dump(include={"id", "title", "feature_id",
                                                        "type", "size", "depends_on_ids"})
                                   for t in s.tickets],
                       "uncovered": [u.model_dump() for u in s.uncovered]})
    text, _ = reply(value)
    approved = isinstance(value, dict) and value.get("decision") == "approve"
    return {"ticket_feedback": "" if approved else (text or "Revise the tickets.")}


def after_ticket_review(s: AssayState) -> str:
    """Spec: S5.10 | Ticket: 07 | Traces to: I5

    Build steps:
    1. Task: Return `"tickets" if s.ticket_feedback else "export_tickets"`.
       Expected outcome: nothing is exported unreviewed.
    """
    return "tickets" if s.ticket_feedback else "export_tickets"


def export_tickets(s: AssayState, runtime: Runtime[AppContext]):
    """Write tickets.csv and agent-prompt.md.

    Spec: S5.10 | Ticket: 07 | Traces to: C1

    Build steps:
    1. Task: `names = md.tickets(s, ctx(runtime).folder(s))`.
       Expected outcome: the CSV and the prompt with the CSV embedded.
    2. Task: Return `{"stage": "Done", "files": files(s, *names)}`.
       Expected outcome: the session is finished; downloads are available.
    """
    names = md.tickets(s, ctx(runtime).folder(s))
    return {"stage": "Done", "files": files(s, *names)}
