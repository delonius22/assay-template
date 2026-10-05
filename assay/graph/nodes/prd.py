"""PRD: write it (rules enforced inside the agent call), render, and get sign-off."""
from datetime import date

from langgraph.runtime import Runtime
from langgraph.types import interrupt

from ...domain.ids import requirement_ids
from ...llm import agents as A
from ...render import markdown as md
from ..context import AppContext, ctx
from ..state import AssayState, log_view
from .shared import files, glossary_text, reply


def prd(s: AssayState, runtime: Runtime[AppContext]):
    """Write the PRD core and narrative, number requirements, render markdown and PDF.

    Spec: S5.8 | Ticket: 05 | Traces to: I3, I4

    Build steps:
    1. Task: `c = ctx(runtime)`; build `dynamic` from f"Initiative: {s.title}", the brief JSON or "none",
       f"Session log (cite these IDs):\\n{log_view(s)}", f"Questionnaire IDs you may also cite: {s.q_ids or 'none'}",
       f"Glossary:\\n{glossary_text(s)}", and f"Reviewer feedback to address:\\n{s.prd_feedback}" when present.
       Expected outcome: the agent can cite only IDs it was given.
    2. Task: `core = c.run(A.PRD_CORE, dynamic, s)`; `nar = c.run(A.PRD_NARRATIVE, dynamic + "\\n\\nStories, features,
       and requirements already written:\\n" + core.model_dump_json(), s)`.
       Expected outcome: both parts pass S3.4; they share one cached prefix.
    3. Task: `fr, nfr = requirement_ids(core)`; `doc_id = s.doc_id or f"PRD-{date.today().year}-{s.slug.upper()[:16]}"`;
       `s2 = s.model_copy(update={"prd_core": core, "prd_narrative": nar, "fr_ids": fr, "nfr_ids": nfr, "doc_id": doc_id})`;
       `names = md.prd(s2, c.folder(s))`.
       Expected outcome: prd.md and prd.pdf written.
    4. Task: Return `{"prd_core": core, "prd_narrative": nar, "fr_ids": fr, "nfr_ids": nfr, "doc_id": doc_id,
       "prd_feedback": "", "stage": "PRD review", "files": files(s, *names)}`.
       Expected outcome: the review pause comes next.
    """
    raise NotImplementedError("S5.8")


def prd_review_ask(s: AssayState, runtime: Runtime[AppContext]):
    """Pause for review; only a named approver may approve (I8).

    Spec: S5.8 | Ticket: 05 | Traces to: I7, I8

    Build steps:
    1. Task: `approvers = ctx(runtime).settings.approvers`; `value = interrupt({"kind": "approval", "version": s.prd_version,
       "files": ["prd.pdf", "prd.md"], "error": s.review_error or None})`; `text, user = reply(value)`;
       `decision = value.get("decision") if isinstance(value, dict) else "changes"`.
       Expected outcome: the reviewer's decision and identity.
    2. Task: If `decision == "approve"`: when `approvers and user not in approvers`, return
       `{"review_error": f"{user} is not an approver. Approvers: {', '.join(sorted(approvers))}."}`;
       otherwise return `{"approved_by": user, "review_error": "", "prd_feedback": ""}`.
       Expected outcome: approval by a non-approver repeats the pause with the reason.
    3. Task: Otherwise `major, minor = s.prd_version.split(".")` and return `{"prd_feedback": text or "Revise the PRD.",
       "prd_version": f"{major}.{int(minor) + 1}", "review_error": "", "approved_by": ""}`.
       Expected outcome: changes produce version 0.2, 0.3, ….
    """
    raise NotImplementedError("S5.8")


def after_review(s: AssayState) -> str:
    """Spec: S5.8 | Ticket: 05 | Traces to: I8

    Build steps:
    1. Task: Return `"prd_review_ask"` when `s.review_error`; `"prd"` when `s.prd_feedback`; otherwise `"stamp_approval"`.
       Expected outcome: refused approval asks again; changes rewrite; approval stamps.
    """
    raise NotImplementedError("S5.8")


def stamp_approval(s: AssayState, runtime: Runtime[AppContext]):
    """Re-render so the PDF shows Approved and the approver.

    Spec: S5.8 | Ticket: 05 | Traces to: I8

    Build steps:
    1. Task: `names = md.prd(s, ctx(runtime).folder(s))`.
       Expected outcome: the template prints status Approved because `s.approved_by` is set.
    2. Task: Return `{"stage": "Spec", "files": files(s, *names)}`.
       Expected outcome: the spec stage starts.
    """
    raise NotImplementedError("S5.8")
