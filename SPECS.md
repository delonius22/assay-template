# SPECS — Assay

## Traceability

Every requirement traces to an invariant (I*), assumption (A*), or
convention (C*) in the decomposition, and to a PRD goal. Untraced items are
scope creep.

## Decision log

Append-only. ID · decision · stage · effect.

- D1 · Hierarchy is story, then feature, then ticket · forge · PRD stories are business goals; features sit under stories; tickets under features.
- D2 · Typed data is the source of truth; files are generated and never read back · forge · Rules check models, not text.
- D3 · LangGraph with a hand-written validate-and-retry loop; no Pydantic AI · forge · S4.5 owns the loop.
- D4 · A person reviews tickets before export (recommended default, not yet confirmed) · forge · Adds a pause to S5.10. Reverse by removing the review step.
- D5 · Ticket coverage includes NFR IDs, not only FR (recommended default, not yet confirmed) · forge · S3.6 checks every PRD ID.
- D6 · Shipped complete, not stubbed: data shapes, prompts, reference text, templates, the PDF renderer, the browser UI, graph wiring · skeleton · These are contracts and assets; behavior is stubbed.
- D7 · Stubs raise NotImplementedError naming their S-ID; the web app maps it to HTTP 501 · skeleton · The server runs from day one and shows what is missing.
- D8 · Ticket list order is build order; dependencies point backward only · forge · No cycle detection needed (I15).
- D9 · The repository's copy of the plan validator skips virtual environments · skeleton · A `.venv` inside the repo no longer produces false failures from third-party code.

## Data shapes

All owned by the domain models module unless noted. Consumers cite the owner; they never restate fields.

- NewEntry / LogEntry | owner: domain models | form: model | fields: type, title, area, detail, source, priority, owner, status, positions, scope_side, journey_path, metric, covers_rollback (+ id, superseded_by, recorded_at)
- Metric | owner: domain models | form: model | fields: measure, baseline, target, by_when
- GlossaryTerm | owner: domain models | form: model | fields: term, definition, avoid
- Question, GrillTurn, Turn | owner: domain models | form: model | fields: see model
- CurrentStateMap | owner: domain models | form: model | fields: components, data_flow, data_stores, tests, flags_and_jobs, unknowns, files_read
- Brief, BriefCritique | owner: domain models | form: model | fields: ask, why, outcome, known_steps, constraints / ready, issues
- QItem, FollowUp, Confirmation, Questionnaire | owner: domain models | form: model
- Answer, ResponseSheet | owner: domain models | form: model | fields: question_id, response, text / respondent, role, round, answers, comments, submitted_at
- Reconciliation | owner: domain models | form: model
- DodItemDraft, DodItem, DodTurn | owner: domain models | form: model | level ∈ ticket, feature, story, release
- StoryDraft, FeatureDraft, Requirement, NFR, PRDCore, PRDNarrative | owner: domain models | form: model
- Seams, Module, Decision, Coverage, Spec | owner: domain models | form: model | Coverage.sections ∈ SpecRef
- TicketDraft, TicketPlan, Ticket, Uncovered | owner: domain models | form: model
- AssayState | owner: graph state | form: model | the whole session; checkpointed
- Settings | owner: settings | form: model (frozen dataclass)
- AppContext | owner: graph context | form: model (dataclass) | settings, store, get_model, limits
- AgentSpec, CallRecord, Limits | owner: model call loop | form: model (dataclass)
- Deps | owner: code tools | form: model (dataclass) | roots, known_ids, prd_ids, feature_ids, files_read
- GateItem | owner: intake rules | form: model (NamedTuple) | label, ok, why
- Interrupt payload | owner: S5 contract | form: contract | open + fixed keys: kind ∈ question, dod_question, map_review, brief_fix, await_answers, approval, seams, ticket_review
- Resume value | owner: S8.3 contract | form: contract | fixed keys: text, user, decision, brief
- Store namespaces | owner: graph context | form: contract | ("team","dod"), ("team","glossary"), ("responses", slug, "r<N>"), ("calls", slug), ("sessions",)
- CSV columns | owner: S6.5 contract | form: contract | Level, ID, Parent ID, Title, Description, Acceptance Criteria, Definition of Done, Requirements, Spec Sections, Priority, Size, Type, Depends On, Unblocks, Sources

## Build order

- S1.1 — configuration first; everything reads it
- S1.2 — pure; reports what is missing
- S2.1, S2.2, S2.3, S2.4, S2.5, S2.6 — pure leaves; no fakes needed
- S3.1, S3.2, S3.3, S3.4, S3.5, S3.6 — pure leaves; the rules every later stage enforces
- S4.2 — pure message building; the call loop needs it
- S4.5 — the loop, tested with a scripted fake model
- S4.6 — validators compose S3 rules
- S4.4 — code tools, tested on a temporary directory
- S4.1, S4.3 — real gateway boundary, after fakes prove the loop
- S7.1, S7.2 — persistence, SQLite first, Postgres second
- S5.1, S5.2 — state helpers and runtime context
- S6.1, S6.2, S6.3, S6.4, S6.5, S6.6 — renderers, each tested on fixed models
- S5.3, S5.4, S5.5, S5.6, S5.7, S5.8, S5.9, S5.10 — workflow nodes, in pipeline order
- S5.11 — wiring (shipped complete; verify only)
- S8.1, S8.2, S8.3, S8.4, S8.5 — web layer last
- S8.6 — browser UI (shipped complete; verify only)

## S1: Configuration
**Traces to:** I9, A1 | **PRD:** Goal
**Done when:** settings load from environment with documented defaults and missing gateway settings are listed. | **Depends on:** —
- [ ] S1.1 — Load every setting from environment variables with the defaults in the example environment file.
  - Pitfall: a model per role falls back to the default model only when its own variable is empty, not when it is unset to an empty string by a template.
- [ ] S1.2 — List each missing gateway setting and each role without a model.
  - Pitfall: listing the key's value in an error message leaks it (I9); list names only.

## S2: Identity assignment
**Traces to:** I2, I15 | **PRD:** Goal
**Done when:** every ID is assigned by code, sequential per type, never reused. | **Depends on:** S1
- [ ] S2.1 — Append log entries with IDs `<type>-NNN`, numbered per type; mark superseded entries, never delete them.
  - Pitfall: numbering from the count of new entries instead of the whole log reuses IDs.
- [ ] S2.2 — Return only entries not superseded.
  - Pitfall: none beyond S2.1.
- [ ] S2.3 — Number questions Q-01… (round 1) or Q-F01… (follow-up round), follow-ups `<id>a`, confirmations K-01… (round 1 only).
  - Pitfall: confirmations in a follow-up round would collide with round-one K-IDs.
- [ ] S2.4 — Apply a DoD turn: withdraw listed IDs, add new items as DOD-<level letter>NN (team) or DOD-A<letter>NN (additions), never reusing a withdrawn number.
  - Pitfall: counting only kept items reuses the number of a withdrawn item.
- [ ] S2.5 — Number requirements FR-01… and NFR-01… in list order.
- [ ] S2.6 — Number tickets T-001… in list order and convert 1-based depends_on and unblocks positions into ticket IDs.
  - Pitfall: positions are 1-based; an off-by-one silently links the wrong ticket.

## S3: Rules
**Traces to:** I1, I3, I4, I5, I15 | **PRD:** Success criteria 2
**Done when:** each rule is a pure function returning a list of problems, empty when it passes. | **Depends on:** S2
- [ ] S3.1 — Shared rules: walk every string in a model; flag compliance assertions (including "conforms to") unless the text says "confirm"; flag more than one question mark; list vague words.
  - Pitfall: matching "compliant" also flags "non-compliant findings to confirm"; the "confirm" escape exists for that.
- [ ] S3.2 — Intake: require typed flags on entries (scope side, journey path, owners on open questions and regulation); compute the 11-item exit gate from typed fields only.
  - Pitfall: checking the words "out of scope" instead of `scope_side` lets wording pass the gate.
  - Input: log, dod_agreed. Work: per gate item, a typed-field test. Output: GateItem list. Failure: none raised; failures are returned. Test: a log with "out of scope" wording but `scope_side="in"` fails the scope item.
- [ ] S3.3 — DoD: reject vague statements, "the team" as verifier, and statements over 18 words; a team standard needs 1 to 12 ticket-level items.
- [ ] S3.4 — PRD: stories S-01… and features F-01… numbered in order; every requirement belongs to a known feature and cites known sources; every feature has a functional requirement; no compliance claims.
  - Pitfall: feature numbering restarts per story if built per story; it must run across all stories.
- [ ] S3.5 — Spec: coverage lists exactly the PRD IDs; modules serve only PRD IDs.
- [ ] S3.6 — Tickets: known feature; user story shape for tickets; spike question and timebox; enabler unblocks later tickets; 3 to 7 Given/When/Then criteria; dependencies earlier only; size L rejected; every FR and NFR covered or listed as uncovered with a reason (D5).
  - Pitfall: checking dependencies with `d > i` instead of `d >= i` lets a ticket depend on itself.

## S4: Model layer
**Traces to:** I1, I10, I11, I13, A1, A2 | **PRD:** Goal, Success criteria 2 and 5
**Done when:** any tool-calling model returns validated typed output, with bounded retries and cache-friendly messages. | **Depends on:** S3
- [ ] S4.1 — Retry transient gateway errors (408, 409, 425, 429, 5xx, timeouts, connection errors) with capped exponential backoff and jitter, honouring Retry-After; raise permanent errors at once.
  - Pitfall: retrying a 400 or 401 burns attempts and delays a clear error.
  - Input: a zero-argument callable. Work: call; on transient error wait and retry. Output: the callable's result. Failure: the last error re-raised after `attempts`. Test: a fake raising 429 twice then succeeding waits base·2⁰ then base·2¹.
- [ ] S4.2 — Build messages with the static prefix first (marked cacheable in explicit mode) and the dynamic part last; extract token and cache counts from a response.
  - Pitfall: any per-call value in the static prefix (a date, a user) defeats caching silently.
- [ ] S4.3 — Create the gateway chat client with the client's own retries off (S4.1 owns retries) and a timeout.
- [ ] S4.4 — Read-only code tools confined to allowlisted roots: list, read, search; deny secret-bearing names; redact credential-looking lines.
  - Pitfall: resolving `root / "../x"` without checking the resolved path escapes the root.
  - Input: tool name and arguments. Work: validate arguments, resolve path inside a root, read with a byte cap. Output: text or list. Failure: ToolError returned to the model as text. Test: `.env` refused; a password line redacted; `../` refused.
- [ ] S4.5 — The validate-and-retry loop: force a tool call, run code tools, parse output with the schema, run validators, return problems to the model, stop after the rejection or step limit; record tokens, cache hits, retries, rejections.
  - Pitfall: every tool call in a model message needs a tool-result reply, or the next request fails.
- [ ] S4.6 — Agent validators composed from S3 rules, one per agent.

## S5: Workflow
**Traces to:** I5, I6, I7, I8, I15 | **PRD:** Goal, Success criteria 1, 3, 4
**Done when:** a full session runs from setup to export with every pause resumable. | **Depends on:** S4, S6, S7
- [ ] S5.1 — State helpers: known IDs, PRD IDs, feature IDs, and a compact log view for prompts.
- [ ] S5.2 — Runtime context: route roles to models, run an agent and log the call record to the store, read and write the team DoD, glossary, and questionnaire responses; refuse to run without a context.
  - Pitfall: the context is not checkpointed; a resume without it must fail with a message naming the cause.
- [ ] S5.3 — Setup loads the team DoD and glossary; routing picks the mode; the grill loop alternates a model turn and a human pause, recording who answered.
  - Pitfall: calling the model and `interrupt()` in one node re-bills the call on every resume (I7).
- [ ] S5.4 — Mode 2: map the code, show the map, record developer corrections as a correction entry.
- [ ] S5.5 — Mode 3: critique the brief and pause for fixes; write the questionnaire; wait for web-form responses; reconcile new responses only; allow one follow-up round; hand remaining gaps to the live grill.
  - Pitfall: re-reading round-one responses in round two duplicates log entries.
- [ ] S5.6 — The intake gate node: coded gate, then route to the grill (gaps), the DoD (only the DoD missing), or the PRD (pass).
- [ ] S5.7 — The DoD loop: team standard once (saved to the store and shared), then initiative additions; checker problems loop back.
- [ ] S5.8 — The PRD: write core and narrative, number requirements, render; pause for review; only an approver approves (I8); changes bump the version; approval re-renders as Approved.
- [ ] S5.9 — Seams proposed and confirmed by developers, then the spec.
- [ ] S5.10 — Tickets: cut the plan, pause for a person to review (D4), export the CSV and agent prompt on approval, re-cut with feedback on changes.
- [ ] S5.11 — Wiring of all nodes and routers (shipped complete; verify with the end-to-end test).

## S6: Rendering
**Traces to:** C1, C5, D2 | **PRD:** Goal, Success criteria 1
**Done when:** every output file is generated from models through one template each. | **Depends on:** S2, S5.1
- [ ] S6.1 — Intake, session log, and glossary markdown.
- [ ] S6.2 — Questionnaire and DoD markdown.
- [ ] S6.3 — PRD markdown with front matter, and the PDF.
  - Pitfall: Jinja whitespace control can join table rows onto one line; render a fixture and parse its front matter in the test.
- [ ] S6.4 — Spec markdown.
- [ ] S6.5 — Ticket CSV rows: each story, then each feature followed by its tickets; Definition of Done attached by level; story titles from the goal clause.
  - Pitfall: multi-line cells must be written by the csv module, never joined by hand.
- [ ] S6.6 — The tracker agent prompt with the CSV embedded and counts pluralised.

## S7: Persistence
**Traces to:** I6, I16, C4 | **PRD:** Success criteria 3
**Done when:** checkpoints and the store survive a restart. | **Depends on:** S1
- [ ] S7.1 — Register every domain model and the session state with the checkpoint serializer.
  - Pitfall: a hand-written list misses the next new model; generate it from the module.
- [ ] S7.2 — Open Postgres (pool, saver, store, setup) when a database URL is set; otherwise SQLite in a local file.

## S8: Web app
**Traces to:** I8, I12, A3, A4, C2 | **PRD:** Users, Success criteria 4
**Done when:** a PM can run a session in the browser and download the CSV and prompt. | **Depends on:** S5, S7
- [ ] S8.1 — Identity from the SSO header, or the development user; 401 when neither.
- [ ] S8.2 — Background runner: one step at a time per session (lock), errors captured, status derived from the checkpoint.
  - Pitfall: a lock that is never released after an exception leaves the session "working" forever.
- [ ] S8.3 — Session endpoints: list, create (slug and brief validated), get, reply (approver check), retry.
  - Input: JSON bodies. Work: validate, then start or resume through the runner. Output: session status. Failure: 401, 403, 404, 409, 422 with a message. Test: a non-approver's approve returns 403.
- [ ] S8.4 — Questionnaire endpoints: serve the current round; accept responses with known question IDs only; list who answered.
- [ ] S8.5 — Downloads limited to the session's own generated files; usage totals with cache-hit rate.
  - Pitfall: building a file path from the URL without checking the session's file list allows path traversal.
- [ ] S8.6 — Browser UI (shipped complete): every pause kind renders; non-approvers see a disabled Approve button.
