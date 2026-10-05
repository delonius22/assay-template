"""Definition of Done: the shared team standard once, then initiative additions."""
from langgraph.runtime import Runtime
from langgraph.types import interrupt

from ...domain.ids import apply_dod_turn
from ...domain.models import Turn
from ...llm import agents as A
from ...render import markdown as md
from ...rules import dod as dod_rules
from ..context import AppContext, ctx
from ..state import AssayState, log_view
from .shared import files, reply

TEAM_SESSION = ("Session type: TEAM STANDARD, shared by every initiative. Start by asking for the bank's "
                "mandated SDLC or control standard.")
ADDITIONS_SESSION = ("Session type: ADDITIONS for this initiative only, on top of the team standard. Propose "
                     "additions triggered by the intake log; propose none if nothing warrants it.")


def dod_think(s: AssayState, runtime: Runtime[AppContext]):
    """One DoD turn; on done, check and save the team standard or the additions.

    Spec: S5.7 | Ticket: 04 | Traces to: I2, I5

    Build steps:
    1. Task: `c = ctx(runtime)`; `team_phase = s.dod_phase == "team"`; `last = s.dod_transcript[-1] if s.dod_transcript else None`;
       `agreed = "\\n".join(f"{i.id} [{i.level}] {i.statement}" for i in s.dod_team + s.dod_additions) or "(none yet)"`.
       Expected outcome: the agent sees what is already agreed.
    2. Task: Build `dynamic` from `TEAM_SESSION` (team phase) or `ADDITIONS_SESSION + "\\n\\nIntake log:\\n" + log_view(s)`,
       then f"Items agreed so far:\\n{agreed}", then the checker problems in `s.dod_agenda` when any, then the last
       question, recommendation, and answer with `last.user` (or "First turn.").
       Expected outcome: per-turn state in the dynamic part only.
    3. Task: `turn = c.run(A.DOD, dynamic, s)`; `items, retired = apply_dod_turn(s.dod_team if team_phase else s.dod_additions,
       s.dod_retired, turn, additions=not team_phase)`; `update = {("dod_team" if team_phase else "dod_additions"): items,
       "dod_retired": retired, "challenge": turn.challenge, "dod_agenda": [], "stage": "Definition of Done",
       "dod_pending": None if turn.done else turn.next_question}`; return `update` when `not turn.done`.
       Expected outcome: IDs never reused (I2).
    4. Task: `problems = dod_rules.team_problems(items) if team_phase else dod_rules.draft_problems(items)`; when any,
       return `update | {"dod_agenda": problems}`.
       Expected outcome: the router loops back with the problems.
    5. Task: Team phase: `c.save_team_dod(items, by=s.dod_transcript[-1].user if s.dod_transcript else s.pm)`;
       `md.dod(items, c.settings.artifacts_dir / "definition-of-done.md", f"Definition of Done — {c.settings.team_name}")`;
       return `update | {"dod_phase": "additions", "dod_transcript": []}`. Additions phase: when `items`,
       `name = md.dod(items, c.folder(s) / "dod-additions.md", f"DoD additions — {s.title}")` (else `name = ""`);
       return `update | {"dod_phase": "done", "dod_transcript": [], "files": files(s, name)}`.
       Expected outcome: the team standard is shared; additions belong to this initiative.
    """
    raise NotImplementedError("S5.7")


def dod_ask(s: AssayState):
    """Spec: S5.7 | Ticket: 04 | Traces to: I7

    Build steps:
    1. Task: `q = s.dod_pending`; `text, user = reply(interrupt({"kind": "dod_question", "challenge": s.challenge,
       "question": q.text, "recommended": q.recommended_answer, "reason": q.reason}))`.
       Expected outcome: pause for the PM's answer.
    2. Task: Return `{"dod_transcript": s.dod_transcript + [Turn(question=q.text, recommended=q.recommended_answer,
       answer=text, user=user)], "dod_pending": None}`.
       Expected outcome: the answer is recorded with who gave it.
    """
    raise NotImplementedError("S5.7")


def after_dod(s: AssayState) -> str:
    """Spec: S5.7 | Ticket: 04 | Traces to: I5

    Build steps:
    1. Task: Return `"dod_ask"` when `s.dod_pending`; `"intake_gate_node"` when `s.dod_phase == "done"`;
       otherwise `"dod_think"`.
       Expected outcome: checker problems and the team-to-additions switch both loop to dod_think.
    """
    raise NotImplementedError("S5.7")
