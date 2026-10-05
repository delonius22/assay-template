"""Tests for assay.domain.ids (build step 3).

Covers: S2.1, S2.2, S2.3, S2.4, S2.5, S2.6. Each test guards one expected outcome
from the build steps in src/assay/domain/ids.py.
"""

import pytest

from assay.domain.ids import (
    add_entries,
    all_answerable_ids,
    apply_dod_turn,
    assign_tickets,
    live,
    question_ids,
    requirement_ids,
)


@pytest.mark.skip(reason="skeleton: S2.1 not implemented")
def test_add_entries_1_the_original_log_is_identical_after() -> None:
    """The original log is identical after the call.

    Spec: S2.1 | Traces to: I2
    Expected outcome: The original log is identical after the call.
    """


@pytest.mark.skip(reason="skeleton: S2.1 not implemented")
def test_add_entries_2_two_calls_that_each_add_one() -> None:
    """Two calls that each add one decision produce D-001 then D-002.

    Spec: S2.1 | Traces to: I2
    Expected outcome: Two calls that each add one decision produce D-001 then D-002.
    """


@pytest.mark.skip(reason="skeleton: S2.1 not implemented")
def test_add_entries_3_a_superseded_entry_stays_in_the() -> None:
    """A superseded entry stays in the log and lists its replacements.

    Spec: S2.1 | Traces to: I2
    Expected outcome: A superseded entry stays in the log and lists its
                      replacements.
    """


@pytest.mark.skip(reason="skeleton: S2.2 not implemented")
def test_live_1_a_superseded_entry_is_absent_every() -> None:
    """A superseded entry is absent; every other entry keeps its position.

    Spec: S2.2 | Traces to: I2
    Expected outcome: A superseded entry is absent; every other entry keeps its
                      position.
    """


@pytest.mark.skip(reason="skeleton: S2.3 not implemented")
def test_question_ids_1_two_round_2_questions_are_numbered() -> None:
    """Two round-2 questions are numbered Q-F01 and Q-F02.

    Spec: S2.3 | Traces to: I2
    Expected outcome: Two round-2 questions are numbered Q-F01 and Q-F02.
    """


@pytest.mark.skip(reason="skeleton: S2.3 not implemented")
def test_all_answerable_ids_1_a_question_with_one_follow_up() -> None:
    """A question with one follow-up adds Q-01a.

    Spec: S2.3 | Traces to: I2, I12
    Expected outcome: A question with one follow-up adds Q-01a.
    """


@pytest.mark.skip(reason="skeleton: S2.3 not implemented")
def test_all_answerable_ids_2_round_2_contains_no_k_ids() -> None:
    """Round 2 contains no K IDs.

    Spec: S2.3 | Traces to: I2, I12
    Expected outcome: Round 2 contains no K IDs.
    """


@pytest.mark.skip(reason="skeleton: S2.4 not implemented")
def test_apply_dod_turn_1_a_withdrawn_item_is_absent_and() -> None:
    """A withdrawn item is absent and its ID is in the retired list.

    Spec: S2.4 | Traces to: I2
    Expected outcome: A withdrawn item is absent and its ID is in the retired list.
    """


@pytest.mark.skip(reason="skeleton: S2.4 not implemented")
def test_apply_dod_turn_2_withdrawing_dod_t01_then_adding_an() -> None:
    """Withdrawing DOD-T01 then adding an item gives DOD-T02.

    Spec: S2.4 | Traces to: I2
    Expected outcome: Withdrawing DOD-T01 then adding an item gives DOD-T02.
    """


@pytest.mark.skip(reason="skeleton: S2.5 not implemented")
def test_requirement_ids_1_three_functional_and_one_non_functional() -> None:
    """Three functional and one non-functional give FR-01 to FR-03 and NFR-01.

    Spec: S2.5 | Traces to: I2
    Expected outcome: Three functional and one non-functional give FR-01 to FR-03
                      and NFR-01.
    """


@pytest.mark.skip(reason="skeleton: S2.6 not implemented")
def test_assign_tickets_1_four_tickets_are_t_001_to() -> None:
    """Four tickets are T-001 to T-004.

    Spec: S2.6 | Traces to: I2, I15
    Expected outcome: Four tickets are T-001 to T-004.
    """


@pytest.mark.skip(reason="skeleton: S2.6 not implemented")
def test_assign_tickets_2_a_ticket_depending_on_position_3() -> None:
    """A ticket depending on position 3 lists T-003.

    Spec: S2.6 | Traces to: I2, I15
    Expected outcome: A ticket depending on position 3 lists T-003.
    """
