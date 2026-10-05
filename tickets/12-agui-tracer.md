# 12 — Tracer bullet: an AG-UI client receives the first question as an interrupt

**What to build:** An AG-UI client posts a run for a new thread with a title and mode. It receives run started, step events as setup and the first grill turn run, a state snapshot, and run finished with an interrupt carrying the first question and its response schema. It resumes with an answer and receives the next interrupt.
**Traces to:** S9.1, S9.2, S9.3, S9.4, S9.5, S9.7
**Blocked by:** 02
**Status:** ready-for-agent
- [ ] A new thread starts a session; the first run ends with outcome "interrupt".
- [ ] Each node produces a step started and a step finished event.
- [ ] A resume with an invalid payload is refused with the reason.
- [ ] Re-requesting a waiting session re-sends the same interrupt ID without running a step.
- [ ] Closing the stream mid-run does not stop the run.

## Context
- I7: a model call and a pause never share a node.
- I18: resume payloads are validated against the pause's response schema.
- D11: own endpoint on the background runner; no ag-ui-langgraph.
- D12: pauses travel as standard interrupts (RUN_FINISHED outcome "interrupt").
- Failure mode: a subscriber joining mid-run misses the end unless it is always published.
