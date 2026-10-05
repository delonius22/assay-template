"""Tests for assay.rules.dod (build step 6).

Covers: S3.3. Each test guards one expected outcome from the build steps in
src/assay/rules/dod.py.
"""

import pytest

from assay.rules.dod import draft_problems, team_problems


@pytest.mark.skip(reason="skeleton: S3.3 not implemented")
def test_draft_problems_1_code_is_clean_produces_one_problem() -> None:
    """'Code is clean' produces one problem.

    Spec: S3.3 | Traces to: I1
    Expected outcome: 'Code is clean' produces one problem.
    """


@pytest.mark.skip(reason="skeleton: S3.3 not implemented")
def test_draft_problems_2_a_19_word_statement_produces_one() -> None:
    """A 19-word statement produces one problem.

    Spec: S3.3 | Traces to: I1
    Expected outcome: A 19-word statement produces one problem.
    """


@pytest.mark.skip(reason="skeleton: S3.3 not implemented")
def test_team_problems_1_a_standard_with_13_ticket_level() -> None:
    """A standard with 13 ticket-level items produces a problem.

    Spec: S3.3 | Traces to: I1
    Expected outcome: A standard with 13 ticket-level items produces a problem.
    """
