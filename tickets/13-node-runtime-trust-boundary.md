# 13 — The Next.js runtime reaches Python, and nothing else can

**What to build:** The Next.js service reads the signed-in user from the SSO header and forwards every AG-UI and REST call to Python with the service token and that user. Python refuses any call without the token.
**Traces to:** S9.6, S10.1, S10.2, S10.3
**Blocked by:** 12
**Status:** ready-for-agent
- [ ] A call to Python without the service token is refused.
- [ ] A user header sent by the browser is ignored; only the SSO proxy's header is forwarded.
- [ ] A request with no signed-in user is refused, except the configured development user.
- [ ] Session, download, usage, and questionnaire calls work through the proxy.

## Context
- I17: Python accepts AG-UI calls only from the Node service.
- A4: the SSO proxy sets a trusted user header.
- ADR 0001: one Next.js service holds the UI and the CopilotKit runtime.
- Failure mode: comparing tokens with ordinary equality leaks timing.
