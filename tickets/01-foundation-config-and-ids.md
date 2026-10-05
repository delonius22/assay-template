# 01 — Foundation: settings and code-assigned IDs

**What to build:** Prefactoring. Settings load from the environment and report what is missing. Every ID the app will ever show — log entries, questions, DoD items, requirements, tickets — is assigned by code, sequentially, and never reused.
**Traces to:** S1.1, S1.2, S2.1, S2.2, S2.3, S2.4, S2.5, S2.6
**Blocked by:** None — can start immediately
**Status:** ready-for-agent
- [ ] Settings load with documented defaults; per-role models fall back to the default model.
- [ ] Missing gateway URL, key, and per-role models are listed by name, never by value.
- [ ] Log entries number per type (D-001, A-001…); superseding marks, never deletes.
- [ ] Withdrawn DoD IDs are never reused.
- [ ] Tickets number T-001… and positions become IDs.
- [ ] All ID and settings contract tests pass.

## Context
- I2: IDs are assigned by code, never by a model, never reused.
- I9: secrets never in logs or messages; report missing settings by name only.
- I15: ticket list order is build order; positions are 1-based.
- Failure mode: off-by-one when converting positions to IDs links the wrong ticket.
