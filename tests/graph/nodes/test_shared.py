"""Tests for assay.graph.nodes.shared (build step 21).

Covers: S5.3, S6.1. Each test guards one expected outcome from the build steps in
src/assay/graph/nodes/shared.py.
"""

import pytest

from assay.graph.nodes.shared import files, glossary_text, reply, write_intake


@pytest.mark.skip(reason="skeleton: S5.3 not implemented")
def test_reply_1_a_mapping_with_user_dana_returns() -> None:
    """A mapping with user 'dana' returns 'dana'.

    Spec: S5.3 | Traces to: I12
    Expected outcome: A mapping with user 'dana' returns 'dana'.
    """


@pytest.mark.skip(reason="skeleton: S6.1 not implemented")
def test_write_intake_1_after_a_grill_turn_session_log() -> None:
    """After a grill turn, session-log.md lists the new entries.

    Spec: S6.1 | Traces to: C1
    Expected outcome: After a grill turn, session-log.md lists the new entries.
    """


@pytest.mark.skip(reason="skeleton: S5.3 not implemented")
def test_files_1_adding_prd_md_twice_lists_it() -> None:
    """Adding 'prd.md' twice lists it once.

    Spec: S5.3 | Traces to: I12
    Expected outcome: Adding 'prd.md' twice lists it once.
    """


@pytest.mark.skip(reason="skeleton: S5.3 not implemented")
def test_glossary_text_1_two_terms_give_two_lines() -> None:
    """Two terms give two lines.

    Spec: S5.3 | Traces to: C1
    Expected outcome: Two terms give two lines.
    """
