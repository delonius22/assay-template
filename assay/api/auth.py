"""Identity comes from the bank's SSO proxy header (A4). The app never handles passwords."""
from fastapi import HTTPException, Request


def user_from(request: Request, header: str, dev_user: str) -> str:
    """The signed-in user ID.

    Spec: S8.1 | Ticket: 02 | Traces to: I8, A4

    Build steps:
    1. Task: `user = request.headers.get(header, "").strip() or dev_user`.
       Expected outcome: the SSO header wins; the development user is the fallback.
    2. Task: If `not user`, raise `HTTPException(401, f"Not signed in: missing {header} header from the SSO proxy.")`.
       Expected outcome: no anonymous access.
    3. Task: Return `user`.
       Expected outcome: recorded on every answer and approval.
    """
    user = request.headers.get(header, "").strip() or dev_user
    if not user:
        raise HTTPException(401, f"Not signed in: missing {header} header from the SSO proxy.")
    return user
