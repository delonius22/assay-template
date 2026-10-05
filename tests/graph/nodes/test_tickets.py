"""Tests for assay.graph.nodes.tickets (build step 26).

Covers: S5.10. Each test guards one expected outcome from the build steps in
src/assay/graph/nodes/tickets.py.
"""

import pytest

from assay.graph.nodes.tickets import (
    after_ticket_review,
    export_tickets,
    ticket_review_ask,
    tickets,
)


@pytest.mark.skip(reason="skeleton: S5.10 not implemented")
def test_tickets_1_reviewer_feedback_appears_in_the_prompt() -> None:
    """Reviewer feedback appears in the prompt.

    Spec: S5.10 | Traces to: I15
    Expected outcome: Reviewer feedback appears in the prompt.
    """


@pytest.mark.skip(reason="skeleton: S5.10 not implemented")
def test_tickets_2_tickets_are_numbered_t_001_onward() -> None:
    """Tickets are numbered T-001 onward.

    Spec: S5.10 | Traces to: I15
    Expected outcome: Tickets are numbered T-001 onward.
    """


@pytest.mark.skip(reason="skeleton: S5.10 not implemented")
def test_ticket_review_ask_1_resuming_runs_no_model_call() -> None:
    """Resuming runs no model call.

    Spec: S5.10 | Traces to: I7
    Expected outcome: Resuming runs no model call.
    """


@pytest.mark.skip(reason="skeleton: S5.10 not implemented")
def test_ticket_review_ask_2_changes_produce_feedback_approval_clears_it() -> None:
    """Changes produce feedback; approval clears it.

    Spec: S5.10 | Traces to: I7
    Expected outcome: Changes produce feedback; approval clears it.
    """


@pytest.mark.skip(reason="skeleton: S5.10 not implemented")
def test_after_ticket_review_1_approval_routes_to_export_tickets() -> None:
    """Approval routes to export_tickets.

    Spec: S5.10 | Traces to: I5
    Expected outcome: Approval routes to export_tickets.
    """


@pytest.mark.skip(reason="skeleton: S5.10 not implemented")
def test_export_tickets_1_tickets_csv_and_agent_prompt_md() -> None:
    """tickets.csv and agent-prompt.md are listed in files.

    Spec: S5.10 | Traces to: C1
    Expected outcome: tickets.csv and agent-prompt.md are listed in files.
    """
