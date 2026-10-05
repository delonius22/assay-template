"""Tests for assay.llm.call (build step 13).

Covers: S4.5. Each test guards one expected outcome from the build steps in
src/assay/llm/call.py.
"""

import pytest

from assay.llm.call import AgentSpec, CallRecord, Limits, OutputError, call, validation_errors


@pytest.mark.skip(reason="skeleton: S4.5 not implemented")
def test_call_record_dict_1_the_result_contains_all_twelve_fields() -> None:
    """The result contains all twelve fields.

    Spec: S4.5 | Traces to: I1
    Expected outcome: The result contains all twelve fields.
    """


@pytest.mark.skip(reason="skeleton: S4.5 not implemented")
def test_validation_errors_1_a_missing_done_field_yields_done() -> None:
    """A missing 'done' field yields 'done: Field required'.

    Spec: S4.5 | Traces to: I1
    Expected outcome: A missing 'done' field yields 'done: Field required'.
    """


@pytest.mark.skip(reason="skeleton: S4.5 not implemented")
def test_call_1_the_model_is_never_asked_for() -> None:
    """The model is never asked for free text.

    Spec: S4.5 | Traces to: I1, I11
    Expected outcome: The model is never asked for free text.
    """


@pytest.mark.skip(reason="skeleton: S4.5 not implemented")
def test_call_2_one_rate_limit_then_success_records() -> None:
    """One rate limit then success records one transient retry.

    Spec: S4.5 | Traces to: I1, I11
    Expected outcome: One rate limit then success records one transient retry.
    """


@pytest.mark.skip(reason="skeleton: S4.5 not implemented")
def test_call_3_every_tool_call_receives_exactly_one() -> None:
    """Every tool call receives exactly one reply.

    Spec: S4.5 | Traces to: I1, I11
    Expected outcome: Every tool call receives exactly one reply.
    """


@pytest.mark.skip(reason="skeleton: S4.5 not implemented")
def test_call_4_an_invented_source_id_is_rejected() -> None:
    """An invented source ID is rejected once and fixed on the next turn.

    Spec: S4.5 | Traces to: I1, I11
    Expected outcome: An invented source ID is rejected once and fixed on the next
                      turn.
    """


@pytest.mark.skip(reason="skeleton: S4.5 not implemented")
def test_call_5_a_valid_first_answer_returns_after() -> None:
    """A valid first answer returns after one step.

    Spec: S4.5 | Traces to: I1, I11
    Expected outcome: A valid first answer returns after one step.
    """
