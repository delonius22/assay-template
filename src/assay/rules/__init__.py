"""Rules as pure functions, used both as agent validators and as stage gates.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C1 Trustworthy output. Some rules apply to every agent's text:
never assert compliance, ask one question at a time, never use unverifiable words.
This file owns those checks; it never decides what happens when they fail.

Why this comes now: IDs exist (step 3). Every stage-specific rule file after this
one reuses these checks, so they come first among the rules.

Build order: Step 4 of 33 (package marker; shares step with assay.rules.common).
Previous: src/assay/domain/ids.py (step 3), which assigns every log, question, DoD,
requirement, and ticket ID.
Next: src/assay/rules/intake.py (step 5), which holds the intake entry rules and the
11-item exit gate.

Build these in order:
    1. common: the first module of this package.

Depends on:
    Nothing beyond what its modules import.
    Standard library: none.
    Third-party: none.

Depended on by:
    assay.llm.agents: the agent validators. assay.graph.nodes: the stage gates.
    assay.rules.dod, prd, spec, tickets.

Spec coverage: S3.1 | Traces to: I1, I4
"""
