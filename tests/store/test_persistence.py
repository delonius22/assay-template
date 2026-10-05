"""Tests for assay.store.persistence (build step 16).

Covers: S7.1, S7.2. Each test guards one expected outcome from the build steps in
src/assay/store/persistence.py.
"""

import pytest

from assay.store.persistence import Persistence, open_persistence, serializer


@pytest.mark.skip(reason="skeleton: S7.1 not implemented")
def test_serializer_1_the_list_includes_logentry_and_assaystate() -> None:
    """The list includes LogEntry and AssayState and nothing from pydantic.

    Spec: S7.1 | Traces to: I16
    Expected outcome: The list includes LogEntry and AssayState and nothing from
                      pydantic.
    """


@pytest.mark.skip(reason="skeleton: S7.1 not implemented")
def test_serializer_2_a_session_saved_and_reloaded_with() -> None:
    """A session saved and reloaded with LANGGRAPH_STRICT_MSGPACK=true loads
    without error.

        Spec: S7.1 | Traces to: I16
        Expected outcome: A session saved and reloaded with
                          LANGGRAPH_STRICT_MSGPACK=true loads without error.
    """


@pytest.mark.skip(reason="skeleton: S7.2 not implemented")
def test_open_persistence_1_development_without_postgres_installed_still_imports() -> None:
    """Development without Postgres installed still imports this module.

    Spec: S7.2 | Traces to: I6, I16
    Expected outcome: Development without Postgres installed still imports this
                      module.
    """


@pytest.mark.skip(reason="skeleton: S7.2 not implemented")
def test_open_persistence_2_a_session_saved_by_one_pool() -> None:
    """A session saved by one pool loads in a fresh pool after restart.

    Spec: S7.2 | Traces to: I6, I16
    Expected outcome: A session saved by one pool loads in a fresh pool after
                      restart.
    """


@pytest.mark.skip(reason="skeleton: S7.2 not implemented")
def test_open_persistence_3_starting_twice_reuses_the_same_sqlite() -> None:
    """Starting twice reuses the same SQLite file.

    Spec: S7.2 | Traces to: I6, I16
    Expected outcome: Starting twice reuses the same SQLite file.
    """
