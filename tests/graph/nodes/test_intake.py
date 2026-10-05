"""Tests for assay.graph.nodes.intake (build step 22).

Covers: S5.3, S5.4, S5.5, S5.6. Each test guards one expected outcome from the build
steps in src/assay/graph/nodes/intake.py.
"""

import pytest

from assay.graph.nodes.intake import (
    after_brief,
    after_gate,
    after_grill,
    after_read,
    after_reconcile,
    await_answers_ask,
    brief_check,
    brief_fix_ask,
    confirm_map_ask,
    explore,
    grill_ask,
    grill_think,
    intake_gate_node,
    read_responses,
    reconcile,
    route_mode,
    setup,
    write_questionnaire,
)


@pytest.mark.skip(reason="skeleton: S5.3 not implemented")
def test_setup_1_mode_3_without_a_brief_raises() -> None:
    """Mode 3 without a brief raises.

    Spec: S5.3 | Traces to: I6, I12
    Expected outcome: Mode 3 without a brief raises.
    """


@pytest.mark.skip(reason="skeleton: S5.3 not implemented")
def test_setup_2_a_second_session_skips_the_team() -> None:
    """A second session skips the team phase.

    Spec: S5.3 | Traces to: I6, I12
    Expected outcome: A second session skips the team phase.
    """


@pytest.mark.skip(reason="skeleton: S5.3 not implemented")
def test_setup_3_intake_md_exists_after_setup() -> None:
    """intake.md exists after setup.

    Spec: S5.3 | Traces to: I6, I12
    Expected outcome: intake.md exists after setup.
    """


@pytest.mark.skip(reason="skeleton: S5.3 not implemented")
def test_route_mode_1_mode_3_routes_to_brief_check() -> None:
    """Mode 3 routes to brief_check.

    Spec: S5.3 | Traces to: I5
    Expected outcome: Mode 3 routes to brief_check.
    """


@pytest.mark.skip(reason="skeleton: S5.3 not implemented")
def test_grill_think_1_the_static_prompt_is_identical_on() -> None:
    """The static prompt is identical on every turn.

    Spec: S5.3 | Traces to: I1, I7
    Expected outcome: The static prompt is identical on every turn.
    """


@pytest.mark.skip(reason="skeleton: S5.3 not implemented")
def test_grill_think_2_a_new_term_is_visible_to() -> None:
    """A new term is visible to the next session.

    Spec: S5.3 | Traces to: I1, I7
    Expected outcome: A new term is visible to the next session.
    """


@pytest.mark.skip(reason="skeleton: S5.3 not implemented")
def test_grill_think_3_recorded_entries_receive_ids_like_d() -> None:
    """Recorded entries receive IDs like D-001.

    Spec: S5.3 | Traces to: I1, I7
    Expected outcome: Recorded entries receive IDs like D-001.
    """


@pytest.mark.skip(reason="skeleton: S5.3 not implemented")
def test_grill_think_4_a_done_turn_returns_no_pending() -> None:
    """A done turn returns no pending question.

    Spec: S5.3 | Traces to: I1, I7
    Expected outcome: A done turn returns no pending question.
    """


@pytest.mark.skip(reason="skeleton: S5.3 not implemented")
def test_grill_ask_1_resuming_runs_no_model_call() -> None:
    """Resuming runs no model call.

    Spec: S5.3 | Traces to: I7
    Expected outcome: Resuming runs no model call.
    """


@pytest.mark.skip(reason="skeleton: S5.3 not implemented")
def test_grill_ask_2_the_answer_is_recorded_with_the() -> None:
    """The answer is recorded with the answering user.

    Spec: S5.3 | Traces to: I7
    Expected outcome: The answer is recorded with the answering user.
    """


@pytest.mark.skip(reason="skeleton: S5.3 not implemented")
def test_after_grill_1_no_pending_question_routes_to_intake() -> None:
    """No pending question routes to intake_gate_node.

    Spec: S5.3 | Traces to: I5
    Expected outcome: No pending question routes to intake_gate_node.
    """


@pytest.mark.skip(reason="skeleton: S5.4 not implemented")
def test_explore_1_the_returned_map_lists_the_files() -> None:
    """The returned map lists the files it was built from.

    Spec: S5.4 | Traces to: I10
    Expected outcome: The returned map lists the files it was built from.
    """


@pytest.mark.skip(reason="skeleton: S5.4 not implemented")
def test_confirm_map_ask_1_resuming_runs_no_model_call() -> None:
    """Resuming runs no model call.

    Spec: S5.4 | Traces to: I7
    Expected outcome: Resuming runs no model call.
    """


@pytest.mark.skip(reason="skeleton: S5.4 not implemented")
def test_confirm_map_ask_2_a_reply_of_ok_changes_nothing() -> None:
    """A reply of 'ok' changes nothing; any other reply adds a C entry.

    Spec: S5.4 | Traces to: I7
    Expected outcome: A reply of 'ok' changes nothing; any other reply adds a C
                      entry.
    """


@pytest.mark.skip(reason="skeleton: S5.5 not implemented")
def test_brief_check_1_a_brief_with_a_testable_outcome() -> None:
    """A brief with a testable outcome returns no issues.

    Spec: S5.5 | Traces to: I12
    Expected outcome: A brief with a testable outcome returns no issues.
    """


@pytest.mark.skip(reason="skeleton: S5.5 not implemented")
def test_after_brief_1_a_brief_with_issues_routes_to() -> None:
    """A brief with issues routes to brief_fix_ask.

    Spec: S5.5 | Traces to: I5
    Expected outcome: A brief with issues routes to brief_fix_ask.
    """


@pytest.mark.skip(reason="skeleton: S5.5 not implemented")
def test_brief_fix_ask_1_resuming_runs_no_model_call() -> None:
    """Resuming runs no model call.

    Spec: S5.5 | Traces to: I7
    Expected outcome: Resuming runs no model call.
    """


@pytest.mark.skip(reason="skeleton: S5.5 not implemented")
def test_brief_fix_ask_2_an_edited_brief_replaces_the_old() -> None:
    """An edited brief replaces the old one.

    Spec: S5.5 | Traces to: I7
    Expected outcome: An edited brief replaces the old one.
    """


@pytest.mark.skip(reason="skeleton: S5.5 not implemented")
def test_write_questionnaire_1_the_questionnaire_has_1_to_30() -> None:
    """The questionnaire has 1 to 30 questions.

    Spec: S5.5 | Traces to: I2
    Expected outcome: The questionnaire has 1 to 30 questions.
    """


@pytest.mark.skip(reason="skeleton: S5.5 not implemented")
def test_write_questionnaire_2_the_returned_ids_include_q_01() -> None:
    """The returned IDs include Q-01.

    Spec: S5.5 | Traces to: I2
    Expected outcome: The returned IDs include Q-01.
    """


@pytest.mark.skip(reason="skeleton: S5.5 not implemented")
def test_await_answers_ask_1_resuming_runs_no_model_call() -> None:
    """Resuming runs no model call.

    Spec: S5.5 | Traces to: I7
    Expected outcome: Resuming runs no model call.
    """


@pytest.mark.skip(reason="skeleton: S5.5 not implemented")
def test_await_answers_ask_2_resuming_clears_the_no_responses_note() -> None:
    """Resuming clears the 'no responses' note.

    Spec: S5.5 | Traces to: I7
    Expected outcome: Resuming clears the 'no responses' note.
    """


@pytest.mark.skip(reason="skeleton: S5.5 not implemented")
def test_read_responses_1_a_resubmitted_sheet_is_not_read() -> None:
    """A resubmitted sheet is not read twice.

    Spec: S5.5 | Traces to: I12
    Expected outcome: A resubmitted sheet is not read twice.
    """


@pytest.mark.skip(reason="skeleton: S5.5 not implemented")
def test_read_responses_2_with_no_responses_the_note_is() -> None:
    """With no responses the note is returned.

    Spec: S5.5 | Traces to: I12
    Expected outcome: With no responses the note is returned.
    """


@pytest.mark.skip(reason="skeleton: S5.5 not implemented")
def test_after_read_1_a_note_routes_back_to_await() -> None:
    """A note routes back to await_answers_ask.

    Spec: S5.5 | Traces to: I5
    Expected outcome: A note routes back to await_answers_ask.
    """


@pytest.mark.skip(reason="skeleton: S5.5 not implemented")
def test_reconcile_1_recorded_entries_cite_ids_like_q() -> None:
    """Recorded entries cite IDs like Q-02.

    Spec: S5.5 | Traces to: I1, I2
    Expected outcome: Recorded entries cite IDs like Q-02.
    """


@pytest.mark.skip(reason="skeleton: S5.5 not implemented")
def test_reconcile_2_a_corrected_answer_becomes_a_decision() -> None:
    """A corrected answer becomes a decision.

    Spec: S5.5 | Traces to: I1, I2
    Expected outcome: A corrected answer becomes a decision.
    """


@pytest.mark.skip(reason="skeleton: S5.5 not implemented")
def test_reconcile_3_round_1_with_two_blocking_gaps() -> None:
    """Round 1 with two blocking gaps opens round 2.

    Spec: S5.5 | Traces to: I1, I2
    Expected outcome: Round 1 with two blocking gaps opens round 2.
    """


@pytest.mark.skip(reason="skeleton: S5.5 not implemented")
def test_reconcile_4_round_2_with_remaining_gaps_sends() -> None:
    """Round 2 with remaining gaps sends them to the grill.

    Spec: S5.5 | Traces to: I1, I2
    Expected outcome: Round 2 with remaining gaps sends them to the grill.
    """


@pytest.mark.skip(reason="skeleton: S5.5 not implemented")
def test_after_reconcile_1_a_newly_opened_round_2_waits() -> None:
    """A newly opened round 2 waits for answers.

    Spec: S5.5 | Traces to: I5
    Expected outcome: A newly opened round 2 waits for answers.
    """


@pytest.mark.skip(reason="skeleton: S5.6 not implemented")
def test_intake_gate_node_1_intake_md_shows_the_current_gate() -> None:
    """intake.md shows the current gate.

    Spec: S5.6 | Traces to: I5
    Expected outcome: intake.md shows the current gate.
    """


@pytest.mark.skip(reason="skeleton: S5.6 not implemented")
def test_intake_gate_node_2_a_passing_gate_sets_stage_prd() -> None:
    """A passing gate sets stage 'PRD'.

    Spec: S5.6 | Traces to: I5
    Expected outcome: A passing gate sets stage 'PRD'.
    """


@pytest.mark.skip(reason="skeleton: S5.6 not implemented")
def test_after_gate_1_an_empty_agenda_routes_to_prd() -> None:
    """An empty agenda routes to prd.

    Spec: S5.6 | Traces to: I5
    Expected outcome: An empty agenda routes to prd.
    """
