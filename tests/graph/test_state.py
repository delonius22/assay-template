"""Tests for assay.graph.state (build step 17).

Covers: S5.1. Each test guards one expected outcome from the build steps in
src/assay/graph/state.py.
"""

import pytest

from assay.graph.state import AssayState, log_view


@pytest.mark.skip(reason="skeleton: S5.1 not implemented")
def test_assay_state_feature_ids_1_a_prd_with_features_f_01() -> None:
    """A PRD with features F-01 and F-02 returns both.

    Spec: S5.1 | Traces to: I2
    Expected outcome: A PRD with features F-01 and F-02 returns both.
    """


@pytest.mark.skip(reason="skeleton: S5.1 not implemented")
def test_assay_state_prd_ids_1_fr_01_and_nfr_01_are() -> None:
    """FR-01 and NFR-01 are both included.

    Spec: S5.1 | Traces to: I3
    Expected outcome: FR-01 and NFR-01 are both included.
    """


@pytest.mark.skip(reason="skeleton: S5.1 not implemented")
def test_assay_state_known_ids_1_d_001_and_q_01_are() -> None:
    """D-001 and Q-01 are both included.

    Spec: S5.1 | Traces to: I3
    Expected outcome: D-001 and Q-01 are both included.
    """


@pytest.mark.skip(reason="skeleton: S5.1 not implemented")
def test_log_view_1_an_out_of_scope_entry_shows() -> None:
    """An out-of-scope entry shows 'scope:out'.

    Spec: S5.1 | Traces to: I3
    Expected outcome: An out-of-scope entry shows 'scope:out'.
    """


@pytest.mark.skip(reason="skeleton: S5.1 not implemented")
def test_log_view_2_an_empty_log_gives_empty() -> None:
    """An empty log gives '(empty)'.

    Spec: S5.1 | Traces to: I3
    Expected outcome: An empty log gives '(empty)'.
    """
