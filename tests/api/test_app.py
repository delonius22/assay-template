"""Tests for assay.api.app (build step 31).

Covers: S8.3, S8.4, S8.5, S9.7. Each test guards one expected outcome from the build
steps in src/assay/api/app.py.
"""

import pytest

from assay.api.app import (
    NewSession,
    Reply,
    Responses,
    Services,
    create_app,
    handle_create,
    handle_download,
    handle_get,
    handle_list,
    handle_me,
    handle_questionnaire,
    handle_reply,
    handle_responses,
    handle_retry,
    handle_submit,
    handle_usage,
)


@pytest.mark.skip(reason="skeleton: S8.3 not implemented")
def test_handle_me_1_a_non_approver_sees_approver_false() -> None:
    """A non-approver sees approver false.

    Spec: S8.3 | Traces to: I8
    Expected outcome: A non-approver sees approver false.
    """


@pytest.mark.skip(reason="skeleton: S8.3 not implemented")
def test_handle_list_1_the_newest_session_is_listed_first() -> None:
    """The newest session is listed first.

    Spec: S8.3 | Traces to: I6
    Expected outcome: The newest session is listed first.
    """


@pytest.mark.skip(reason="skeleton: S8.3 not implemented")
def test_handle_create_1_a_duplicate_slug_gets_409() -> None:
    """A duplicate slug gets 409.

    Spec: S8.3 | Traces to: I12
    Expected outcome: A duplicate slug gets 409.
    """


@pytest.mark.skip(reason="skeleton: S8.3 not implemented")
def test_handle_create_2_the_response_shows_the_first_pause() -> None:
    """The response shows the first pause or 'working'.

    Spec: S8.3 | Traces to: I12
    Expected outcome: The response shows the first pause or 'working'.
    """


@pytest.mark.skip(reason="skeleton: S8.3 not implemented")
def test_handle_get_1_an_unknown_slug_gets_404() -> None:
    """An unknown slug gets 404.

    Spec: S8.3 | Traces to: I6
    Expected outcome: An unknown slug gets 404.
    """


@pytest.mark.skip(reason="skeleton: S8.3 not implemented")
def test_handle_reply_1_a_non_approver_s_approval_gets() -> None:
    """A non-approver's approval gets 403.

    Spec: S8.3 | Traces to: I8, I12
    Expected outcome: A non-approver's approval gets 403.
    """


@pytest.mark.skip(reason="skeleton: S8.3 not implemented")
def test_handle_reply_2_the_status_shows_the_next_pause() -> None:
    """The status shows the next pause.

    Spec: S8.3 | Traces to: I8, I12
    Expected outcome: The status shows the next pause.
    """


@pytest.mark.skip(reason="skeleton: S8.3 not implemented")
def test_handle_retry_1_retrying_a_stopped_session_continues_it() -> None:
    """Retrying a stopped session continues it.

    Spec: S8.3 | Traces to: I6
    Expected outcome: Retrying a stopped session continues it.
    """


@pytest.mark.skip(reason="skeleton: S8.4 not implemented")
def test_handle_questionnaire_1_a_mode_1_session_gets_404() -> None:
    """A mode 1 session gets 404.

    Spec: S8.4 | Traces to: I12
    Expected outcome: A mode 1 session gets 404.
    """


@pytest.mark.skip(reason="skeleton: S8.4 not implemented")
def test_handle_questionnaire_2_round_2_returns_no_confirmations() -> None:
    """Round 2 returns no confirmations.

    Spec: S8.4 | Traces to: I12
    Expected outcome: Round 2 returns no confirmations.
    """


@pytest.mark.skip(reason="skeleton: S8.4 not implemented")
def test_handle_submit_1_q_99_is_refused() -> None:
    """Q-99 is refused.

    Spec: S8.4 | Traces to: I12
    Expected outcome: Q-99 is refused.
    """


@pytest.mark.skip(reason="skeleton: S8.4 not implemented")
def test_handle_submit_2_resubmitting_replaces_the_earlier_sheet() -> None:
    """Resubmitting replaces the earlier sheet.

    Spec: S8.4 | Traces to: I12
    Expected outcome: Resubmitting replaces the earlier sheet.
    """


@pytest.mark.skip(reason="skeleton: S8.4 not implemented")
def test_handle_responses_1_one_submission_lists_one_respondent() -> None:
    """One submission lists one respondent.

    Spec: S8.4 | Traces to: I12
    Expected outcome: One submission lists one respondent.
    """


@pytest.mark.skip(reason="skeleton: S8.5 not implemented")
def test_handle_download_1_secrets_gets_404() -> None:
    """'../secrets' gets 404.

    Spec: S8.5 | Traces to: I12
    Expected outcome: '../secrets' gets 404.
    """


@pytest.mark.skip(reason="skeleton: S8.5 not implemented")
def test_handle_download_2_tickets_csv_downloads_as_slug_tickets() -> None:
    """tickets.csv downloads as '<slug>-tickets.csv'.

    Spec: S8.5 | Traces to: I12
    Expected outcome: tickets.csv downloads as '<slug>-tickets.csv'.
    """


@pytest.mark.skip(reason="skeleton: S8.5 not implemented")
def test_handle_usage_1_800_cached_of_1000_input_gives() -> None:
    """800 cached of 1000 input gives 0.8.

    Spec: S8.5 | Traces to: A2
    Expected outcome: 800 cached of 1000 input gives 0.8.
    """


@pytest.mark.skip(reason="skeleton: S8.5 not implemented")
def test_handle_usage_2_the_first_call_is_listed_first() -> None:
    """The first call is listed first.

    Spec: S8.5 | Traces to: A2
    Expected outcome: The first call is listed first.
    """


@pytest.mark.skip(reason="skeleton: S8.3 not implemented")
def test_create_app_1_after_startup_the_app_s_state() -> None:
    """After startup, the app's state holds the services with a runner.

    Spec: S8.3, S9.7 | Traces to: I17
    Expected outcome: After startup, the app's state holds the services with a
                      runner.
    """


@pytest.mark.skip(reason="skeleton: S8.3 not implemented")
def test_create_app_2_post_api_sessions_returns_201() -> None:
    """POST /api/sessions returns 201.

    Spec: S8.3, S9.7 | Traces to: I17
    Expected outcome: POST /api/sessions returns 201.
    """


@pytest.mark.skip(reason="skeleton: S8.3 not implemented")
def test_create_app_3_a_call_without_the_service_token() -> None:
    """A call without the service token gets 403.

    Spec: S8.3, S9.7 | Traces to: I17
    Expected outcome: A call without the service token gets 403.
    """
