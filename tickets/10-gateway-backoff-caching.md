# 10 — The real gateway, with retry and prompt caching

**What to build:** Assay calls the bank's gateway. Transient errors retry with backoff; permanent errors fail at once. The session page shows how much input was served from cache.
**Traces to:** S4.1, S4.3, S4.2, S8.5
**Blocked by:** 02
**Status:** ready-for-agent
- [ ] A 429 twice then success waits base, then twice base.
- [ ] A 400 is raised without waiting.
- [ ] Retry-After is honoured.
- [ ] Explicit cache mode marks only the static prefix.
- [ ] Manual check (A1, A2): one real tool-call request succeeds; a repeated call reports cached tokens.

## Context
- I11: timeouts and bounded retries; transient errors only.
- I9: the gateway key comes from the environment, never logs.
- A1: the gateway is OpenAI-compatible with tool calling.
- A2: the gateway passes cache markers through.
