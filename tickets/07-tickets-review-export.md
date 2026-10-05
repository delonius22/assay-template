# 07 — Tickets are reviewed and exported as a CSV and tracker prompt

**What to build:** Assay cuts tickets for every feature in build order, pauses for the PM to review them, and on approval writes the tickets CSV (each story, then each feature followed by its tickets) and the tracker agent prompt with the CSV embedded. The PM downloads both from the session page.
**Traces to:** S3.6, S5.10, S6.5, S6.6, S8.5
**Blocked by:** 06
**Status:** ready-for-agent
- [ ] A plan missing an FR or NFR is rejected unless listed as uncovered with a reason.
- [ ] A ticket depending on a later ticket is rejected.
- [ ] Requesting changes re-cuts the tickets with the feedback.
- [ ] CSV rows run S-01, F-01, its tickets, F-02, its tickets.
- [ ] Definition of Done items attach by level.
- [ ] Downloads outside the session's own files return 404.

## Context
- I15: list order is build order; dependencies point backward only.
- D4: a person reviews tickets before export.
- D5: coverage includes NFR IDs.
- Failure mode: multi-line cells must be written by the csv module.
