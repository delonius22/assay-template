"""Session state: everything about one initiative, checkpointed after every step (I6).
Typed data only; clients and settings live in AppContext."""
from typing import Literal

from pydantic import BaseModel, Field

from ..domain.ids import live
from ..domain.models import (Brief, CurrentStateMap, DodItem, GlossaryTerm, LogEntry, PRDCore,
                             PRDNarrative, Question, Questionnaire, ResponseSheet, Seams, Spec,
                             Ticket, Turn, Uncovered)

Stage = Literal["Intake", "Definition of Done", "PRD", "PRD review", "Spec", "Tickets", "Done"]


class AssayState(BaseModel):
    slug: str
    title: str
    pm: str
    mode: Literal[1, 2, 3]
    created_by: str = ""
    stage: Stage = "Intake"

    # intake
    brief: Brief | None = None
    brief_issues: list[str] = Field(default_factory=list)
    current_map: CurrentStateMap | None = None
    log: list[LogEntry] = Field(default_factory=list)
    glossary: list[GlossaryTerm] = Field(default_factory=list)
    transcript: list[Turn] = Field(default_factory=list)
    pending: Question | None = None
    challenge: str | None = None
    agenda: list[str] = Field(default_factory=list)

    # mode 3
    questionnaire: Questionnaire | None = None
    q_round: int = 0
    q_ids: list[str] = Field(default_factory=list)
    responses: list[ResponseSheet] = Field(default_factory=list)
    new_responses: list[ResponseSheet] = Field(default_factory=list)
    reconcile_gaps: list[str] = Field(default_factory=list)

    # Definition of Done
    dod_phase: Literal["team", "additions", "done"] = "team"
    dod_team: list[DodItem] = Field(default_factory=list)
    dod_additions: list[DodItem] = Field(default_factory=list)
    dod_transcript: list[Turn] = Field(default_factory=list)
    dod_pending: Question | None = None
    dod_agenda: list[str] = Field(default_factory=list)
    dod_retired: list[str] = Field(default_factory=list)

    # PRD
    prd_core: PRDCore | None = None
    prd_narrative: PRDNarrative | None = None
    prd_version: str = "0.1"
    prd_feedback: str = ""
    review_error: str = ""
    approved_by: str = ""
    doc_id: str = ""
    fr_ids: list[str] = Field(default_factory=list)
    nfr_ids: list[str] = Field(default_factory=list)

    # spec and tickets
    seams: Seams | None = None
    seams_feedback: str = ""
    spec: Spec | None = None
    tickets: list[Ticket] = Field(default_factory=list)
    uncovered: list[Uncovered] = Field(default_factory=list)
    ticket_feedback: str = ""                 # D4: reviewer changes before export
    files: list[str] = Field(default_factory=list)

    @property
    def feature_ids(self) -> set[str]:
        """Every feature ID in the PRD.

        Spec: S5.1 | Ticket: 02 | Traces to: I2

        Build steps:
        1. Task: Return `set()` when `self.prd_core is None`.
           Expected outcome: no PRD yet, no features.
        2. Task: Return `{f.id for st in self.prd_core.stories for f in st.features}`.
           Expected outcome: features across all stories.
        """
        raise NotImplementedError("S5.1")

    @property
    def prd_ids(self) -> set[str]:
        """Every FR- and NFR- ID.

        Spec: S5.1 | Ticket: 02 | Traces to: I3

        Build steps:
        1. Task: Return `set(self.fr_ids) | set(self.nfr_ids)`.
           Expected outcome: the requirement IDs rules check against.
        """
        raise NotImplementedError("S5.1")

    def known_ids(self) -> set[str]:
        """IDs a PRD may cite: every log entry and every questionnaire ID.

        Spec: S5.1 | Ticket: 02 | Traces to: I3

        Build steps:
        1. Task: Return `{e.id for e in self.log} | set(self.q_ids)`.
           Expected outcome: superseded entries stay citable for traceability.
        """
        raise NotImplementedError("S5.1")


def log_view(s: AssayState) -> str:
    """Compact, current view of the log for agent prompts.

    Spec: S5.1 | Ticket: 02 | Traces to: I3

    Build steps:
    1. Task: For each `e` in `live(s.log)`, build flags: f"scope:{e.scope_side}" when set,
       f"path:{e.journey_path}" when set, "rollback" when `e.covers_rollback`, f"metric:{e.metric.target}" when set.
       Expected outcome: the agent sees the typed flags the gate checks.
    2. Task: Join `[e.priority or "", e.status or "", *flags]` (non-empty parts) with ", " into `extra`; build
       f"{e.id} [{e.area}] {e.title}: {e.detail} (source: {e.source}" + ("; " + extra if extra else "") + ")".
       Expected outcome: one line per live entry.
    3. Task: Return `"\\n".join(rows) or "(empty)"`.
       Expected outcome: never an empty string in a prompt.
    """
    raise NotImplementedError("S5.1")
