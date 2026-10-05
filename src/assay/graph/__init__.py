"""The workflow: state, runtime context, nodes, and wiring.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C5 Durable sessions. A paused session is only as complete as
its saved state. This file defines that state and small views of it; it holds no
clients or settings, because state is saved as data.

Why this comes now: Persistence (step 16) can save it; renderers (18, 19) and nodes
(21 to 26) read it.

Build order: Step 17 of 33 (package marker; shares step with assay.graph.state).
Previous: src/assay/store/persistence.py (step 16), which opens Postgres or SQLite
checkpoints and the shared store.
Next: src/assay/render/csv_export.py (step 18), which writes the tickets CSV rows.

Build these in order:
    1. state: the first module of this package.

Depends on:
    Nothing beyond what its modules import.
    Standard library: none.
    Third-party: none.

Depended on by:
    assay.graph.context, assay.graph.nodes, assay.graph.build,
    assay.render.markdown, assay.api.

Spec coverage: S5.1 | Traces to: I6
"""
