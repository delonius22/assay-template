"""The domain: typed models and code-side ID assignment.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C2 Recorded understanding and C4 Traceable documents. Every
answer, decision, document, and ticket has one declared shape here. Agents must
return these shapes, rules check them, and renderers print them. This file holds
data only; it never validates business rules.

Why this comes now: Settings exist (step 1). Nothing can be validated, stored, or
rendered until the data is defined, and every later module imports from here.

Build order: Step 2 of 33 (package marker; shares step with assay.domain.models).
Previous: src/assay/settings.py (step 1), which defines Settings, the configuration
every later module reads.
Next: src/assay/domain/ids.py (step 3), which assigns every log, question, DoD,
requirement, and ticket ID.

Build these in order:
    1. models: the first module of this package.

Depends on:
    Nothing beyond what its modules import.
    Standard library: none.
    Third-party: none.

Depended on by:
    assay.domain.ids, assay.rules, assay.llm, assay.graph, assay.render, and
    assay.api: every typed value in the system.

Spec coverage: S2.1, S3.2, S5.2, S5.3, S5.4, S5.5, S5.7, S5.8, S5.9, S5.10, S8.4 | Traces to: I1, I2, I3, I15
"""
