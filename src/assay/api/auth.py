"""Read the signed-in user from the SSO proxy's header.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C6 People decide. Every answer and approval is attributed to a
person. This file owns who that is; it never handles passwords.

Why this comes now: The workflow is complete (steps 1 to 27). The web layer starts
with identity.

Build order: Step 28 of 33.
Previous: src/assay/graph/build.py (step 27), which wires every node and edge of the
workflow.
Next: src/assay/api/runner.py (step 29), which runs sessions in the background and
publishes each run's progress.

Build these in order:
    1. user_from: the only function.

Depends on:
    Nothing in this project (foundation root for the web layer). Placed at step 28
    because every endpoint attributes requests to a user.
    Standard library: none.
    Third-party: fastapi.

Depended on by:
    assay.api.app: every route.

Spec coverage: S8.1 | Traces to: I8, A4
"""

from fastapi import HTTPException, Request


def user_from(request: Request, header: str, dev_user: str) -> str:
    """Return the signed-in user's ID.

    Problem piece: C6: no anonymous answers or approvals.

    Why it matters: Approvals and the audit trail depend on knowing who acted. The
                    SSO proxy sets a trusted header (A4); the development user
                    exists only so local runs work without a proxy.

    What: The trimmed header value, else the development user, else HTTP 401. Called
          as user_from(request: Request, header: str, dev_user: str) and returns
          str.

    Spec: S8.1 | Ticket: 02 | Traces to: I8, A4

    Raises:
        HTTPException: 401 'Not signed in: missing <header> header from the SSO
        proxy.'

    Build steps:
    1. Task: Use the trimmed header value, falling back to the development user;
             refuse with 401 and the message above when both are empty.
       Expected outcome: A request with no header and no development user gets 401.
    """
    raise NotImplementedError("S8.1: user_from")
