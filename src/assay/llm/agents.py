"""Define every agent from its prompt files, output shape, and rules.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C1 Trustworthy output. Each agent is a prompt, an output
shape, and the rules its output must pass. This file assembles them; it never calls
a model.

Why this comes now: The call loop (step 13) defines AgentSpec. The workflow (steps
21 to 26) asks for agents by name.

Build order: Step 14 of 33.
Previous: src/assay/llm/call.py (step 13), which runs the validate-and-retry loop
every agent call goes through.
Next: src/assay/llm/client.py (step 15), which creates the gateway chat client.

Build these in order:
    1. text: the smallest piece.
    2. static: builds on text.
    3. agent: uses static; the validators below plug into it.
    4. v_grill: validators follow in pipeline order.
    5. v_explore: mode 2's map.
    6. v_questionnaire: mode 3's batch.
    7. v_reconcile: mode 3's results.
    8. v_dod: the DoD stage.
    9. v_prd_core: the PRD.
    10. v_prd_narrative: the PRD prose.
    11. v_spec: the spec.
    12. v_tickets: the backlog.
    13. post_explore: runs after v_explore passes.

Depends on:
    assay.domain.models: every agent output shape.
    assay.rules: common, dod, intake, prd, spec, tickets. The validators.
    assay.llm.call: AgentSpec. What this file builds.
    assay.llm.tools: Deps. What validators receive.
    Standard library: functools, pathlib.
    Third-party: none.

Depended on by:
    assay.graph.nodes: every agent call.

Spec coverage: S4.6 | Traces to: I1, I3, I4, I15
"""

from functools import lru_cache
from pathlib import Path

from assay.domain.models import (
    BriefCritique,
    CurrentStateMap,
    DodTurn,
    GrillTurn,
    PRDCore,
    PRDNarrative,
    Questionnaire,
    Reconciliation,
    Seams,
    Spec,
    TicketPlan,
)
from assay.llm.call import AgentSpec
from assay.llm.tools import Deps
from assay.rules import common, dod, intake, prd, spec, tickets

PROMPTS = Path(__file__).resolve().parent.parent / "prompts"  # S4.6: content files
AGENTS: dict[
    str, tuple[str, str, tuple[str, ...], bool]
] = {  # S4.6: name -> (role, task, refs, tools)
    "grill": ("grill", "grill.md", ("question-bank.md",), True),
    "explore": ("explore", "explore.md", ("mode-2.md",), True),
    "brief": ("questionnaire", "brief.md", (), False),
    "questionnaire": ("questionnaire", "questionnaire.md", ("question-bank.md",), True),
    "reconcile": ("reconcile", "reconcile.md", (), True),
    "dod": ("dod", "dod.md", ("dod-question-bank.md",), False),
    "prd_core": ("prd", "prd.md", ("style-guide.md",), False),
    "prd_narrative": ("prd", "prd.md", ("style-guide.md",), False),
    "seams": ("spec", "seams.md", (), True),
    "spec": ("spec", "spec.md", (), True),
    "tickets": ("tickets", "tickets.md", (), False),
}


@lru_cache
def text(name: str) -> str:
    """Return one prompt file's text, trimmed.

    Problem piece: C1: prompts are editable files, not Python strings.

    Why it matters: PMs tune wording without touching code; caching avoids
                    re-reading files on every turn. A prompt read from disk on every
                    turn would slow each grill question for no benefit, since
                    prompts change only on deploy.

    What: Reads a file under PROMPTS and returns its trimmed text. Called as
          text(name: str) and returns str.

    Spec: S4.6 | Ticket: 02 | Traces to: I1

    Build steps:
    1. Task: Read the named file under PROMPTS as UTF-8 and return it trimmed.
       Expected outcome: 'common.md' returns text starting '# Rules for every task'.
    """
    raise NotImplementedError("S4.6: text")


def static(task: str, *refs: str) -> str:
    """Return the cacheable prefix: common rules, the task, then references.

    Problem piece: C1: one identical prefix per agent, so it caches (A2).

    Why it matters: The order must never vary between calls, or the provider sees a
                    different prefix and caches nothing.

    What: Common rules, the task file, then each reference file, separated by a
          horizontal rule. Called as static(task: str) and returns str.

    Spec: S4.6 | Ticket: 02 | Traces to: A2

    Build steps:
    1. Task: Join common.md, the task file, and each reference file under
             'reference/', separated by a blank line, three hyphens, and a blank
             line.
       Expected outcome: Both PRD agents produce the identical prefix.
    """
    raise NotImplementedError("S4.6: static")


def agent(name: str, mode: int | None = None) -> AgentSpec:
    """Return the AgentSpec for a named agent.

    Problem piece: C1: one place that pairs each agent with its prompt, shape, and
                   rules.

    Why it matters: The workflow asks for agents by name. Building specs on demand,
                    from the AGENTS table, keeps the pairing of prompt, output
                    shape, and validators in one readable place.

    What: Looks up the name in AGENTS; the grill agent appends the mode reference
          (mode-1.md, mode-2.md, or mode-3.md). Pairs each agent with its output
          shape and validators.

    Spec: S4.6 | Ticket: 02 | Traces to: I1

    Raises:
        KeyError: an unknown agent name.

    Build steps:
    1. Task: Look up role, task, references, and tool use; for 'grill' add the
             mode's reference file.
       Think about: Why must each grill mode be a different spec?
       Expected outcome: agent('grill', 2) includes mode-2.md.
    2. Task: Pair the agent with its output shape and validators: grill GrillTurn
             with v_grill; explore CurrentStateMap with v_explore and post_explore;
             brief BriefCritique with none; questionnaire Questionnaire with
             v_questionnaire; reconcile Reconciliation with v_reconcile; dod DodTurn
             with v_dod; prd_core PRDCore with v_prd_core; prd_narrative
             PRDNarrative with v_prd_narrative; seams Seams with none; spec Spec
             with v_spec; tickets TicketPlan with v_tickets.
       Expected outcome: agent('tickets') returns a spec whose output is TicketPlan.
    """
    raise NotImplementedError("S4.6: agent")


def v_grill(out: GrillTurn, deps: Deps) -> list[str]:
    """Return problems with one grill turn.

    Problem piece: C1 and C3: one question, gate-ready entries, no compliance
                   claims.

    Why it matters: Each turn both records entries and asks the next question, so it
                    must satisfy the question rule, the entry rules, and the
                    compliance rule at once.

    What: A next question unless done, one question only, known superseded IDs,
          entry flags, and no compliance claims.

    Spec: S4.6 | Ticket: 02 | Traces to: I1, I4

    Build steps:
    1. Task: Require a next question unless done, and check it asks one question.
       Expected outcome: done=false with no question is rejected.
    2. Task: Require superseded IDs to be known, then add entry and compliance
             problems.
       Expected outcome: Superseding D-999 is rejected.
    """
    raise NotImplementedError("S4.6: v_grill")


def v_explore(out: CurrentStateMap, deps: Deps) -> list[str]:
    """Require at least one file read when code access is configured.

    Problem piece: C1: maps are built from code, not guesses.

    Why it matters: A map produced without reading code is a guess presented as
                    evidence, which mode 2 exists to prevent.

    What: No problem without code roots; otherwise a problem until a file has been
          read. Called as v_explore(out: CurrentStateMap, deps: Deps) and returns
          list[str].

    Spec: S4.6 | Ticket: 09 | Traces to: I1

    Build steps:
    1. Task: Return no problems without code roots; otherwise require that at least
             one file was read.
       Expected outcome: A map before any read is rejected.
    """
    raise NotImplementedError("S4.6: v_explore")


def v_questionnaire(out: Questionnaire, deps: Deps) -> list[str]:
    """Return problems with a questionnaire.

    Problem piece: C1 and C6: answerable questions with backward dependencies.

    Why it matters: Developers answer offline, so a compound question or a forward
                    dependency produces answers nobody can use.

    What: One question each, dependencies pointing to earlier questions, and no
          compliance claims. Called as v_questionnaire(out: Questionnaire, deps:
          Deps) and returns list[str].

    Spec: S4.6 | Ticket: 08 | Traces to: I1, I4

    Build steps:
    1. Task: Check each question asks one question and depends only on earlier
             positions, then add compliance problems.
       Expected outcome: A question depending on itself is rejected.
    """
    raise NotImplementedError("S4.6: v_questionnaire")


def v_reconcile(out: Reconciliation, deps: Deps) -> list[str]:
    """Return problems with a reconciliation.

    Problem piece: C1 and C3: reconciled entries are gate-ready.

    Why it matters: Entries from answers feed the same gate as grill entries, so
                    they need the same flags.

    What: The intake entry problems for every recorded entry, plus any compliance
          assertion anywhere in the reconciliation.

    Spec: S4.6 | Ticket: 08 | Traces to: I1, I4

    Build steps:
    1. Task: Return entry problems plus compliance problems.
       Expected outcome: A scope entry without a side is rejected.
    """
    raise NotImplementedError("S4.6: v_reconcile")


def v_dod(out: DodTurn, deps: Deps) -> list[str]:
    """Return problems with one Definition of Done turn.

    Problem piece: C1 and C6: one question, verifiable items.

    Why it matters: The DoD is grilled like intake, so the same one-question rule
                    applies, plus item quality.

    What: A next question unless done, one question only, and item problems. Called
          as v_dod(out: DodTurn, deps: Deps) and returns list[str].

    Spec: S4.6 | Ticket: 04 | Traces to: I1

    Build steps:
    1. Task: Require a next question unless done, check it asks one question, then
             add item problems.
       Expected outcome: 'Code is clean' is rejected.
    """
    raise NotImplementedError("S4.6: v_dod")


def v_prd_core(out: PRDCore, deps: Deps) -> list[str]:
    """Return problems with the PRD core.

    Problem piece: C1 and C4: the S3.4 rules applied to this session.

    Why it matters: The core is where invented sources would enter the PRD, so the
                    session's known IDs are checked here.

    What: The PRD core rules, using the session's known IDs. Called as
          v_prd_core(out: PRDCore, deps: Deps) and returns list[str].

    Spec: S4.6 | Ticket: 05 | Traces to: I3

    Build steps:
    1. Task: Return the PRD core rule's problems for the session's known IDs.
       Expected outcome: Citing D-999 is rejected.
    """
    raise NotImplementedError("S4.6: v_prd_core")


def v_prd_narrative(out: PRDNarrative, deps: Deps) -> list[str]:
    """Return problems with the PRD narrative.

    Problem piece: C1 and C4: objectives sourced.

    Why it matters: Objectives are what approvers sign for, so they must cite real
                    sources. An objective with an invented source would put a
                    success measure in front of approvers that nobody ever agreed.

    What: The narrative rules, using the session's known IDs. Called as
          v_prd_narrative(out: PRDNarrative, deps: Deps) and returns list[str].

    Spec: S4.6 | Ticket: 05 | Traces to: I3

    Build steps:
    1. Task: Return the narrative rule's problems for the session's known IDs.
       Expected outcome: An objective citing D-999 is rejected.
    """
    raise NotImplementedError("S4.6: v_prd_narrative")


def v_spec(out: Spec, deps: Deps) -> list[str]:
    """Return problems with a spec.

    Problem piece: C1 and C4: coverage matches the PRD.

    Why it matters: The spec must address every requirement and nothing else,
                    measured against this session's PRD IDs.

    What: The spec rule, using the session's PRD IDs. Called as v_spec(out: Spec,
          deps: Deps) and returns list[str].

    Spec: S4.6 | Ticket: 06 | Traces to: I1

    Build steps:
    1. Task: Return the spec rule's problems for the session's PRD IDs.
       Expected outcome: A spec missing FR-02 is rejected.
    """
    raise NotImplementedError("S4.6: v_spec")


def v_tickets(out: TicketPlan, deps: Deps) -> list[str]:
    """Return problems with a ticket plan.

    Problem piece: C1 and C4: the S3.6 rules for this session.

    Why it matters: Tickets must target this session's features and cover this
                    session's requirements. Checking against another session's
                    features would let tickets target capabilities this PRD never
                    approved.

    What: The ticket rule, using the session's features and PRD IDs. Called as
          v_tickets(out: TicketPlan, deps: Deps) and returns list[str].

    Spec: S4.6 | Ticket: 07 | Traces to: I15

    Build steps:
    1. Task: Return the ticket rule's problems for the session's features and PRD
             IDs.
       Expected outcome: A plan missing FR-03 is rejected.
    """
    raise NotImplementedError("S4.6: v_tickets")


def post_explore(out: CurrentStateMap, deps: Deps) -> CurrentStateMap:
    """Record which files a map was built from.

    Problem piece: C2: the map cites its evidence.

    Why it matters: Reviewers trust a map more when they can see which files it
                    rests on. Developers reviewing the map can then open the same
                    files and check the agent's reading for themselves.

    What: Sets the map's files_read to the sorted, de-duplicated files read during
          the call. Called as post_explore(out: CurrentStateMap, deps: Deps) and
          returns CurrentStateMap.

    Spec: S4.6 | Ticket: 09 | Traces to: I1

    Build steps:
    1. Task: Set files_read to the unique files read, sorted, and return the map.
       Expected outcome: A file read twice appears once.
    """
    raise NotImplementedError("S4.6: post_explore")
