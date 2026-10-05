"""Run intake: setup, the three modes, the grill loop, and the intake gate.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C3 Gated progress and C6 People decide. Intake turns what
people know into a recorded, gated understanding. This file owns setup, mode
routing, grilling, the mode 2 map, the mode 3 questionnaire, and the gate node.

Why this comes now: Shared helpers (21) exist; intake is the first stage of every
session.

Build order: Step 22 of 33.
Previous: src/assay/graph/nodes/shared.py (step 21), which holds the helpers several
stages share.
Next: src/assay/graph/nodes/dod.py (step 23), which runs the Definition of Done
stage.

Build these in order:
    1. setup: the first node.
    2. route_mode: a pure router.
    3. grill_think: the grill loop's thinking half.
    4. grill_ask: the pause after the step above.
    5. after_grill: a pure router.
    6. explore: mode 2's first node.
    7. confirm_map_ask: the pause after the step above.
    8. brief_check: mode 3's first node.
    9. after_brief: a pure router.
    10. brief_fix_ask: the pause after the step above.
    11. write_questionnaire: after the brief passes.
    12. await_answers_ask: the pause after the step above.
    13. read_responses: after the PM continues.
    14. after_read: a pure router.
    15. reconcile: after responses are read.
    16. after_reconcile: a pure router.
    17. intake_gate_node: the gate node.
    18. after_gate: a pure router.

Depends on:
    assay.domain.ids: add_entries, all_answerable_ids. Recording and question IDs.
    assay.domain.models: Brief, NewEntry, Questionnaire, Turn. Shapes created here.
    assay.graph.context: AppContext, ctx. Dependencies.
    assay.graph.state: AssayState, log_view. The session and its log view.
    assay.graph.nodes.shared: files, glossary_text, reply, write_intake.
    assay.llm.agents: agent. The grill, explore, brief, questionnaire, and reconcile
    agents.
    assay.render.markdown: questionnaire. The printable questionnaire.
    assay.rules.intake: gate, failures. The exit gate.
    Standard library: json.
    Third-party: langgraph (Runtime, interrupt).

Depended on by:
    assay.graph.build: wires these nodes.

Spec coverage: S5.3, S5.4, S5.5, S5.6 | Traces to: I5, I6, I7
"""

import json

from langgraph.runtime import Runtime
from langgraph.types import interrupt

from assay.domain.ids import add_entries, all_answerable_ids
from assay.domain.models import Brief, NewEntry, Questionnaire, Turn
from assay.graph.context import AppContext, ctx
from assay.graph.nodes.shared import files, glossary_text, reply, write_intake
from assay.graph.state import AssayState, log_view
from assay.llm.agents import agent
from assay.render import markdown as md
from assay.rules import intake as gate_rules


def setup(s: AssayState, runtime: Runtime[AppContext]) -> dict[str, object]:
    """Start a session: load the team DoD and glossary, refuse mode 3 without a brief.

    Problem piece: C5 and C6: every session starts from the team's shared records.

    Why it matters: A team that has agreed its DoD must not be asked again, and
                    every session must use the shared glossary. Refusing mode 3
                    without a brief fails bad input at the start instead of
                    mid-questionnaire.

    What: Raises for mode 3 without a brief; otherwise loads the team DoD (phase
          'additions' when one exists, else 'team') and glossary, writes intake
          files, and returns those fields.

    Spec: S5.3 | Ticket: 02 | Traces to: I6, I12

    Raises:
        ValueError: 'Mode 3 needs a brief with the ask, the why, and the outcome.'

    Build steps:
    1. Task: Refuse mode 3 without a brief with the message above.
       Expected outcome: Mode 3 without a brief raises.
    2. Task: Load the team DoD and glossary; set the DoD phase to 'additions' when a
             team standard exists, else 'team'.
       Expected outcome: A second session skips the team phase.
    3. Task: Write the intake files from the updated state and return the loaded
             fields and file names.
       Expected outcome: intake.md exists after setup.
    """
    raise NotImplementedError("S5.3: setup")


def route_mode(s: AssayState) -> str:
    """Return the next node's name.

    Problem piece: C3: each mode starts in its own place.

    Why it matters: The three modes differ only in how they start; routing on the
                    mode keeps the rest of the graph shared.

    What: Reads state only and returns the next node: mode 1 to grill_think, mode 2
          to explore, mode 3 to brief_check.

    Spec: S5.3 | Ticket: 02 | Traces to: I5

    Build steps:
    1. Task: Choose the next node: mode 1 to grill_think, mode 2 to explore, mode 3
             to brief_check.
       Think about: Why must a router never read files or call anything?
       Expected outcome: Mode 3 routes to brief_check.
    """
    raise NotImplementedError("S5.3: route_mode")


def grill_think(s: AssayState, runtime: Runtime[AppContext]) -> dict[str, object]:
    """Run one grill turn: record the last answer and choose the next question.

    Problem piece: C2 and C6: intake one question at a time.

    Why it matters: Each answer changes what to ask next, so each turn records what
                    was learned and picks the next question. Everything that changes
                    per turn goes in the dynamic prompt so the agent's instructions
                    stay cacheable.

    What: Calls the grill agent for the session's mode, saves new glossary terms,
          appends entries with code IDs, rewrites intake files, and returns log,
          glossary, challenge, files, and the next question (none when done).

    Spec: S5.3 | Ticket: 02 | Traces to: I1, I7

    Build steps:
    1. Task: Build the dynamic prompt from: initiative and mode; the brief or
             'none'; the current-state map or 'n/a'; the glossary; the log view; the
             gate gaps (or 'Gate gaps: none reported yet.'); and the last question,
             recommendation, answer, and answering user (or a first-turn
             instruction).
       Think about: Why must none of this go into the agent's static prompt?
       Expected outcome: The static prompt is identical on every turn.
    2. Task: Run the grill agent for the session's mode and save any new glossary
             terms to the shared store.
       Expected outcome: A new term is visible to the next session.
    3. Task: Append recorded entries with code-assigned IDs, marking superseded
             ones, merge glossary terms, and rewrite the intake files.
       Expected outcome: Recorded entries receive IDs like D-001.
    4. Task: Return the log, glossary, challenge, files, and the next question, or
             none when the agent says intake is done.
       Expected outcome: A done turn returns no pending question.
    """
    raise NotImplementedError("S5.3: grill_think")


def grill_ask(s: AssayState) -> dict[str, object]:
    """Pause for a person (question) and record the reply.

    Problem piece: C6: a person answers each grill question.

    Why it matters: LangGraph reruns a paused node from its first line, so the pause
                    lives alone (I7); recording who answered makes the transcript
                    evidence.

    What: Pauses with kind 'question'; on resume returns a Turn recording the
          question, recommendation, answer, and answering user, with the pending
          question cleared.

    Spec: S5.3 | Ticket: 02 | Traces to: I7

    Build steps:
    1. Task: Pause with an interrupt of kind 'question' carrying the challenge,
             area, question, recommended answer, and reason, and nothing else in
             this node.
       Think about: What would rerun on resume if this node also called a model?
       Expected outcome: Resuming runs no model call.
    2. Task: Turn the resume value into a Turn recording the question,
             recommendation, answer, and answering user, with the pending question
             cleared.
       Expected outcome: The answer is recorded with the answering user.
    """
    raise NotImplementedError("S5.3: grill_ask")


def after_grill(s: AssayState) -> str:
    """Return the next node's name.

    Problem piece: C3: ask while there is a question, else check the gate.

    Why it matters: The agent's 'done' is a claim; the gate decides. Trusting the
                    agent's own claim of completion would let an intake with no
                    failure path or no out-of-scope list reach the PRD.

    What: Reads state only and returns the next node: grill_ask while a question is
          pending, otherwise intake_gate_node.

    Spec: S5.3 | Ticket: 02 | Traces to: I5

    Build steps:
    1. Task: Choose the next node: grill_ask while a question is pending, otherwise
             intake_gate_node.
       Think about: Why must a router never read files or call anything?
       Expected outcome: No pending question routes to intake_gate_node.
    """
    raise NotImplementedError("S5.3: after_grill")


def explore(s: AssayState, runtime: Runtime[AppContext]) -> dict[str, object]:
    """Map the current code for a mode 2 change.

    Problem piece: C2: argue about the gap, not the present.

    Why it matters: People's memory of a system is less reliable than its code; the
                    map anchors every later question.

    What: Runs the explore agent with the title, brief or 'none given', and
          glossary; returns the map.

    Spec: S5.4 | Ticket: 09 | Traces to: I10

    Build steps:
    1. Task: Build the dynamic prompt from the change title, the brief as
             description and evidence (or 'none given'), and the glossary, then run
             the explore agent.
       Expected outcome: The returned map lists the files it was built from.
    """
    raise NotImplementedError("S5.4: explore")


def confirm_map_ask(s: AssayState) -> dict[str, object]:
    """Pause for a person (map_review) and record the reply.

    Problem piece: C2 and C6: developers correct the map before grilling.

    Why it matters: A wrong map produces a wrong PRD; corrections must be on the
                    record. Recording corrections as entries, rather than editing
                    the map silently, keeps the evidence of what developers changed.

    What: Pauses with kind 'map_review'; on resume returns nothing when the reply is
          'ok', 'yes', 'correct', or empty, otherwise a correction entry (type C,
          area Delivery, titled 'Developer corrections to the current-state map',
          sourced to the user).

    Spec: S5.4 | Ticket: 09 | Traces to: I7

    Build steps:
    1. Task: Pause with an interrupt of kind 'map_review' carrying the map, and
             nothing else in this node.
       Think about: What would rerun on resume if this node also called a model?
       Expected outcome: Resuming runs no model call.
    2. Task: Turn the resume value into nothing when the reply is 'ok', 'yes',
             'correct', or empty, otherwise a correction entry (type C, area
             Delivery, titled 'Developer corrections to the current-state map',
             sourced to the user).
       Expected outcome: A reply of 'ok' changes nothing; any other reply adds a C
                         entry.
    """
    raise NotImplementedError("S5.4: confirm_map_ask")


def brief_check(s: AssayState, runtime: Runtime[AppContext]) -> dict[str, object]:
    """Judge whether the mode 3 brief is ready.

    Problem piece: C3: a weak brief never reaches developers.

    Why it matters: A vague outcome produces a vague questionnaire; fixing the brief
                    first saves developer time. Developer time is the scarcest input
                    in mode 3, so a brief that cannot produce good questions must
                    stop here.

    What: Runs the brief agent on the brief and returns its issues, or none when
          ready.

    Spec: S5.5 | Ticket: 08 | Traces to: I12

    Build steps:
    1. Task: Run the brief agent on the brief and return no issues when it is ready,
             else its issues.
       Expected outcome: A brief with a testable outcome returns no issues.
    """
    raise NotImplementedError("S5.5: brief_check")


def after_brief(s: AssayState) -> str:
    """Return the next node's name.

    Problem piece: C3: fix the brief before asking developers.

    Why it matters: The questionnaire is only as good as the brief. Sending a flawed
                    brief onward would waste a whole round of developer answers on
                    questions nobody can act on.

    What: Reads state only and returns the next node: brief_fix_ask when there are
          issues, otherwise write_questionnaire.

    Spec: S5.5 | Ticket: 08 | Traces to: I5

    Build steps:
    1. Task: Choose the next node: brief_fix_ask when there are issues, otherwise
             write_questionnaire.
       Think about: Why must a router never read files or call anything?
       Expected outcome: A brief with issues routes to brief_fix_ask.
    """
    raise NotImplementedError("S5.5: after_brief")


def brief_fix_ask(s: AssayState) -> dict[str, object]:
    """Pause for a person (brief_fix) and record the reply.

    Problem piece: C6: the PM fixes the brief.

    Why it matters: Only the PM owns the ask, the why, and the outcome. Developers
                    cannot fix the brief for the PM, so the session must wait for
                    the PM's own correction.

    What: Pauses with kind 'brief_fix'; on resume returns the edited brief
          (validated as a Brief) and cleared issues, keeping the old brief when none
          is sent.

    Spec: S5.5 | Ticket: 08 | Traces to: I7

    Build steps:
    1. Task: Pause with an interrupt of kind 'brief_fix' carrying the issues and the
             current brief, and nothing else in this node.
       Think about: What would rerun on resume if this node also called a model?
       Expected outcome: Resuming runs no model call.
    2. Task: Turn the resume value into the edited brief (validated as a Brief) and
             cleared issues, keeping the old brief when none is sent.
       Expected outcome: An edited brief replaces the old one.
    """
    raise NotImplementedError("S5.5: brief_fix_ask")


def write_questionnaire(s: AssayState, runtime: Runtime[AppContext]) -> dict[str, object]:
    """Write the round 1 questionnaire.

    Problem piece: C6: one batch developers answer offline.

    Why it matters: Developers answer better on their own time; the questionnaire
                    must be validated and numbered before anyone sees it.

    What: Runs the questionnaire agent, numbers its answerable IDs for round 1,
          writes the printable copy, and returns the questionnaire, round, IDs, and
          files.

    Spec: S5.5 | Ticket: 08 | Traces to: I2

    Build steps:
    1. Task: Run the questionnaire agent with the brief and glossary.
       Expected outcome: The questionnaire has 1 to 30 questions.
    2. Task: Number every answerable ID for round 1, write the printable copy with
             the form link '/q/<slug>', and return the questionnaire, round 1, the
             IDs, and files.
       Expected outcome: The returned IDs include Q-01.
    """
    raise NotImplementedError("S5.5: write_questionnaire")


def await_answers_ask(s: AssayState) -> dict[str, object]:
    """Pause for a person (await_answers) and record the reply.

    Problem piece: C6: the PM decides when enough answers are in.

    Why it matters: Answers arrive through the web form at any time; the PM, not a
                    timer, decides to continue.

    What: Pauses with kind 'await_answers'; on resume returns a cleared note. Called
          as await_answers_ask(s: AssayState) and returns dict[str, object].

    Spec: S5.5 | Ticket: 08 | Traces to: I7

    Build steps:
    1. Task: Pause with an interrupt of kind 'await_answers' carrying the round, the
             form link, and any note, and nothing else in this node.
       Think about: What would rerun on resume if this node also called a model?
       Expected outcome: Resuming runs no model call.
    2. Task: Turn the resume value into a cleared note.
       Expected outcome: Resuming clears the 'no responses' note.
    """
    raise NotImplementedError("S5.5: await_answers_ask")


def read_responses(s: AssayState, runtime: Runtime[AppContext]) -> dict[str, object]:
    """Collect new questionnaire responses for the current round.

    Problem piece: C6: only new answers are reconciled.

    Why it matters: Round two must never reconcile round one's answers again, or the
                    log fills with duplicates.

    What: Returns all and new responses, or a note telling the PM to share the form
          when there are none.

    Spec: S5.5 | Ticket: 08 | Traces to: I12

    Build steps:
    1. Task: Read the round's responses and keep those whose respondent and round
             are not already recorded.
       Think about: Which pair identifies a response as already seen?
       Expected outcome: A resubmitted sheet is not read twice.
    2. Task: With none new, return the note 'No new responses yet. Share the form
             link with the developers.'; otherwise return the combined and new
             responses.
       Expected outcome: With no responses the note is returned.
    """
    raise NotImplementedError("S5.5: read_responses")


def after_read(s: AssayState) -> str:
    """Return the next node's name.

    Problem piece: C6: keep waiting until answers exist.

    Why it matters: Reconciling nothing would waste a model call. Moving on with no
                    answers would make reconciliation invent conclusions from an
                    empty input.

    What: Reads state only and returns the next node: await_answers_ask when a note
          is set, otherwise reconcile.

    Spec: S5.5 | Ticket: 08 | Traces to: I5

    Build steps:
    1. Task: Choose the next node: await_answers_ask when a note is set, otherwise
             reconcile.
       Think about: Why must a router never read files or call anything?
       Expected outcome: A note routes back to await_answers_ask.
    """
    raise NotImplementedError("S5.5: after_read")


def reconcile(s: AssayState, runtime: Runtime[AppContext]) -> dict[str, object]:
    """Turn new responses into entries; allow at most one follow-up round.

    Problem piece: C2 and C3: answers become decisions, and gaps get one more
                   chance.

    Why it matters: Batched answers cannot react to each other, so contradictions
                    and blocking gaps are found here. Limiting follow-ups to one
                    round of at most eight questions stops developers being asked
                    forever; more than eight gaps means the brief was not ready.

    What: Records entries with sources, writes intake files, and either opens round
          2 for blocking gaps or puts the gaps and contradictions on the agenda.

    Spec: S5.5 | Ticket: 08 | Traces to: I1, I2

    Build steps:
    1. Task: Build the dynamic prompt from the brief, the round's questionnaire and
             IDs, the log view as 'already recorded', and the new responses, asking
             for questionnaire IDs and names in sources.
       Expected outcome: Recorded entries cite IDs like Q-02.
    2. Task: Run the reconcile agent, append its entries, and rewrite the intake
             files.
       Expected outcome: A corrected answer becomes a decision.
    3. Task: When this is round 1 with blocking gaps and 1 to 8 follow-up questions
             (and at most 8 gaps), open round 2: a questionnaire summarised
             'Follow-up on blocking gaps only.', its printable copy, and the
             follow-up IDs appended.
       Think about: Why only one follow-up round?
       Expected outcome: Round 1 with two blocking gaps opens round 2.
    4. Task: Otherwise put the blocking gaps and contradictions on the agenda for
             the live grill.
       Expected outcome: Round 2 with remaining gaps sends them to the grill.
    """
    raise NotImplementedError("S5.5: reconcile")


def after_reconcile(s: AssayState) -> str:
    """Return the next node's name.

    Problem piece: C3: wait for follow-ups or move to the gate.

    Why it matters: Only a fresh follow-up round needs more answers. Only a
                    just-opened second round needs more answers; everything else
                    must reach the gate, or the session stalls.

    What: Reads state only and returns the next node: await_answers_ask when round 2
          has just opened (round 2, gaps, no agenda), otherwise intake_gate_node.

    Spec: S5.5 | Ticket: 08 | Traces to: I5

    Build steps:
    1. Task: Choose the next node: await_answers_ask when round 2 has just opened
             (round 2, gaps, no agenda), otherwise intake_gate_node.
       Think about: Why must a router never read files or call anything?
       Expected outcome: A newly opened round 2 waits for answers.
    """
    raise NotImplementedError("S5.5: after_reconcile")


def intake_gate_node(s: AssayState, runtime: Runtime[AppContext]) -> dict[str, object]:
    """Check the intake gate and decide the next stage.

    Problem piece: C3: intake ends only when the gate passes.

    Why it matters: The agent's 'done' is a claim; the gate is the decision. Storing
                    the result in state keeps the router pure.

    What: Rewrites intake files, computes failures, and returns the agenda and
          stage: 'Definition of Done' when only the DoD fails, 'PRD' when nothing
          fails, else 'Intake'.

    Spec: S5.6 | Ticket: 03 | Traces to: I5

    Build steps:
    1. Task: Rewrite the intake files and compute the gate failures with the DoD
             counted as agreed only in phase 'done'.
       Expected outcome: intake.md shows the current gate.
    2. Task: Set the stage: 'Definition of Done' when the only failure is the DoD
             item, 'PRD' when there are none, otherwise 'Intake'; return the
             failures as the agenda.
       Think about: Why route DoD-only failures differently?
       Expected outcome: A passing gate sets stage 'PRD'.
    """
    raise NotImplementedError("S5.6: intake_gate_node")


def after_gate(s: AssayState) -> str:
    """Return the next node's name.

    Problem piece: C3: the gate's decision applied.

    Why it matters: Routing reads the stored result; it never re-checks. Re-checking
                    the gate inside the router would hide work in a decision and
                    could disagree with what the gate node recorded.

    What: Reads state only and returns the next node: prd when the agenda is empty,
          dod_think when the stage is 'Definition of Done', otherwise grill_think.

    Spec: S5.6 | Ticket: 03 | Traces to: I5

    Build steps:
    1. Task: Choose the next node: prd when the agenda is empty, dod_think when the
             stage is 'Definition of Done', otherwise grill_think.
       Think about: Why must a router never read files or call anything?
       Expected outcome: An empty agenda routes to prd.
    """
    raise NotImplementedError("S5.6: after_gate")
