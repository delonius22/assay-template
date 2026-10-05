# Assay — project skeleton

Assay grills an idea until it holds up, writes a bank-grade PRD and a developer spec, and
cuts the work into **stories, features, and tickets**. It hands off a CSV and a prompt for
the agent that creates the tickets in your tracker.

This repository is a **spec-skeleton**: every file and function exists, every import is in
place, and no function body contains logic. Docstrings carry the problem, why each piece
matters, and conceptual build steps. You implement it in build order.

## Two services

| Service | Folder | Language | Build order |
|---|---|---|---|
| Assay service: workflow, agents, REST and AG-UI endpoints | `src/assay/` | Python 3.14 | `BUILD_ORDER.md` (33 steps) |
| Web app: Next.js with CopilotKit and the CopilotKit runtime | `web/` | TypeScript 7 | `web/BUILD_ORDER.md` (12 steps) |

Browsers reach only the web app. The web app calls Python over AG-UI and REST with a shared
service token and the signed-in user (ADR 0001). Build the Python service first.

## Start here

| Read | For |
|---|---|
| `PRD.md` | What and why |
| `SPECS.md` | Requirements (S-IDs), data shapes, decision log (D1 to D16) |
| `CONTEXT.md` | Glossary: session, run, step, stage, pause, story, feature, ticket |
| `docs/adr/` | Decisions that are hard to reverse |
| `tickets/` | Fifteen tickets with acceptance criteria; they set what to build first |
| `BUILD_ORDER.md`, `web/BUILD_ORDER.md` | The order within and across tickets |
| `TRACEABILITY.md`, `web/TRACEABILITY.md` | Every requirement to its file, functions, and tests |

## Set up

```bash
# Python service
uv python install 3.14
uv sync --python 3.14
uv run pytest -q                 # stubs skipped; acceptance tests xfail until built

# Web app
cd web
npm ci
npm run typecheck && npm run lint && npm test
```

## How to work

1. Pick a frontier ticket (all of its "Blocked by" tickets done). Start with `tickets/01`.
2. Find its functions: `grep -rn "Ticket: 02" src web/src`.
3. Build each function from its docstring, in its file's "Build these in order" list.
   Un-skip its stub tests (Python) or turn its `it.todo` entries into tests (web).
4. The ticket is done when its functions are built and its acceptance tests pass rather
   than xfail.
5. A decision the spec does not cover goes in `SPECS.md` under the decision log. Open
   questions are logged in `BUILD_ORDER.md` (OQ-1 is open now).

## Tests

| Where | Now | Purpose |
|---|---|---|
| `tests/<package>/test_*.py` | 262 skipped | One per build-step outcome; the checklist for each function |
| `tests/acceptance/` | 44 xfail | End-to-end behaviour. A stub raising NotImplementedError is reported as "not built yet: S<x>.<y>"; any other error fails |
| `web/test/` | 35 todo | One per build-step outcome in the web app |

## Checks (run in CI)

```bash
uv run ruff check . && uv run ruff format --check .
uv run mypy src
uv run python .plan-conductor/check_skeleton.py . --lang python --python .venv/bin/python
uv run python .plan-conductor/validate_chain.py .
cd web && npm run typecheck && npm run lint && python ../.plan-conductor/check_skeleton.py . --lang typescript
```

## What ships complete

Data shapes, prompt and reference text (`src/assay/prompts/`), output templates
(`src/assay/templates/`), and the vendored PDF renderer (`src/assay/vendor/`). Everything
else is a stub (D14, D15).

## Configuration

Python: copy `.env.example` to `.env`. Web: set `ASSAY_PYTHON_URL`, `ASSAY_SERVICE_TOKEN`
(the same value as Python's), and `ASSAY_USER_HEADER` to the header your SSO proxy sets.
Never commit secrets.
