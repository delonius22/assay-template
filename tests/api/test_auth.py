"""Tests for assay.api.auth (build step 28).

Covers: S8.1. Each test guards one expected outcome from the build steps in
src/assay/api/auth.py.
"""

import pytest

from assay.api.auth import user_from


@pytest.mark.skip(reason="skeleton: S8.1 not implemented")
def test_user_from_1_a_request_with_no_header_and() -> None:
    """A request with no header and no development user gets 401.

    Spec: S8.1 | Traces to: I8, A4
    Expected outcome: A request with no header and no development user gets 401.
    """
