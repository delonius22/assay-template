"""Tests for assay.llm.resilience (build step 11).

Covers: S4.1. Each test guards one expected outcome from the build steps in
src/assay/llm/resilience.py.
"""

import pytest

from assay.llm.resilience import is_transient, retry_after_s, status_of, with_backoff


@pytest.mark.skip(reason="skeleton: S4.1 not implemented")
def test_status_of_1_an_exception_carrying_status_429_returns() -> None:
    """An exception carrying status 429 returns 429.

    Spec: S4.1 | Traces to: I11
    Expected outcome: An exception carrying status 429 returns 429.
    """


@pytest.mark.skip(reason="skeleton: S4.1 not implemented")
def test_is_transient_1_a_429_is_transient_a_400() -> None:
    """A 429 is transient; a 400 is not; a timeout error is transient.

    Spec: S4.1 | Traces to: I11
    Expected outcome: A 429 is transient; a 400 is not; a timeout error is
                      transient.
    """


@pytest.mark.skip(reason="skeleton: S4.1 not implemented")
def test_retry_after_s_1_a_header_of_7_returns_7() -> None:
    """A header of '7' returns 7.0.

    Spec: S4.1 | Traces to: I11
    Expected outcome: A header of '7' returns 7.0.
    """


@pytest.mark.skip(reason="skeleton: S4.1 not implemented")
def test_with_backoff_1_a_400_is_raised_without_any() -> None:
    """A 400 is raised without any wait.

    Spec: S4.1 | Traces to: I11
    Expected outcome: A 400 is raised without any wait.
    """


@pytest.mark.skip(reason="skeleton: S4.1 not implemented")
def test_with_backoff_2_with_the_factor_fixed_at_1() -> None:
    """With the factor fixed at 1, base 1, two 429s then success wait 1 then 2
    seconds.

        Spec: S4.1 | Traces to: I11
        Expected outcome: With the factor fixed at 1, base 1, two 429s then success wait
                          1 then 2 seconds.
    """


@pytest.mark.skip(reason="skeleton: S4.1 not implemented")
def test_with_backoff_3_tests_observe_each_wait_without_real() -> None:
    """Tests observe each wait without real delays.

    Spec: S4.1 | Traces to: I11
    Expected outcome: Tests observe each wait without real delays.
    """
