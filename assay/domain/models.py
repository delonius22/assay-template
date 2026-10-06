"""Typed domain models: the single source of truth.

Every agent returns one of these, every rule checks one of these, and every
file (markdown, PDF, CSV) is generated from these. Nothing is parsed back
from files. The model never assigns IDs; code does.

Hierarchy: Story (a business goal) -> Feature (a capability that delivers
it) -> Ticket (a buildable, testable slice of a feature).
"""

import re
from datetime import datetime, timezone
from typing import Literal

from pydantic import BaseModel, Field, field_validator

Area = Literal["Problem", "Outcome", "Users", "Scope", "Journeys", "Data", "Integrations",
               "Non-functional", "Regulation", "Rollout", "Delivery"]
EntryType = Literal["D", "A", "R", "Q", "C"]
Priority = Literal["Blocking", "Important", "Useful"]
MoSCoW = Literal["Must have", "Should have", "Could have", "Won't have"]
Role = Literal["Developer", "Architecture", "Data", "Security", "Operations", "QA"]
SpecRef = Literal["modules", "interfaces", "data", "key_flows", "integrations", "security",
                  "nfr_design", "observability", "rollout", "testing"]
DoDLevel = Literal["ticket", "feature", "story", "release"]

USER_STORY = re.compile(r"^As an? .+?, I want .+?, so that .+", re.I | re.S)


def now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


class Metric(BaseModel):
    measure: str
    baseline: str
    target: str
    by_when: str


class NewEntry(BaseModel):
    """A log entry proposed by an agent. Code assigns the ID."""
    type: EntryType = Field(description="D decision, A assumption, R risk, Q open question, C correction")
    title: str = Field(description="One line, plain language")
    area: Area
    detail: str
    source: str = Field(description="Who said it and their role, e.g. 'Priya (Lead Developer)'")
    priority: Priority | None = Field(None, description="Required for Q entries")
    owner: str | None = Field(None, description="Role that owns resolving or validating it")
    status: Literal["Open", "Closed", "Parked", "Accepted as risk"] | None = None
    positions: list[str] = Field(default_factory=list, description="For disagreements: 'Name (role): position'")
    # Typed flags the intake gate checks, instead of searching the text.
    scope_side: Literal["in", "out"] | None = Field(None, description="Required for Scope entries")
    journey_path: Literal["happy", "failure"] | None = Field(None, description="Required for Journeys entries")
    metric: Metric | None = Field(None, description="For Outcome entries that set a measurable target")
    covers_rollback: bool = Field(False, description="Rollout entries: true if it states how to roll back")


class LogEntry(NewEntry):
    id: str
    superseded_by: list[str] = Field(default_factory=list)
    recorded_at: str = Field(default_factory=now)


class GlossaryTerm(BaseModel):
    term: str
    definition: str = Field(description="One sentence: what it IS")
    avoid: list[str] = Field(default_factory=list)


class Question(BaseModel):
    text: str = Field(description="Exactly one question")
    recommended_answer: str
    reason: str = Field(description="One line: why you recommend it")
    area: Area


class GrillTurn(BaseModel):
    recorded: list[NewEntry] = Field(default_factory=list, description="Entries from the latest answer")
    supersedes: list[str] = Field(default_factory=list, description="IDs of entries the new ones replace")
    glossary_updates: list[GlossaryTerm] = Field(default_factory=list)
    challenge: str | None = Field(None, description="Plain pushback if the latest answer was weak or risky")
    next_question: Question | None = None
    done: bool = Field(False, description="True only when every area is covered")


class Turn(BaseModel):
    """A question and the human answer, with who answered (for audit)."""
    question: str
    recommended: str
    answer: str
    user: str
    at: str = Field(default_factory=now)



class CurrentStateMap(BaseModel):
    components: list[str]
    data_flow: str
    data_stores: list[str]
    tests: str = Field(description="Existing tests in this area, and gaps")
    flags_and_jobs: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list, description="Things the code did not settle")
    files_read: list[str] = Field(default_factory=list)


class Brief(BaseModel):
    ask: str
    why: str
    outcome: str
    known_steps: str = ""
    constraints: str = ""


class BriefCritique(BaseModel):
    ready: bool
    issues: list[str] = Field(default_factory=list, description="What the PM must fix, one per item")


class FollowUp(BaseModel):
    condition: str
    text: str


class QItem(BaseModel):
    text: str
    owner_role: Role
    priority: Priority
    why_it_matters: str
    proposed_answer: str
    reason: str
    depends_on: list[int] = Field(default_factory=list, description="1-based positions of earlier questions")
    follow_ups: list[FollowUp] = Field(default_factory=list)
    area: Area


class Confirmation(BaseModel):
    statement: str
    source: str = Field(description="File or document where this was found")


class Questionnaire(BaseModel):
    summary: str = Field(description="One paragraph on what the questions cover")
    questions: list[QItem] = Field(min_length=1, max_length=30)
    confirmations: list[Confirmation] = Field(default_factory=list)


class Answer(BaseModel):
    question_id: str
    response: Literal["Confirm", "Correct", "Don't know", "No answer"]
    text: str = ""


class ResponseSheet(BaseModel):
    """One developer's answers, submitted through the web form."""
    respondent: str
    role: str
    round: int
    answers: list[Answer]
    comments: str = ""
    submitted_at: str = Field(default_factory=now)


class Reconciliation(BaseModel):
    recorded: list[NewEntry] = Field(description="Decisions, assumptions, risks, conflicts as entries")
    contradictions: list[str] = Field(default_factory=list)
    blocking_gaps: list[str] = Field(default_factory=list)
    follow_up_questions: list[QItem] = Field(default_factory=list, max_length=8)



class DodItemDraft(BaseModel):
    level: DoDLevel = Field(description="ticket: every ticket; feature: once per feature; "
                                        "story: once per story; release: once per release")
    statement: str = Field(description="A verifiable condition, under about 15 words")
    category: str
    how_verified: str
    evidence: str = Field(description="The proof that exists afterwards, and where")
    verified_by: str = Field(description="A named role, never 'the team'")
    source: str
    mandated: str = ""
    needs_team_confirmation: bool = False


class DodItem(DodItemDraft):
    id: str


class DodTurn(BaseModel):
    agreed: list[DodItemDraft] = Field(default_factory=list)
    remove: list[str] = Field(default_factory=list, description="IDs of agreed items to withdraw")
    challenge: str | None = None
    next_question: Question | None = None
    done: bool = False


class FeatureDraft(BaseModel):
    id: str = Field(pattern=r"^F-\d{2}$", description="F-01, F-02... numbered across all stories")
    name: str = Field(description="A business capability, not a component")
    summary: str


class StoryDraft(BaseModel):
    id: str = Field(pattern=r"^S-\d{2}$")
    text: str = Field(description="As a <actor>, I want <goal>, so that <benefit>.")
    features: list[FeatureDraft] = Field(min_length=1)

    @field_validator("text")
    @classmethod
    def _shape(cls, v: str) -> str:
        if not USER_STORY.match(v.strip()):
            raise ValueError("must read 'As a…, I want…, so that…'")
        return v.strip()


class Requirement(BaseModel):
    text: str = Field(description="Testable, uses must/should/may")
    priority: MoSCoW
    feature_id: str
    sources: list[str] = Field(min_length=1, description="Session log or questionnaire IDs")


class NFR(BaseModel):
    area: str
    text: str
    priority: MoSCoW
    sources: list[str] = Field(min_length=1)


class PRDCore(BaseModel):
    stories: list[StoryDraft] = Field(min_length=1, max_length=8)
    functional: list[Requirement] = Field(min_length=1)
    non_functional: list[NFR] = Field(default_factory=list)


class Objective(BaseModel):
    objective: str
    measure: str
    baseline: str
    target: str
    by_when: str
    source: str


class Stakeholder(BaseModel):
    group: str
    interest: str
    role: Literal["Accountable", "Responsible", "Consulted", "Informed"]


class DataItem(BaseModel):
    data: str
    classification: str
    purpose: str
    retention: str
    shared_with: str
    source: str


class RiskControl(BaseModel):
    area: str
    consideration: str
    owner: str
    status: str = "Compliance to confirm"


class PRDNarrative(BaseModel):
    executive_summary: str
    problem: str
    evidence: str
    cost_of_doing_nothing: str
    objectives: list[Objective] = Field(min_length=1)
    in_scope: list[str]
    out_of_scope: list[str] = Field(min_length=1)
    later_phases: list[str] = Field(default_factory=list)
    stakeholders: list[Stakeholder] = Field(default_factory=list)
    data: list[DataItem] = Field(default_factory=list)
    risk_controls: list[RiskControl] = Field(default_factory=list)
    dependencies: list[str] = Field(default_factory=list)
    release_approach: str
    rollback: str
    training_and_procedures: str
    customer_communication: str

class Seams(BaseModel):
    seams: list[str] = Field(min_length=1, description="Highest practical test boundaries")
    rationale: str
    prior_art: list[str] = Field(default_factory=list)


class Module(BaseModel):
    name: str
    change: Literal["New", "Changed"]
    responsibility: str
    serves: list[str] = Field(description="FR-/NFR- IDs")


class Decision(BaseModel):
    decision: str
    alternatives: str
    reason: str
    adr_needed: bool = False


class Coverage(BaseModel):
    requirement: str
    sections: list[SpecRef]
    notes: str = ""


class Spec(BaseModel):
    summary: str
    current_state: str = ""
    modules: list[Module] = Field(min_length=1)
    interfaces: str
    data: str
    key_flows: str
    integrations: str
    security: str
    nfr_design: str
    observability: str
    rollout: str
    testing: str
    decisions: list[Decision] = Field(default_factory=list)
    prd_issues: list[str] = Field(default_factory=list)
    coverage: list[Coverage] = Field(min_length=1)
    out_of_scope: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)


class TicketDraft(BaseModel):
    feature_id: str
    type: Literal["Ticket", "Spike", "Enabler"] = "Ticket"
    title: str
    user_story: str = Field("", description="Tickets: As a…, I want…, so that… (the slice it delivers)")
    question: str = Field("", description="Spikes: the question it must answer")
    timebox: str = Field("", description="Spikes: e.g. '2 days'")
    unblocks: list[int] = Field(default_factory=list, description="Enablers: 1-based positions of LATER tickets")
    acceptance_criteria: list[str] = Field(description="Given…, when…, then… (3 to 7)")
    requirements: list[str] = Field(default_factory=list, description="FR-/NFR- IDs")
    spec_refs: list[SpecRef] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    size: Literal["XS", "S", "M", "L"]
    priority: MoSCoW
    depends_on: list[int] = Field(default_factory=list, description="1-based positions of EARLIER tickets")
    notes: str = ""


class Uncovered(BaseModel):
    id: str
    reason: str


class TicketPlan(BaseModel):
    """Tickets in build order. The list order IS the build order."""
    tickets: list[TicketDraft] = Field(min_length=1)
    uncovered: list[Uncovered] = Field(default_factory=list)


class Ticket(TicketDraft):
    id: str
    depends_on_ids: list[str] = Field(default_factory=list)
    unblocks_ids: list[str] = Field(default_factory=list)
