# Assay — spec

Parent for every ticket. No tracker is configured, so this file is the
parent reference.

## Problem Statement

As a product manager, I turn vague asks into delivery work by hand. I miss
questions, I lose track of who said what, and my tickets drift from what
was approved. Reviewers cannot trace a ticket back to a decision.

## Solution

I start a session in the browser. Assay grills me (and, through me or a web
form, the developers) one question at a time and records every answer with
its source. It will not move on until the intake is complete. It agrees a
Definition of Done with me, writes a PRD that an approver signs, writes a
developer spec against seams the developers confirm, and cuts stories,
features, and tickets that I review. I download a CSV and a prompt that a
tracker agent uses to create the tickets. I can stop at any point and
resume later.

## User Stories

### Epic A — Core pipeline
1. As a PM, I want to start a session by naming what I am building and how much is known, so that Assay picks the right method.
2. As a PM, I want one question at a time with a recommended answer, so that I can confirm quickly instead of starting cold.
3. As a PM, I want to paste what the developers said, so that their discussion is recorded without me rewriting it.
4. As a PM, I want Assay to push back on weak answers, so that the PRD does not rest on them.
5. As a PM, I want the session to refuse to write a PRD until every area is covered, so that gaps surface early.
6. As a PM, I want to agree the team's Definition of Done once and reuse it, so that every initiative starts from the same bar.
7. As a PM, I want initiative-specific additions to the Definition of Done, so that special sign-offs are not forgotten.
8. As an approver, I want a PRD in the bank's house style with every requirement traced to a source, so that I can sign it with confidence.
9. As an approver, I want only named approvers able to approve, so that sign-off means something.
10. As a PM, I want to request changes and get a new PRD version, so that review is iterative and versioned.
11. As a developer, I want to confirm the test seams before the spec is written, so that tickets are testable.
12. As a PM, I want to review the cut tickets before export, so that nothing leaves Assay unreviewed.
13. As a PM, I want a CSV ordered story, then feature, then its tickets, so that the hierarchy is obvious.
14. As a PM, I want a prompt for a tracker agent with the CSV embedded, so that creating the tickets is one handoff.
15. As a reviewer, I want every ticket traced to requirements and every requirement covered, so that nothing is dropped.

### Epic B — Input modes
16. As a PM with a clear brief, I want a questionnaire developers answer in the browser, so that I do not have to schedule a meeting.
17. As a developer, I want each question to show a proposed answer, so that I can confirm or correct quickly.
18. As a PM, I want only blocking gaps to trigger a follow-up round, and at most one, so that developers are not asked forever.
19. As a PM changing an existing system, I want Assay to map the current code first, so that we argue about the gap, not about how it works today.
20. As a security reviewer, I want agents to read only allowlisted code and never see secrets, so that code access is safe.

### Epic C — Production readiness
21. As an operator, I want gateway calls retried with backoff on transient errors only, so that brief outages do not fail sessions.
22. As an operator, I want prompt caching and a per-session cache-hit rate, so that I can see cost savings working.
23. As a PM, I want my session saved after every step in Postgres, so that a restart or a week away loses nothing.

## Implementation Decisions

- Typed models are the source of truth; files are generated only (D2). Shapes per SPECS ## Data shapes.
- Rules are pure functions used both as agent validators and as stage gates (S3, S4.6, S5.6).
- The model loop forces a tool call and returns rule problems to the model (S4.5, D3).
- A model call and a human pause never share a node (I7, S5).
- Ticket order is build order (D8, S3.6, S2.6).
- Stubs raise NotImplementedError with their S-ID; the web app answers 501 (D7).

## Testing Decisions

Seams, carried from the reference implementation's tests (ruled; not re-asked):
1. Rules as pure functions: call them on models.
2. The compiled graph invoked with a scripted fake chat model, in-memory checkpoints, and an in-memory store.
3. The HTTP API through a test client with the same fake model.

Good tests assert external behavior only: returned problems, files produced, statuses, HTTP codes. No network and no credentials (I13). The Postgres restart test runs only when a test database URL is set.

## Out of Scope

- Pushing directly into Jira or any tracker. The handoff is a CSV and an agent prompt.
- Writing code for tickets. Assay stops at the backlog.
- Deciding whether a regulation applies or is met. Assay flags; Compliance decides.
- Per-ticket build prompts for coding agents. Cut in favour of one tracker prompt.
- Model-based parsing of answer files. Developers answer in a web form.
- Multi-worker deployment. One worker for the pilot (A3).
- Copilot skills. The Python app replaces them.

## Further Notes

D4 (ticket review) and D5 (NFR coverage) are recommended defaults awaiting confirmation.
