# Epics

## Epic A — Core pipeline
Theme: one mode 1 session runs from first question to exported CSV and prompt.
Done when: tickets 01 to 07 are done and the end-to-end flow test passes.
Members (dependency order): 01, 02, 03, 04, 05, 06, 07.
Trace: PRD Goal and success criteria 1, 2, 4; S1–S3, S4.2, S4.5, S4.6, S5.1–S5.3, S5.6–S5.11, S6, S7.1, S8.1–S8.3, S8.5, S8.6.

## Epic B — Input modes
Theme: modes 2 and 3 feed the same intake gate.
Done when: tickets 08 and 09 are done; the mode 3 web-form test and the code-tool test pass.
Members: 08, 09.
Trace: PRD Users; S4.4, S5.4, S5.5, S8.4.

## Epic C — Production readiness
Theme: the real gateway and Postgres.
Done when: tickets 10 and 11 are done; the backoff tests and the Postgres restart test pass.
Members: 10, 11.
Trace: PRD success criteria 3 and 5; S4.1, S4.3, S7.2.

## Epic D — Live web app (AG-UI and CopilotKit)
Theme: a PM and developers use Assay through the CopilotKit app, live, over AG-UI.
Done when: tickets 12 to 15 are done; the AG-UI acceptance tests pass; a full session runs in the browser.
Members (dependency order): 12, 13, 14, 15.
Trace: PRD success criterion 6; S9, S10.
