"""The model layer: caching, retries, code tools, the validated call loop, agents, and the client.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C1 Trustworthy output. Agent calls repeat the same
instructions every turn. This file orders messages so the repeated part can be
cached, and reads back how much was cached; it never calls a model.

Why this comes now: The rules exist (steps 4 to 9). The call loop (step 13) needs
both functions.

Build order: Step 10 of 33 (package marker; shares step with assay.llm.caching).
Previous: src/assay/rules/tickets.py (step 9), which holds the ticket plan rules.
Next: src/assay/llm/resilience.py (step 11), which retries transient gateway errors
with backoff.

Build these in order:
    1. caching: the first module of this package.

Depends on:
    Nothing beyond what its modules import.
    Standard library: none.
    Third-party: none.

Depended on by:
    assay.llm.call: builds messages and records usage.

Spec coverage: S4.2 | Traces to: A2
"""
