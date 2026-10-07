"""Spec: developers confirm test seams, then the spec is written."""
from langgraph.runtime import Runtime
from langgraph.types import interrupt

from ...llm import agents as A
from ...render import markdown as md
from ..context import AppContext, ctx
from ..state import AssayState
from .shared import files, glossary_text, reply


def prd_brief(s: AssayState) -> str:
    """Stories, features, and numbered requirements as prompt text.

    Spec: S5.9 | Ticket: 06 | Traces to: I3

    Build steps:
    1. Task: `reqs = [f"{i}: {r.text} (feature {r.feature_id})" for i, r in zip(s.fr_ids, s.prd_core.functional)]`;
       `nfrs = [f"{i}: [{n.area}] {n.text}" for i, n in zip(s.nfr_ids, s.prd_core.non_functional)]`.
       Expected outcome: every requirement with its ID.
    2. Task: Return f"Stories and features:\\n{s.prd_core.model_dump_json(include={'stories'})}\\n\\nRequirements:\\n" +
       "\\n".join(reqs + nfrs).
       Expected outcome: the spec and ticket agents see the approved structure.
    """
    reqs = [f"{i}: {r.text} (feature {r.feature_id})" for i, r in zip(s.fr_ids, s.prd_core.functional)]
    nfrs = [f"{i}: [{n.area}] {n.text}" for i, n in zip(s.nfr_ids, s.prd_core.non_functional)]
    return (f"Stories and features:\n{s.prd_core.model_dump_json(include={'stories'})}\n\nRequirements:\n"
            + "\n".join(reqs + nfrs))


def seams(s: AssayState, runtime: Runtime[AppContext]):
    """Spec: S5.9 | Ticket: 06 | Traces to: I1

    Build steps:
    1. Task: `dynamic = f"{prd_brief(s)}\\n\\nFeedback on the earlier proposal: {s.seams_feedback or 'none'}"`.
       Expected outcome: corrections shape the next proposal.
    2. Task: Return `{"seams": ctx(runtime).run(A.SEAMS, dynamic, s), "stage": "Spec"}`.
       Expected outcome: proposed seams in state.
    """
    dynamic = f"{prd_brief(s)}\n\nFeedback on the earlier proposal: {s.seams_feedback or 'none'}"
    return {"seams": ctx(runtime).run(A.SEAMS, dynamic, s), "stage": "Spec"}


def seams_ask(s: AssayState):
    """Spec: S5.9 | Ticket: 06 | Traces to: I7

    Build steps:
    1. Task: `value = interrupt({"kind": "seams", "seams": s.seams.model_dump()})`; `text, _ = reply(value)`.
       Expected outcome: developers review the seams.
    2. Task: `approved = isinstance(value, dict) and value.get("decision") == "approve"`; return
       `{"seams_feedback": "" if approved else (text or "Propose different seams.")}`.
       Expected outcome: feedback triggers a new proposal.
    """
    value = interrupt({"kind": "seams", "seams": s.seams.model_dump()})
    text, _ = reply(value)
    approved = isinstance(value, dict) and value.get("decision") == "approve"
    return {"seams_feedback": "" if approved else (text or "Propose different seams.")}


def after_seams(s: AssayState) -> str:
    """Spec: S5.9 | Ticket: 06 | Traces to: I5

    Build steps:
    1. Task: Return `"seams" if s.seams_feedback else "spec"`.
       Expected outcome: confirmed seams move on.
    """
    return "seams" if s.seams_feedback else "spec"


def spec(s: AssayState, runtime: Runtime[AppContext]):
    """Spec: S5.9 | Ticket: 06 | Traces to: I1

    Build steps:
    1. Task: `c = ctx(runtime)`; build `dynamic` from `prd_brief(s)`, f"Agreed seams: {s.seams.model_dump_json()}",
       the current-state map JSON or "n/a", and f"Glossary:\\n{glossary_text(s)}".
       Expected outcome: the spec is designed against agreed seams.
    2. Task: `sp = c.run(A.SPEC, dynamic, s)`; `name = md.spec(s.model_copy(update={"spec": sp}), c.folder(s))`.
       Expected outcome: spec.md written; coverage already checked by S3.5.
    3. Task: Return `{"spec": sp, "stage": "Tickets", "files": files(s, name)}`.
       Expected outcome: tickets come next.
    """
    c = ctx(runtime)
    dynamic = "\n\n".join([
        prd_brief(s),
        f"Agreed seams: {s.seams.model_dump_json()}",
        f"Current-state map: {s.current_map.model_dump_json() if s.current_map else 'n/a'}",
        f"Glossary:\n{glossary_text(s)}",
    ])
    sp = c.run(A.SPEC, dynamic, s)
    name = md.spec(s.model_copy(update={"spec": sp}), c.folder(s))
    return {"spec": sp, "stage": "Tickets", "files": files(s, name)}
