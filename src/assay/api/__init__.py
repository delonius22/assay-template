"""The web layer: identity, the session runner, the AG-UI endpoint, and the REST app.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C6 People decide. Every answer and approval is attributed to a
person. This file owns who that is; it never handles passwords.

Why this comes now: The workflow is complete (steps 1 to 27). The web layer starts
with identity.

Build order: Step 28 of 33 (package marker; shares step with assay.api.auth).
Previous: src/assay/graph/build.py (step 27), which wires every node and edge of the
workflow.
Next: src/assay/api/runner.py (step 29), which runs sessions in the background and
publishes each run's progress.

Build these in order:
    1. auth: the first module of this package.

Depends on:
    Nothing beyond what its modules import.
    Standard library: none.
    Third-party: none.

Depended on by:
    assay.api.app: every route.

Spec coverage: S8.1 | Traces to: I8, A4
"""
