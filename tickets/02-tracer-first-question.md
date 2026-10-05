# 02 — Tracer bullet: a PM answers the first question in the browser

**What to build:** A PM opens the web app, starts a mode 1 session, and sees the first grill question with a recommended answer. They answer; Assay records the answer with their name, writes the session log, and shows the next question. Runs on SQLite with a scripted fake model. This is the thinnest path through every layer.
**Traces to:** S3.1, S4.2, S4.5, S4.6, S5.1, S5.2, S5.3, S5.11, S6.1, S7.1, S7.2, S8.1, S8.2, S8.3, S8.6
**Blocked by:** 01
**Status:** ready-for-agent
- [ ] Creating a session returns status "waiting" with a question pending.
- [ ] A compound question from the model is rejected and replaced by a single one.
- [ ] The answer is recorded with the SSO user and a timestamp.
- [ ] The session log file lists entries with their sources.
- [ ] Every model call is logged with tokens and cache reads.
- [ ] A missing runtime context fails with a message naming the cause.

## Context
- I1: model output passes schema and rules before use.
- I4: no generated text asserts compliance.
- I6: every completed step is checkpointed.
- I7: a model call and a human pause never share a node.
- I12: request bodies and slugs are validated at the boundary.
- I16: checkpointed types are registered with the serializer.
- Failure mode: every tool call in a model message needs a tool-result reply.
- Failure mode: an exception inside a run must release the session lock.
