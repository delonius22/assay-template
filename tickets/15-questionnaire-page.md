# 15 — Developers answer the questionnaire in the web app

**What to build:** A developer opens the questionnaire link, signs in through SSO, confirms or corrects each proposed answer, and submits. The PM sees who answered.
**Traces to:** S10.7
**Blocked by:** 13, 08
**Status:** ready-for-agent
- [ ] The current round's questions and follow-ups render.
- [ ] Unknown question IDs are refused by the server and the reason shown.
- [ ] Resubmitting replaces the developer's earlier answers.

## Context
- I12: submissions are validated against the session's question IDs.
- D13: a plain React page, no CopilotKit components.
