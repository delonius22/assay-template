# Confrontation — rulings

Forge phase 4. The requirements were settled in conversation and in a working
reference implementation, so findings already ruled on are cited, not re-opened.

## Contradictions
- None open. The earlier conflict between "plain business PRD" and "precise enough to cut tickets" was resolved by splitting PRD and spec (ruled in conversation).

## Prior art
- Copilot skills version of the same pipeline exists (pm-grill, to-prd, to-spec, to-tickets). Ruling: build the Python app as the long-term runtime; the skills are retired.

## Scope creep (cut)
- Jira CSV export: cut. Ruling: hand off a CSV plus an agent prompt instead.
- Per-story build prompts: cut. Ruling: one prompt for a tracker-creation agent.
- Answer-sheet parsing by a model: cut. Developers answer in a web form.

## Load-bearing assumptions
- A1 gateway compatibility and tool calling. Test: one gateway request with a tool (ticket 10).
- A2 cache passthrough. Test: two identical calls, compare cached tokens (ticket 10).

## Revised done
- Unchanged: a PM goes from idea to an approved PRD and a tickets CSV plus tracker prompt, with every step saved and resumable.

## Rulings recorded this stage
- 2026-10-05: Mode min; requirements pre-filled from conversation. Nothing re-asked.
- 2026-10-05: Ticket review pause and NFR coverage adopted as recommended defaults (D4, D5). Both were offered and not answered; reverse by deleting S5.10's review step or S3.6's NFR clause.
