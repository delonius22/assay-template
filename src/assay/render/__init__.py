"""Outputs: markdown from templates, the PRD PDF, and the tickets CSV.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C4 Traceable documents. The CSV is the handoff a tracker agent
imports. This file owns its rows and columns; it never decides what tickets exist.

Why this comes now: State exists (step 17). The markdown renderer (step 19) embeds
this CSV in the agent prompt.

Build order: Step 18 of 33 (package marker; shares step with assay.render.csv_export).
Previous: src/assay/graph/state.py (step 17), which defines AssayState, the session
saved after every step.
Next: src/assay/render/markdown.py (step 19), which writes every markdown artifact,
the PDF, and the tracker prompt.

Build these in order:
    1. csv_export: the first module of this package.

Depends on:
    Nothing beyond what its modules import.
    Standard library: none.
    Third-party: none.

Depended on by:
    assay.render.markdown: the CSV file and the prompt that embeds it.

Spec coverage: S6.5 | Traces to: C6
"""
