"""Tests for assay.render.markdown (build step 19).

Covers: S6.1, S6.2, S6.3, S6.4, S6.6. Each test guards one expected outcome from the
build steps in src/assay/render/markdown.py.
"""

import pytest

from assay.render.markdown import (
    dod,
    glossary,
    intake,
    prd,
    questionnaire,
    spec,
    template_env,
    tickets,
    write,
)


@pytest.mark.skip(reason="skeleton: S6.1 not implemented")
def test_template_env_1_a_rendered_table_keeps_one_row() -> None:
    """A rendered table keeps one row per line.

    Spec: S6.1 | Traces to: C1
    Expected outcome: A rendered table keeps one row per line.
    """


@pytest.mark.skip(reason="skeleton: S6.1 not implemented")
def test_template_env_2_count_of_1_story_writes_1() -> None:
    """count of 1 story writes '1 story'; of 2 writes '2 stories'.

    Spec: S6.1 | Traces to: C1
    Expected outcome: count of 1 story writes '1 story'; of 2 writes '2 stories'.
    """


@pytest.mark.skip(reason="skeleton: S6.1 not implemented")
def test_write_1_writing_twice_leaves_identical_files() -> None:
    """Writing twice leaves identical files.

    Spec: S6.1 | Traces to: C1
    Expected outcome: Writing twice leaves identical files.
    """


@pytest.mark.skip(reason="skeleton: S6.1 not implemented")
def test_intake_1_intake_md_shows_every_gate_item() -> None:
    """intake.md shows every gate item ticked or with its reason.

    Spec: S6.1 | Traces to: I5
    Expected outcome: intake.md shows every gate item ticked or with its reason.
    """


@pytest.mark.skip(reason="skeleton: S6.1 not implemented")
def test_glossary_1_terms_appear_sorted_by_name() -> None:
    """Terms appear sorted by name.

    Spec: S6.1 | Traces to: C1
    Expected outcome: Terms appear sorted by name.
    """


@pytest.mark.skip(reason="skeleton: S6.2 not implemented")
def test_questionnaire_1_round_2_writes_questionnaire_followup_md() -> None:
    """Round 2 writes questionnaire-followup.md.

    Spec: S6.2 | Traces to: C1
    Expected outcome: Round 2 writes questionnaire-followup.md.
    """


@pytest.mark.skip(reason="skeleton: S6.2 not implemented")
def test_dod_1_items_appear_under_their_level_headings() -> None:
    """Items appear under their level headings.

    Spec: S6.2 | Traces to: C1
    Expected outcome: Items appear under their level headings.
    """


@pytest.mark.skip(reason="skeleton: S6.3 not implemented")
def test_prd_1_closed_questions_are_absent_from_the() -> None:
    """Closed questions are absent from the PRD.

    Spec: S6.3 | Traces to: I3
    Expected outcome: Closed questions are absent from the PRD.
    """


@pytest.mark.skip(reason="skeleton: S6.3 not implemented")
def test_prd_2_the_pdf_shows_approved_once_approved() -> None:
    """The PDF shows Approved once approved_by is set.

    Spec: S6.3 | Traces to: I3
    Expected outcome: The PDF shows Approved once approved_by is set.
    """


@pytest.mark.skip(reason="skeleton: S6.4 not implemented")
def test_spec_1_spec_md_lists_every_coverage_row() -> None:
    """spec.md lists every coverage row.

    Spec: S6.4 | Traces to: C1
    Expected outcome: spec.md lists every coverage row.
    """


@pytest.mark.skip(reason="skeleton: S6.6 not implemented")
def test_tickets_1_the_csv_s_first_row_is() -> None:
    """The CSV's first row is the header.

    Spec: S6.6 | Traces to: C1, C6
    Expected outcome: The CSV's first row is the header.
    """


@pytest.mark.skip(reason="skeleton: S6.6 not implemented")
def test_tickets_2_the_prompt_contains_a_csv_code() -> None:
    """The prompt contains a csv code block and '1 story, 2 features, 4 tickets'.

    Spec: S6.6 | Traces to: C1, C6
    Expected outcome: The prompt contains a csv code block and '1 story, 2 features,
                      4 tickets'.
    """
