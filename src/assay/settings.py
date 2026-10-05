"""Hold every setting the app reads, loaded once from the environment.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C5 Durable sessions and C6 People decide. Where sessions are
stored, which gateway and models to call, and who may approve are deployment facts,
not code. This file owns their shape and how they are read; it never uses them.

Why this comes now: Nothing else can be written or tested without knowing what can
be configured, and configuration depends on nothing in the project.

Build order: Step 1 of 33.
Previous: none. This is the start of the project.
Next: src/assay/domain/models.py (step 2), which defines the typed models every
agent returns and every rule checks.

Build these in order:
    1. Settings: the shape everything else reads.
    2. env: the smallest piece; load_settings reuses it.
    3. load_settings: uses env for every field.
    4. missing_config: reads a finished Settings.

Depends on:
    Nothing in this project. This module is the start of the project. Build it
    first.
    Standard library: json, os, dataclasses, pathlib, typing.
    Third-party: none.

Depended on by:
    Every module that needs a setting, starting with assay.llm.client,
    assay.store.persistence, assay.graph.context, and assay.api.app.

Spec coverage: S1.1, S1.2 | Traces to: I9, A1, A4
"""

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

ROLES: tuple[str, ...] = (
    "grill",
    "explore",
    "questionnaire",
    "reconcile",
    "dod",
    "prd",
    "spec",
    "tickets",
)  # S1.1: one model per agent role


@dataclass(frozen=True)
class Settings:
    """Every setting, frozen after loading.

    Problem piece: C5 and C6: storage, models, identity, and approvers in one
                   immutable value.

    Why it matters: Settings are read by many modules over a long-running process.
                    If any module could change them, two requests could see
                    different approvers or gateways, so the value is frozen once
                    loaded and passed around instead of re-read.

    What: One field per environment variable in .env.example, with the defaults S1.1
          lists.

    Spec: S1.1 | Ticket: — | Traces to: —
    """

    artifacts_dir: Path
    database_url: str
    sqlite_path: Path
    gateway_url: str
    gateway_key: str
    gateway_headers: dict[str, str]
    models: dict[str, str]
    timeout_s: float
    cache_mode: Literal["explicit", "auto", "off"]
    retry_attempts: int
    retry_base_s: float
    retry_cap_s: float
    max_steps: int
    max_output_retries: int
    code_roots: tuple[Path, ...]
    user_header: str
    dev_user: str
    approvers: frozenset[str]
    team_name: str
    service_token: str


def env(name: str, default: str = "") -> str:
    """Return one environment variable, or a default when it is unset.

    Problem piece: C5: one way to read configuration, so defaults are applied
                   consistently.

    Why it matters: Every setting has a documented default. Reading variables in
                    many different ways invites one place to treat an empty value as
                    set and another as unset, which makes per-role model fallback
                    behave differently from everything else.

    What: Takes a variable name and a default; returns the variable's text or the
          default. Called as env(name: str, default: str) and returns str.

    Spec: S1.1 | Ticket: 01 | Traces to: I9

    Build steps:
    1. Task: Return the variable's value from the process environment, or the
             default when the variable is absent.
       Expected outcome: An unset variable returns the default; a set variable
                         returns its exact text.
    """
    raise NotImplementedError("S1.1: env")


def load_settings() -> Settings:
    """Build Settings from environment variables.

    Problem piece: C5 and C6: turn the environment into one frozen Settings value at
                   startup.

    Why it matters: A misconfigured deployment should fail when it starts, not
                    halfway through a session. Loading everything at once, with
                    defaults, means a bad value such as invalid gateway headers
                    stops the app immediately instead of breaking a PM's work.

    What: Reads every ASSAY_ variable listed in .env.example, applies its default,
          and returns Settings. Invalid JSON in the gateway headers fails loudly.

    Spec: S1.1 | Ticket: 01 | Traces to: I9, A1

    Build steps:
    1. Task: Read the default model, then one model per role in ROLES from
             ASSAY_MODEL_<ROLE>, falling back to the default when a role's own
             variable is unset.
       Think about: Why does an unset role fall back while a role set to empty text
                    does not?
       Expected outcome: A role without its own variable uses the default model.
    2. Task: Parse list-shaped settings: code roots separated by the operating
             system's path separator and resolved to absolute paths; approvers
             separated by commas, trimmed, with blanks dropped.
       Expected outcome: ASSAY_APPROVERS of 'dana, lee ,' yields exactly dana and
                         lee.
    3. Task: Parse ASSAY_GATEWAY_HEADERS as a JSON object, defaulting to an empty
             object.
       Think about: What should happen at startup if the JSON is invalid?
       Expected outcome: Invalid JSON raises an error at load time.
    4. Task: Return Settings with these defaults: artifacts ./data, SQLite
             ./data/assay.sqlite, timeout 120 seconds, cache mode explicit, 5 retry
             attempts, 1.0 second base, 30 second cap, 40 steps, 3 output retries,
             user header X-Forwarded-User, team name 'Delivery team', and empty text
             for the database URL, gateway, key, development user, and service
             token.
       Expected outcome: With no ASSAY_ variables set, every field holds its
                         documented default.
    """
    raise NotImplementedError("S1.1: load_settings")


def missing_config(s: Settings) -> list[str]:
    """Name every setting that must be set before models can be called.

    Problem piece: C1: refuse to run agents against a half-configured gateway.

    Why it matters: Without a gateway or a model for every role, the first agent
                    call fails mid-session. Reporting the gaps up front lets an
                    operator fix them before a PM starts, and reporting names rather
                    than values keeps secrets out of messages (I9).

    What: Takes Settings; returns the variable names still missing, empty when
          complete. Called as missing_config(s: Settings) and returns list[str].

    Spec: S1.2 | Ticket: 01 | Traces to: I9

    Build steps:
    1. Task: List 'ASSAY_MODEL or ASSAY_MODEL_<ROLE>' for every role without a
             model, then ASSAY_GATEWAY_URL and ASSAY_GATEWAY_KEY when empty.
       Think about: What would leak if a message included the value instead of the
                    name?
       Expected outcome: A missing URL and missing models are named; the key's value
                         never appears.
    """
    raise NotImplementedError("S1.2: missing_config")
