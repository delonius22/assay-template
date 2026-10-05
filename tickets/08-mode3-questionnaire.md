# 08 — Developers answer a questionnaire in the browser

**What to build:** A PM with a clear brief starts a mode 3 session. Assay critiques the brief, writes a questionnaire, and shows the PM a link. Developers open it, confirm or correct each proposed answer, and submit. The PM continues; Assay reconciles the new answers, runs at most one follow-up round, and hands remaining gaps to the live grill.
**Traces to:** S5.5, S8.4, S2.3, S6.2
**Blocked by:** 03
**Status:** ready-for-agent
- [ ] Unknown question IDs in a submission return 422.
- [ ] Continuing with no responses keeps waiting and says why.
- [ ] Round-two reconciliation reads only new responses.
- [ ] Remaining blocking gaps go to the live grill.

## Context
- I12: submissions are validated against the session's question IDs.
- Failure mode: re-reading round-one responses duplicates log entries.
