"""Tests for assay.domain.models (build step 2).

Covers: S2.1, S3.2, S5.2, S5.3, S5.4, S5.5, S5.7, S5.8, S5.9, S5.10, S8.4. Each test
guards one expected outcome from the build steps in src/assay/domain/models.py.
"""

import pytest

from assay.domain.models import (
    NFR,
    Answer,
    Brief,
    BriefCritique,
    Confirmation,
    Coverage,
    CurrentStateMap,
    DataItem,
    Decision,
    DodItem,
    DodItemDraft,
    DodTurn,
    FeatureDraft,
    FollowUp,
    GlossaryTerm,
    GrillTurn,
    LogEntry,
    Metric,
    Module,
    NewEntry,
    Objective,
    PRDCore,
    PRDNarrative,
    QItem,
    Question,
    Questionnaire,
    Reconciliation,
    Requirement,
    ResponseSheet,
    RiskControl,
    Seams,
    Spec,
    Stakeholder,
    StoryDraft,
    Ticket,
    TicketDraft,
    TicketPlan,
    Turn,
    Uncovered,
    now,
)


@pytest.mark.skip(reason="skeleton: S2.1 not implemented")
def test_now_1_the_result_parses_as_a_utc() -> None:
    """The result parses as a UTC timestamp with no fractional seconds.

    Spec: S2.1 | Traces to: I2
    Expected outcome: The result parses as a UTC timestamp with no fractional
                      seconds.
    """
