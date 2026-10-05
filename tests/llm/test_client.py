"""Tests for assay.llm.client (build step 15).

Covers: S4.3. Each test guards one expected outcome from the build steps in
src/assay/llm/client.py.
"""

import pytest

from assay.llm.client import make_model


@pytest.mark.skip(reason="skeleton: S4.3 not implemented")
def test_make_model_1_constructing_a_client_makes_no_network() -> None:
    """Constructing a client makes no network call; a real call is checked manually
    (A1).

        Spec: S4.3 | Traces to: I9, I11, A1
        Expected outcome: Constructing a client makes no network call; a real call is
                          checked manually (A1).
    """
