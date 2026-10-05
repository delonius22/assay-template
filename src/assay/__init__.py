"""Assay: grill an idea into a bank-grade PRD, a spec, and a tickets CSV.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C5 Durable sessions and C6 People decide. Where sessions are
stored, which gateway and models to call, and who may approve are deployment facts,
not code. This file owns their shape and how they are read; it never uses them.

Why this comes now: Nothing else can be written or tested without knowing what can
be configured, and configuration depends on nothing in the project.

Build order: Step 1 of 33 (package marker; shares step with assay.settings).
Previous: none. This is the start of the project.
Next: src/assay/domain/models.py (step 2), which defines the typed models every
agent returns and every rule checks.

Build these in order:
    1. settings: the first module of this package.

Depends on:
    Nothing beyond what its modules import.
    Standard library: none.
    Third-party: none.

Depended on by:
    Every module that needs a setting, starting with assay.llm.client,
    assay.store.persistence, assay.graph.context, and assay.api.app.

Spec coverage: S1.1, S1.2 | Traces to: I9, A1, A4
"""
