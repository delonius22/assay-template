"""Tests for assay.rules.spec (build step 8).

Covers: S3.5. Each test guards one expected outcome from the build steps in
src/assay/rules/spec.py.
"""

import pytest

from assay.rules.spec import problems


@pytest.mark.skip(reason="skeleton: S3.5 not implemented")
def test_problems_1_a_spec_omitting_fr_02_produces() -> None:
    """A spec omitting FR-02 produces a problem naming FR-02.

    Spec: S3.5 | Traces to: I1
    Expected outcome: A spec omitting FR-02 produces a problem naming FR-02.
    """


@pytest.mark.skip(reason="skeleton: S3.5 not implemented")
def test_problems_2_a_module_serving_fr_99_produces() -> None:
    """A module serving FR-99 produces a problem.

    Spec: S3.5 | Traces to: I1
    Expected outcome: A module serving FR-99 produces a problem.
    """
