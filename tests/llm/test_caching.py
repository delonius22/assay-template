"""Tests for assay.llm.caching (build step 10).

Covers: S4.2. Each test guards one expected outcome from the build steps in
src/assay/llm/caching.py.
"""

import pytest

from assay.llm.caching import build_messages, usage_of


@pytest.mark.skip(reason="skeleton: S4.2 not implemented")
def test_build_messages_1_in_explicit_mode_only_the_system() -> None:
    """In explicit mode only the system message carries the marker.

    Spec: S4.2 | Traces to: A2
    Expected outcome: In explicit mode only the system message carries the marker.
    """


@pytest.mark.skip(reason="skeleton: S4.2 not implemented")
def test_build_messages_2_the_dynamic_text_is_always_the() -> None:
    """The dynamic text is always the last message.

    Spec: S4.2 | Traces to: A2
    Expected outcome: The dynamic text is always the last message.
    """


@pytest.mark.skip(reason="skeleton: S4.2 not implemented")
def test_usage_of_1_a_response_reporting_800_cached_input() -> None:
    """A response reporting 800 cached input tokens returns cache_read_tokens 800.

    Spec: S4.2 | Traces to: A2
    Expected outcome: A response reporting 800 cached input tokens returns
                      cache_read_tokens 800.
    """
