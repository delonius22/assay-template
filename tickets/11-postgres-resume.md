# 11 — Sessions survive a restart on Postgres

**What to build:** With a database URL set, checkpoints and shared records live in Postgres. A PM stops mid-session; the application restarts with fresh connections; the PM resumes at the same question.
**Traces to:** S7.2
**Blocked by:** 02
**Status:** ready-for-agent
- [ ] Tables are created on startup if missing.
- [ ] The restart test passes against a real database.
- [ ] Saved sessions load in strict deserialization mode.

## Context
- I6: every completed step is persisted.
- I16: checkpointed types are registered with the serializer.
