"""Runs sessions in the background so a web request never waits on a model.
One worker (A3): per-session locks live in memory."""
import logging
import threading
from typing import Any

from langgraph.types import Command

from ..graph.context import AppContext
from ..graph.state import AssayState

log = logging.getLogger("assay.runner")


class Busy(Exception):
    """The session is already running a step."""


class Runner:
    def __init__(self, app, context: AppContext, background: bool = True):
        """Hold the compiled graph and context; prepare lock tables. (Complete.)"""
        self.app, self.context, self.background = app, context, background
        self.locks: dict[str, threading.Lock] = {}
        self.errors: dict[str, str] = {}
        self.guard = threading.Lock()

    @staticmethod
    def config(slug: str) -> dict:
        """LangGraph config for one session. (Complete.)"""
        return {"configurable": {"thread_id": slug}, "recursion_limit": 500}

    def lock_for(self, slug: str) -> threading.Lock:
        """Spec: S8.2 | Ticket: 02 | Traces to: I6

        Build steps:
        1. Task: `with self.guard:` return `self.locks.setdefault(slug, threading.Lock())`.
           Expected outcome: exactly one lock per session, created safely under concurrency.
        """
        raise NotImplementedError("S8.2")

    def running(self, slug: str) -> bool:
        """Spec: S8.2 | Ticket: 02 | Traces to: I6

        Build steps:
        1. Task: Return `self.lock_for(slug).locked()`.
           Expected outcome: True while a step runs.
        """
        raise NotImplementedError("S8.2")

    def run(self, slug: str, payload: Any, lock: threading.Lock) -> None:
        """Run one invoke and always release the lock.

        Spec: S8.2 | Ticket: 02 | Traces to: I6

        Build steps:
        1. Task: In `try:` call `self.app.invoke(payload, self.config(slug), context=self.context)` then
           `self.errors.pop(slug, None)`.
           Expected outcome: the context is passed on every invoke, resumes included.
        2. Task: `except Exception as exc:` call `log.exception("session %s failed", slug)` and set
           `self.errors[slug] = f"{type(exc).__name__}: {exc}"`.
           Expected outcome: the UI shows the error and offers Retry.
        3. Task: `finally: lock.release()`.
           Expected outcome: a failed step never leaves the session stuck as working.
        """
        raise NotImplementedError("S8.2")

    def submit(self, slug: str, payload: Any) -> None:
        """Spec: S8.2 | Ticket: 02 | Traces to: I6

        Build steps:
        1. Task: `lock = self.lock_for(slug)`; if `not lock.acquire(blocking=False)`, raise `Busy(slug)`.
           Expected outcome: one step at a time per session.
        2. Task: `self.errors.pop(slug, None)`; when `self.background`, start
           `threading.Thread(target=self.run, args=(slug, payload, lock), daemon=True)`; otherwise call
           `self.run(slug, payload, lock)` directly.
           Expected outcome: tests run synchronously; the server runs in the background.
        """
        raise NotImplementedError("S8.2")

    def start(self, state: AssayState) -> None:
        """Spec: S8.2 | Ticket: 02 | Traces to: I6

        Build steps:
        1. Task: `self.submit(state.slug, state)`.
           Expected outcome: a new session starts at setup.
        """
        raise NotImplementedError("S8.2")

    def resume(self, slug: str, value: dict) -> None:
        """Spec: S8.2 | Ticket: 02 | Traces to: I6

        Build steps:
        1. Task: `self.submit(slug, Command(resume=value))`.
           Expected outcome: the paused node receives the value.
        """
        raise NotImplementedError("S8.2")

    def retry(self, slug: str) -> None:
        """Spec: S8.2 | Ticket: 02 | Traces to: I6

        Build steps:
        1. Task: `self.submit(slug, None)`.
           Expected outcome: invoking with None continues from the last saved step.
        """
        raise NotImplementedError("S8.2")

    def status(self, slug: str) -> dict:
        """Session status for the UI, derived from the checkpoint.

        Spec: S8.2 | Ticket: 02 | Traces to: I6

        Build steps:
        1. Task: `snap = self.app.get_state(self.config(slug))`; `v = snap.values or {}`;
           `pending = [i.value for t in snap.tasks for i in t.interrupts]`.
           Expected outcome: saved values and any pause payload.
        2. Task: Status is "missing" when `not v`; "working" when `self.running(slug)`; "error" when
           `slug in self.errors`; "waiting" when `pending`; "stopped" when `snap.next`; otherwise "done".
           Expected outcome: survives restarts because it reads the checkpoint.
        3. Task: Return `{"slug": slug, "status": status, "pending": pending[0] if pending else None,
           "error": self.errors.get(slug), "stage": v.get("stage"), "title": v.get("title"), "mode": v.get("mode"),
           "pm": v.get("pm"), "files": v.get("files", []), "agenda": v.get("agenda", []), "q_round": v.get("q_round", 0)}`.
           Expected outcome: the JSON the UI renders.
        """
        raise NotImplementedError("S8.2")
