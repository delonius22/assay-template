# 05 — An approver signs a traced PRD

**What to build:** Assay writes the PRD (stories with their features, requirements, narrative), renders markdown and the house-style PDF, and pauses for review. A named approver approves; anyone may request changes, which produce a new version. On approval the PDF is re-rendered as Approved.
**Traces to:** S3.4, S5.8, S6.3
**Blocked by:** 04
**Status:** ready-for-agent
- [ ] A requirement citing an unknown source is rejected and fixed by retry.
- [ ] Features number F-01… across all stories.
- [ ] A non-approver's approval is refused and the review pause repeats with the reason.
- [ ] Requesting changes bumps the version from 0.1 to 0.2.
- [ ] The PDF opens and shows Approved after sign-off.

## Context
- I3: every requirement cites a known source ID.
- I4: no compliance assertions.
- I8: only a named approver may approve.
- Failure mode: template whitespace control joins table rows onto one line.
