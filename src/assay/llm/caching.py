"""Build cache-friendly messages and read token usage.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C1 Trustworthy output. Agent calls repeat the same
instructions every turn. This file orders messages so the repeated part can be
cached, and reads back how much was cached; it never calls a model.

Why this comes now: The rules exist (steps 4 to 9). The call loop (step 13) needs
both functions.

Build order: Step 10 of 33.
Previous: src/assay/rules/tickets.py (step 9), which holds the ticket plan rules.
Next: src/assay/llm/resilience.py (step 11), which retries transient gateway errors
with backoff.

Build these in order:
    1. build_messages: the smallest piece of the model layer.
    2. usage_of: independent of build_messages.

Depends on:
    Nothing in this project (foundation root for the model layer). Placed at step 10
    because the call loop builds every request with it.
    Standard library: none.
    Third-party: langchain-core.

Depended on by:
    assay.llm.call: builds messages and records usage.

Spec coverage: S4.2 | Traces to: A2
"""

from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage


def build_messages(static: str, dynamic: str, mode: str) -> list[BaseMessage]:
    """Return a system message with the static text, then a human message with the dynamic text.

    Problem piece: C1: every agent call ordered so its unchanging prefix can be
                   cached (A2).

    Why it matters: Providers cache the longest prefix that matches a recent
                    request. If anything that changes per call sits before the
                    instructions, nothing is cached and every grill turn pays for
                    the full reference text again.

    What: In 'explicit' mode the static text carries a cache marker; in 'auto' and
          'off' it is plain. The dynamic text always comes last.

    Spec: S4.2 | Ticket: 02 | Traces to: A2

    Build steps:
    1. Task: Put the static text in the system message; in explicit mode wrap it as
             one text block carrying the cache-control marker {'type': 'ephemeral'}.
       Think about: What would happen to caching if a date were added to the static
                    text?
       Expected outcome: In explicit mode only the system message carries the
                         marker.
    2. Task: Return the system message followed by a human message holding the
             dynamic text.
       Expected outcome: The dynamic text is always the last message.
    """
    raise NotImplementedError("S4.2: build_messages")


def usage_of(message: object) -> dict[str, int]:
    """Return token counts from one model response, including cache reads.

    Problem piece: C1: proof that caching works.

    Why it matters: Without reading cached tokens back, nobody can tell whether the
                    gateway honours caching (A2). Gateways report usage in slightly
                    different shapes, so missing fields must count as zero rather
                    than crash a call.

    What: Input, output, cache-read, and cache-write tokens; zeros when the response
          has no usage. Called as usage_of(message: object) and returns dict[str,
          int].

    Spec: S4.2 | Ticket: 10 | Traces to: A2

    Build steps:
    1. Task: Read the response's usage, treating a missing value as empty, and
             return the four counts as integers: input_tokens, output_tokens,
             cache_read_tokens (from the input details' cache_read),
             cache_write_tokens (from cache_creation).
       Expected outcome: A response reporting 800 cached input tokens returns
                         cache_read_tokens 800.
    """
    raise NotImplementedError("S4.2: usage_of")
