# 03 — The intake gate decides when intake is done

**What to build:** After the grill agent says it is done, Assay checks the 11-item exit gate on typed fields. Gaps send the PM back to the grill with the gaps listed; a missing Definition of Done sends them to the DoD stage; a pass moves on.
**Traces to:** S3.2, S5.6
**Blocked by:** 02
**Status:** ready-for-agent
- [ ] A log whose wording says "out of scope" but whose scope flag says "in" fails the scope item.
- [ ] Entries missing required flags are rejected while the agent is writing.
- [ ] An open blocking question keeps the gate shut.
- [ ] The intake file shows every gate item ticked or unticked with the reason.

## Context
- I5: a stage advances only when its gate passes.
- D2: rules check typed fields, never text.
- Failure mode: word-matching lets phrasing pass the gate.
