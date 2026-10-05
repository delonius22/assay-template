"""Open the checkpointer and store: Postgres in production, SQLite in development."""
import inspect
import sqlite3
from dataclasses import dataclass
from typing import Callable

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.store.base import BaseStore
from pydantic import BaseModel

from ..domain import models as domain
from ..settings import Settings


@dataclass
class Persistence:
    checkpointer: BaseCheckpointSaver
    store: BaseStore
    close: Callable[[], None]
    backend: str


def serializer() -> JsonPlusSerializer:
    """A checkpoint serializer that allows every domain model and the session state.

    Spec: S7.1 | Ticket: 02 | Traces to: I16

    Build steps:
    1. Task: `allowed = [(c.__module__, c.__name__) for _, c in inspect.getmembers(domain, inspect.isclass)
       if issubclass(c, BaseModel) and c.__module__ == domain.__name__]`.
       Expected outcome: generated from the module, so a new model is never forgotten.
    2. Task: Append `("assay.graph.state", "AssayState")`.
       Expected outcome: the state itself is allowed.
    3. Task: Return `JsonPlusSerializer(allowed_msgpack_modules=allowed)`.
       Expected outcome: saved sessions load with LANGGRAPH_STRICT_MSGPACK=true.
    """
    raise NotImplementedError("S7.1")


def open_persistence(s: Settings) -> Persistence:
    """Postgres when `s.database_url` is set, else SQLite at `s.sqlite_path`.

    Spec: S7.2 | Ticket: 02, 11 | Traces to: I6, I16

    Build steps:
    1. Task: Postgres branch (ticket 11). Import inside the branch: `from langgraph.checkpoint.postgres import PostgresSaver`,
       `from langgraph.store.postgres import PostgresStore`, `from psycopg.rows import dict_row`,
       `from psycopg_pool import ConnectionPool`. Build `pool = ConnectionPool(s.database_url, min_size=1, max_size=10,
       open=True, kwargs={"autocommit": True, "prepare_threshold": 0, "row_factory": dict_row})`.
       Expected outcome: a shared pool; autocommit and dict rows are what the LangGraph savers require.
    2. Task: `saver, store = PostgresSaver(pool, serde=serializer()), PostgresStore(pool)`; call `saver.setup()` and
       `store.setup()`; return `Persistence(saver, store, pool.close, "postgres")`.
       Expected outcome: tables created if missing; safe on every start.
    3. Task: SQLite branch (ticket 02). Import inside the branch: `from langgraph.checkpoint.sqlite import SqliteSaver`,
       `from langgraph.store.sqlite import SqliteStore`. Run `s.sqlite_path.parent.mkdir(parents=True, exist_ok=True)`;
       `conn = sqlite3.connect(s.sqlite_path, check_same_thread=False, isolation_level=None)`.
       Expected outcome: one connection shared by background threads.
    4. Task: `saver, store = SqliteSaver(conn, serde=serializer()), SqliteStore(conn)`; `saver.setup()`; `store.setup()`;
       return `Persistence(saver, store, conn.close, "sqlite")`.
       Expected outcome: same behavior as Postgres, no server needed.
    """
    raise NotImplementedError("S7.2")
