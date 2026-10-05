"""Create the chat client for one model on the bank's gateway.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C1 Trustworthy output. Every model call goes through the
bank's gateway. This file owns how a client is made; replace only this file if the
gateway is not OpenAI-compatible (A1).

Why this comes now: Fakes prove the loop (steps 10 to 14). The real client comes
after, as the outer boundary.

Build order: Step 15 of 33.
Previous: src/assay/llm/agents.py (step 14), which defines every agent from prompt
files, output shapes, and rule validators.
Next: src/assay/store/persistence.py (step 16), which opens Postgres or SQLite
checkpoints and the shared store.

Build these in order:
    1. make_model: the only function.

Depends on:
    assay.settings: Settings. Gateway URL, key, headers, and timeout.
    Standard library: none.
    Third-party: langchain-core, langchain-openai (imported inside make_model).

Depended on by:
    assay.graph.context: one client per role.

Spec coverage: S4.3 | Traces to: I9, I11, A1
"""

from langchain_core.language_models import BaseChatModel

from assay.settings import Settings


def make_model(model: str, s: Settings) -> BaseChatModel:
    """Return a chat client for one model on the gateway.

    Problem piece: C1: the real boundary behind every agent call.

    Why it matters: Tests never touch the gateway, so the import of the
                    OpenAI-compatible client is kept inside this function. The
                    client's own retries are switched off because retry with backoff
                    already owns retries; two retry layers would multiply waits and
                    hide failures.

    What: An OpenAI-compatible chat client with the gateway URL, key, headers,
          timeout, no client retries, and temperature 0.2.

    Spec: S4.3 | Ticket: 10 | Traces to: I9, I11, A1

    Build steps:
    1. Task: Import the OpenAI-compatible chat client inside the function, then
             create it with the gateway URL, key, extra headers (or none), the
             timeout, zero client retries, and temperature 0.2.
       Think about: Why must the client's own retries be zero?
       Expected outcome: Constructing a client makes no network call; a real call is
                         checked manually (A1).
    """
    raise NotImplementedError("S4.3: make_model")
