# PRD — Assay

## Problem

Product managers at the bank turn vague asks into delivery work by hand.
Questions go unasked, answers are not written down, written answers drift
from what people said, and tickets drift from the written answers. Today's
workaround is meetings plus a PM's notes, then a PRD and tickets written
from memory. It fails because nothing checks coverage, nothing records who
said what, and nothing traces a ticket back to an approved requirement.

## Goal

A PM goes from an idea to an approved PRD, a developer spec, and a CSV of
stories, features, and tickets, plus a prompt that lets a tracker agent
create them. Every requirement traces to a recorded source, and every step
is saved so a session can stop and resume.

## Non-goals

- Pushing directly into Jira or any tracker. The handoff is a CSV and an agent prompt.
- Writing code for tickets. Assay stops at the backlog.
- Deciding whether a regulation applies or is met. Assay flags; Compliance decides.
- Per-ticket build prompts for coding agents. Cut in favour of one tracker prompt.
- Model-based parsing of answer files. Developers answer in a web form.
- Multi-worker deployment. One worker for the pilot (A3).
- Copilot skills. The Python app replaces them.

## Users

- **Product manager:** starts sessions, answers or relays answers, agrees the Definition of Done, downloads outputs.
- **Developer:** answers mode 3 questionnaires in the browser; confirms map corrections and test seams.
- **Approver:** a named person who signs off the PRD.
- **Tracker agent:** receives the CSV and prompt and creates the work items.

## Success criteria

- A full mode 1 session with a fake model produces `tickets.csv` ordered story, feature, its tickets, and an agent prompt that embeds the CSV.
- Three planted model errors (a compound question, an invented source ID, a ticket plan missing a requirement) are each rejected and fixed by retry.
- A session stopped mid-way and resumed after an application restart continues at the same question, on Postgres.
- A non-approver's approval is refused with HTTP 403.
- With the real gateway, the session page reports a cache-hit rate above zero after the second grill turn (tests A2).

## Constraints

- Runs against the bank's OpenAI-compatible model gateway with approved models only.
- Postgres in production; identity from the bank's SSO proxy header.
- The PRD PDF follows the Wells Fargo house style.
- Hierarchy is story, then feature, then ticket.
- Python 3.11+, LangGraph, no Pydantic AI.

## Key assumptions

| ID | Assumption | Risk | How tested |
|---|---|---|---|
| A1 | Gateway is OpenAI-compatible with tool calling | High: the validate loop depends on it | One tool-call request (ticket 10) |
| A2 | Gateway passes cache markers through | Medium: cost, not correctness | Two identical calls compare cached tokens (ticket 10) |
| A3 | One worker carries pilot load | Low | Five concurrent sessions |
| A4 | SSO proxy sets a trusted user header | High: approvals depend on it | Inspect headers behind the proxy |

## Prior art

A Copilot-skills version of the same pipeline exists from earlier work.
Building the app anyway because skills cannot enforce gates, persist
sessions across days, or serve developers a questionnaire form. A complete
reference implementation also exists; this repository is the stubbed
template for implementing it from the spec.
