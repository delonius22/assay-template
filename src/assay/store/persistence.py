"""Open the checkpoint saver and the shared store.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C5 Durable sessions. Sessions must survive a closed tab or a
restart. This file opens storage and registers saved types; it never decides what is
saved.

Why this comes now: Models (step 2) define what is saved and Settings (step 1) say
where. The workflow needs storage before it can pause.

Build order: Step 16 of 33.
Previous: src/assay/llm/client.py (step 15), which creates the gateway chat client.
Next: src/assay/graph/state.py (step 17), which defines AssayState, the session
saved after every step.

Build these in order:
    1. Persistence: the return type.
    2. serializer: needed before any saver is created.
    3. open_persistence: uses serializer.

Depends on:
    assay.domain.models: every model, registered with the serializer.
    assay.settings: Settings. Database URL and SQLite path.
    Standard library: inspect, sqlite3, dataclasses, collections.abc.
    Third-party: langgraph, langgraph-checkpoint-postgres, langgraph-checkpoint-sqlite, psycopg, psycopg-pool, pydantic.

Depended on by:
    assay.api.app: opens persistence at startup.

Spec coverage: S7.1, S7.2 | Traces to: I6, I16
"""

import inspect
import sqlite3
from collections.abc import Callable
from dataclasses import dataclass

from langgraph.checkpoint.base import BaseCheckpointSaver
from langgraph.checkpoint.serde.jsonplus import JsonPlusSerializer
from langgraph.store.base import BaseStore
from pydantic import BaseModel

from assay.domain import models as domain
from assay.settings import Settings


@dataclass
class Persistence:
    """The opened checkpoint saver, store, and how to close them.

    Problem piece: C5: one handle for everything that persists.

    Why it matters: Startup opens storage once and shutdown must close it; bundling
                    them keeps both in step.

    What: Checkpointer, store, a close function, and the backend name.

    Spec: S7.2 | Ticket: — | Traces to: —
    """

    checkpointer: BaseCheckpointSaver[str]
    store: BaseStore
    close: Callable[[], None]
    backend: str


def serializer() -> JsonPlusSerializer:
    """Return a checkpoint serializer that allows every domain model and the session state.

    Problem piece: C5: saved sessions still load after an upgrade (I16).

    Why it matters: LangGraph is moving to refuse unregistered custom types when
                    loading checkpoints. Without registration, a routine upgrade
                    would strand every paused session. Generating the list from the
                    models module means a new model can never be forgotten.

    What: Allows every Pydantic model defined in the domain models module, plus
          assay.graph.state AssayState. Called as serializer() and returns
          JsonPlusSerializer.

    Spec: S7.1 | Ticket: 02 | Traces to: I16

    Build steps:
    1. Task: Collect every Pydantic model class defined in the domain models module
             itself, as (module, class name) pairs, and add ('assay.graph.state',
             'AssayState').
       Think about: Why only classes defined in that module, not ones it imports?
       Expected outcome: The list includes LogEntry and AssayState and nothing from
                         pydantic.
    2. Task: Return a JSON-plus serializer whose allowed msgpack modules are that
             list.
       Expected outcome: A session saved and reloaded with
                         LANGGRAPH_STRICT_MSGPACK=true loads without error.
    """
    raise NotImplementedError("S7.1: serializer")


def open_persistence(s: Settings) -> Persistence:
    """Open Postgres when a database URL is set, else SQLite in a local file.

    Problem piece: C5: every completed step saved, in production and in development.

    Why it matters: Production needs Postgres so several people and restarts share
                    sessions; developers need no server. Both must behave
                    identically, and both must create their tables on first start.

    What: Postgres: a connection pool with autocommit, no prepared statements, and
          dictionary rows; a saver using serializer() and a store; tables created.
          SQLite: one shared connection with the same.

    Spec: S7.2 | Ticket: 02, 11 | Traces to: I6, I16

    Build steps:
    1. Task: With a database URL, import the Postgres saver, store, row factory, and
             pool inside this branch; open a pool of 1 to 10 connections with
             autocommit on, prepare threshold 0, and dictionary rows.
       Think about: Why must the Postgres imports stay inside this branch?
       Expected outcome: Development without Postgres installed still imports this
                         module.
    2. Task: Create the saver with serializer() and the store on that pool, run both
             setups, and return Persistence named 'postgres' with the pool's close.
       Expected outcome: A session saved by one pool loads in a fresh pool after
                         restart.
    3. Task: Without a URL, create the SQLite file's folder, open one connection
             usable from any thread in autocommit mode, create the SQLite saver and
             store the same way, and return Persistence named 'sqlite'.
       Expected outcome: Starting twice reuses the same SQLite file.
    """
    raise NotImplementedError("S7.2: open_persistence")
