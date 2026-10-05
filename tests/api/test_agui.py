"""Tests for assay.api.agui (build step 30).

Covers: S9.2, S9.3, S9.4, S9.5, S9.6, S9.7. Each test guards one expected outcome
from the build steps in src/assay/api/agui.py.
"""

import pytest

from assay.api.agui import (
    AnswerReply,
    BriefReply,
    ContinueReply,
    DecisionReply,
    SessionView,
    check_service_call,
    encode_stream,
    interrupt_for,
    resume_value,
    run_events,
    session_view,
    start_from_props,
)


@pytest.mark.skip(reason="skeleton: S9.2 not implemented")
def test_interrupt_for_1_the_same_pause_re_sent_has() -> None:
    """The same pause re-sent has the same ID.

    Spec: S9.2 | Traces to: I18
    Expected outcome: The same pause re-sent has the same ID.
    """


@pytest.mark.skip(reason="skeleton: S9.2 not implemented")
def test_interrupt_for_2_an_approval_interrupt_s_schema_requires() -> None:
    """An approval interrupt's schema requires 'decision'.

    Spec: S9.2 | Traces to: I18
    Expected outcome: An approval interrupt's schema requires 'decision'.
    """


@pytest.mark.skip(reason="skeleton: S9.3 not implemented")
def test_resume_value_1_an_entry_for_an_unknown_interrupt() -> None:
    """An entry for an unknown interrupt ID is refused.

    Spec: S9.3 | Traces to: I18, I12
    Expected outcome: An entry for an unknown interrupt ID is refused.
    """


@pytest.mark.skip(reason="skeleton: S9.3 not implemented")
def test_resume_value_2_resolve_with_the_spec_owner_before() -> None:
    """Resolve with the spec owner before implementing; logged as OQ-1 in
    BUILD_ORDER.md.

        Spec: S9.3 | Traces to: I18, I12
        Expected outcome: Resolve with the spec owner before implementing; logged as
                          OQ-1 in BUILD_ORDER.md.
    """


@pytest.mark.skip(reason="skeleton: S9.3 not implemented")
def test_resume_value_3_an_approval_payload_without_decision_is() -> None:
    """An approval payload without 'decision' is refused.

    Spec: S9.3 | Traces to: I18, I12
    Expected outcome: An approval payload without 'decision' is refused.
    """


@pytest.mark.skip(reason="skeleton: S9.3 not implemented")
def test_resume_value_4_an_answerreply_becomes_a_value_with() -> None:
    """An AnswerReply becomes a value with text and user.

    Spec: S9.3 | Traces to: I18, I12
    Expected outcome: An AnswerReply becomes a value with text and user.
    """


@pytest.mark.skip(reason="skeleton: S9.4 not implemented")
def test_session_view_1_a_snapshot_never_contains_the_log() -> None:
    """A snapshot never contains the log.

    Spec: S9.4 | Traces to: I12
    Expected outcome: A snapshot never contains the log.
    """


@pytest.mark.skip(reason="skeleton: S9.5 not implemented")
def test_start_from_props_1_mode_3_without_a_brief_is() -> None:
    """Mode 3 without a brief is refused.

    Spec: S9.5 | Traces to: I12
    Expected outcome: Mode 3 without a brief is refused.
    """


@pytest.mark.skip(reason="skeleton: S9.5 not implemented")
def test_start_from_props_2_the_session_appears_in_the_session() -> None:
    """The session appears in the session list.

    Spec: S9.5 | Traces to: I12
    Expected outcome: The session appears in the session list.
    """


@pytest.mark.skip(reason="skeleton: S9.6 not implemented")
def test_check_service_call_1_a_wrong_token_is_refused() -> None:
    """A wrong token is refused.

    Spec: S9.6 | Traces to: I17
    Expected outcome: A wrong token is refused.
    """


@pytest.mark.skip(reason="skeleton: S9.6 not implemented")
def test_check_service_call_2_a_correct_token_with_a_user() -> None:
    """A correct token with a user returns that user.

    Spec: S9.6 | Traces to: I17
    Expected outcome: A correct token with a user returns that user.
    """


@pytest.mark.skip(reason="skeleton: S9.4 not implemented")
def test_run_events_1_the_first_step_event_is_never() -> None:
    """The first step event is never missed.

    Spec: S9.4, S9.5 | Traces to: I7, I18
    Expected outcome: The first step event is never missed.
    """


@pytest.mark.skip(reason="skeleton: S9.4 not implemented")
def test_run_events_2_re_requesting_a_waiting_session_runs() -> None:
    """Re-requesting a waiting session runs no step.

    Spec: S9.4, S9.5 | Traces to: I7, I18
    Expected outcome: Re-requesting a waiting session runs no step.
    """


@pytest.mark.skip(reason="skeleton: S9.4 not implemented")
def test_run_events_3_each_node_produces_a_start_a() -> None:
    """Each node produces a start, a finish, and a snapshot.

    Spec: S9.4, S9.5 | Traces to: I7, I18
    Expected outcome: Each node produces a start, a finish, and a snapshot.
    """


@pytest.mark.skip(reason="skeleton: S9.4 not implemented")
def test_run_events_4_a_run_reaching_a_pause_ends() -> None:
    """A run reaching a pause ends with outcome interrupt.

    Spec: S9.4, S9.5 | Traces to: I7, I18
    Expected outcome: A run reaching a pause ends with outcome interrupt.
    """


@pytest.mark.skip(reason="skeleton: S9.7 not implemented")
def test_encode_stream_1_each_event_arrives_as_one_data() -> None:
    """Each event arrives as one 'data:' line.

    Spec: S9.7 | Traces to: I7
    Expected outcome: Each event arrives as one 'data:' line.
    """
