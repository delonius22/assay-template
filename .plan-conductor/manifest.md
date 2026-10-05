# Plan Conductor — Assay

## Classification
tier: L (score 6: horizon 2, handoff 1, decisions 1, reversibility 2)
field: green  idea: certain  mode: min
tracker: none  parent: specs/assay-spec.md

## Rulings
- 2026-10-05: Mode min at the user's request ("just the project template"). Requirements pre-filled from the conversation and the working reference implementation; nothing re-asked.
- 2026-10-05: A5: "stubbed db" read as a stubbed repository.
- 2026-10-05: Forge §1–2 skipped (written spec existed); §4 rulings carried from conversation (.project-forge/confrontation.md); §7 skipped (min mode).
- 2026-10-05: Test seams carried from the reference implementation's suite; not re-asked.
- 2026-10-05: D4 (ticket review) and D5 (NFR coverage) adopted as recommended defaults; awaiting user confirmation.
- 2026-10-05: No tracker configured; tickets written as local files (one per ticket). Granularity quiz deferred to hand-over.

## Chain
- [x] forge — artifacts: PRD.md, SPECS.md, .project-forge/
- [x] to-spec — artifacts: specs/assay-spec.md, specs/epics.md
- [x] to-tickets — artifacts: tickets/01 to tickets/11
- [x] skeleton — artifacts: assay/, tests/, README.md

## Scope 2 — AG-UI (opened 2026-10-05)
tier: L (score 6: horizon 2, handoff 1, decisions 2, reversibility 1) — raised from M by the CopilotKit ruling
field: brown  idea: certain  mode: min
Chain: grill-docs → forge §3–6 (seeded from grill) → to-spec → to-tickets → skeleton (spec-skeleton; replaces planf3 by ruling)
- [x] grill-docs — artifacts: CONTEXT.md, docs/adr/0001-copilotkit-with-node-runtime.md
- [x] forge §3–6 — artifacts: PRD.md, SPECS.md (S9, S10, D10–D16), .project-forge/decomposition.md
- [x] to-spec — artifacts: specs/assay-spec.md (Epic D), specs/epics.md
- [x] to-tickets — artifacts: tickets/12 to tickets/15
- [x] skeleton — artifacts: src/, tests/, BUILD_ORDER.md, TRACEABILITY.md, web/
Research findings (verified against installed packages):
- ag-ui-protocol 1.0.0 has standard interrupts: RUN_FINISHED outcome "interrupt" with Interrupt(id, reason, message, response_schema); resume via RunAgentInput.resume (ResumeEntry: interrupt_id, status, payload).
- ag-ui-langgraph 0.0.46 builds LangGraph context as a dict from the request; it cannot pass AppContext. Standard interrupt outcome is off by default (emit_interrupt_outcome=False).
- The adapter streams the graph inside the HTTP request; Assay runs steps in the background (S8.2).
- CopilotKit production path: React app → CopilotKit Runtime (Node.js, /api/copilotkit) → HttpAgent → Python AG-UI endpoint. Direct connection exists only as `agents__unsafe_dev_only`: unsupported, no server-side middleware, auth entirely on the caller.
Rulings:
- 2026-10-05: Frontend is CopilotKit (user). Reverses C2 (one HTML page, no build step). The vanilla page is retired when the CopilotKit app reaches parity.
Grill (stage: done):
- [x] G1: Node.js runtime service accepted — yes: one Next.js app (UI + CopilotKit runtime) behind SSO, forwarding user ID; Python accepts calls only from it. ADR 0001.
- [x] G2: Own AG-UI endpoint on the background runner (user: "for sure"). Built on ag-ui-protocol 1.0 core types only; ag-ui-langgraph is not a dependency. Keeps S8.2 background steps and AppContext injection.
- [x] G3: Questionnaire is an ordinary React page in the Next.js app (no CopilotKit components), submitting through a Next.js route to S8.4 (user accepted recommendation).
- [x] G4: Glossary resolved in CONTEXT.md: session = AG-UI thread; run = one execution from start or resume to the next pause, finish, or error; step = one graph node; pause = AG-UI interrupt (user accepted recommendation).
- 2026-10-05: Skeleton regenerated with spec-skeleton (user). Its conventions govern code and test stubs; planf3 is replaced by spec-skeleton build steps in docstrings. Existing behavior tests kept as an acceptance suite.
- 2026-10-05: Python baseline 3.14 (3.15.0 final scheduled 2026-10-09, not yet released). Web: TypeScript 7.0.2, Next.js 16.3, React 19.3, CopilotKit 1.77, @ag-ui/client 1.0.2.

## Decision log
→ SPECS.md#decision-log
