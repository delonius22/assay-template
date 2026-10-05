"""Tests for assay.rules.intake (build step 5).

Covers: S3.2. Each test guards one expected outcome from the build steps in
src/assay/rules/intake.py.
"""

import pytest

from assay.rules.intake import GateItem, entry_problems, failures, gate


@pytest.mark.skip(reason="skeleton: S3.2 not implemented")
def test_entry_problems_1_a_question_with_no_owner_produces() -> None:
    """A question with no owner produces that problem.

    Spec: S3.2 | Traces to: I5
    Expected outcome: A question with no owner produces that problem.
    """


@pytest.mark.skip(reason="skeleton: S3.2 not implemented")
def test_entry_problems_2_a_scope_decision_with_no_side() -> None:
    """A scope decision with no side produces a problem naming in or out.

    Spec: S3.2 | Traces to: I5
    Expected outcome: A scope decision with no side produces a problem naming in or
                      out.
    """


@pytest.mark.skip(reason="skeleton: S3.2 not implemented")
def test_entry_problems_3_a_regulation_entry_without_an_owner() -> None:
    """A regulation entry without an owner produces a problem.

    Spec: S3.2 | Traces to: I5
    Expected outcome: A regulation entry without an owner produces a problem.
    """


@pytest.mark.skip(reason="skeleton: S3.2 not implemented")
def test_gate_1_a_superseded_decision_never_satisfies_an() -> None:
    """A superseded decision never satisfies an item.

    Spec: S3.2 | Traces to: I5
    Expected outcome: A superseded decision never satisfies an item.
    """


@pytest.mark.skip(reason="skeleton: S3.2 not implemented")
def test_gate_2_a_scope_entry_worded_out_of() -> None:
    """A scope entry worded 'out of scope' but flagged 'in' fails the scope item.

    Spec: S3.2 | Traces to: I5
    Expected outcome: A scope entry worded 'out of scope' but flagged 'in' fails the
                      scope item.
    """


@pytest.mark.skip(reason="skeleton: S3.2 not implemented")
def test_gate_3_an_open_blocking_q_001_fails() -> None:
    """An open blocking Q-001 fails with 'blocking questions still open: Q-001'.

    Spec: S3.2 | Traces to: I5
    Expected outcome: An open blocking Q-001 fails with 'blocking questions still
                      open: Q-001'.
    """


@pytest.mark.skip(reason="skeleton: S3.2 not implemented")
def test_failures_1_a_fully_passing_gate_returns_no() -> None:
    """A fully passing gate returns no lines.

    Spec: S3.2 | Traces to: I5
    Expected outcome: A fully passing gate returns no lines.
    """
