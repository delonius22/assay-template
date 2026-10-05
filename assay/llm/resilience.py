"""Retry with exponential backoff and jitter, for transient gateway errors only (I11)."""
import logging
import random
import time
from typing import Callable, TypeVar

T = TypeVar("T")
log = logging.getLogger("assay.retry")

TRANSIENT_STATUS = {408, 409, 425, 429, 500, 502, 503, 504}
TRANSIENT_NAMES = {"RateLimitError", "APITimeoutError", "APIConnectionError", "InternalServerError",
                   "ConnectError", "ReadTimeout", "ConnectTimeout", "RemoteProtocolError", "TimeoutError"}


def status_of(exc: BaseException) -> int | None:
    """The HTTP status carried by an exception, if any.

    Spec: S4.1 | Ticket: 10 | Traces to: I11

    Build steps:
    1. Task: Read `code = getattr(exc, "status_code", None)`.
       Expected outcome: OpenAI-client errors expose `status_code`.
    2. Task: If `code is None` and `getattr(exc, "response", None) is not None`, read
       `code = getattr(exc.response, "status_code", None)`.
       Expected outcome: HTTP-library errors expose it on the response.
    3. Task: Return `code if isinstance(code, int) else None`.
       Expected outcome: an int or None, never a string.
    """
    raise NotImplementedError("S4.1")


def is_transient(exc: BaseException) -> bool:
    """True when sending the same request again could succeed.

    Spec: S4.1 | Ticket: 10 | Traces to: I11

    Build steps:
    1. Task: Return True if `status_of(exc) in TRANSIENT_STATUS`.
       Expected outcome: 429 and 5xx retry; 400 and 401 do not.
    2. Task: Otherwise return `any(cls.__name__ in TRANSIENT_NAMES for cls in type(exc).__mro__)`.
       Expected outcome: timeouts and dropped connections retry, matched by class name so no
       client library import is needed.
    """
    raise NotImplementedError("S4.1")


def retry_after_s(exc: BaseException) -> float | None:
    """Seconds from the gateway's Retry-After header, if present and numeric.

    Spec: S4.1 | Ticket: 10 | Traces to: I11

    Build steps:
    1. Task: `headers = getattr(getattr(exc, "response", None), "headers", None) or {}`.
       Expected outcome: a mapping, possibly empty.
    2. Task: `value = headers.get("retry-after") or headers.get("Retry-After")`.
       Expected outcome: the raw header or None.
    3. Task: Return `float(value)` when `value is not None`; return None on `TypeError` or `ValueError`.
       Expected outcome: date-form headers are ignored rather than crashing.
    """
    raise NotImplementedError("S4.1")


def with_backoff(fn: Callable[[], T], *, attempts: int, base_s: float, cap_s: float,
                 sleep: Callable[[float], None] = time.sleep,
                 rand: Callable[[], float] = random.random) -> T:
    """Call fn; on a transient error wait and retry, up to `attempts` calls in total.

    Spec: S4.1 | Ticket: 10 | Traces to: I11

    Build steps:
    1. Task: Loop `for n in range(attempts)`: `return fn()` on success.
       Expected outcome: the first success returns immediately.
    2. Task: On `Exception as exc`: re-raise when `not is_transient(exc)` or `n == attempts - 1`.
       Expected outcome: permanent errors and the final failure surface unchanged.
    3. Task: Compute `wait = min(cap_s, base_s * (2 ** n)) * (0.5 + rand() / 2)`; if
       `(ra := retry_after_s(exc)) is not None`, set `wait = max(wait, min(ra, cap_s))`.
       Expected outcome: exponential, capped, jittered, never shorter than Retry-After.
    4. Task: `log.warning("transient model error (%s); retry %d/%d in %.1fs", type(exc).__name__, n + 1, attempts - 1, wait)`
       then `sleep(wait)`.
       Expected outcome: one log line per retry; tests inject `sleep` to avoid real waits.
    """
    raise NotImplementedError("S4.1")
