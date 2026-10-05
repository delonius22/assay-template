"""Define the session state that is checkpointed after every step.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C5 Durable sessions. A paused session is only as complete as
its saved state. This file defines that state and small views of it; it holds no
clients or settings, because state is saved as data.

Why this comes now: Persistence (step 16) can save it; renderers (18, 19) and nodes
(21 to 26) read it.

Build order: Step 17 of 33.
Previous: src/assay/store/persistence.py (step 16), which opens Postgres or SQLite
checkpoints and the shared store.
Next: src/assay/render/csv_export.py (step 18), which writes the tickets CSV rows.

Build these in order:
    1. AssayState: the state itself.
    2. log_view: a view over the state.

Depends on:
    assay.domain.ids: live. The current log view.
    assay.domain.models: every field type.
    Standard library: typing.
    Third-party: pydantic.

Depended on by:
    assay.graph.context, assay.graph.nodes, assay.graph.build,
    assay.render.markdown, assay.api.

Spec coverage: S5.1 | Traces to: I6
"""

from typing import Literal

from pydantic import BaseModel, Field

from assay.domain.ids import live
from assay.domain.models import (
    Brief,
    CurrentStateMap,
    DodItem,
    GlossaryTerm,
    LogEntry,
    PRDCore,
    PRDNarrative,
    Question,
    Questionnaire,
    ResponseSheet,
    Seams,
    Spec,
    Ticket,
    Turn,
    Uncovered,
)

type Stage = Literal[
    "Intake", "Definition of Done", "PRD", "PRD review", "Spec", "Tickets", "Done"
]  # S5.3


class AssayState(BaseModel):
    """Everything about one session.

    Problem piece: C5: the single value LangGraph saves after every step.

    Why it matters: Anything not in this state is lost at a pause, so every fact a
                    later step needs lives here. It must be plain data because it is
                    serialized; clients and settings live in the runtime context.

    What: Identity and stage, intake, mode 3, Definition of Done, PRD, spec, and
          ticket fields.

    Spec: S5.1 | Ticket: — | Traces to: —
    """

    slug: str
    title: str
    pm: str
    mode: Literal[1, 2, 3]
    created_by: str = ""
    stage: Stage = "Intake"
    brief: Brief | None = None
    brief_issues: list[str] = Field(default_factory=list)
    current_map: CurrentStateMap | None = None
    log: list[LogEntry] = Field(default_factory=list)
    glossary: list[GlossaryTerm] = Field(default_factory=list)
    transcript: list[Turn] = Field(default_factory=list)
    pending: Question | None = None
    challenge: str | None = None
    agenda: list[str] = Field(default_factory=list)
    questionnaire: Questionnaire | None = None
    q_round: int = 0
    q_ids: list[str] = Field(default_factory=list)
    responses: list[ResponseSheet] = Field(default_factory=list)
    new_responses: list[ResponseSheet] = Field(default_factory=list)
    reconcile_gaps: list[str] = Field(default_factory=list)
    dod_phase: Literal["team", "additions", "done"] = "team"
    dod_team: list[DodItem] = Field(default_factory=list)
    dod_additions: list[DodItem] = Field(default_factory=list)
    dod_transcript: list[Turn] = Field(default_factory=list)
    dod_pending: Question | None = None
    dod_agenda: list[str] = Field(default_factory=list)
    dod_retired: list[str] = Field(default_factory=list)
    prd_core: PRDCore | None = None
    prd_narrative: PRDNarrative | None = None
    prd_version: str = "0.1"
    prd_feedback: str = ""
    review_error: str = ""
    approved_by: str = ""
    doc_id: str = ""
    fr_ids: list[str] = Field(default_factory=list)
    nfr_ids: list[str] = Field(default_factory=list)
    seams: Seams | None = None
    seams_feedback: str = ""
    spec: Spec | None = None
    tickets: list[Ticket] = Field(default_factory=list)
    uncovered: list[Uncovered] = Field(default_factory=list)
    ticket_feedback: str = ""
    files: list[str] = Field(default_factory=list)

    def feature_ids(self) -> set[str]:
        """Return every feature ID in the PRD.

        Problem piece: C4: tickets may target only approved features.

        Why it matters: The ticket rules need the set of real features; before a PRD
                        exists there are none.

        What: The IDs of every feature under every story, or an empty set before the
              PRD.

        Spec: S5.1 | Ticket: 02 | Traces to: I2

        Build steps:
        1. Task: Return no IDs before the PRD core exists, otherwise every feature
                 ID across all stories.
           Expected outcome: A PRD with features F-01 and F-02 returns both.
        """
        raise NotImplementedError("S5.1: feature_ids")

    def prd_ids(self) -> set[str]:
        """Return every FR and NFR ID.

        Problem piece: C4: the requirement IDs rules check against.

        Why it matters: Spec coverage and ticket coverage are both measured against
                        this set. Computing it in one place keeps the spec gate and
                        the ticket gate measuring coverage against exactly the same
                        set.

        What: The union of the functional and non-functional requirement IDs. Called
              as prd_ids() and returns set[str].

        Spec: S5.1 | Ticket: 02 | Traces to: I3

        Build steps:
        1. Task: Return the union of the FR and NFR IDs.
           Expected outcome: FR-01 and NFR-01 are both included.
        """
        raise NotImplementedError("S5.1: prd_ids")

    def known_ids(self) -> set[str]:
        """Return every ID a PRD may cite.

        Problem piece: C4: sources that really exist (I3).

        Why it matters: A requirement may cite any log entry, superseded or not, and
                        any questionnaire ID; anything else is invented.

        What: Every log entry ID, superseded or not, plus every questionnaire ID,
              including follow-ups and confirmations.

        Spec: S5.1 | Ticket: 02 | Traces to: I3

        Build steps:
        1. Task: Return every log entry ID together with every questionnaire ID.
           Think about: Why do superseded entries stay citable?
           Expected outcome: D-001 and Q-01 are both included.
        """
        raise NotImplementedError("S5.1: known_ids")


def log_view(s: AssayState) -> str:
    """Return a compact, current view of the log for prompts.

    Problem piece: C2: agents see what was decided, with the flags the gate reads.

    Why it matters: Agents get the state's view, not a growing chat history; it must
                    be short and show the typed flags, or the agent cannot tell why
                    the gate still fails.

    What: One line per live entry: ID, area, title, detail, source, and its
          priority, status, and flags.

    Spec: S5.1 | Ticket: 02 | Traces to: I3

    Build steps:
    1. Task: Write one line per live entry: '<id> [<area>] <title>: <detail>
             (source: <source>; <extras>)', where extras list priority, status,
             scope:<side>, path:<path>, rollback, and metric:<target> when present.
       Expected outcome: An out-of-scope entry shows 'scope:out'.
    2. Task: Return '(empty)' when there are no live entries.
       Expected outcome: An empty log gives '(empty)'.
    """
    raise NotImplementedError("S5.1: log_view")
