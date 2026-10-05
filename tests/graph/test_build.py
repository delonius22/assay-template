"""Tests for assay.graph.build (build step 27).

Covers: S5.11. Each test guards one expected outcome from the build steps in
src/assay/graph/build.py.
"""

import pytest

from assay.graph.build import build_graph


@pytest.mark.skip(reason="skeleton: S5.11 not implemented")
def test_build_graph_1_the_compiled_graph_has_25_nodes() -> None:
    """The compiled graph has 25 nodes including start and end.

    Spec: S5.11 | Traces to: I5, I7
    Expected outcome: The compiled graph has 25 nodes including start and end.
    """


@pytest.mark.skip(reason="skeleton: S5.11 not implemented")
def test_build_graph_2_a_mode_1_session_pauses_first() -> None:
    """A mode 1 session pauses first at grill_ask.

    Spec: S5.11 | Traces to: I5, I7
    Expected outcome: A mode 1 session pauses first at grill_ask.
    """


@pytest.mark.skip(reason="skeleton: S5.11 not implemented")
def test_build_graph_3_a_full_scripted_session_pauses_at() -> None:
    """A full scripted session pauses at question, dod_question, approval, seams,
    ticket_review in order.

        Spec: S5.11 | Traces to: I5, I7
        Expected outcome: A full scripted session pauses at question, dod_question,
                          approval, seams, ticket_review in order.
    """
