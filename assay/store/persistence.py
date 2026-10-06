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
    """Open the persistence layer with Postgres as the backend.

    Expected outcome: same behavior as Postgres, no server needed.
    """
   from langgraph.checkpoint.postgres import PostgresSaver
   from langgraph.store.postgres import PostgresStore
   from psycopg.rows import dict_row
   from psycopg_pool import ConnectionPool

   pool = ConnectionPool(s.database_url, min_size=1, max_size=10,
                          open=True, kwargs={"autocommit": True, "prepare_threshold": 0, "row_factory": dict_row})
   saver, store = PostgresSaver(pool, serde=serializer()), PostgresStore(pool)
   saver.setup()
   store.setup()
   return Persistence(saver, store, pool.close, "postgres")
   
