"""Define every typed shape the system passes around.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C2 Recorded understanding and C4 Traceable documents. Every
answer, decision, document, and ticket has one declared shape here. Agents must
return these shapes, rules check them, and renderers print them. This file holds
data only; it never validates business rules.

Why this comes now: Settings exist (step 1). Nothing can be validated, stored, or
rendered until the data is defined, and every later module imports from here.

Build order: Step 2 of 33.
Previous: src/assay/settings.py (step 1), which defines Settings, the configuration
every later module reads.
Next: src/assay/domain/ids.py (step 3), which assigns every log, question, DoD,
requirement, and ticket ID.

Build these in order:
    1. now: used as a default by the records below.
    2. Metric: a measure with a baseline, target, and date.
    3. NewEntry: a log entry proposed by an agent, before code gives it an ID.
    4. LogEntry: a recorded log entry with its code-assigned ID.
    5. GlossaryTerm: one shared term and its meaning.
    6. Question: one question with a recommended answer.
    7. GrillTurn: what one grill turn produced.
    8. Turn: a question and the human answer, with who answered and when.
    9. CurrentStateMap: how the existing code works today.
    10. Brief: the PM's ask, why, and outcome.
    11. BriefCritique: whether a brief is ready, and what to fix.
    12. FollowUp: a pre-written follow-up question with its condition.
    13. QItem: one questionnaire question.
    14. Confirmation: a fact found in code, for developers to confirm.
    15. Questionnaire: one round of developer questions.
    16. Answer: one developer's answer to one question.
    17. ResponseSheet: one developer's answers for one round.
    18. Reconciliation: what a round of answers produced.
    19. DodItemDraft: a Definition of Done item before it has an ID.
    20. DodItem: a Definition of Done item with its code-assigned ID.
    21. DodTurn: what one Definition of Done turn produced.
    22. FeatureDraft: a business capability inside a story.
    23. StoryDraft: a business goal and its features.
    24. Requirement: a testable functional requirement.
    25. NFR: a non-functional requirement.
    26. PRDCore: the traceable core of the PRD.
    27. Objective: a business objective with its measure.
    28. Stakeholder: a stakeholder group and its role.
    29. DataItem: a piece of data the initiative touches.
    30. RiskControl: a risk or regulatory area to confirm.
    31. PRDNarrative: the business narrative of the PRD.
    32. Seams: the agreed test boundaries.
    33. Module: a module the spec builds or changes.
    34. Decision: a design decision and its alternatives.
    35. Coverage: which spec sections address a requirement.
    36. Spec: the developer spec.
    37. TicketDraft: a ticket before code numbers it.
    38. Uncovered: a requirement deliberately left without a ticket.
    39. TicketPlan: tickets in build order.
    40. Ticket: a ticket with its code-assigned ID.

Depends on:
    Nothing in this project (foundation root). Placed at step 2 because every later
    module imports these shapes.
    Standard library: re, datetime, typing.
    Third-party: pydantic.

Depended on by:
    assay.domain.ids, assay.rules, assay.llm, assay.graph, assay.render, and
    assay.api: every typed value in the system.

Spec coverage: S2.1, S3.2, S5.2, S5.3, S5.4, S5.5, S5.7, S5.8, S5.9, S5.10, S8.4 | Traces to: I1, I2, I3, I15
"""

import re
from datetime import UTC, datetime
from typing import Literal

from pydantic import BaseModel, Field

Area = Literal[
    "Problem",
    "Outcome",
    "Users",
    "Scope",
    "Journeys",
    "Data",
    "Integrations",
    "Non-functional",
    "Regulation",
    "Rollout",
    "Delivery",
]
EntryType = Literal["D", "A", "R", "Q", "C"]
Priority = Literal["Blocking", "Important", "Useful"]
MoSCoW = Literal["Must have", "Should have", "Could have", "Won't have"]
Role = Literal["Developer", "Architecture", "Data", "Security", "Operations", "QA"]
SpecRef = Literal[
    "modules",
    "interfaces",
    "data",
    "key_flows",
    "integrations",
    "security",
    "nfr_design",
    "observability",
    "rollout",
    "testing",
]
DoDLevel = Literal["ticket", "feature", "story", "release"]


USER_STORY = re.compile(r"^As an? .+?, I want .+?, so that .+", re.I | re.S)  # S3.4: story wording


def now() -> str:
    """Return the current time as an ISO 8601 UTC timestamp with seconds.

    Problem piece: C2: every record says when it happened.

    Why it matters: Audit needs times in one unambiguous format. Local time or mixed
                    precision makes records from different servers impossible to
                    order, so every timestamp in the system comes from this one
                    function.

    What: Returns the current UTC time as text such as 2026-10-05T14:03:09+00:00.
          Called as now() and returns str.

    Spec: S2.1 | Ticket: 01 | Traces to: I2

    Build steps:
    1. Task: Return the current moment in UTC, formatted as ISO 8601 to whole
             seconds.
       Expected outcome: The result parses as a UTC timestamp with no fractional
                         seconds.
    """
    raise NotImplementedError("S2.1: now")


class Metric(BaseModel):
    """A measure with a baseline, target, and date.

    Problem piece: C4: success that can be checked.

    Why it matters: An outcome without a number cannot be tested, so the gate
                    demands one. Keeping the measure, baseline, target, and date
                    together stops a target being recorded without its starting
                    point.

    What: Four text fields describing one measurable outcome.

    Spec: S3.2 | Ticket: — | Traces to: —
    """

    measure: str
    baseline: str
    target: str
    by_when: str


class NewEntry(BaseModel):
    """A log entry proposed by an agent, before code gives it an ID.

    Problem piece: C2: one recorded decision, assumption, risk, question, or
                   correction.

    Why it matters: Every later document cites these entries, so they must carry who
                    said what and the typed flags the gate reads. Leaving the ID out
                    stops a model inventing or reusing identifiers (I2).

    What: Type, title, area, detail, source, optional priority, owner, status,
          positions, and the gate flags scope_side, journey_path, metric, and
          covers_rollback.

    Spec: S2.1 | Ticket: — | Traces to: —
    """

    type: EntryType = Field(
        description="D decision, A assumption, R risk, Q open question, C correction"
    )
    title: str = Field(description="One line, plain language")
    area: Area
    detail: str
    source: str = Field(description="Who said it and their role, e.g. 'Priya (Lead Developer)'")
    priority: Priority | None = Field(None, description="Required for Q entries")
    owner: str | None = Field(None, description="Role that owns resolving or validating it")
    status: Literal["Open", "Closed", "Parked", "Accepted as risk"] | None = None
    positions: list[str] = Field(
        default_factory=list, description="For disagreements: 'Name (role): position'"
    )
    scope_side: Literal["in", "out"] | None = Field(None, description="Required for Scope entries")
    journey_path: Literal["happy", "failure"] | None = Field(
        None, description="Required for Journeys entries"
    )
    metric: Metric | None = Field(
        None, description="For Outcome entries that set a measurable target"
    )
    covers_rollback: bool = Field(
        False, description="Rollout entries: true if it states how to roll back"
    )


class LogEntry(NewEntry):
    """A recorded log entry with its code-assigned ID.

    Problem piece: C2: the citable unit every PRD line traces to.

    Why it matters: Traceability needs a stable handle. A superseded entry must stay
                    visible so a reader can see why a decision changed, so
                    replacement is recorded rather than deleting the entry.

    What: A NewEntry plus id, superseded_by, and recorded_at.

    Spec: S2.1 | Ticket: — | Traces to: —
    """

    id: str
    superseded_by: list[str] = Field(default_factory=list)
    recorded_at: str = Field(default_factory=now)


class GlossaryTerm(BaseModel):
    """One shared term and its meaning.

    Problem piece: C4: one word means one thing everywhere.

    Why it matters: When two teams use one word for two things, the defect appears
                    late and costs the most. A term with its definition and the
                    words to avoid keeps documents consistent.

    What: Term, one-sentence definition, and words to avoid.

    Spec: S5.2 | Ticket: — | Traces to: —
    """

    term: str
    definition: str = Field(description="One sentence: what it IS")
    avoid: list[str] = Field(default_factory=list)


class Question(BaseModel):
    """One question with a recommended answer.

    Problem piece: C6: a person confirms or corrects instead of starting cold.

    Why it matters: A recommended answer is faster to confirm than a blank question
                    is to answer, and its reason shows the person what the agent
                    assumed.

    What: Question text, recommended answer, reason, and the area it covers.

    Spec: S5.3 | Ticket: — | Traces to: —
    """

    text: str = Field(description="Exactly one question")
    recommended_answer: str
    reason: str = Field(description="One line: why you recommend it")
    area: Area


class GrillTurn(BaseModel):
    """What one grill turn produced.

    Problem piece: C2 and C6: record the last answer and choose the next question.

    Why it matters: Each turn both records what was learned and moves the
                    conversation on. Keeping both in one typed output lets the rules
                    check the recorded entries and the single next question
                    together.

    What: Recorded entries, superseded IDs, glossary updates, an optional challenge,
          an optional next question, and a done flag.

    Spec: S5.3 | Ticket: — | Traces to: —
    """

    recorded: list[NewEntry] = Field(
        default_factory=list, description="Entries from the latest answer"
    )
    supersedes: list[str] = Field(
        default_factory=list, description="IDs of entries the new ones replace"
    )
    glossary_updates: list[GlossaryTerm] = Field(default_factory=list)
    challenge: str | None = Field(
        None, description="Plain pushback if the latest answer was weak or risky"
    )
    next_question: Question | None = None
    done: bool = Field(False, description="True only when every area is covered")


class Turn(BaseModel):
    """A question and the human answer, with who answered and when.

    Problem piece: C2 and C6: the audit trail of human input.

    Why it matters: A bank must show who said what. Recording the answerer and time
                    on every answer turns the transcript into evidence rather than
                    notes.

    What: Question, recommended answer, the answer given, the user, and a timestamp.

    Spec: S5.3 | Ticket: — | Traces to: —
    """

    question: str
    recommended: str
    answer: str
    user: str
    at: str = Field(default_factory=now)


class CurrentStateMap(BaseModel):
    """How the existing code works today.

    Problem piece: C2: argue about the gap, not about the present.

    Why it matters: In mode 2, people's memory of a system is less reliable than its
                    code. A map built from files the agent read, corrected by
                    developers, anchors every later question.

    What: Components, data flow, data stores, tests, flags and jobs, unknowns, and
          files read.

    Spec: S5.4 | Ticket: — | Traces to: —
    """

    components: list[str]
    data_flow: str
    data_stores: list[str]
    tests: str = Field(description="Existing tests in this area, and gaps")
    flags_and_jobs: list[str] = Field(default_factory=list)
    unknowns: list[str] = Field(default_factory=list, description="Things the code did not settle")
    files_read: list[str] = Field(default_factory=list)


class Brief(BaseModel):
    """The PM's ask, why, and outcome.

    Problem piece: C6: the business decisions that only the PM makes.

    Why it matters: Mode 3 sends questions to developers, but the ask, the why, and
                    the outcome are business decisions. Holding them in one shape
                    keeps them out of the developer questionnaire.

    What: Ask, why, outcome, known steps, and constraints.

    Spec: S5.5 | Ticket: — | Traces to: —
    """

    ask: str
    why: str
    outcome: str
    known_steps: str = ""
    constraints: str = ""


class BriefCritique(BaseModel):
    """Whether a brief is ready, and what to fix.

    Problem piece: C3: a weak brief never reaches developers.

    Why it matters: A vague outcome produces a vague questionnaire. Checking the
                    brief first stops developers spending time on questions that
                    cannot be answered well.

    What: A ready flag and a list of issues for the PM.

    Spec: S5.5 | Ticket: — | Traces to: —
    """

    ready: bool
    issues: list[str] = Field(
        default_factory=list, description="What the PM must fix, one per item"
    )


class FollowUp(BaseModel):
    """A pre-written follow-up question with its condition.

    Problem piece: C6: batch questions that can still branch.

    Why it matters: Batched questions cannot react to answers, so likely branches
                    are written in advance and answered only when their condition
                    holds.

    What: A condition and the follow-up text.

    Spec: S5.5 | Ticket: — | Traces to: —
    """

    condition: str
    text: str


class QItem(BaseModel):
    """One questionnaire question.

    Problem piece: C6: a question routed to the right developer role.

    Why it matters: Developers answer offline, so each question must carry its
                    owner, priority, reason, and proposed answer, or the answers
                    come back shallow.

    What: Text, owner role, priority, why it matters, proposed answer, reason,
          earlier dependencies, follow-ups, and area.

    Spec: S5.5 | Ticket: — | Traces to: —
    """

    text: str
    owner_role: Role
    priority: Priority
    why_it_matters: str
    proposed_answer: str
    reason: str
    depends_on: list[int] = Field(
        default_factory=list, description="1-based positions of earlier questions"
    )
    follow_ups: list[FollowUp] = Field(default_factory=list)
    area: Area


class Confirmation(BaseModel):
    """A fact found in code, for developers to confirm.

    Problem piece: C2: answer from code before asking people.

    Why it matters: Questions the code already answers waste developer time; turning
                    them into confirmations still lets a developer correct a
                    misreading.

    What: A statement and the file or document it came from.

    Spec: S5.5 | Ticket: — | Traces to: —
    """

    statement: str
    source: str = Field(description="File or document where this was found")


class Questionnaire(BaseModel):
    """One round of developer questions.

    Problem piece: C6: the batch developers answer in the browser.

    Why it matters: Mode 3 depends on one coherent batch with a summary, a capped
                    number of questions, and confirmations, so developers can answer
                    it in one sitting.

    What: A summary, 1 to 30 questions, and confirmations.

    Spec: S5.5 | Ticket: — | Traces to: —
    """

    summary: str = Field(description="One paragraph on what the questions cover")
    questions: list[QItem] = Field(min_length=1, max_length=30)
    confirmations: list[Confirmation] = Field(default_factory=list)


class Answer(BaseModel):
    """One developer's answer to one question.

    Problem piece: C6: confirm, correct, or say who would know.

    Why it matters: A closed set of responses makes answers comparable across
                    developers and lets reconciliation tell confirmation from
                    correction.

    What: Question ID, response, and optional text.

    Spec: S8.4 | Ticket: — | Traces to: —
    """

    question_id: str
    response: Literal["Confirm", "Correct", "Don't know", "No answer"]
    text: str = ""


class ResponseSheet(BaseModel):
    """One developer's answers for one round.

    Problem piece: C2 and C6: who answered what, and when.

    Why it matters: Reconciliation must know who gave each answer and in which
                    round, so later rounds never re-read earlier sheets.

    What: Respondent, role, round, answers, comments, and submission time.

    Spec: S8.4 | Ticket: — | Traces to: —
    """

    respondent: str
    role: str
    round: int
    answers: list[Answer]
    comments: str = ""
    submitted_at: str = Field(default_factory=now)


class Reconciliation(BaseModel):
    """What a round of answers produced.

    Problem piece: C2: answers become recorded entries, gaps, and follow-ups.

    Why it matters: Answers on their own are not decisions. Reconciliation turns
                    them into entries, names contradictions, and limits follow-ups
                    to blocking gaps.

    What: Recorded entries, contradictions, blocking gaps, and at most eight
          follow-up questions.

    Spec: S5.5 | Ticket: — | Traces to: —
    """

    recorded: list[NewEntry] = Field(
        description="Decisions, assumptions, risks, conflicts as entries"
    )
    contradictions: list[str] = Field(default_factory=list)
    blocking_gaps: list[str] = Field(default_factory=list)
    follow_up_questions: list[QItem] = Field(default_factory=list, max_length=8)


class DodItemDraft(BaseModel):
    """A Definition of Done item before it has an ID.

    Problem piece: C6: a check every piece of work must pass.

    Why it matters: A DoD item is only useful if two people can agree it is met,
                    someone owns it, and evidence exists afterwards; the fields
                    force all three.

    What: Level, statement, category, how verified, evidence, verifier, source,
          mandate, and a team-confirmation flag.

    Spec: S5.7 | Ticket: — | Traces to: —
    """

    level: DoDLevel = Field(
        description="ticket: every ticket; feature: once per feature; "
        "story: once per story; release: once per release"
    )
    statement: str = Field(description="A verifiable condition, under about 15 words")
    category: str
    how_verified: str
    evidence: str = Field(description="The proof that exists afterwards, and where")
    verified_by: str = Field(description="A named role, never 'the team'")
    source: str
    mandated: str = ""
    needs_team_confirmation: bool = False


class DodItem(DodItemDraft):
    """A Definition of Done item with its code-assigned ID.

    Problem piece: C2 and C6: a citable quality check.

    Why it matters: Tickets and features list their DoD items by ID, so the ID must
                    be stable and never reused after withdrawal.

    What: A DodItemDraft plus its id.

    Spec: S5.7 | Ticket: — | Traces to: —
    """

    id: str


class DodTurn(BaseModel):
    """What one Definition of Done turn produced.

    Problem piece: C6: agree the standard one question at a time.

    Why it matters: Each turn may add items, withdraw items, push back, and ask the
                    next question; one typed output lets the rules check all of it.

    What: Agreed items, IDs to withdraw, an optional challenge, an optional next
          question, and a done flag.

    Spec: S5.7 | Ticket: — | Traces to: —
    """

    agreed: list[DodItemDraft] = Field(default_factory=list)
    remove: list[str] = Field(default_factory=list, description="IDs of agreed items to withdraw")
    challenge: str | None = None
    next_question: Question | None = None
    done: bool = False


class FeatureDraft(BaseModel):
    """A business capability inside a story.

    Problem piece: C4: the middle level of story, feature, ticket.

    Why it matters: Approvers recognise capabilities, not components. Numbering
                    features across all stories gives each one a single ID the whole
                    pipeline uses.

    What: An F-NN id, a name, and a summary.

    Spec: S5.8 | Ticket: — | Traces to: —
    """

    id: str = Field(pattern=r"^F-\d{2}$", description="F-01, F-02... numbered across all stories")
    name: str = Field(description="A business capability, not a component")
    summary: str


class StoryDraft(BaseModel):
    """A business goal and its features.

    Problem piece: C4: the top level of story, feature, ticket.

    Why it matters: A story says who benefits and why; the features under it say
                    how. The wording check lives in the PRD rules so this shape
                    stays pure data.

    What: An S-NN id, the story text, and at least one feature.

    Spec: S5.8 | Ticket: — | Traces to: —
    """

    id: str = Field(pattern=r"^S-\d{2}$")
    text: str = Field(description="As a <actor>, I want <goal>, so that <benefit>.")
    features: list[FeatureDraft] = Field(min_length=1)


class Requirement(BaseModel):
    """A testable functional requirement.

    Problem piece: C4: a claim that traces to a source.

    Why it matters: A requirement without a feature cannot be built and one without
                    a source cannot be trusted, so both are required fields.

    What: Text, priority, feature ID, and at least one source ID.

    Spec: S5.8 | Ticket: — | Traces to: —
    """

    text: str = Field(description="Testable, uses must/should/may")
    priority: MoSCoW
    feature_id: str
    sources: list[str] = Field(min_length=1, description="Session log or questionnaire IDs")


class NFR(BaseModel):
    """A non-functional requirement.

    Problem piece: C4: qualities that must also trace to a source.

    Why it matters: Performance, security, and audit needs drive design as much as
                    features do, and they need the same traceability.

    What: Area, text, priority, and at least one source ID.

    Spec: S5.8 | Ticket: — | Traces to: —
    """

    area: str
    text: str
    priority: MoSCoW
    sources: list[str] = Field(min_length=1)


class PRDCore(BaseModel):
    """The traceable core of the PRD.

    Problem piece: C4: stories, features, and requirements.

    Why it matters: Writing the traceable core separately from the narrative lets
                    the rules check numbering and sources on a smaller output.

    What: One to eight stories, functional requirements, and non-functional
          requirements.

    Spec: S5.8 | Ticket: — | Traces to: —
    """

    stories: list[StoryDraft] = Field(min_length=1, max_length=8)
    functional: list[Requirement] = Field(min_length=1)
    non_functional: list[NFR] = Field(default_factory=list)


class Objective(BaseModel):
    """A business objective with its measure.

    Problem piece: C4: success an approver can check.

    Why it matters: Objectives tie the PRD to the outcome agreed in intake; each
                    must cite its source.

    What: Objective, measure, baseline, target, date, and source.

    Spec: S5.8 | Ticket: — | Traces to: —
    """

    objective: str
    measure: str
    baseline: str
    target: str
    by_when: str
    source: str


class Stakeholder(BaseModel):
    """A stakeholder group and its role.

    Problem piece: C6: who is accountable, responsible, consulted, informed.

    Why it matters: Approvers need to see who owns what; a closed set of roles keeps
                    the table unambiguous.

    What: Group, interest, and role.

    Spec: S5.8 | Ticket: — | Traces to: —
    """

    group: str
    interest: str
    role: Literal["Accountable", "Responsible", "Consulted", "Informed"]


class DataItem(BaseModel):
    """A piece of data the initiative touches.

    Problem piece: C4: data, classification, and retention.

    Why it matters: A bank must know what data is held, why, and for how long; each
                    row cites its source.

    What: Data, classification, purpose, retention, sharing, and source.

    Spec: S5.8 | Ticket: — | Traces to: —
    """

    data: str
    classification: str
    purpose: str
    retention: str
    shared_with: str
    source: str


class RiskControl(BaseModel):
    """A risk or regulatory area to confirm.

    Problem piece: C4 and C6: flagged areas with owners.

    Why it matters: Only Compliance may conclude a regulation is met, so each area
                    is recorded with an owner and a status that defaults to
                    'Compliance to confirm' (I4).

    What: Area, consideration, owner, and status.

    Spec: S5.8 | Ticket: — | Traces to: —
    """

    area: str
    consideration: str
    owner: str
    status: str = "Compliance to confirm"


class PRDNarrative(BaseModel):
    """The business narrative of the PRD.

    Problem piece: C4: the prose approvers read.

    Why it matters: Approvers judge what and why; the narrative carries problem,
                    evidence, scope, and rollout, separately from the traceable
                    core.

    What: Summary, problem, evidence, cost of delay, objectives, scope lists,
          stakeholders, data, risks, dependencies, and rollout text.

    Spec: S5.8 | Ticket: — | Traces to: —
    """

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
    """The agreed test boundaries.

    Problem piece: C6: developers confirm how work will be tested.

    Why it matters: Tests are only as useful as the boundary they test at; agreeing
                    seams before the spec stops every ticket being hard to test.

    What: One or more seams, the rationale, and prior art.

    Spec: S5.9 | Ticket: — | Traces to: —
    """

    seams: list[str] = Field(min_length=1, description="Highest practical test boundaries")
    rationale: str
    prior_art: list[str] = Field(default_factory=list)


class Module(BaseModel):
    """A module the spec builds or changes.

    Problem piece: C4: design that traces to requirements.

    Why it matters: Every module must serve real requirements, or it is design
                    nobody asked for.

    What: Name, new or changed, responsibility, and the requirement IDs it serves.

    Spec: S5.9 | Ticket: — | Traces to: —
    """

    name: str
    change: Literal["New", "Changed"]
    responsibility: str
    serves: list[str] = Field(description="FR-/NFR- IDs")


class Decision(BaseModel):
    """A design decision and its alternatives.

    Problem piece: C4: why the design is this way.

    Why it matters: Recording rejected alternatives stops the same debate being
                    reopened.

    What: Decision, alternatives, reason, and whether an ADR is needed.

    Spec: S5.9 | Ticket: — | Traces to: —
    """

    decision: str
    alternatives: str
    reason: str
    adr_needed: bool = False


class Coverage(BaseModel):
    """Which spec sections address a requirement.

    Problem piece: C4: no requirement left without design.

    Why it matters: A requirement that maps to no design is one nobody builds; a
                    closed set of section names makes coverage checkable.

    What: Requirement ID, section names, and notes.

    Spec: S5.9 | Ticket: — | Traces to: —
    """

    requirement: str
    sections: list[SpecRef]
    notes: str = ""


class Spec(BaseModel):
    """The developer spec.

    Problem piece: C4: the design tickets are cut from.

    Why it matters: Developers need modules, interfaces, data, security, and testing
                    in one place, with coverage proving every requirement is
                    addressed.

    What: Text for each section, modules, decisions, PRD issues, coverage, out of
          scope, and open questions.

    Spec: S5.9 | Ticket: — | Traces to: —
    """

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
    """A ticket before code numbers it.

    Problem piece: C4: a buildable, testable slice of one feature.

    Why it matters: Positions in the list stand in for IDs until code assigns them,
                    so dependencies can be checked to point backward only (I15).

    What: Feature, type, title, user story or spike question, criteria,
          requirements, spec sections, sources, size, priority, dependencies,
          unblocks, and notes.

    Spec: S5.10 | Ticket: — | Traces to: —
    """

    feature_id: str
    type: Literal["Ticket", "Spike", "Enabler"] = "Ticket"
    title: str
    user_story: str = Field(
        "", description="Tickets: As a…, I want…, so that… (the slice it delivers)"
    )
    question: str = Field("", description="Spikes: the question it must answer")
    timebox: str = Field("", description="Spikes: e.g. '2 days'")
    unblocks: list[int] = Field(
        default_factory=list, description="Enablers: 1-based positions of LATER tickets"
    )
    acceptance_criteria: list[str] = Field(description="Given…, when…, then… (3 to 7)")
    requirements: list[str] = Field(default_factory=list, description="FR-/NFR- IDs")
    spec_refs: list[SpecRef] = Field(default_factory=list)
    sources: list[str] = Field(default_factory=list)
    size: Literal["XS", "S", "M", "L"]
    priority: MoSCoW
    depends_on: list[int] = Field(
        default_factory=list, description="1-based positions of EARLIER tickets"
    )
    notes: str = ""


class Uncovered(BaseModel):
    """A requirement deliberately left without a ticket.

    Problem piece: C4: an explicit gap instead of a silent one.

    Why it matters: Some requirements are met elsewhere; recording the reason keeps
                    the coverage check honest.

    What: Requirement ID and reason.

    Spec: S5.10 | Ticket: — | Traces to: —
    """

    id: str
    reason: str


class TicketPlan(BaseModel):
    """Tickets in build order.

    Problem piece: C4: the backlog, ordered.

    Why it matters: List order is build order, which makes dependency cycles
                    impossible by construction.

    What: Tickets and uncovered requirements.

    Spec: S5.10 | Ticket: — | Traces to: —
    """

    tickets: list[TicketDraft] = Field(min_length=1)
    uncovered: list[Uncovered] = Field(default_factory=list)


class Ticket(TicketDraft):
    """A ticket with its code-assigned ID.

    Problem piece: C2 and C4: the unit a tracker receives.

    Why it matters: Trackers keep history by ID, so tickets get stable IDs and their
                    dependencies become IDs instead of positions.

    What: A TicketDraft plus id, depends_on_ids, and unblocks_ids.

    Spec: S5.10 | Ticket: — | Traces to: —
    """

    id: str
    depends_on_ids: list[str] = Field(default_factory=list)
    unblocks_ids: list[str] = Field(default_factory=list)
