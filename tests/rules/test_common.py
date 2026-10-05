"""Tests for assay.rules.common (build step 4).

Covers: S3.1. Each test guards one expected outcome from the build steps in
src/assay/rules/common.py.
"""

import pytest

from assay.rules.common import compliance_claims, one_question, strings, vague_words


@pytest.mark.skip(reason="skeleton: S3.1 not implemented")
def test_strings_1_a_model_holding_a_list_of() -> None:
    """A model holding a list of rows yields every row's text and no numbers.

    Spec: S3.1 | Traces to: I4
    Expected outcome: A model holding a list of rows yields every row's text and no
                      numbers.
    """


@pytest.mark.skip(reason="skeleton: S3.1 not implemented")
def test_compliance_claims_1_the_design_conforms_to_reg_e() -> None:
    """'The design conforms to Reg E.' produces one problem.

    Spec: S3.1 | Traces to: I4
    Expected outcome: 'The design conforms to Reg E.' produces one problem.
    """


@pytest.mark.skip(reason="skeleton: S3.1 not implemented")
def test_compliance_claims_2_reg_e_applicability_compliance_to_confirm() -> None:
    """'Reg E applicability: Compliance to confirm.' produces no problem.

    Spec: S3.1 | Traces to: I4
    Expected outcome: 'Reg E applicability: Compliance to confirm.' produces no
                      problem.
    """


@pytest.mark.skip(reason="skeleton: S3.1 not implemented")
def test_one_question_1_what_problem_who_has_it_produces() -> None:
    """'What problem? Who has it?' produces one problem.

    Spec: S3.1 | Traces to: I1
    Expected outcome: 'What problem? Who has it?' produces one problem.
    """


@pytest.mark.skip(reason="skeleton: S3.1 not implemented")
def test_vague_words_1_properly_tested_yields_properly_cleanup_done() -> None:
    """'Properly tested' yields properly; 'cleanup done' yields nothing.

    Spec: S3.1 | Traces to: I1
    Expected outcome: 'Properly tested' yields properly; 'cleanup done' yields
                      nothing.
    """
