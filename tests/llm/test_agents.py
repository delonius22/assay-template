"""Tests for assay.llm.agents (build step 14).

Covers: S4.6. Each test guards one expected outcome from the build steps in
src/assay/llm/agents.py.
"""

import pytest

from assay.llm.agents import (
    agent,
    post_explore,
    static,
    text,
    v_dod,
    v_explore,
    v_grill,
    v_prd_core,
    v_prd_narrative,
    v_questionnaire,
    v_reconcile,
    v_spec,
    v_tickets,
)


@pytest.mark.skip(reason="skeleton: S4.6 not implemented")
def test_text_1_common_md_returns_text_starting_rules() -> None:
    """'common.md' returns text starting '# Rules for every task'.

    Spec: S4.6 | Traces to: I1
    Expected outcome: 'common.md' returns text starting '# Rules for every task'.
    """


@pytest.mark.skip(reason="skeleton: S4.6 not implemented")
def test_static_1_both_prd_agents_produce_the_identical() -> None:
    """Both PRD agents produce the identical prefix.

    Spec: S4.6 | Traces to: A2
    Expected outcome: Both PRD agents produce the identical prefix.
    """


@pytest.mark.skip(reason="skeleton: S4.6 not implemented")
def test_agent_1_agent_grill_2_includes_mode_2() -> None:
    """agent('grill', 2) includes mode-2.md.

    Spec: S4.6 | Traces to: I1
    Expected outcome: agent('grill', 2) includes mode-2.md.
    """


@pytest.mark.skip(reason="skeleton: S4.6 not implemented")
def test_agent_2_agent_tickets_returns_a_spec_whose() -> None:
    """agent('tickets') returns a spec whose output is TicketPlan.

    Spec: S4.6 | Traces to: I1
    Expected outcome: agent('tickets') returns a spec whose output is TicketPlan.
    """


@pytest.mark.skip(reason="skeleton: S4.6 not implemented")
def test_v_grill_1_done_false_with_no_question_is() -> None:
    """done=false with no question is rejected.

    Spec: S4.6 | Traces to: I1, I4
    Expected outcome: done=false with no question is rejected.
    """


@pytest.mark.skip(reason="skeleton: S4.6 not implemented")
def test_v_grill_2_superseding_d_999_is_rejected() -> None:
    """Superseding D-999 is rejected.

    Spec: S4.6 | Traces to: I1, I4
    Expected outcome: Superseding D-999 is rejected.
    """


@pytest.mark.skip(reason="skeleton: S4.6 not implemented")
def test_v_explore_1_a_map_before_any_read_is() -> None:
    """A map before any read is rejected.

    Spec: S4.6 | Traces to: I1
    Expected outcome: A map before any read is rejected.
    """


@pytest.mark.skip(reason="skeleton: S4.6 not implemented")
def test_v_questionnaire_1_a_question_depending_on_itself_is() -> None:
    """A question depending on itself is rejected.

    Spec: S4.6 | Traces to: I1, I4
    Expected outcome: A question depending on itself is rejected.
    """


@pytest.mark.skip(reason="skeleton: S4.6 not implemented")
def test_v_reconcile_1_a_scope_entry_without_a_side() -> None:
    """A scope entry without a side is rejected.

    Spec: S4.6 | Traces to: I1, I4
    Expected outcome: A scope entry without a side is rejected.
    """


@pytest.mark.skip(reason="skeleton: S4.6 not implemented")
def test_v_dod_1_code_is_clean_is_rejected() -> None:
    """'Code is clean' is rejected.

    Spec: S4.6 | Traces to: I1
    Expected outcome: 'Code is clean' is rejected.
    """


@pytest.mark.skip(reason="skeleton: S4.6 not implemented")
def test_v_prd_core_1_citing_d_999_is_rejected() -> None:
    """Citing D-999 is rejected.

    Spec: S4.6 | Traces to: I3
    Expected outcome: Citing D-999 is rejected.
    """


@pytest.mark.skip(reason="skeleton: S4.6 not implemented")
def test_v_prd_narrative_1_an_objective_citing_d_999_is() -> None:
    """An objective citing D-999 is rejected.

    Spec: S4.6 | Traces to: I3
    Expected outcome: An objective citing D-999 is rejected.
    """


@pytest.mark.skip(reason="skeleton: S4.6 not implemented")
def test_v_spec_1_a_spec_missing_fr_02_is() -> None:
    """A spec missing FR-02 is rejected.

    Spec: S4.6 | Traces to: I1
    Expected outcome: A spec missing FR-02 is rejected.
    """


@pytest.mark.skip(reason="skeleton: S4.6 not implemented")
def test_v_tickets_1_a_plan_missing_fr_03_is() -> None:
    """A plan missing FR-03 is rejected.

    Spec: S4.6 | Traces to: I15
    Expected outcome: A plan missing FR-03 is rejected.
    """


@pytest.mark.skip(reason="skeleton: S4.6 not implemented")
def test_post_explore_1_a_file_read_twice_appears_once() -> None:
    """A file read twice appears once.

    Spec: S4.6 | Traces to: I1
    Expected outcome: A file read twice appears once.
    """
