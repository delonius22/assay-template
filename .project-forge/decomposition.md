# Decomposition — Assay

## Invariants (true however it is built)

- I1 — A language model sometimes returns confident, wrong output. Every model output must pass a typed schema and the rules before anything uses it.
- I2 — IDs are assigned by code, never by a model, and never reused. People and trackers refer to them.
- I3 — A PRD requirement is only trustworthy if it cites a recorded source, so every requirement cites a known log or questionnaire ID.
- I4 — Only Compliance can say a regulation is met. No generated text asserts compliance.
- I5 — A stage advances only when its gate passes.
- I6 — People stop mid-session. Every completed step is persisted, and a resume continues at the same step.
- I7 — A paused LangGraph node reruns from its first line on resume, so a model call and a human pause never share a node.
- I8 — Only a named approver may approve a PRD.
- I9 — Secrets never appear in code, on the command line, or in logs. The gateway key comes from the environment.
- I10 — Agents may read code only inside allowlisted directories, and a credential-looking line never reaches a model.
- I11 — Every gateway call has a timeout and bounded retries; only transient errors are retried.
- I12 — External input (request bodies, slugs, question IDs, file names) is validated at the boundary and fails loudly.
- I13 — Tests need no network and no credentials.
- I14 — Dependencies are pinned.
- I15 — Ticket list order is build order, and dependencies point only backward, so dependency cycles cannot exist.
- I16 — Checkpointed custom types are registered with the serializer, so saved sessions still load after an upgrade.

## Assumptions (believed; could be false)

- A1 — The bank's model gateway is OpenAI-compatible and supports tool calling. Cheapest check: one request with one tool through the gateway.
- A2 — The gateway passes prompt-cache markers through and reports cached tokens. Check: two identical calls; the second reports cache reads.
- A3 — One web worker carries pilot load. Check: run five sessions at once and watch latency.
- A4 — The SSO proxy sets a trusted user-ID header on every request. Check: inspect headers behind the proxy.
- A5 — "Stubbed db" in the request means a stubbed repository, not a database.

## Inherited conventions (true only because it is how it is done)

- C1 — Outputs are markdown, PDF, and CSV, because people, agents, and trackers all read text.
- C2 — A FastAPI web app with one HTML page.
- C3 — LangGraph for the workflow; langchain-core for model calls.
- C4 — Postgres for checkpoints and shared records; SQLite for local development.
- C5 — The PRD PDF follows the Wells Fargo house style.
- C6 — Hierarchy: story, then feature, then ticket.

## Dependency structure

Configuration → identity assignment and rules (pure leaves) → model layer (fakes first) → persistence → workflow nodes → wiring → web app. Every requirement in SPECS.md traces to these IDs.
