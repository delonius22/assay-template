"""Tests for assay.graph.nodes.spec (build step 25).

Covers: S5.9. Each test guards one expected outcome from the build steps in
src/assay/graph/nodes/spec.py.
"""

import pytest

from assay.graph.nodes.spec import after_seams, prd_brief, seams, seams_ask, spec


@pytest.mark.skip(reason="skeleton: S5.9 not implemented")
def test_prd_brief_1_the_text_contains_fr_01_and() -> None:
    """The text contains 'FR-01:' and 'NFR-01:'.

    Spec: S5.9 | Traces to: I3
    Expected outcome: The text contains 'FR-01:' and 'NFR-01:'.
    """


@pytest.mark.skip(reason="skeleton: S5.9 not implemented")
def test_seams_1_feedback_text_appears_in_the_prompt() -> None:
    """Feedback text appears in the prompt.

    Spec: S5.9 | Traces to: I1
    Expected outcome: Feedback text appears in the prompt.
    """


@pytest.mark.skip(reason="skeleton: S5.9 not implemented")
def test_seams_ask_1_resuming_runs_no_model_call() -> None:
    """Resuming runs no model call.

    Spec: S5.9 | Traces to: I7
    Expected outcome: Resuming runs no model call.
    """


@pytest.mark.skip(reason="skeleton: S5.9 not implemented")
def test_seams_ask_2_corrections_produce_feedback_approval_clears_it() -> None:
    """Corrections produce feedback; approval clears it.

    Spec: S5.9 | Traces to: I7
    Expected outcome: Corrections produce feedback; approval clears it.
    """


@pytest.mark.skip(reason="skeleton: S5.9 not implemented")
def test_after_seams_1_feedback_routes_back_to_seams() -> None:
    """Feedback routes back to seams.

    Spec: S5.9 | Traces to: I5
    Expected outcome: Feedback routes back to seams.
    """


@pytest.mark.skip(reason="skeleton: S5.9 not implemented")
def test_spec_1_the_spec_covers_every_requirement() -> None:
    """The spec covers every requirement.

    Spec: S5.9 | Traces to: I1
    Expected outcome: The spec covers every requirement.
    """


@pytest.mark.skip(reason="skeleton: S5.9 not implemented")
def test_spec_2_spec_md_is_listed_in_files() -> None:
    """spec.md is listed in files.

    Spec: S5.9 | Traces to: I1
    Expected outcome: spec.md is listed in files.
    """
