"""Model layer: retry with backoff, prompt caching, and call records."""

import pytest
from langchain_core.messages import SystemMessage

from assay.llm.agents import agent
from assay.llm.caching import build_messages
from assay.llm.call import Limits, call
from assay.llm.resilience import is_transient, with_backoff
from assay.llm.tools import Deps
from tests.support.fakes import USAGE, ScriptedChat
from tests.support.script import script


class Gateway429(Exception):
    """Test helper: Gateway429."""

    status_code = 429


class Gateway400(Exception):
    """Test helper: Gateway400."""

    status_code = 400


def test_backoff_retries_transient_errors_with_growing_waits():
    """Backoff retries transient errors with growing waits.

    Spec: S4.1 | Traces to: I11
    Expected outcome: two 429s then success wait 1 then 2 seconds.
    """
    calls, waits = [], []

    def flaky():
        """Test helper: flaky."""
        calls.append(1)
        if len(calls) < 3:
            raise Gateway429("rate limited")
        return "ok"

    assert (
        with_backoff(flaky, attempts=5, base_s=1, cap_s=30, sleep=waits.append, rand=lambda: 1.0)
        == "ok"
    )
    assert waits == [1.0, 2.0]  # base * 2^n, full jitter factor in this test


def test_backoff_never_retries_permanent_errors():
    """Backoff never retries permanent errors.

    Spec: S4.1 | Traces to: I11
    Expected outcome: a 400 is raised with no wait.
    """
    waits = []
    with pytest.raises(Gateway400):
        with_backoff(
            lambda: (_ for _ in ()).throw(Gateway400("bad request")),
            attempts=5,
            base_s=1,
            cap_s=30,
            sleep=waits.append,
        )
    assert waits == []


def test_backoff_honours_retry_after():
    """Backoff honours retry after.

    Spec: S4.1 | Traces to: I11
    Expected outcome: a Retry-After of 7 waits 7 seconds.
    """

    class WithHeader(Exception):
        """Test helper: WithHeader."""

        status_code = 503
        response = type("R", (), {"headers": {"retry-after": "7"}})()

    waits, n = [], []

    def fn():
        """Test helper: fn."""
        n.append(1)
        if len(n) == 1:
            raise WithHeader()
        return 1

    with_backoff(fn, attempts=3, base_s=1, cap_s=30, sleep=waits.append, rand=lambda: 0.0)
    assert waits == [7.0]


def test_timeouts_and_connection_errors_are_transient():
    """Timeouts and connection errors are transient.

    Spec: S4.1 | Traces to: I11
    Expected outcome: a timeout error is transient and a ValueError is not.
    """

    class APITimeoutError(Exception):
        """A stand-in for the client library's timeout error."""

    assert is_transient(APITimeoutError()) and not is_transient(ValueError())


def test_explicit_cache_mode_marks_the_static_prefix_only():
    """Explicit cache mode marks the static prefix only.

    Spec: S4.2 | Traces to: A2
    Expected outcome: only the system message carries the cache marker in explicit mode.
    """
    msgs = build_messages("STATIC RULES", "dynamic state", "explicit")
    assert isinstance(msgs[0], SystemMessage)
    assert msgs[0].content[0]["cache_control"] == {"type": "ephemeral"}
    assert msgs[1].content == "dynamic state"
    assert isinstance(build_messages("S", "D", "auto")[0].content, str)


class FlakyThenScripted(ScriptedChat):
    """Test helper: FlakyThenScripted."""

    failures: int = 1

    def _generate(self, messages, stop=None, run_manager=None, **kw):
        """Test helper: generate."""
        if self.failures:
            self.failures -= 1
            raise Gateway429("rate limited")
        return super()._generate(messages, stop, run_manager, **kw)


def test_call_records_cache_hits_retries_and_rejections():
    """Call records cache hits retries and rejections.

    Spec: S4.5 | Traces to: I1
    Expected outcome: the record shows one retry, one rejection, and the cached tokens.
    """
    from collections import Counter

    model = FlakyThenScripted(script=script, calls=Counter(), rejections=[])
    deps = Deps(known_ids={"D-001", "D-002", "D-003", "D-009"})
    out, rec = call(model, agent("prd_core"), "write it", deps, Limits(sleep=lambda s: None))
    assert out.stories[0].id == "S-01"
    assert rec.transient_retries == 1  # the 429, retried with backoff
    assert rec.rejections == 1  # D-999 rejected, then fixed
    assert rec.cache_read_tokens == 2 * USAGE["input_token_details"]["cache_read"]
