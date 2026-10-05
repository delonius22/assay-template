"""Hold run-time dependencies that LangGraph injects into every node.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C1 Trustworthy output and C5 Durable sessions. Nodes need
settings, the store, and models, none of which may be saved in a checkpoint. This
file owns those dependencies and their helpers; it never runs a workflow step.

Why this comes now: The call loop (13), client (15), state (17), and store exist.
Nodes (21 to 26) take this as runtime.context.

Build order: Step 20 of 33.
Previous: src/assay/render/markdown.py (step 19), which writes every markdown
artifact, the PDF, and the tracker prompt.
Next: src/assay/graph/nodes/shared.py (step 21), which holds the helpers several
stages share.

Build these in order:
    1. AppContext: the context class.
    2. ctx: every node calls it first.

Depends on:
    assay.domain.models: DodItem, GlossaryTerm, ResponseSheet. Shared records.
    assay.graph.state: AssayState. The session the helpers read.
    assay.llm.call: AgentSpec, Limits, call. Running agents.
    assay.llm.client: make_model. Real clients.
    assay.llm.tools: Deps, roots_from. Validator and tool context.
    assay.settings: Settings. Everything configurable.
    Standard library: logging, uuid, dataclasses, pathlib, collections.abc.
    Third-party: langchain-core, langgraph, pydantic.

Depended on by:
    assay.graph.nodes: every node. assay.api.app and assay.api.runner: built at
    startup.

Spec coverage: S5.2 | Traces to: I1, I6, I11
"""

import logging
import uuid
from collections.abc import Callable
from dataclasses import dataclass, field
from pathlib import Path

from langchain_core.language_models import BaseChatModel
from langgraph.store.base import BaseStore
from pydantic import BaseModel

from assay.domain.models import DodItem, GlossaryTerm, ResponseSheet
from assay.graph.state import AssayState
from assay.llm.call import AgentSpec, Limits, call
from assay.llm.client import make_model
from assay.llm.tools import Deps, roots_from
from assay.settings import Settings

log = logging.getLogger("assay.calls")


@dataclass
class AppContext:
    """Settings, the store, and model access for one running app.

    Problem piece: C1 and C5: dependencies nodes need but checkpoints must not hold.

    Why it matters: LangGraph saves state, not context, so the context is passed on
                    every invoke including resumes. Keeping model clients and the
                    store here lets nodes be plain, testable functions.

    What: Settings, store, an optional test model factory, call limits, and a
          per-role model cache.

    Spec: S5.2 | Ticket: — | Traces to: —
    """

    settings: Settings
    store: BaseStore
    get_model: Callable[[str], BaseChatModel] | None = None
    limits: Limits | None = None
    models_cache: dict[str, BaseChatModel] = field(default_factory=dict, repr=False)

    def __post_init__(self) -> None:
        """Derive call limits from settings when none are given.

        Problem piece: C1: every call bounded by the configured limits.

        Why it matters: Tests inject their own limits; production derives them from
                        settings so operators control cost. Without derived limits a
                        production call would run with test defaults, and a
                        misbehaving agent could exceed the operator's budget.

        What: When no limits were given, builds them from the settings' cache mode,
              steps, rejections, and retry values.

        Spec: S5.2 | Ticket: 02 | Traces to: I11

        Build steps:
        1. Task: When no limits were given, build them from the settings: cache
                 mode, max steps, max output retries as max rejections, and the
                 retry attempts, base, and cap.
           Expected outcome: A context without limits uses the configured max steps.
        """
        raise NotImplementedError("S5.2: __post_init__")

    def model_for(self, role: str) -> BaseChatModel:
        """Return the chat model for a role.

        Problem piece: C1: the right model for each task.

        Why it matters: Roles can use different models; creating each client once
                        avoids rebuilding connections every call. Tests swap in a
                        scripted model here, which is how the whole pipeline runs
                        without a gateway or credentials (I13).

        What: The test factory's model when set; otherwise one cached gateway client
              per role. Called as model_for(role: str) and returns BaseChatModel.

        Spec: S5.2 | Ticket: 02 | Traces to: A1

        Build steps:
        1. Task: Use the test factory when present; otherwise create the role's
                 client once from its configured model and reuse it.
           Expected outcome: Two calls for one role return the same client.
        """
        raise NotImplementedError("S5.2: model_for")

    def deps(self, s: AssayState) -> Deps:
        """Return validator and tool context for a session.

        Problem piece: C1: rules see this session's IDs; tools see only allowed
                       roots.

        Why it matters: Validators must check against this session's known IDs,
                        never another session's. A validator given another session's
                        IDs would accept sources that do not exist in this session's
                        record.

        What: Deps with the allowed roots, known IDs, PRD IDs, and feature IDs of
              the session.

        Spec: S5.2 | Ticket: 02 | Traces to: I3, I10

        Build steps:
        1. Task: Build Deps from the configured code roots and the session's known,
                 PRD, and feature IDs.
           Expected outcome: A session citing D-001 has D-001 in known IDs.
        """
        raise NotImplementedError("S5.2: deps")

    def run(self, spec: AgentSpec, dynamic: str, s: AssayState) -> BaseModel:
        """Run an agent and record the call.

        Problem piece: C1: every agent call validated, logged, and attributable.

        Why it matters: Recording every call in the store gives auditors the trail
                        and proves caching works; logging must never include prompt
                        text or secrets (I9).

        What: Runs the call loop, saves the call record under ('calls', slug) with
              the stage, logs one line, returns the output.

        Spec: S5.2 | Ticket: 02 | Traces to: I1, I11

        Build steps:
        1. Task: Run the call loop with the role's model, the session's deps, the
                 limits, and the model name.
           Expected outcome: Validated output is returned.
        2. Task: Save the record under the session's calls namespace with a random
                 key and the current stage, and log one line of counters with no
                 prompt text.
           Expected outcome: The store holds one record per call.
        """
        raise NotImplementedError("S5.2: run")

    def folder(self, s: AssayState) -> Path:
        """Return the session's output folder.

        Problem piece: C4: one folder per session's files.

        Why it matters: Downloads are served only from this folder, so its location
                        must be computed one way.

        What: The artifacts directory, then 'initiatives', then the slug. Called as
              folder(s: AssayState) and returns Path.

        Spec: S5.2 | Ticket: 02 | Traces to: C1

        Build steps:
        1. Task: Return the artifacts directory joined with 'initiatives' and the
                 slug.
           Expected outcome: Slug 'alerts' maps to <artifacts>/initiatives/alerts.
        """
        raise NotImplementedError("S5.2: folder")

    def team_dod(self) -> list[DodItem]:
        """Return the shared team Definition of Done.

        Problem piece: C6: every session starts from the team's standard.

        Why it matters: The team agrees its standard once; every later session must
                        read the same one. If each session kept its own copy, a team
                        that changed its standard would see old sessions and new
                        sessions disagree.

        What: Items stored under ('team', 'dod') key 'current', or an empty list.
              Called as team_dod() and returns list[DodItem].

        Spec: S5.2 | Ticket: 04 | Traces to: I2

        Build steps:
        1. Task: Read key 'current' from the team DoD namespace and return its items
                 as DodItem, or an empty list when absent.
           Expected outcome: A fresh store returns an empty list.
        """
        raise NotImplementedError("S5.2: team_dod")

    def save_team_dod(self, items: list[DodItem], by: str) -> None:
        """Save the team Definition of Done.

        Problem piece: C6: the agreed standard shared by later sessions.

        Why it matters: Saving who agreed it gives the standard an owner for audit.
                        Saving it outside any one session is what lets the second
                        initiative skip straight to additions.

        What: Stores the items and the agreeing user under ('team', 'dod') key
              'current'. Called as save_team_dod(items: list[DodItem], by: str) and
              returns None.

        Spec: S5.2 | Ticket: 04 | Traces to: I6

        Build steps:
        1. Task: Store the items as plain data and the user under key 'current'.
           Expected outcome: The next session reads the same items.
        """
        raise NotImplementedError("S5.2: save_team_dod")

    def glossary(self) -> list[GlossaryTerm]:
        """Return the shared glossary.

        Problem piece: C4: one vocabulary across sessions.

        Why it matters: Terms resolved in one session must be visible in every
                        other, or documents drift apart.

        What: Every term stored under ('team', 'glossary') as GlossaryTerm values,
              shared by every session in the deployment.

        Spec: S5.2 | Ticket: 02 | Traces to: C1

        Build steps:
        1. Task: Read every record in the team glossary namespace as GlossaryTerm.
           Expected outcome: A saved term is returned.
        """
        raise NotImplementedError("S5.2: glossary")

    def save_terms(self, terms: list[GlossaryTerm]) -> None:
        """Save glossary terms.

        Problem piece: C4: new or changed terms shared at once.

        Why it matters: Keying by the lowercase term makes a redefinition replace
                        the old one instead of duplicating it.

        What: Stores each term under its lowercase name in ('team', 'glossary'),
              replacing any earlier definition of the same term.

        Spec: S5.2 | Ticket: 02 | Traces to: C1

        Build steps:
        1. Task: Store each term under its lowercase name in the team glossary
                 namespace.
           Expected outcome: Saving 'Threshold' twice leaves one record.
        """
        raise NotImplementedError("S5.2: save_terms")

    def responses(self, slug: str, round_no: int) -> list[ResponseSheet]:
        """Return a round's questionnaire responses.

        Problem piece: C6: developers' answers for reconciliation.

        Why it matters: Answers arrive through the web form at any time; reading
                        them from the store decouples submission from the run.

        What: Every sheet stored under ('responses', slug, 'r<round>'). Called as
              responses(slug: str, round_no: int) and returns list[ResponseSheet].

        Spec: S5.2 | Ticket: 08 | Traces to: I12

        Build steps:
        1. Task: Read every record in the session's round namespace as
                 ResponseSheet.
           Expected outcome: One developer's sheet for round 1 is returned.
        """
        raise NotImplementedError("S5.2: responses")


def ctx(runtime: object) -> AppContext:
    """Return the AppContext from a node's runtime.

    Problem piece: C5: a forgotten context fails with its cause named.

    Why it matters: The context is passed on every invoke but never saved. A resume
                    without it would otherwise fail deep inside a node with an
                    unhelpful error.

    What: The runtime's context when it is an AppContext; otherwise a RuntimeError
          naming the cause. Called as ctx(runtime: object) and returns AppContext.

    Spec: S5.2 | Ticket: 02 | Traces to: I6

    Raises:
        RuntimeError: 'No AppContext. Pass context=AppContext(...) on every invoke,
        including resumes; LangGraph does not checkpoint it.'

    Build steps:
    1. Task: Return the runtime's context when it is an AppContext; otherwise raise
             the RuntimeError with the message above.
       Expected outcome: A runtime with no context raises that message.
    """
    raise NotImplementedError("S5.2: ctx")
