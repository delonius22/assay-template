"""Graph nodes by stage. Model calls and pauses never share a node (I7).

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C6 People decide. Replies, file lists, and intake files are
handled the same way in every stage. This file owns those helpers.

Why this comes now: Context (20), state (17), and the markdown writer (19) exist;
every node file imports these.

Build order: Step 21 of 33 (package marker; shares step with assay.graph.nodes.shared).
Previous: src/assay/graph/context.py (step 20), which defines AppContext, the
run-time dependencies injected into every node.
Next: src/assay/graph/nodes/intake.py (step 22), which runs intake: setup, the three
modes, the grill loop, and the gate.

Build these in order:
    1. shared: the first module of this package.

Depends on:
    Nothing beyond what its modules import.
    Standard library: none.
    Third-party: none.

Depended on by:
    Every node module.

Spec coverage: S5.3, S6.1 | Traces to: I12
"""
