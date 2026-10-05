# Assay — project template

Assay grills an idea until it holds up, writes a bank-grade PRD and a
developer spec, and cuts the work into **stories, features, and tickets**.
It hands off a CSV and a prompt for the agent that creates the tickets in
your tracker.

This repository is a **stubbed template**. Every function that owns
behavior raises `NotImplementedError("S<x>.<y>")` and carries its build
steps in its docstring. You implement it ticket by ticket until every test
is green.

## Start here

| Read | For |
|---|---|
| `PRD.md` | What and why: problem, goal, non-goals, success criteria |
| `SPECS.md` | Requirements (S-IDs), invariants, data shapes, decision log, build order |
| `specs/assay-spec.md` | User stories and testing decisions |
| `specs/epics.md` | Three epics and their tickets |
| `tickets/` | Eleven tickets with acceptance criteria and context capsules |
| `.project-forge/` | Decomposition (I/A/C IDs), confrontation rulings, stack choices |

## Set up

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
assay check                      # build progress and configuration
LANGGRAPH_STRICT_MSGPACK=true pytest tests/green -q    # must pass now
pytest tests/contract -q         # red until built
assay serve                      # runs now; API answers 501 naming what to build
```

## How to work

1. Pick a **frontier ticket**: one whose "Blocked by" tickets are all done.
   Start with `tickets/01`, then the tracer bullet `tickets/02`.
2. Find every function citing it: `grep -rn "Ticket: 02" assay`.
3. Implement each one from its docstring's build steps, bottom-up **within
   the ticket**. Run the narrowest test after each function.
4. A ticket is done when every function citing it is implemented and its
   contract tests pass. Tick its acceptance criteria.
5. A decision the spec doesn't cover goes in `SPECS.md` under Decision log,
   never only in a code comment.

## Build order

Copied verbatim from `SPECS.md`. Tickets set the order of work; this is the
order within and across them.

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

## Tests

| Folder | State now | Count | What it proves |
|---|---|---|---|
| `tests/green/` | Pass | 22 | Every module imports, the graph compiles, the CLI and server run, prompts, templates, UI, and PDF renderer are valid, data shapes hold |
| `tests/contract/` | Red | 39 | The behavior of every stub. Each fails with `NotImplementedError` naming its S-ID until built. The Postgres restart test is skipped without `ASSAY_TEST_DATABASE_URL`. |
| `tests/ui/` | Pass | 1 script | Every screen renders in a simulated browser (`npm install && npm test`) |

`tests/support/` holds the scripted fake chat model and a full scripted
session. Three of its outputs are wrong on purpose (a compound question,
an invented source ID, a ticket plan missing a requirement); the contract
tests pass only when the rules reject each one and the retry fixes it.

CI (`.github/workflows/ci.yml`) runs the plan validator and the green tests
on every push, and the contract tests against a Postgres service, allowed
to fail until every ticket is done.

## What ships complete (decision D6)

Data shapes (`assay/domain/models.py`), prompts and reference text
(`assay/prompts/`), output templates (`assay/templates/`), the PDF renderer,
the browser UI, the graph wiring, and the app factory. Everything else is
yours to build.

## Open decisions

D4 (a person reviews tickets before export) and D5 (ticket coverage includes
NFRs) are recommended defaults awaiting confirmation. See `SPECS.md`.

## Configuration

Copy `.env.example` to `.env`. You need the gateway URL and key, a model
per role, a Postgres URL for anything shared, approvers, and the code roots
agents may read. Never commit `.env`.
