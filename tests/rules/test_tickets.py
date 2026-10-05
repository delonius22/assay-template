"""Tests for assay.rules.tickets (build step 9).

Covers: S3.6. Each test guards one expected outcome from the build steps in
src/assay/rules/tickets.py.
"""

import pytest

from assay.rules.tickets import plan_problems


@pytest.mark.skip(reason="skeleton: S3.6 not implemented")
def test_plan_problems_1_a_ticket_for_f_09_produces() -> None:
    """A ticket for F-09 produces 'Ticket 1 (...): unknown feature F-09'.

    Spec: S3.6 | Traces to: I1, I15
    Expected outcome: A ticket for F-09 produces 'Ticket 1 (...): unknown feature
                      F-09'.
    """


@pytest.mark.skip(reason="skeleton: S3.6 not implemented")
def test_plan_problems_2_a_spike_without_a_timebox_produces() -> None:
    """A spike without a timebox produces a problem.

    Spec: S3.6 | Traces to: I1, I15
    Expected outcome: A spike without a timebox produces a problem.
    """


@pytest.mark.skip(reason="skeleton: S3.6 not implemented")
def test_plan_problems_3_a_ticket_with_2_criteria_produces() -> None:
    """A ticket with 2 criteria produces a problem.

    Spec: S3.6 | Traces to: I1, I15
    Expected outcome: A ticket with 2 criteria produces a problem.
    """


@pytest.mark.skip(reason="skeleton: S3.6 not implemented")
def test_plan_problems_4_a_ticket_depending_on_itself_produces() -> None:
    """A ticket depending on itself produces a problem.

    Spec: S3.6 | Traces to: I1, I15
    Expected outcome: A ticket depending on itself produces a problem.
    """


@pytest.mark.skip(reason="skeleton: S3.6 not implemented")
def test_plan_problems_5_dropping_nfr_01_from_every_ticket() -> None:
    """Dropping NFR-01 from every ticket produces 'No ticket covers ['NFR-01']'.

    Spec: S3.6 | Traces to: I1, I15
    Expected outcome: Dropping NFR-01 from every ticket produces 'No ticket covers
                      ['NFR-01']'.
    """
