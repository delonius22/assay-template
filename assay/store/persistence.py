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
    """A checkpoint serializer that allows every domain model and the session state. """
    allowed = [(c.__module__, c.__name__) for _, c in inspect.getmembers(domain, inspect.isclass)
       if issubclass(c, BaseModel) and c.__module__ == domain.__name__]
    allowed.append(("assay.graph.state", "AssayState"))
    return JsonPlusSerializer(allowed_msgpack_modules=allowed)


def open_persistence(s: Settings) -> Persistence:
    """Open the checkpointer and store: Postgres when a database URL is set, else SQLite.

    Spec: S7.2 | Ticket: 02, 11 | Traces to: I6, I16
    """
    if s.database_url:
        from langgraph.checkpoint.postgres import PostgresSaver
        from langgraph.store.postgres import PostgresStore
        from psycopg.rows import dict_row
        from psycopg_pool import ConnectionPool

        pool = ConnectionPool(s.database_url, min_size=1, max_size=10,
                              open=True, kwargs={"autocommit": True, "prepare_threshold": 0,
                                                 "row_factory": dict_row})
        saver, store = PostgresSaver(pool, serde=serializer()), PostgresStore(pool)
        saver.setup()
        store.setup()
        return Persistence(saver, store, pool.close, "postgres")
    from langgraph.checkpoint.sqlite import SqliteSaver
    from langgraph.store.sqlite import SqliteStore

    s.sqlite_path.parent.mkdir(parents=True, exist_ok=True)
    # One connection per backend: the checkpointer and the store each run their own
    # BEGIN/COMMIT transactions, so a shared connection would let them interleave.
    def _conn() -> sqlite3.Connection:
        c = sqlite3.connect(s.sqlite_path, check_same_thread=False)
        c.isolation_level = None  # autocommit mode; langgraph issues explicit BEGIN/COMMIT
        return c

    saver_conn, store_conn = _conn(), _conn()
    saver, store = SqliteSaver(saver_conn, serde=serializer()), SqliteStore(store_conn)
    saver.setup()
    store.setup()

    def close() -> None:
        saver_conn.close()
        store_conn.close()

    return Persistence(saver, store, close, "sqlite")
    
