# 14 — A PM runs a whole session in the CopilotKit app

**What to build:** The PM lists sessions, starts one, and watches its steps live. Each pause appears as a card chosen by its kind; the PM answers, approves, or requests changes, and the session moves on. Downloads appear when ready.
**Traces to:** S10.4, S10.5, S10.6
**Blocked by:** 13
**Status:** ready-for-agent
- [ ] Every pause kind renders a card with its own wording.
- [ ] A reply that does not match the response schema is refused before sending.
- [ ] Non-approvers see Approve disabled.
- [ ] Stage progress updates without refreshing.
- [ ] Reopening a session mid-step shows the same pause or progress.

## Context
- I8: only named approvers approve.
- I18: replies match the pause's response schema.
- D12: standard interrupts with response schemas.
- Failure mode: schema-only forms lose the domain wording; pick the card by reason.
