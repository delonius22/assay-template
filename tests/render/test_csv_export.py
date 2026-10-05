"""Tests for assay.render.csv_export (build step 18).

Covers: S6.5. Each test guards one expected outcome from the build steps in
src/assay/render/csv_export.py.
"""

import pytest

from assay.render.csv_export import dod_cell, rows, story_title, to_csv, top_priority


@pytest.mark.skip(reason="skeleton: S6.5 not implemented")
def test_story_title_1_as_an_agent_i_want_to() -> None:
    """'As an agent, I want to view settings so that I can help.' becomes 'View
    settings'.

        Spec: S6.5 | Traces to: C6
        Expected outcome: 'As an agent, I want to view settings so that I can help.'
                          becomes 'View settings'.
    """


@pytest.mark.skip(reason="skeleton: S6.5 not implemented")
def test_dod_cell_1_two_items_give_two_lines() -> None:
    """Two items give two lines.

    Spec: S6.5 | Traces to: C6
    Expected outcome: Two items give two lines.
    """


@pytest.mark.skip(reason="skeleton: S6.5 not implemented")
def test_top_priority_1_should_have_and_must_have_give() -> None:
    """Should have and Must have give Must have.

    Spec: S6.5 | Traces to: C6
    Expected outcome: Should have and Must have give Must have.
    """


@pytest.mark.skip(reason="skeleton: S6.5 not implemented")
def test_rows_1_f_01_lists_fr_01_and() -> None:
    """F-01 lists FR-01 and FR-02.

    Spec: S6.5 | Traces to: C6, I15
    Expected outcome: F-01 lists FR-01 and FR-02.
    """


@pytest.mark.skip(reason="skeleton: S6.5 not implemented")
def test_rows_2_the_first_row_is_the_s() -> None:
    """The first row is the S-01 story.

    Spec: S6.5 | Traces to: C6, I15
    Expected outcome: The first row is the S-01 story.
    """


@pytest.mark.skip(reason="skeleton: S6.5 not implemented")
def test_rows_3_rows_run_s_01_f_01() -> None:
    """Rows run S-01, F-01, T-001, T-002, F-02, T-003.

    Spec: S6.5 | Traces to: C6, I15
    Expected outcome: Rows run S-01, F-01, T-001, T-002, F-02, T-003.
    """


@pytest.mark.skip(reason="skeleton: S6.5 not implemented")
def test_rows_4_a_spike_row_s_description_starts() -> None:
    """A spike row's description starts with 'Question:'.

    Spec: S6.5 | Traces to: C6, I15
    Expected outcome: A spike row's description starts with 'Question:'.
    """


@pytest.mark.skip(reason="skeleton: S6.5 not implemented")
def test_to_csv_1_a_cell_with_two_lines_reads() -> None:
    """A cell with two lines reads back as one cell.

    Spec: S6.5 | Traces to: C1
    Expected outcome: A cell with two lines reads back as one cell.
    """
