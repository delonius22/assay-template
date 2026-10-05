# 09 — Mode 2 maps the existing code safely

**What to build:** A PM changing an existing system starts a mode 2 session. Assay reads the allowlisted code, drafts a current-state map, and pauses for developers to confirm or correct it; corrections are recorded, then grilling starts.
**Traces to:** S4.4, S5.4
**Blocked by:** 02
**Status:** ready-for-agent
- [ ] The map is rejected until at least one file has been read (when code access is configured).
- [ ] Paths outside the allowed roots are refused.
- [ ] Secret-named files are refused and credential-looking lines are redacted.
- [ ] Developer corrections are recorded as a correction entry.

## Context
- I10: code access only inside allowlisted roots; credentials never reach a model.
- Failure mode: resolving a relative path without checking the result escapes the root.
