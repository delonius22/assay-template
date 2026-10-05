"""Persistence: checkpoints and the shared store.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C5 Durable sessions. Sessions must survive a closed tab or a
restart. This file opens storage and registers saved types; it never decides what is
saved.

Why this comes now: Models (step 2) define what is saved and Settings (step 1) say
where. The workflow needs storage before it can pause.

Build order: Step 16 of 33 (package marker; shares step with assay.store.persistence).
Previous: src/assay/llm/client.py (step 15), which creates the gateway chat client.
Next: src/assay/graph/state.py (step 17), which defines AssayState, the session
saved after every step.

Build these in order:
    1. persistence: the first module of this package.

Depends on:
    Nothing beyond what its modules import.
    Standard library: none.
    Third-party: none.

Depended on by:
    assay.api.app: opens persistence at startup.

Spec coverage: S7.1, S7.2 | Traces to: I6, I16
"""
