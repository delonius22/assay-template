"""Retry transient gateway errors with exponential backoff and jitter.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C1 Trustworthy output. Gateways drop connections and
rate-limit. This file decides what to retry and how long to wait; it never knows
what is being called.

Why this comes now: Caching exists (step 10). The call loop (step 13) sends every
request through this.

Build order: Step 11 of 33.
Previous: src/assay/llm/caching.py (step 10), which builds cache-friendly messages
and reads token usage.
Next: src/assay/llm/tools.py (step 12), which gives agents read-only, sandboxed
access to allowlisted code.

Build these in order:
    1. status_of: the smallest piece; is_transient uses it.
    2. is_transient: uses status_of.
    3. retry_after_s: independent.
    4. with_backoff: the public entry; combines the three above.

Depends on:
    Nothing in this project (foundation root). Placed at step 11 because the call
    loop wraps every request in it.
    Standard library: logging, random, time, collections.abc.
    Third-party: none.

Depended on by:
    assay.llm.call: wraps every gateway request.

Spec coverage: S4.1 | Traces to: I11
"""

import logging
import random
import time
from collections.abc import Callable

log = logging.getLogger("assay.retry")
TRANSIENT_STATUS: set[int] = {408, 409, 425, 429, 500, 502, 503, 504}  # S4.1
TRANSIENT_NAMES: set[str] = {  # S4.1: client errors that are safe to retry
    "RateLimitError",
    "APITimeoutError",
    "APIConnectionError",
    "InternalServerError",
    "ConnectError",
    "ReadTimeout",
    "ConnectTimeout",
    "RemoteProtocolError",
    "TimeoutError",
}


def status_of(exc: BaseException) -> int | None:
    """Return the HTTP status an exception carries, if any.

    Problem piece: C1: tell a rate limit from a bad request.

    Why it matters: Retry decisions depend on the status code, and different client
                    libraries put it in different places.

    What: Returns the status from the exception itself or from its response; None
          otherwise. Called as status_of(exc: BaseException) and returns int | None.

    Spec: S4.1 | Ticket: 10 | Traces to: I11

    Build steps:
    1. Task: Look for an integer status code on the exception, then on its response;
             return None when neither has one.
       Expected outcome: An exception carrying status 429 returns 429.
    """
    raise NotImplementedError("S4.1: status_of")


def is_transient(exc: BaseException) -> bool:
    """Return True when sending the same request again could succeed.

    Problem piece: C1: retry only what retrying can fix (I11).

    Why it matters: Retrying a 400 or 401 wastes attempts and delays a clear error;
                    not retrying a 429 fails sessions during brief load spikes.
                    Classifying by status and by error type name avoids importing
                    every client library.

    What: True for TRANSIENT_STATUS codes and for errors whose type or any base type
          is in TRANSIENT_NAMES.

    Spec: S4.1 | Ticket: 10 | Traces to: I11

    Build steps:
    1. Task: Return True for a transient status, or when the error's type or any
             parent type is named in TRANSIENT_NAMES.
       Expected outcome: A 429 is transient; a 400 is not; a timeout error is
                         transient.
    """
    raise NotImplementedError("S4.1: is_transient")


def retry_after_s(exc: BaseException) -> float | None:
    """Return the seconds from a Retry-After header, if present and numeric.

    Problem piece: C1: wait as long as the gateway asks.

    Why it matters: Retrying sooner than the gateway asks guarantees another rate
                    limit. A gateway that says 'wait 30 seconds' will keep refusing
                    anything sooner, so ignoring it burns every remaining attempt.

    What: Returns the numeric Retry-After value from the exception's response
          headers; None otherwise. Called as retry_after_s(exc: BaseException) and
          returns float | None.

    Spec: S4.1 | Ticket: 10 | Traces to: I11

    Build steps:
    1. Task: Read Retry-After (either capitalisation) from the response headers and
             return it as seconds; return None when absent or not a number.
       Think about: What should a date-form Retry-After do?
       Expected outcome: A header of '7' returns 7.0.
    """
    raise NotImplementedError("S4.1: retry_after_s")


def with_backoff[T](
    fn: Callable[[], T],
    *,
    attempts: int,
    base_s: float,
    cap_s: float,
    sleep: Callable[[float], None] = time.sleep,
    rand: Callable[[], float] = random.random,
) -> T:
    """Call fn, retrying transient errors with capped, jittered exponential backoff.

    Problem piece: C1: brief gateway trouble never fails a PM's session (I11).

    Why it matters: Many sessions retrying at the same moments create a thundering
                    herd; jitter spreads them out. A cap keeps a session from
                    waiting minutes. Honouring Retry-After respects the gateway's
                    own advice.

    What: Makes up to 'attempts' calls. After the n-th transient failure waits
          min(cap, base x 2 to the n) scaled by a random 50 to 100 percent, but
          never less than Retry-After. Re-raises permanent errors at once and the
          last error when attempts run out.

    Spec: S4.1 | Ticket: 10 | Traces to: I11

    Build steps:
    1. Task: Return the first successful result; re-raise immediately when the error
             is not transient or no attempts remain.
       Expected outcome: A 400 is raised without any wait.
    2. Task: Compute the wait for the n-th retry as the capped exponential delay
             times a random factor between 0.5 and 1.0, raised to Retry-After when
             that is larger (also capped).
       Think about: Why scale by a random factor at all?
       Expected outcome: With the factor fixed at 1, base 1, two 429s then success
                         wait 1 then 2 seconds.
    3. Task: Log one warning per retry naming the error type, the retry number, and
             the wait, then wait using the injected sleep.
       Expected outcome: Tests observe each wait without real delays.
    """
    raise NotImplementedError("S4.1: with_backoff")
