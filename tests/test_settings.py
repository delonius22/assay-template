"""Tests for assay.settings (build step 1).

Covers: S1.1, S1.2. Each test guards one expected outcome from the build steps in
src/assay/settings.py.
"""

import pytest

from assay.settings import Settings, env, load_settings, missing_config


@pytest.mark.skip(reason="skeleton: S1.1 not implemented")
def test_env_1_an_unset_variable_returns_the_default() -> None:
    """An unset variable returns the default; a set variable returns its exact
    text.

        Spec: S1.1 | Traces to: I9
        Expected outcome: An unset variable returns the default; a set variable returns
                          its exact text.
    """


@pytest.mark.skip(reason="skeleton: S1.1 not implemented")
def test_load_settings_1_a_role_without_its_own_variable() -> None:
    """A role without its own variable uses the default model.

    Spec: S1.1 | Traces to: I9, A1
    Expected outcome: A role without its own variable uses the default model.
    """


@pytest.mark.skip(reason="skeleton: S1.1 not implemented")
def test_load_settings_2_assay_approvers_of_dana_lee_yields() -> None:
    """ASSAY_APPROVERS of 'dana, lee ,' yields exactly dana and lee.

    Spec: S1.1 | Traces to: I9, A1
    Expected outcome: ASSAY_APPROVERS of 'dana, lee ,' yields exactly dana and lee.
    """


@pytest.mark.skip(reason="skeleton: S1.1 not implemented")
def test_load_settings_3_invalid_json_raises_an_error_at() -> None:
    """Invalid JSON raises an error at load time.

    Spec: S1.1 | Traces to: I9, A1
    Expected outcome: Invalid JSON raises an error at load time.
    """


@pytest.mark.skip(reason="skeleton: S1.1 not implemented")
def test_load_settings_4_with_no_assay_variables_set_every() -> None:
    """With no ASSAY_ variables set, every field holds its documented default.

    Spec: S1.1 | Traces to: I9, A1
    Expected outcome: With no ASSAY_ variables set, every field holds its documented
                      default.
    """


@pytest.mark.skip(reason="skeleton: S1.2 not implemented")
def test_missing_config_1_a_missing_url_and_missing_models() -> None:
    """A missing URL and missing models are named; the key's value never appears.

    Spec: S1.2 | Traces to: I9
    Expected outcome: A missing URL and missing models are named; the key's value
                      never appears.
    """
