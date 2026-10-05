"""Tests for assay.graph.nodes.dod (build step 23).

Covers: S5.7. Each test guards one expected outcome from the build steps in
src/assay/graph/nodes/dod.py.
"""

import pytest

from assay.graph.nodes.dod import after_dod, dod_ask, dod_think


@pytest.mark.skip(reason="skeleton: S5.7 not implemented")
def test_dod_think_1_the_additions_prompt_contains_the_intake() -> None:
    """The additions prompt contains the intake log.

    Spec: S5.7 | Traces to: I2, I5
    Expected outcome: The additions prompt contains the intake log.
    """


@pytest.mark.skip(reason="skeleton: S5.7 not implemented")
def test_dod_think_2_a_new_team_item_is_dod() -> None:
    """A new team item is DOD-T01.

    Spec: S5.7 | Traces to: I2, I5
    Expected outcome: A new team item is DOD-T01.
    """


@pytest.mark.skip(reason="skeleton: S5.7 not implemented")
def test_dod_think_3_a_team_standard_with_no_ticket() -> None:
    """A team standard with no ticket item loops back.

    Spec: S5.7 | Traces to: I2, I5
    Expected outcome: A team standard with no ticket item loops back.
    """


@pytest.mark.skip(reason="skeleton: S5.7 not implemented")
def test_dod_think_4_after_additions_the_phase_is_done() -> None:
    """After additions, the phase is 'done'.

    Spec: S5.7 | Traces to: I2, I5
    Expected outcome: After additions, the phase is 'done'.
    """


@pytest.mark.skip(reason="skeleton: S5.7 not implemented")
def test_dod_ask_1_resuming_runs_no_model_call() -> None:
    """Resuming runs no model call.

    Spec: S5.7 | Traces to: I7
    Expected outcome: Resuming runs no model call.
    """


@pytest.mark.skip(reason="skeleton: S5.7 not implemented")
def test_dod_ask_2_the_answer_is_recorded_with_the() -> None:
    """The answer is recorded with the answering user.

    Spec: S5.7 | Traces to: I7
    Expected outcome: The answer is recorded with the answering user.
    """


@pytest.mark.skip(reason="skeleton: S5.7 not implemented")
def test_after_dod_1_phase_done_routes_to_intake_gate() -> None:
    """Phase 'done' routes to intake_gate_node.

    Spec: S5.7 | Traces to: I5
    Expected outcome: Phase 'done' routes to intake_gate_node.
    """
