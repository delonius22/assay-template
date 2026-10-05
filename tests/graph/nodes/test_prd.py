"""Tests for assay.graph.nodes.prd (build step 24).

Covers: S5.8. Each test guards one expected outcome from the build steps in
src/assay/graph/nodes/prd.py.
"""

import pytest

from assay.graph.nodes.prd import after_review, prd, prd_review_ask, stamp_approval


@pytest.mark.skip(reason="skeleton: S5.8 not implemented")
def test_prd_1_reviewer_feedback_appears_in_the_prompt() -> None:
    """Reviewer feedback appears in the prompt.

    Spec: S5.8 | Traces to: I3, I4
    Expected outcome: Reviewer feedback appears in the prompt.
    """


@pytest.mark.skip(reason="skeleton: S5.8 not implemented")
def test_prd_2_requirements_are_fr_01_onward() -> None:
    """Requirements are FR-01 onward.

    Spec: S5.8 | Traces to: I3, I4
    Expected outcome: Requirements are FR-01 onward.
    """


@pytest.mark.skip(reason="skeleton: S5.8 not implemented")
def test_prd_3_prd_pdf_is_listed_in_files() -> None:
    """prd.pdf is listed in files.

    Spec: S5.8 | Traces to: I3, I4
    Expected outcome: prd.pdf is listed in files.
    """


@pytest.mark.skip(reason="skeleton: S5.8 not implemented")
def test_prd_review_ask_1_resuming_runs_no_model_call() -> None:
    """Resuming runs no model call.

    Spec: S5.8 | Traces to: I7, I8
    Expected outcome: Resuming runs no model call.
    """


@pytest.mark.skip(reason="skeleton: S5.8 not implemented")
def test_prd_review_ask_2_a_non_approver_s_approval_is() -> None:
    """A non-approver's approval is refused.

    Spec: S5.8 | Traces to: I7, I8
    Expected outcome: A non-approver's approval is refused.
    """


@pytest.mark.skip(reason="skeleton: S5.8 not implemented")
def test_prd_review_ask_3_changes_to_version_0_1_produce() -> None:
    """Changes to version 0.1 produce 0.2.

    Spec: S5.8 | Traces to: I7, I8
    Expected outcome: Changes to version 0.1 produce 0.2.
    """


@pytest.mark.skip(reason="skeleton: S5.8 not implemented")
def test_after_review_1_an_approval_routes_to_stamp_approval() -> None:
    """An approval routes to stamp_approval.

    Spec: S5.8 | Traces to: I5
    Expected outcome: An approval routes to stamp_approval.
    """


@pytest.mark.skip(reason="skeleton: S5.8 not implemented")
def test_stamp_approval_1_the_pdf_s_status_reads_approved() -> None:
    """The PDF's status reads Approved.

    Spec: S5.8 | Traces to: I8
    Expected outcome: The PDF's status reads Approved.
    """
