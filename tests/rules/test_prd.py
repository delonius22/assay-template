"""Tests for assay.rules.prd (build step 7).

Covers: S3.4. Each test guards one expected outcome from the build steps in
src/assay/rules/prd.py.
"""

import pytest

from assay.rules.prd import core_problems, narrative_problems


@pytest.mark.skip(reason="skeleton: S3.4 not implemented")
def test_core_problems_1_a_story_low_balance_alerts_produces() -> None:
    """A story 'Low-balance alerts' produces a wording problem.

    Spec: S3.4 | Traces to: I3, I4
    Expected outcome: A story 'Low-balance alerts' produces a wording problem.
    """


@pytest.mark.skip(reason="skeleton: S3.4 not implemented")
def test_core_problems_2_restarting_f_01_under_the_second() -> None:
    """Restarting F-01 under the second story produces a problem.

    Spec: S3.4 | Traces to: I3, I4
    Expected outcome: Restarting F-01 under the second story produces a problem.
    """


@pytest.mark.skip(reason="skeleton: S3.4 not implemented")
def test_core_problems_3_a_source_d_999_produces_a() -> None:
    """A source D-999 produces a problem naming D-999.

    Spec: S3.4 | Traces to: I3, I4
    Expected outcome: A source D-999 produces a problem naming D-999.
    """


@pytest.mark.skip(reason="skeleton: S3.4 not implemented")
def test_narrative_problems_1_an_objective_citing_d_999_produces() -> None:
    """An objective citing D-999 produces a problem.

    Spec: S3.4 | Traces to: I3, I4
    Expected outcome: An objective citing D-999 produces a problem.
    """
