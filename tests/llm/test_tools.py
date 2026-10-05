"""Tests for assay.llm.tools (build step 12).

Covers: S4.4. Each test guards one expected outcome from the build steps in
src/assay/llm/tools.py.
"""

import pytest

from assay.llm.tools import (
    Deps,
    ListFiles,
    ReadFile,
    SearchCode,
    ToolError,
    denied,
    list_files,
    read_file,
    redact,
    resolve,
    roots_from,
    run_tool,
    search_code,
)


@pytest.mark.skip(reason="skeleton: S4.4 not implemented")
def test_roots_from_1_a_root_srv_repos_payments_is() -> None:
    """A root /srv/repos/payments is addressed as 'payments'.

    Spec: S4.4 | Traces to: I10
    Expected outcome: A root /srv/repos/payments is addressed as 'payments'.
    """


@pytest.mark.skip(reason="skeleton: S4.4 not implemented")
def test_denied_1_env_and_config_env_are_both() -> None:
    """'.env' and 'config/.env' are both denied.

    Spec: S4.4 | Traces to: I10
    Expected outcome: '.env' and 'config/.env' are both denied.
    """


@pytest.mark.skip(reason="skeleton: S4.4 not implemented")
def test_redact_1_token_abcdef123456_becomes_the_redaction_marker() -> None:
    """'token = abcdef123456' becomes the redaction marker.

    Spec: S4.4 | Traces to: I10
    Expected outcome: 'token = abcdef123456' becomes the redaction marker.
    """


@pytest.mark.skip(reason="skeleton: S4.4 not implemented")
def test_resolve_1_elsewhere_x_py_is_refused() -> None:
    """'elsewhere/x.py' is refused.

    Spec: S4.4 | Traces to: I10, I12
    Expected outcome: 'elsewhere/x.py' is refused.
    """


@pytest.mark.skip(reason="skeleton: S4.4 not implemented")
def test_resolve_2_payments_etc_passwd_is_refused_as() -> None:
    """'payments/../../etc/passwd' is refused as outside the allowed directories.

    Spec: S4.4 | Traces to: I10, I12
    Expected outcome: 'payments/../../etc/passwd' is refused as outside the allowed
                      directories.
    """


@pytest.mark.skip(reason="skeleton: S4.4 not implemented")
def test_list_files_1_payments_py_searches_only_payments() -> None:
    """'payments/**/*.py' searches only payments.

    Spec: S4.4 | Traces to: I10, I12
    Expected outcome: 'payments/**/*.py' searches only payments.
    """


@pytest.mark.skip(reason="skeleton: S4.4 not implemented")
def test_list_files_2_a_root_s_env_never_appears() -> None:
    """A root's .env never appears.

    Spec: S4.4 | Traces to: I10, I12
    Expected outcome: A root's .env never appears.
    """


@pytest.mark.skip(reason="skeleton: S4.4 not implemented")
def test_read_file_1_a_missing_file_is_refused() -> None:
    """A missing file is refused.

    Spec: S4.4 | Traces to: I10, I12
    Expected outcome: A missing file is refused.
    """


@pytest.mark.skip(reason="skeleton: S4.4 not implemented")
def test_read_file_2_reading_a_file_containing_a_password() -> None:
    """Reading a file containing a password returns the redaction marker on that
    line.

        Spec: S4.4 | Traces to: I10, I12
        Expected outcome: Reading a file containing a password returns the redaction
                          marker on that line.
    """


@pytest.mark.skip(reason="skeleton: S4.4 not implemented")
def test_search_code_1_is_refused() -> None:
    """'(' is refused.

    Spec: S4.4 | Traces to: I10, I12
    Expected outcome: '(' is refused.
    """


@pytest.mark.skip(reason="skeleton: S4.4 not implemented")
def test_search_code_2_searching_def_w_returns_a_hit() -> None:
    r"""Searching 'def \w+' returns a hit like 'payments/src/app.py:1: def save()'.

    Spec: S4.4 | Traces to: I10, I12
    Expected outcome: Searching 'def \w+' returns a hit like 'payments/src/app.py:1:
                      def save()'.
    """


@pytest.mark.skip(reason="skeleton: S4.4 not implemented")
def test_run_tool_1_calling_deletefile_is_refused() -> None:
    """Calling 'DeleteFile' is refused.

    Spec: S4.4 | Traces to: I12
    Expected outcome: Calling 'DeleteFile' is refused.
    """


@pytest.mark.skip(reason="skeleton: S4.4 not implemented")
def test_run_tool_2_a_valid_readfile_call_returns_numbered() -> None:
    """A valid ReadFile call returns numbered lines.

    Spec: S4.4 | Traces to: I12
    Expected outcome: A valid ReadFile call returns numbered lines.
    """
