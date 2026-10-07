"""Agent specs: static prompt text from prompts/*.md, a typed output, and
validators composed from assay.rules.

Prompt loading and the spec table are complete because they run at import.
The validators are stubbed (S4.6).
"""
from functools import lru_cache
from pathlib import Path

from ..domain.models import (BriefCritique, CurrentStateMap, DodTurn, GrillTurn, PRDCore,
                             PRDNarrative, Questionnaire, Reconciliation, Seams, Spec, TicketPlan)
from ..rules import common, dod, intake, prd, spec, tickets
from .call import AgentSpec
from .tools import Deps

PROMPTS = Path(__file__).resolve().parent.parent / "prompts"


@lru_cache
def text(name: str) -> str:
    """Read one prompt file. (Complete.)"""
    return (PROMPTS / name).read_text(encoding="utf-8").strip()


def static(task: str, *refs: str) -> str:
    """Common rules + task + reference files: the cacheable prefix. (Complete.)"""
    parts = [text("common.md"), text(task)] + [text(f"reference/{r}") for r in refs]
    return "\n\n---\n\n".join(parts)


def v_grill(out: GrillTurn, deps: Deps) -> list[str]:
   """Problems with one grill turn.

   Spec: S4.6 | Ticket: 02 | Traces to: I1, I4

   Build steps:
   1. Task: Add "done is false, so next_question is required." when `not out.done and out.next_question is None`.
      Expected outcome: the loop always has a next step.
   2. Task: When `out.next_question`, extend with `common.one_question(out.next_question.text)`.
      Expected outcome: compound questions rejected.
   3. Task: Add f"Unknown IDs in supersedes: {bad}" when `bad := [i for i in out.supersedes if i not in deps.known_ids]`.
      Expected outcome: only real entries are superseded.
   4. Task: Return problems + `intake.entry_problems(out.recorded)` + `common.compliance_claims(out)`.
      Expected outcome: entries carry gate flags; no compliance claims.
   """
   problems: list[str] = []
   if not out.done and out.next_question is None:
      problems.append("done is false, so next_question is required.")
   if out.next_question:
      problems.extend(common.one_question(out.next_question.text))
   if bad := [i for i in out.supersedes if i not in deps.known_ids]:
      problems.append(f"Unknown IDs in supersedes: {bad}")
   return problems + intake.entry_problems(out.recorded) + common.compliance_claims(out)


def v_explore(out: CurrentStateMap, deps: Deps) -> list[str]:
   """Require at least one file read when code access is configured.

   Spec: S4.6 | Ticket: 09 | Traces to: I1

   Build steps:
   1. Task: Return `[]` when `not deps.roots`.
      Expected outcome: no code access, nothing to require.
   2. Task: Return `[] if deps.files_read else ["Read the relevant code with ReadFile before mapping it."]`.
      Expected outcome: maps are built from code, not guesses.
   """
   if not deps.roots:
      return []
   return [] if deps.files_read else ["Read the relevant code with ReadFile before mapping it."]


def post_explore(out: CurrentStateMap, deps: Deps) -> CurrentStateMap:
   """Record which files the map was built from.

   Spec: S4.6 | Ticket: 09 | Traces to: I1

   Build steps:
   1. Task: Set `out.files_read = sorted(set(deps.files_read))` and return `out`.
      Expected outcome: the map cites its evidence.
   """
   out.files_read = sorted(set(deps.files_read))
   return out


def v_questionnaire(out: Questionnaire, deps: Deps) -> list[str]:
   """Problems with a questionnaire.

   Spec: S4.6 | Ticket: 08 | Traces to: I1, I4

   Build steps:
   1. Task: For each `(i, q)` in `enumerate(out.questions, 1)`, extend with
      `common.one_question(q.text, f"Question {i}: ")` and add
      f"Question {i}: depends_on must point to earlier questions." when `any(d >= i or d < 1 for d in q.depends_on)`.
      Expected outcome: one question each, dependencies backward.
   2. Task: Return problems + `common.compliance_claims(out)`.
      Expected outcome: no compliance claims.
   """
   problems: list[str] = []
   for i, q in enumerate(out.questions, 1):
      problems.extend(common.one_question(q.text, f"Question {i}: "))
      if any(d >= i or d < 1 for d in q.depends_on):
         problems.append(f"Question {i}: depends_on must point to earlier questions.")
   return problems + common.compliance_claims(out)

def v_reconcile(out: Reconciliation, deps: Deps) -> list[str]:
   """Problems with a reconciliation.

   Spec: S4.6 | Ticket: 08 | Traces to: I1, I4

   Build steps:
   1. Task: Return `intake.entry_problems(out.recorded) + common.compliance_claims(out)`.
      Expected outcome: reconciled entries are gate-ready.
   """
   return intake.entry_problems(out.recorded) + common.compliance_claims(out)


def v_dod(out: DodTurn, deps: Deps) -> list[str]:
   """Problems with one DoD turn.

   Spec: S4.6 | Ticket: 04 | Traces to: I1

   Build steps:
   1. Task: Add "done is false, so next_question is required." when `not out.done and out.next_question is None`;
      extend with `common.one_question(out.next_question.text)` when there is a next question.
      Expected outcome: one question at a time.
   2. Task: Return problems + `dod.draft_problems(out.agreed)`.
      Expected outcome: agreed items are verifiable and owned.
   """
   problems: list[str] = []
   if not out.done and out.next_question is None:
      problems.append("done is false, so next_question is required.")
   if out.next_question is not None:
      problems.extend(common.one_question(out.next_question.text))
   return problems + dod.draft_problems(out.agreed)


def v_prd_core(out: PRDCore, deps: Deps) -> list[str]:
   """Spec: S4.6 | Ticket: 05 | Traces to: I3

   Build steps:
   1. Task: Return `prd.core_problems(out, deps.known_ids)`.
      Expected outcome: the S3.4 rules, fed the session's known IDs.
   """
   return prd.core_problems(out, deps.known_ids)


def v_prd_narrative(out: PRDNarrative, deps: Deps) -> list[str]:
   """Spec: S4.6 | Ticket: 05 | Traces to: I3

   Build steps:
   1. Task: Return `prd.narrative_problems(out, deps.known_ids)`.
      Expected outcome: objectives are sourced.
   """
   return prd.narrative_problems(out, deps.known_ids)


def v_spec(out: Spec, deps: Deps) -> list[str]:
   """Spec: S4.6 | Ticket: 06 | Traces to: I1

   Build steps:
   1. Task: Return `spec.problems(out, deps.prd_ids)`.
      Expected outcome: coverage matches the PRD exactly.
   """
   return spec.problems(out, deps.prd_ids)


def v_tickets(out: TicketPlan, deps: Deps) -> list[str]:
   """Spec: S4.6 | Ticket: 07 | Traces to: I15

   Build steps:
   1. Task: Return `tickets.plan_problems(out, deps.feature_ids, deps.prd_ids)`.
      Expected outcome: the S3.6 rules with the session's features and requirement IDs.
   """
   return tickets.plan_problems(out, deps.feature_ids, deps.prd_ids)


GRILL = {
    1: AgentSpec("grill", "grill", static("grill.md", "question-bank.md", "mode-1.md"), GrillTurn, [v_grill], tools=True),
    2: AgentSpec("grill", "grill", static("grill.md", "question-bank.md", "mode-2.md"), GrillTurn, [v_grill], tools=True),
    3: AgentSpec("grill", "grill", static("grill.md", "question-bank.md", "mode-3.md"), GrillTurn, [v_grill], tools=True),
}
EXPLORE = AgentSpec("explore", "explore", static("explore.md", "mode-2.md"), CurrentStateMap,
                    [v_explore], tools=True, post=post_explore)
BRIEF = AgentSpec("brief", "questionnaire", static("brief.md"), BriefCritique)
QUESTIONNAIRE = AgentSpec("questionnaire", "questionnaire", static("questionnaire.md", "question-bank.md"),
                          Questionnaire, [v_questionnaire], tools=True)
RECONCILE = AgentSpec("reconcile", "reconcile", static("reconcile.md"), Reconciliation, [v_reconcile], tools=True)
DOD = AgentSpec("dod", "dod", static("dod.md", "dod-question-bank.md"), DodTurn, [v_dod])
PRD_CORE = AgentSpec("prd_core", "prd", static("prd.md", "style-guide.md"), PRDCore, [v_prd_core])
PRD_NARRATIVE = AgentSpec("prd_narrative", "prd", static("prd.md", "style-guide.md"), PRDNarrative, [v_prd_narrative])
SEAMS = AgentSpec("seams", "spec", static("seams.md"), Seams, tools=True)
SPEC = AgentSpec("spec", "spec", static("spec.md"), Spec, [v_spec], tools=True)
TICKETS = AgentSpec("tickets", "tickets", static("tickets.md"), TicketPlan, [v_tickets])


def agent(name: str, mode: int | None = None) -> AgentSpec:
    """Return the AgentSpec for a named agent. (Spec: S4.6 | Ticket: 02 | Traces to: I1)

    'grill' requires mode 1, 2, or 3; every other name is a plain lookup.
    """
    if name == "grill":
        if mode not in (1, 2, 3):
            raise KeyError("grill needs mode 1, 2, or 3")
        return GRILL[mode]
    table = {
        "explore": EXPLORE,
        "brief": BRIEF,
        "questionnaire": QUESTIONNAIRE,
        "reconcile": RECONCILE,
        "dod": DOD,
        "prd_core": PRD_CORE,
        "prd_narrative": PRD_NARRATIVE,
        "seams": SEAMS,
        "spec": SPEC,
        "tickets": TICKETS,
    }
    if name not in table:
        raise KeyError(name)
    return table[name]
