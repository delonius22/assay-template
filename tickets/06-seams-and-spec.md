# 06 — Developers confirm seams, then the spec is written

**What to build:** Assay proposes test seams and pauses for developers to confirm or correct them, then writes the developer spec with a coverage table mapping every PRD requirement to spec sections.
**Traces to:** S3.5, S5.9, S6.4
**Blocked by:** 05
**Status:** ready-for-agent
- [ ] Corrections re-propose the seams; approval moves on.
- [ ] A spec missing a requirement in coverage is rejected and fixed.
- [ ] The spec file lists modules, interfaces, security, and coverage.

## Context
- I1: model output passes schema and rules before use.
- Seams favour the highest stable boundary; fewer is better.
