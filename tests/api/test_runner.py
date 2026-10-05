"""Tests for assay.api.runner (build step 29).

Covers: S8.2, S9.1. Each test guards one expected outcome from the build steps in
src/assay/api/runner.py.
"""

import pytest

from assay.api.runner import BusyError, Runner, RunProgress


@pytest.mark.skip(reason="skeleton: S8.2 not implemented")
def test_runner___init_1_a_new_runner_reports_no_session() -> None:
    """A new runner reports no session as running.

    Spec: S8.2 | Traces to: I6
    Expected outcome: A new runner reports no session as running.
    """


@pytest.mark.skip(reason="skeleton: S8.2 not implemented")
def test_runner_config_1_the_slug_alerts_becomes_thread_alerts() -> None:
    """The slug 'alerts' becomes thread 'alerts'.

    Spec: S8.2 | Traces to: I6
    Expected outcome: The slug 'alerts' becomes thread 'alerts'.
    """


@pytest.mark.skip(reason="skeleton: S8.2 not implemented")
def test_runner_lock_for_1_two_calls_for_one_slug_return() -> None:
    """Two calls for one slug return the same lock.

    Spec: S8.2 | Traces to: I6
    Expected outcome: Two calls for one slug return the same lock.
    """


@pytest.mark.skip(reason="skeleton: S8.2 not implemented")
def test_runner_running_1_a_session_mid_step_reports_true() -> None:
    """A session mid-step reports True.

    Spec: S8.2 | Traces to: I6
    Expected outcome: A session mid-step reports True.
    """


@pytest.mark.skip(reason="skeleton: S9.1 not implemented")
def test_runner_subscribe_1_two_subscribers_both_receive_the_next() -> None:
    """Two subscribers both receive the next event.

    Spec: S9.1 | Traces to: I7
    Expected outcome: Two subscribers both receive the next event.
    """


@pytest.mark.skip(reason="skeleton: S9.1 not implemented")
def test_runner_unsubscribe_1_unsubscribing_twice_does_not_fail() -> None:
    """Unsubscribing twice does not fail.

    Spec: S9.1 | Traces to: I7
    Expected outcome: Unsubscribing twice does not fail.
    """


@pytest.mark.skip(reason="skeleton: S9.1 not implemented")
def test_runner_publish_1_a_subscriber_that_never_reads_does() -> None:
    """A subscriber that never reads does not slow the run.

    Spec: S9.1 | Traces to: I7
    Expected outcome: A subscriber that never reads does not slow the run.
    """


@pytest.mark.skip(reason="skeleton: S8.2 not implemented")
def test_runner_run_1_every_node_produces_one_start_and() -> None:
    """Every node produces one start and one finish.

    Spec: S8.2, S9.1 | Traces to: I6, I7
    Expected outcome: Every node produces one start and one finish.
    """


@pytest.mark.skip(reason="skeleton: S8.2 not implemented")
def test_runner_run_2_a_grill_turn_publishes_start_then() -> None:
    """A grill turn publishes start then finish.

    Spec: S8.2, S9.1 | Traces to: I6, I7
    Expected outcome: A grill turn publishes start then finish.
    """


@pytest.mark.skip(reason="skeleton: S8.2 not implemented")
def test_runner_run_3_a_failing_step_publishes_ended_with() -> None:
    """A failing step publishes ended with outcome error.

    Spec: S8.2, S9.1 | Traces to: I6, I7
    Expected outcome: A failing step publishes ended with outcome error.
    """


@pytest.mark.skip(reason="skeleton: S8.2 not implemented")
def test_runner_run_4_a_failed_step_leaves_the_session() -> None:
    """A failed step leaves the session not running.

    Spec: S8.2, S9.1 | Traces to: I6, I7
    Expected outcome: A failed step leaves the session not running.
    """


@pytest.mark.skip(reason="skeleton: S8.2 not implemented")
def test_runner_submit_1_a_second_submit_during_a_run() -> None:
    """A second submit during a run raises BusyError.

    Spec: S8.2 | Traces to: I6
    Expected outcome: A second submit during a run raises BusyError.
    """


@pytest.mark.skip(reason="skeleton: S8.2 not implemented")
def test_runner_submit_2_in_inline_mode_the_run_has() -> None:
    """In inline mode the run has finished when submit returns.

    Spec: S8.2 | Traces to: I6
    Expected outcome: In inline mode the run has finished when submit returns.
    """


@pytest.mark.skip(reason="skeleton: S8.2 not implemented")
def test_runner_start_1_a_new_session_runs_setup_first() -> None:
    """A new session runs setup first.

    Spec: S8.2 | Traces to: I6
    Expected outcome: A new session runs setup first.
    """


@pytest.mark.skip(reason="skeleton: S8.2 not implemented")
def test_runner_resume_1_the_paused_node_receives_the_reply() -> None:
    """The paused node receives the reply.

    Spec: S8.2 | Traces to: I6
    Expected outcome: The paused node receives the reply.
    """


@pytest.mark.skip(reason="skeleton: S8.2 not implemented")
def test_runner_retry_1_after_a_failed_step_retry_continues() -> None:
    """After a failed step, retry continues from the last saved step.

    Spec: S8.2 | Traces to: I6
    Expected outcome: After a failed step, retry continues from the last saved step.
    """


@pytest.mark.skip(reason="skeleton: S8.2 not implemented")
def test_runner_status_1_a_paused_session_reports_its_pause() -> None:
    """A paused session reports its pause.

    Spec: S8.2 | Traces to: I6
    Expected outcome: A paused session reports its pause.
    """


@pytest.mark.skip(reason="skeleton: S8.2 not implemented")
def test_runner_status_2_a_session_interrupted_by_a_restart() -> None:
    """A session interrupted by a restart reports stopped.

    Spec: S8.2 | Traces to: I6
    Expected outcome: A session interrupted by a restart reports stopped.
    """


@pytest.mark.skip(reason="skeleton: S8.2 not implemented")
def test_runner_status_3_the_json_includes_files_for_downloads() -> None:
    """The JSON includes files for downloads.

    Spec: S8.2 | Traces to: I6
    Expected outcome: The JSON includes files for downloads.
    """
