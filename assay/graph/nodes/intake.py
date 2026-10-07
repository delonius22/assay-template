"""Intake: setup, the three modes, the grill loop, and the intake gate."""
import json

from langgraph.runtime import Runtime
from langgraph.types import interrupt

from ...domain.ids import add_entries, all_answerable_ids
from ...domain.models import Brief, NewEntry, Questionnaire, Turn
from ...llm import agents as A
from ...render import markdown as md
from ...rules import intake as gate_rules
from ..context import AppContext, ctx
from ..state import AssayState, log_view
from .shared import files, glossary_text, reply, write_intake


# ------------------------------------------------------------------ setup and grill (S5.3)
def setup(s: AssayState, runtime: Runtime[AppContext]):
    """Load the team DoD and glossary; refuse mode 3 without a brief.

    Spec: S5.3 | Ticket: 02 | Traces to: I6, I12

    Build steps:
    1. Task: `c = ctx(runtime)`; if `s.mode == 3 and not s.brief`, raise
       `ValueError("Mode 3 needs a brief with the ask, the why, and the outcome.")`.
       Expected outcome: bad input fails loudly.
    2. Task: `team = c.team_dod()`; build
       `update = {"dod_team": team, "dod_phase": "additions" if team else "team", "glossary": c.glossary()}`.
       Expected outcome: a team with a saved standard skips straight to additions.
    3. Task: `names = write_intake(s.model_copy(update=update), c)`; return `update | {"files": files(s, *names)}`.
       Expected outcome: intake.md exists from the first step.
    """
    c = ctx(runtime)
    if s.mode == 3 and not s.brief:
        raise ValueError("Mode 3 needs a brief with the ask, the why, and the outcome.")
    team = c.team_dod()
    update = {"dod_team": team, "dod_phase": "additions" if team else "team", "glossary": c.glossary()}
    names = write_intake(s.model_copy(update=update), c)
    return update | {"files": files(s, *names)}


def route_mode(s: AssayState) -> str:
    """Spec: S5.3 | Ticket: 02 | Traces to: I5

    Build steps:
    1. Task: Return `{1: "grill_think", 2: "explore", 3: "brief_check"}[s.mode]`.
       Expected outcome: the node that starts this mode.
    """
    return {1: "grill_think", 2: "explore", 3: "brief_check"}[s.mode]


def grill_think(s: AssayState, runtime: Runtime[AppContext]):
    """One grill turn: record the last answer's entries and choose the next question.

    Spec: S5.3 | Ticket: 02 | Traces to: I1, I7

    Build steps:
    1. Task: `c = ctx(runtime)`; `last = s.transcript[-1] if s.transcript else None`.
       Expected outcome: the latest answer, if any.
    2. Task: Build `dynamic = "\\n\\n".join([...])` from: f"Initiative: {s.title} (mode {s.mode})";
       f"Brief: {s.brief.model_dump_json() if s.brief else 'none'}";
       f"Current-state map: {s.current_map.model_dump_json() if s.current_map else 'n/a'}";
       f"Glossary:\\n{glossary_text(s)}"; f"Session log so far:\\n{log_view(s)}";
       the gate gaps ("Gaps the gate found (work through these first):\\n- " + "\\n- ".join(s.agenda)) or
       "Gate gaps: none reported yet."; and the last question, recommendation, and answer with `last.user`, or
       "This is the first turn. Start with the most foundational question.".
       Expected outcome: everything changing per turn is in the dynamic part only (A2).
    3. Task: `turn = c.run(A.GRILL[s.mode], dynamic, s)`; if `turn.glossary_updates`, call `c.save_terms(turn.glossary_updates)`.
       Expected outcome: validated turn; new terms shared team-wide.
    4. Task: `terms = {t.term: t for t in s.glossary} | {t.term: t for t in turn.glossary_updates}`;
       `update = {"log": add_entries(s.log, turn.recorded, turn.supersedes), "glossary": list(terms.values())}`;
       `names = write_intake(s.model_copy(update=update), c)`.
       Expected outcome: code-assigned IDs (I2); files match state.
    5. Task: Return `update | {"challenge": turn.challenge, "files": files(s, *names),
       "pending": None if turn.done else turn.next_question}`.
       Expected outcome: no pending question means the agent thinks intake is done.
    """
    c = ctx(runtime)
    last = s.transcript[-1] if s.transcript else None
    dynamic = "\n\n".join([
        f"Initiative: {s.title} (mode {s.mode})",
        f"Brief: {s.brief.model_dump_json() if s.brief else 'none'}",
        f"Current-state map: {s.current_map.model_dump_json() if s.current_map else 'n/a'}",
        f"Glossary:\n{glossary_text(s)}",
        f"Session log so far:\n{log_view(s)}",
        ("Gaps the gate found (work through these first):\n- " + "\n- ".join(s.agenda))
        if s.agenda else "Gate gaps: none reported yet.",
        (f"Last question: {last.question}\nRecommendation: {last.recommended}\n"
         f"Answer ({last.user}): {last.answer}" if last
         else "This is the first turn. Start with the most foundational question."),
    ])
    turn = c.run(A.GRILL[s.mode], dynamic, s)
    if turn.glossary_updates:
        c.save_terms(turn.glossary_updates)
    terms = {t.term: t for t in s.glossary} | {t.term: t for t in turn.glossary_updates}
    update = {"log": add_entries(s.log, turn.recorded, turn.supersedes),
              "glossary": list(terms.values())}
    names = write_intake(s.model_copy(update=update), c)
    return update | {"challenge": turn.challenge, "files": files(s, *names),
                     "pending": None if turn.done else turn.next_question}


def grill_ask(s: AssayState):
    """Pause for the human answer. Nothing else happens in this node (I7).

    Spec: S5.3 | Ticket: 02 | Traces to: I7

    Build steps:
    1. Task: `q = s.pending`; `text, user = reply(interrupt({"kind": "question", "challenge": s.challenge,
       "area": q.area, "question": q.text, "recommended": q.recommended_answer, "reason": q.reason}))`.
       Expected outcome: the session pauses; the resume value is the answer.
    2. Task: Return `{"transcript": s.transcript + [Turn(question=q.text, recommended=q.recommended_answer,
       answer=text, user=user)], "pending": None}`.
       Expected outcome: the answer is recorded with who gave it and when.
    """
    q = s.pending
    text, user = reply(interrupt({"kind": "question", "challenge": s.challenge, "area": q.area,
                                  "question": q.text, "recommended": q.recommended_answer,
                                  "reason": q.reason}))
    return {"transcript": s.transcript + [Turn(question=q.text, recommended=q.recommended_answer,
                                               answer=text, user=user)],
            "pending": None}


def after_grill(s: AssayState) -> str:
    """Spec: S5.3 | Ticket: 02 | Traces to: I5

    Build steps:
    1. Task: Return `"grill_ask" if s.pending else "intake_gate_node"`.
       Expected outcome: ask while there is a question; otherwise check the gate.
    """
    return "grill_ask" if s.pending else "intake_gate_node"


# ------------------------------------------------------------------ mode 2 (S5.4)
def explore(s: AssayState, runtime: Runtime[AppContext]):
    """Map the current code.

    Spec: S5.4 | Ticket: 09 | Traces to: I10

    Build steps:
    1. Task: `dynamic = f"Change requested: {s.title}\\n\\nDescription and evidence:\\n" +
       (s.brief.model_dump_json(indent=2) if s.brief else "none given") + f"\\n\\nGlossary:\\n{glossary_text(s)}"`.
       Expected outcome: the agent knows what is changing.
    2. Task: Return `{"current_map": ctx(runtime).run(A.EXPLORE, dynamic, s)}`.
       Expected outcome: a map built from code the agent read.
    """
    dynamic = (f"Change requested: {s.title}\n\nDescription and evidence:\n"
               + (s.brief.model_dump_json(indent=2) if s.brief else "none given")
               + f"\n\nGlossary:\n{glossary_text(s)}")
    return {"current_map": ctx(runtime).run(A.EXPLORE, dynamic, s)}


def confirm_map_ask(s: AssayState):
    """Pause for developers to confirm or correct the map.

    Spec: S5.4 | Ticket: 09 | Traces to: I7

    Build steps:
    1. Task: `text, user = reply(interrupt({"kind": "map_review", "map": s.current_map.model_dump()}))`.
       Expected outcome: pause until reviewed.
    2. Task: If `text.lower() in ("ok", "yes", "correct", "")`, return `{}`.
       Expected outcome: a confirmed map changes nothing.
    3. Task: Otherwise build `NewEntry(type="C", title="Developer corrections to the current-state map",
       area="Delivery", detail=text, source=f"{user}, map review")` and return `{"log": add_entries(s.log, [corr])}`.
       Expected outcome: corrections are on the record.
    """
    text, user = reply(interrupt({"kind": "map_review", "map": s.current_map.model_dump()}))
    if text.lower() in ("ok", "yes", "correct", ""):
        return {}
    corr = NewEntry(type="C", title="Developer corrections to the current-state map", area="Delivery",
                    detail=text, source=f"{user}, map review")
    return {"log": add_entries(s.log, [corr])}


# ------------------------------------------------------------------ mode 3 (S5.5)
def brief_check(s: AssayState, runtime: Runtime[AppContext]):
    """Spec: S5.5 | Ticket: 08 | Traces to: I12

    Build steps:
    1. Task: `crit = ctx(runtime).run(A.BRIEF, s.brief.model_dump_json(indent=2), s)`.
       Expected outcome: a ready flag and issues.
    2. Task: Return `{"brief_issues": [] if crit.ready else crit.issues}`.
       Expected outcome: issues route to the fix pause.
    """
    crit = ctx(runtime).run(A.BRIEF, s.brief.model_dump_json(indent=2), s)
    return {"brief_issues": [] if crit.ready else crit.issues}


def after_brief(s: AssayState) -> str:
    """Spec: S5.5 | Ticket: 08 | Traces to: I5

    Build steps:
    1. Task: Return `"brief_fix_ask" if s.brief_issues else "write_questionnaire"`.
       Expected outcome: a weak brief never reaches developers.
    """
    return "brief_fix_ask" if s.brief_issues else "write_questionnaire"


def brief_fix_ask(s: AssayState):
    """Spec: S5.5 | Ticket: 08 | Traces to: I7, I12

    Build steps:
    1. Task: `value = interrupt({"kind": "brief_fix", "issues": s.brief_issues, "brief": s.brief.model_dump()})`.
       Expected outcome: the PM edits the brief in the browser.
    2. Task: `brief = value.get("brief") if isinstance(value, dict) else None`; return
       `{"brief": Brief(**brief) if brief else s.brief, "brief_issues": []}`.
       Expected outcome: the edited brief is validated by its model.
    """
    value = interrupt({"kind": "brief_fix", "issues": s.brief_issues,
                       "brief": s.brief.model_dump()})
    brief = value.get("brief") if isinstance(value, dict) else None
    return {"brief": Brief(**brief) if brief else s.brief, "brief_issues": []}


def write_questionnaire(s: AssayState, runtime: Runtime[AppContext]):
    """Spec: S5.5 | Ticket: 08 | Traces to: I2

    Build steps:
    1. Task: `c = ctx(runtime)`; `q: Questionnaire = c.run(A.QUESTIONNAIRE, f"Brief:\\n{s.brief.model_dump_json(indent=2)}\\n\\nGlossary:\\n{glossary_text(s)}", s)`.
       Expected outcome: a validated questionnaire.
    2. Task: `s2 = s.model_copy(update={"questionnaire": q, "q_round": 1, "q_ids": all_answerable_ids(q, 1)})`;
       `name = md.questionnaire(s2, c.folder(s), f"/q/{s.slug}")`.
       Expected outcome: a printable copy is written.
    3. Task: Return `{"questionnaire": q, "q_round": 1, "q_ids": s2.q_ids, "files": files(s, name)}`.
       Expected outcome: the web form serves these IDs.
    """
    c = ctx(runtime)
    q: Questionnaire = c.run(A.QUESTIONNAIRE,
                             f"Brief:\n{s.brief.model_dump_json(indent=2)}\n\nGlossary:\n{glossary_text(s)}", s)
    s2 = s.model_copy(update={"questionnaire": q, "q_round": 1, "q_ids": all_answerable_ids(q, 1)})
    name = md.questionnaire(s2, c.folder(s), f"/q/{s.slug}")
    return {"questionnaire": q, "q_round": 1, "q_ids": s2.q_ids, "files": files(s, name)}


def await_answers_ask(s: AssayState):
    """Spec: S5.5 | Ticket: 08 | Traces to: I7

    Build steps:
    1. Task: `interrupt({"kind": "await_answers", "round": s.q_round, "form": f"/q/{s.slug}",
       "note": s.agenda[0] if s.agenda else ""})`.
       Expected outcome: the PM shares the link and continues when answers are in.
    2. Task: Return `{"agenda": []}`.
       Expected outcome: the "no responses" note is cleared on resume.
    """
    interrupt({"kind": "await_answers", "round": s.q_round, "form": f"/q/{s.slug}",
               "note": s.agenda[0] if s.agenda else ""})
    return {"agenda": []}


def read_responses(s: AssayState, runtime: Runtime[AppContext]):
    """Spec: S5.5 | Ticket: 08 | Traces to: I12

    Build steps:
    1. Task: `sheets = ctx(runtime).responses(s.slug, s.q_round)`; `seen = {(r.respondent, r.round) for r in s.responses}`;
       `new = [r for r in sheets if (r.respondent, r.round) not in seen]`.
       Expected outcome: only responses not yet reconciled.
    2. Task: If `not new`, return `{"agenda": ["No new responses yet. Share the form link with the developers."]}`.
       Expected outcome: the router waits again.
    3. Task: Return `{"responses": s.responses + new, "new_responses": new, "agenda": []}`.
       Expected outcome: round two never re-reconciles round one.
    """
    sheets = ctx(runtime).responses(s.slug, s.q_round)
    seen = {(r.respondent, r.round) for r in s.responses}
    new = [r for r in sheets if (r.respondent, r.round) not in seen]
    if not new:
        return {"agenda": ["No new responses yet. Share the form link with the developers."]}
    return {"responses": s.responses + new, "new_responses": new, "agenda": []}


def after_read(s: AssayState) -> str:
    """Spec: S5.5 | Ticket: 08 | Traces to: I5

    Build steps:
    1. Task: Return `"await_answers_ask" if s.agenda else "reconcile"`.
       Expected outcome: no responses, keep waiting.
    """
    return "await_answers_ask" if s.agenda else "reconcile"


def reconcile(s: AssayState, runtime: Runtime[AppContext]):
    """Turn new responses into log entries; allow at most one follow-up round.

    Spec: S5.5 | Ticket: 08 | Traces to: I1, I2

    Build steps:
    1. Task: `c = ctx(runtime)`; build `dynamic` from the brief JSON, f"Questionnaire round {s.q_round} (IDs {s.q_ids})"
       with `s.questionnaire.model_dump_json(indent=1)`, "Already recorded (do not repeat):\\n" + `log_view(s)`,
       "New responses:\\n" + `json.dumps([r.model_dump() for r in s.new_responses], indent=1)`, and the instruction
       "Use questionnaire IDs (Q-01, K-01) and the respondent's name in each entry's source.".
       Expected outcome: only new answers are reconciled.
    2. Task: `rec = c.run(A.RECONCILE, dynamic, s)`; `update = {"log": add_entries(s.log, rec.recorded),
       "reconcile_gaps": rec.blocking_gaps}`; `write_intake(s.model_copy(update=update), c)`.
       Expected outcome: decisions recorded with sources.
    3. Task: If `rec.blocking_gaps and s.q_round == 1 and 0 < len(rec.follow_up_questions) <= 8 and
       len(rec.blocking_gaps) <= 8`: `fq = Questionnaire(summary="Follow-up on blocking gaps only.",
       questions=rec.follow_up_questions)`; render it with `md.questionnaire(s.model_copy(update={"questionnaire": fq,
       "q_round": 2}), c.folder(s), f"/q/{s.slug}")`; return update | `{"questionnaire": fq, "q_round": 2,
       "q_ids": s.q_ids + all_answerable_ids(fq, 2), "files": files(s, name), "agenda": []}`.
       Expected outcome: exactly one follow-up round, blocking gaps only.
    4. Task: Otherwise return `update | {"agenda": rec.blocking_gaps + rec.contradictions}`.
       Expected outcome: remaining gaps go to the PM live; more than eight means the brief was not ready.
    """
    c = ctx(runtime)
    dynamic = "\n\n".join([
        s.brief.model_dump_json(indent=2),
        f"Questionnaire round {s.q_round} (IDs {s.q_ids})\n"
        + s.questionnaire.model_dump_json(indent=1),
        "Already recorded (do not repeat):\n" + log_view(s),
        "New responses:\n" + json.dumps([r.model_dump() for r in s.new_responses], indent=1),
        "Use questionnaire IDs (Q-01, K-01) and the respondent's name in each entry's source.",
    ])
    rec = c.run(A.RECONCILE, dynamic, s)
    update = {"log": add_entries(s.log, rec.recorded), "reconcile_gaps": rec.blocking_gaps}
    write_intake(s.model_copy(update=update), c)
    if rec.blocking_gaps and s.q_round == 1 and 0 < len(rec.follow_up_questions) <= 8 \
            and len(rec.blocking_gaps) <= 8:
        fq = Questionnaire(summary="Follow-up on blocking gaps only.",
                           questions=rec.follow_up_questions)
        name = md.questionnaire(s.model_copy(update={"questionnaire": fq, "q_round": 2}),
                                c.folder(s), f"/q/{s.slug}")
        return update | {"questionnaire": fq, "q_round": 2,
                         "q_ids": s.q_ids + all_answerable_ids(fq, 2),
                         "files": files(s, name), "agenda": []}
    return update | {"agenda": rec.blocking_gaps + rec.contradictions}


def after_reconcile(s: AssayState) -> str:
    """Spec: S5.5 | Ticket: 08 | Traces to: I5

    Build steps:
    1. Task: Return `"await_answers_ask"` when `s.q_round == 2 and s.reconcile_gaps and not s.agenda`;
       otherwise `"intake_gate_node"`.
       Expected outcome: a fresh follow-up round waits for answers; everything else goes to the gate.
    """
    if s.q_round == 2 and s.reconcile_gaps and not s.agenda:
        return "await_answers_ask"
    return "intake_gate_node"


# ------------------------------------------------------------------ intake gate (S5.6)
def intake_gate_node(s: AssayState, runtime: Runtime[AppContext]):
    """Spec: S5.6 | Ticket: 03 | Traces to: I5

    Build steps:
    1. Task: `names = write_intake(s, ctx(runtime))`.
       Expected outcome: intake.md shows the current gate.
    2. Task: `failed = gate_rules.failures(gate_rules.gate(s.log, s.dod_phase == "done"))`.
       Expected outcome: the list of open gate items.
    3. Task: `only_dod = bool(failed) and all(f.startswith("Team Definition of Done") for f in failed)`;
       `stage = "Definition of Done" if only_dod else ("PRD" if not failed else "Intake")`.
       Expected outcome: the next stage is decided from state.
    4. Task: Return `{"agenda": failed, "stage": stage, "files": files(s, *names)}`.
       Expected outcome: the router reads `agenda` and `stage` only.
    """
    names = write_intake(s, ctx(runtime))
    failed = gate_rules.failures(gate_rules.gate(s.log, s.dod_phase == "done"))
    only_dod = bool(failed) and all(f.startswith("Team Definition of Done") for f in failed)
    stage = "Definition of Done" if only_dod else ("PRD" if not failed else "Intake")
    return {"agenda": failed, "stage": stage, "files": files(s, *names)}


def after_gate(s: AssayState) -> str:
    """Spec: S5.6 | Ticket: 03 | Traces to: I5

    Build steps:
    1. Task: Return `"prd"` when `not s.agenda`; `"dod_think"` when `s.stage == "Definition of Done"`;
       otherwise `"grill_think"`.
       Expected outcome: a pure router; no I/O.
    """
    if not s.agenda:
        return "prd"
    if s.stage == "Definition of Done":
        return "dod_think"
    return "grill_think"
