"""Run-time dependencies, injected by LangGraph as runtime.context.

Passed on every invoke, resumes included, and never checkpointed.
Store namespaces (SPECS ## Data shapes): ("team","dod"), ("team","glossary"),
("responses", slug, "r<N>"), ("calls", slug).
"""
import logging
import uuid
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from langchain_core.language_models import BaseChatModel
from langgraph.store.base import BaseStore
from pydantic import BaseModel

from ..domain.models import DodItem, GlossaryTerm, ResponseSheet
from ..llm.call import AgentSpec, Limits, call
from ..llm.client import make_model
from ..llm.tools import Deps, roots_from
from ..settings import Settings
from .state import AssayState

log = logging.getLogger("assay.calls")


@dataclass
class AppContext:
    settings: Settings
    store: BaseStore
    get_model: Callable[[str], BaseChatModel] | None = None    # tests inject a fake
    limits: Limits | None = None
    models_cache: dict[str, BaseChatModel] = field(default_factory=dict, repr=False)

    def __post_init__(self):
        """Derive call limits from settings when not given. (Complete.)"""
        if self.limits is None:
            s = self.settings
            self.limits = Limits(cache_mode=s.cache_mode, max_steps=s.max_steps,
                                 max_rejections=s.max_output_retries, retry_attempts=s.retry_attempts,
                                 retry_base_s=s.retry_base_s, retry_cap_s=s.retry_cap_s)

    def model_for(self, role: str) -> BaseChatModel:
        """The chat model for a role.

        Spec: S5.2 | Ticket: 02 | Traces to: A1

        Build steps:
        1. Task: If `self.get_model`, return `self.get_model(role)`.
           Expected outcome: tests get their fake.
        2. Task: If `role not in self.models_cache`, set
           `self.models_cache[role] = make_model(self.settings.models[role], self.settings)`.
           Expected outcome: one client per role, reused.
        3. Task: Return `self.models_cache[role]`.
           Expected outcome: the role's model.
        """
        raise NotImplementedError("S5.2")

    def deps(self, s: AssayState) -> Deps:
        """Per-call dependencies for tools and validators.

        Spec: S5.2 | Ticket: 02 | Traces to: I3, I10

        Build steps:
        1. Task: Return `Deps(roots=roots_from(self.settings.code_roots), known_ids=s.known_ids(),
           prd_ids=s.prd_ids, feature_ids=s.feature_ids)`.
           Expected outcome: validators see this session's IDs; tools see only allowed roots.
        """
        raise NotImplementedError("S5.2")

    def run(self, spec: AgentSpec, dynamic: str, s: AssayState) -> BaseModel:
        """Call an agent and record the call for audit and usage.

        Spec: S5.2 | Ticket: 02 | Traces to: I1, I11

        Build steps:
        1. Task: `out, rec = call(self.model_for(spec.role), spec, dynamic, self.deps(s), self.limits,
           model_name=self.settings.models.get(spec.role, ""))`.
           Expected outcome: validated output and its record.
        2. Task: `self.store.put(("calls", s.slug), uuid.uuid4().hex, {**rec.dict(), "stage": s.stage})`.
           Expected outcome: every call is in the store with tokens, cache reads, retries, rejections.
        3. Task: `log.info("call %s/%s steps=%d in=%d cached=%d out=%d rejections=%d retries=%d", s.slug, spec.name,
           rec.steps, rec.input_tokens, rec.cache_read_tokens, rec.output_tokens, rec.rejections, rec.transient_retries)`.
           Expected outcome: one log line per call; no prompt text, no secrets (I9).
        4. Task: Return `out`.
           Expected outcome: the node gets typed output.
        """
        raise NotImplementedError("S5.2")

    def folder(self, s: AssayState) -> Path:
        """Spec: S5.2 | Ticket: 02 | Traces to: C1

        Build steps:
        1. Task: Return `self.settings.artifacts_dir / "initiatives" / s.slug`.
           Expected outcome: one folder per session for its files.
        """
        raise NotImplementedError("S5.2")

    def team_dod(self) -> list[DodItem]:
        """The shared team Definition of Done, or [] when none is saved.

        Spec: S5.2 | Ticket: 04 | Traces to: I2

        Build steps:
        1. Task: `item = self.store.get(("team", "dod"), "current")`.
           Expected outcome: the saved standard or None.
        2. Task: Return `[DodItem(**d) for d in item.value["items"]] if item else []`.
           Expected outcome: typed items.
        """
        raise NotImplementedError("S5.2")

    def save_team_dod(self, items: list[DodItem], by: str) -> None:
        """Spec: S5.2 | Ticket: 04 | Traces to: I6

        Build steps:
        1. Task: `self.store.put(("team", "dod"), "current", {"items": [i.model_dump() for i in items], "by": by})`.
           Expected outcome: every later session reads this standard.
        """
        raise NotImplementedError("S5.2")

    def glossary(self) -> list[GlossaryTerm]:
        """Spec: S5.2 | Ticket: 02 | Traces to: C1

        Build steps:
        1. Task: Return `[GlossaryTerm(**i.value) for i in self.store.search(("team", "glossary"), limit=1000)]`.
           Expected outcome: the shared glossary.
        """
        raise NotImplementedError("S5.2")

    def save_terms(self, terms: list[GlossaryTerm]) -> None:
        """Spec: S5.2 | Ticket: 02 | Traces to: C1

        Build steps:
        1. Task: For each `t`, `self.store.put(("team", "glossary"), t.term.lower(), t.model_dump())`.
           Expected outcome: one record per term; a re-definition replaces the old one.
        """
        raise NotImplementedError("S5.2")

    def responses(self, slug: str, round_no: int) -> list[ResponseSheet]:
        """Spec: S5.2 | Ticket: 08 | Traces to: I12

        Build steps:
        1. Task: `items = self.store.search(("responses", slug, f"r{round_no}"), limit=500)`.
           Expected outcome: one record per respondent for this round.
        2. Task: Return `[ResponseSheet(**i.value) for i in items]`.
           Expected outcome: typed, already-validated responses.
        """
        raise NotImplementedError("S5.2")


def ctx(runtime) -> AppContext:
    """The AppContext from a node's runtime, with a clear error when missing.

    Spec: S5.2 | Ticket: 02 | Traces to: I6

    Build steps:
    1. Task: `c = getattr(runtime, "context", None)`.
       Expected outcome: the injected context or None.
    2. Task: If `not isinstance(c, AppContext)`, raise `RuntimeError("No AppContext. Pass context=AppContext(...)
       on every invoke, including resumes; LangGraph does not checkpoint it.")`.
       Expected outcome: a forgotten context fails with the cause named.
    3. Task: Return `c`.
       Expected outcome: nodes read settings, store, and models from it.
    """
    raise NotImplementedError("S5.2")
