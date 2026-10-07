"""Runs sessions in the background so a web request never waits on a model.
One worker (A3): per-session locks live in memory."""
import logging
import queue
import threading
from dataclasses import dataclass
from typing import Any, Literal

from langgraph.types import Command

from ..graph.context import AppContext
from ..graph.state import AssayState

log = logging.getLogger("assay.runner")


class Busy(Exception):
    """The session is already running a step."""


# The shared test suite (canonical naming) imports BusyError; the app layer uses Busy.
# One class, two names, so both `except Busy` and `pytest.raises(BusyError)` see it.
BusyError = Busy


@dataclass(frozen=True)
class RunProgress:
    """One progress event from a running session (S9.1).

    Kind (step started, step finished, or ended), the node name, and for
    'ended' the outcome and any error.

    Spec: S9.1
    """

    kind: Literal["step_started", "step_finished", "ended"]
    node: str = ""
    outcome: Literal["pause", "finish", "error"] | None = None
    error: str | None = None


class Runner:
    def __init__(self, app, context: AppContext, background: bool = True):
        """Hold the compiled graph and context; prepare lock tables. (Complete.)"""
        self.app, self.context, self.background = app, context, background
        self.locks: dict[str, threading.Lock] = {}
        self.errors: dict[str, str] = {}
        self.subscribers: dict[str, list] = {}
        self.guard = threading.Lock()

    def subscribe(self, slug: str):
        """Register a queue for one session's progress events; returns it (S9.1).

        Spec: S9.1
        """
        q = queue.Queue()
        with self.guard:
            self.subscribers.setdefault(slug, []).append(q)
        return q

    def unsubscribe(self, slug: str, q) -> None:
        """Drop one of a session's progress queues (S9.1).

        Spec: S9.1
        """
        with self.guard:
            self.subscribers[slug] = [x for x in self.subscribers.get(slug, []) if x is not q]

    def publish(self, slug: str, event: RunProgress) -> None:
        """Deliver one progress event to every subscriber of a session (S9.1).

        Spec: S9.1
        """
        with self.guard:
            queues = list(self.subscribers.get(slug, []))
        for q in queues:
            q.put(event)

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
        with self.guard:
            return self.locks.setdefault(slug, threading.Lock())

    def running(self, slug: str) -> bool:
        """Spec: S8.2 | Ticket: 02 | Traces to: I6

        Build steps:
        1. Task: Return `self.lock_for(slug).locked()`.
           Expected outcome: True while a step runs.
        """
        return self.lock_for(slug).locked()

    def run(self, slug: str, payload: Any, lock: threading.Lock) -> None:
        """Run one invoke and always release the lock.

        Spec: S8.2 | Ticket: 02 | Traces to: I6

        Build steps:
        1. Task: In `try:` stream the step `self.app.stream(payload, self.config(slug), context=self.context,
           stream_mode="tasks")`; for each task event publish `RunProgress("step_finished" if the event
           carries a result else "step_started", node=name)`.
           Expected outcome: a start and a finish per node, streamed as the run proceeds.
        2. Task: When the stream ends, read the checkpoint; publish `RunProgress("ended", outcome="pause")` when
           it is waiting on an interrupt else `outcome="finish"`, then `self.errors.pop(slug, None)`.
           Expected outcome: subscribers learn how the run ended from the same checkpoint status() reads.
        3. Task: `except Exception as exc:` call `log.exception("session %s failed", slug)`, set
           `self.errors[slug] = f"{type(exc).__name__}: {exc}"`, and publish `RunProgress("ended", outcome="error",
           error=str(exc))`.
           Expected outcome: the UI shows the error and offers Retry.
        4. Task: `finally: lock.release()`.
           Expected outcome: a failed step never leaves the session stuck as working.
        """
        try:
            for event in self.app.stream(payload, self.config(slug), context=self.context, stream_mode="tasks"):
                name = event.get("name", "") if isinstance(event, dict) else str(event)
                self.publish(slug, RunProgress("step_finished" if "result" in event else "step_started", node=name))
            self.errors.pop(slug, None)
            snap = self.app.get_state(self.config(slug))
            waiting = [i for t in snap.tasks for i in t.interrupts]
            self.publish(slug, RunProgress("ended", outcome="pause" if waiting else "finish"))
        except Exception as exc:
            log.exception("session %s failed", slug)
            self.errors[slug] = f"{type(exc).__name__}: {exc}"
            self.publish(slug, RunProgress("ended", outcome="error", error=str(exc)))
        finally:
            lock.release()

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
        lock = self.lock_for(slug)
        if not lock.acquire(blocking=False):
            raise Busy(slug)
        self.errors.pop(slug, None)
        if self.background:
            threading.Thread(target=self.run, args=(slug, payload, lock), daemon=True).start()
        else:
            self.run(slug, payload, lock)

    def start(self, state: AssayState) -> None:
        """Spec: S8.2 | Ticket: 02 | Traces to: I6

        Build steps:
        1. Task: `self.submit(state.slug, state)`.
           Expected outcome: a new session starts at setup.
        """
        self.submit(state.slug, state)

    def resume(self, slug: str, value: dict) -> None:
        """Spec: S8.2 | Ticket: 02 | Traces to: I6

        Build steps:
        1. Task: `self.submit(slug, Command(resume=value))`.
           Expected outcome: the paused node receives the value.
        """
        self.submit(slug, Command(resume=value))

    def retry(self, slug: str) -> None:
        """Spec: S8.2 | Ticket: 02 | Traces to: I6

        Build steps:
        1. Task: `self.submit(slug, None)`.
           Expected outcome: invoking with None continues from the last saved step.
        """
        self.submit(slug, None)

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
        snap = self.app.get_state(self.config(slug))
        v = snap.values or {}
        pending = [i.value for t in snap.tasks for i in t.interrupts]
        if not v:
            status = "missing"
        elif self.running(slug):
            status = "working"
        elif slug in self.errors:
            status = "error"
        elif pending:
            status = "waiting"
        elif snap.next:
            status = "stopped"
        else:
            status = "done"
        return {"slug": slug, "status": status, "pending": pending[0] if pending else None,
                "error": self.errors.get(slug), "stage": v.get("stage"), "title": v.get("title"),
                "mode": v.get("mode"), "pm": v.get("pm"), "files": v.get("files", []),
                "agenda": v.get("agenda", []), "q_round": v.get("q_round", 0)}
