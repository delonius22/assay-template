"""Tests for assay.cli (build step 32).

Covers: S8.3. Each test guards one expected outcome from the build steps in
src/assay/cli.py.
"""

import pytest

from assay.cli import build_progress, main


@pytest.mark.skip(reason="skeleton: S8.3 not implemented")
def test_build_progress_1_running_check_does_not_start_the() -> None:
    """Running check does not start the CLI twice.

    Spec: S8.3 | Traces to: I9
    Expected outcome: Running check does not start the CLI twice.
    """


@pytest.mark.skip(reason="skeleton: S8.3 not implemented")
def test_build_progress_2_a_fresh_skeleton_reports_every_function() -> None:
    """A fresh skeleton reports every function as stubbed.

    Spec: S8.3 | Traces to: I9
    Expected outcome: A fresh skeleton reports every function as stubbed.
    """


@pytest.mark.skip(reason="skeleton: S8.3 not implemented")
def test_main_1_help_lists_both_commands() -> None:
    """'--help' lists both commands.

    Spec: S8.3 | Traces to: I9, A3
    Expected outcome: '--help' lists both commands.
    """


@pytest.mark.skip(reason="skeleton: S8.3 not implemented")
def test_main_2_the_server_starts_on_the_given() -> None:
    """The server starts on the given port.

    Spec: S8.3 | Traces to: I9, A3
    Expected outcome: The server starts on the given port.
    """


@pytest.mark.skip(reason="skeleton: S8.3 not implemented")
def test_main_3_a_fresh_skeleton_prints_that_s1() -> None:
    """A fresh skeleton prints that S1.1 must be built first.

    Spec: S8.3 | Traces to: I9, A3
    Expected outcome: A fresh skeleton prints that S1.1 must be built first.
    """
