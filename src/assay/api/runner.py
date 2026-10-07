"""Run sessions in the background and publish their progress.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C5 Durable sessions and C7 Live, standard interaction. A web
request must never wait on a model, and a closed tab must never stop a step. This
file runs one step at a time per session in the background and publishes progress to
subscribers.

Why this comes now: Identity (28) exists; the REST app (31) and the AG-UI endpoint
(30) both drive sessions through this.

Build order: Step 29 of 33.
Previous: src/assay/api/auth.py (step 28), which reads the signed-in user from the
SSO header.
Next: src/assay/api/agui.py (step 30), which serves Assay over the AG-UI protocol.

Build these in order:
    1. BusyError: the refusal type.
    2. RunProgress: the event type subscribers receive.
    3. Runner: the runner itself.

Depends on:
    assay.graph.context: AppContext. Passed on every invoke.
    assay.graph.state: AssayState. New sessions.
    Standard library: logging, queue, threading, dataclasses, typing.
    Third-party: langgraph.

Depended on by:
    assay.api.agui: subscribes to progress. assay.api.app: starts, resumes, retries,
    and reads status.

Spec coverage: S8.2, S9.1 | Traces to: I6, I7
"""

import logging
import queue
import threading
from dataclasses import dataclass
from typing import Callable, Literal

from langgraph.types import Command

from assay.graph.context import AppContext
from assay.graph.state import AssayState

log = logging.getLogger("assay.runner")


class BusyError(Exception):
    """The session is already running a step.

    Problem piece: C5: one step at a time per session.

    Why it matters: Two concurrent resumes would race on the same checkpoint;
                    refusing the second keeps sessions consistent.

    What: Raised when a session's lock is already held.

    Spec: S8.2 | Ticket: — | Traces to: —
    """
    pass


@dataclass(frozen=True)
class RunProgress:
    """One progress event from a running session.

    Problem piece: C7: what live clients are told.

    Why it matters: Clients show steps as they happen and must always learn how a
                    run ended, even if they joined late.

    What: Kind (step started, step finished, or ended), the node name, and for
          'ended' the outcome and any error.

    Spec: S9.1 | Ticket: — | Traces to: —
    """

    kind: Literal["step_started", "step_finished", "ended"]
    node: str = ""
    outcome: Literal["pause", "finish", "error"] | None = None
    error: str | None = None


class Runner:
    """Background execution and progress for every session.

    Problem piece: C5 and C7: sessions run off the request path and report live.

    Why it matters: Model calls take minutes; tying them to a request would let a
                    proxy timeout or closed tab kill a step. Per-session locks
                    prevent races; per-session subscribers carry live progress.

    What: Holds the compiled graph, the context, background mode, locks, errors, and
          subscribers.

    Spec: S8.2 | Ticket: — | Traces to: —
    """

    def __init__(self, app: object, context: AppContext, background: bool = True) -> None:
      """Hold the compiled graph and context; prepare locks, errors, and subscribers.

      Problem piece: C5: one runner per app.

      Why it matters: Locks and subscribers must be shared by every request in the
                  process, so they live on one object.

      What: Stores the graph, context, and background flag, and empty lock, error,
            and subscriber tables guarded by one lock.

      Spec: S8.2 | Ticket: 02 | Traces to: I6

      Build steps:
      1. Task: Store the graph, context, and background flag, and create empty
            tables for locks, errors, and subscribers plus one guard lock for
            creating entries.
      Expected outcome: A new runner reports no session as running.
      """
      self.app = app
      self.context = context
      self.background = background
      self._guard = threading.Lock()
      self._locks: dict[str, threading.Lock] = {}
      self._errors: dict[str, str] = {}
      self._subscribers: dict[str, list[Callable[[RunProgress], None]]] = {}

    @staticmethod
    def config(slug: str) -> dict[str, object]:
      """Return the LangGraph config for one session.

      Problem piece: C5: a session is a LangGraph thread.

      Why it matters: The slug is the thread ID everywhere; a high recursion limit
                  allows long grill loops.

      What: Thread ID set to the slug and a recursion limit of 500. Called as
            config(slug: str) and returns dict[str, object].

      Spec: S8.2 | Ticket: 02 | Traces to: I6

      Build steps:
      1. Task: Return a config whose thread ID is the slug and whose recursion
            limit is 500.
      Expected outcome: The slug 'alerts' becomes thread 'alerts'.
      """
      return {"thread_id": slug, "recursion_limit": 500}

    def lock_for(self, slug: str) -> threading.Lock:
      """Return the one lock for a session.

      Problem piece: C5: one step at a time per session.

      Why it matters: Creating locks without a guard could give two requests two
                  different locks for one session.

      What: The session's lock, created under the guard on first use. Called as
            lock_for(slug: str) and returns threading.Lock.

      Spec: S8.2 | Ticket: 02 | Traces to: I6

      Build steps:
      1. Task: Under the guard, return the session's lock, creating it on first
            use.
      Expected outcome: Two calls for one slug return the same lock.
      """
      with self._guard:
            if slug not in self._locks:
                  self._locks[slug] = threading.Lock()
            return self._locks[slug]

    def running(self, slug: str) -> bool:
      """Return True while a session runs a step.

      Problem piece: C5: status shows work in progress.

      Why it matters: The UI must show 'working' instead of offering actions that
                  would be refused. The status endpoint and every reply check
                  depend on it, so it must read the lock itself rather than a
                  separate flag that could drift.

      What: True when the session's lock is held, meaning a step is running right
            now; False otherwise.

      Spec: S8.2 | Ticket: 02 | Traces to: I6

      Build steps:
      1. Task: Report whether the session's lock is held.
      Expected outcome: A session mid-step reports True.
      """
      return self.lock_for(slug).locked()

    def subscribe(self, slug: str) -> queue.Queue[RunProgress]:
      """Return a new queue that receives a session's progress.

      Problem piece: C7: live clients follow a session.

      Why it matters: Several clients may watch one session; each needs its own
                  queue so no one steals another's events.

      What: A new queue registered for the session; every event published
            afterwards is put on it until it unsubscribes.

      Spec: S9.1 | Ticket: 12 | Traces to: I7

      Build steps:
      1. Task: Create a queue, register it for the session under the guard, and
            return it.
      Expected outcome: Two subscribers both receive the next event.
      """
      q: queue.Queue[RunProgress] = queue.Queue()
      with self._guard:
            if slug not in self._subscribers:
                  self._subscribers[slug] = []
            self._subscribers[slug].append(q)
      return q

    def unsubscribe(self, slug: str, q: queue.Queue[RunProgress]) -> None:
      """Stop sending a session's progress to a queue.

      Problem piece: C7: no leaks after a client leaves.

      Why it matters: A closed stream's queue would otherwise grow forever.
                  Streams close unpredictably when browsers navigate away, so
                  removal must tolerate a queue that is already gone.

      What: Removes the queue from the session's subscribers if present. Called as
            unsubscribe(slug: str, q: queue.Queue[RunProgress]) and returns None.

      Spec: S9.1 | Ticket: 12 | Traces to: I7

      Build steps:
      1. Task: Remove the queue from the session's subscribers under the guard,
            ignoring one already gone.
      Expected outcome: Unsubscribing twice does not fail.
      """
      with self._guard:
            if slug in self._subscribers and q in self._subscribers[slug]:
                  self._subscribers[slug].remove(q)

    def publish(self, slug: str, event: RunProgress) -> None:
      """Send one progress event to every subscriber of a session.

      Problem piece: C7: every watcher sees every event.

      Why it matters: Progress is broadcast; a slow subscriber must never block
                  the run. A run may have many watchers or none; the run's
                  progress must never depend on whether anyone is listening.

      What: Puts the event on each subscriber queue without blocking. Called as
            publish(slug: str, event: RunProgress) and returns None.

      Spec: S9.1 | Ticket: 12 | Traces to: I7

      Build steps:
      1. Task: Put the event on every current subscriber queue without waiting.
      Think about: Why must publishing never block?
      Expected outcome: A subscriber that never reads does not slow the run.
      """
      with self._guard:
            if slug in self._subscribers:
                  for q in self._subscribers[slug]:
                        try:
                              q.put_nowait(event)
                        except queue.Full:
                              pass


    def run(self, slug: str, payload: object, lock: threading.Lock) -> None:
      """Run the graph until it pauses or ends, publishing progress, and always release the lock.

      Problem piece: C5 and C7: a step runs to completion and everyone hears about
                  it.

      Why it matters: Streaming the run's tasks gives a start and finish per node,
                  which is exactly what live clients show. The end must always
                  be published and the lock always released, or a session
                  hangs as 'working' forever.

      What: Streams the graph with the context, publishes step events and how the
            run ended, records any error, and releases the lock.

      Spec: S8.2, S9.1 | Ticket: 02, 12 | Traces to: I6, I7

      Build steps:
      1. Task: Stream the graph with this payload, the session config, and the
            context, in LangGraph's 'tasks' stream mode, which reports each
            node when it starts and again with its result.
      Think about: Why does the context need passing on every run, including
                  resumes?
      Expected outcome: Every node produces one start and one finish.
      2. Task: Publish step_started for a start report and step_finished for a
            result report, noting whether any result carried an interrupt.
      Expected outcome: A grill turn publishes start then finish.
      3. Task: Publish 'ended' with outcome 'pause' when an interrupt occurred,
            else 'finish'; on an exception, log it, record '<ErrorType>:
            <message>' as the session's error, and publish 'ended' with outcome
            'error'.
      Expected outcome: A failing step publishes ended with outcome error.
      4. Task: Release the lock whatever happened.
      Expected outcome: A failed step leaves the session not run ning.
      """
      outcome: Literal["pause", "finish", "error"] = "finish"
      error: str | None = None
      interrupted = False
      try:
            for event in self.app.stream(
                  payload,
                  config=self.config(slug),
                  context=self.context,
                  stream_mode="tasks",
            ):
                  node = event.get("name", "")
                  if "input" in event:
                        self.publish(slug, RunProgress(kind="step_started", node=node))
                  if "result" in event:
                        result = event["result"]
                        if isinstance(result, dict) and result.get("__interrupt__"):
                              interrupted = True
                        if event.get("__interrupt__"):
                              interrupted = True
                        self.publish(slug, RunProgress(kind="step_finished", node=node))
            if interrupted:
                  outcome = "pause"
      except Exception as exc:
            outcome = "error"
            error = f"{type(exc).__name__}: {exc}"
            log.exception("Run failed for session %s", slug)
            with self._guard:
                  self._errors[slug] = error
      finally:
            try:
                  self.publish(
                        slug,
                        RunProgress(kind="ended", outcome=outcome, error=error),
                  )
            finally:
                  lock.release()

    def submit(self, slug: str, payload: object) -> None:
      """Start a run for a session, in the background or inline.

      Problem piece: C5: one step at a time, off the request path.

      Why it matters: Tests run inline for determinism; the server runs in a
                  background thread so requests return at once.

      What: Takes the lock without waiting (BusyError when held), clears the last
            error, and runs in a thread or inline.

      Spec: S8.2 | Ticket: 02 | Traces to: I6

      Raises:
      BusyError: the session is already running.

      Build steps:
      1. Task: Take the session's lock without waiting, raising BusyError when it
            is held, and clear its last error.
      Expected outcome: A second submit during a run raises BusyError.
      2. Task: Run in a background daemon thread when background mode is on,
            otherwise inline.
      Expected outcome: In inline mode the run has finished when submit
                        returns.
      """
      self._lock.acquire(blocking=False)
      self._errors[slug] = None
      if self._background:
            thread = threading.Thread(target=self._run, args=(slug, payload), daemon=True)
            thread.start()
      else:
            self._run(slug, payload)


    def start(self, state: AssayState) -> None:
      """Start a new session.

      Problem piece: C5: a session begins at setup.

      Why it matters: Starting is a run whose payload is the initial state.
                  Routing starts through the same submit path as resumes means
                  one lock and one error policy cover every way a run begins.

      What: Submits the initial state under its slug, so the run begins at setup;
            raises BusyError when already running.

      Spec: S8.2 | Ticket: 02 | Traces to: I6

      Build steps:
      1. Task: Submit the state under its slug.
      Expected outcome: A new session runs setup first.
      """
      self.submit(state.slug, state)


    def resume(self, slug: str, value: dict[str, object]) -> None:
      """Resume a paused session with a reply.

      Problem piece: C5 and C6: a person's reply continues the run.

      Why it matters: The paused node receives the value through LangGraph's
                  resume command. A reply delivered any other way would bypass
                  the paused node and leave the checkpoint waiting forever.

      What: Submits a resume command carrying the value. Called as resume(slug:
            str, value: dict[str, object]) and returns None.

      Spec: S8.2 | Ticket: 02 | Traces to: I6

      Build steps:
      1. Task: Submit a resume command carrying the value.
      Expected outcome: The paused node receives the reply.
      """
      self.submit(slug, {"resume": value})

    def retry(self, slug: str) -> None:
      """Continue from the last saved step.

      Problem piece: C5: recover after an error or restart.

      Why it matters: Invoking with no input continues from the last checkpoint,
                  so nothing completed is redone. Re-running from scratch
                  would repeat model calls that already succeeded and could
                  record their entries twice.

      What: Submits an empty payload, which continues from the last saved step;
            raises BusyError when a step is already running.

      Spec: S8.2 | Ticket: 02 | Traces to: I6

      Build steps:
      1. Task: Submit with no payload.
      Expected outcome: After a failed step, retry continues from the last
                        saved step.
      """
      self.submit(slug, {})

    def status(self, slug: str) -> dict[str, object]:
      """Return a session's status from its checkpoint.

      Problem piece: C5: status survives restarts.

      Why it matters: Status read from the checkpoint is true after a restart;
                  status kept only in memory would not be.

      What: Status (missing, working, error, waiting, stopped, done), the pending
            pause, error, stage, title, mode, PM, files, agenda, and round.

      Spec: S8.2 | Ticket: 02 | Traces to: I6

      Build steps:
      1. Task: Read the saved values and any pending interrupt values from the
            session's checkpoint.
      Expected outcome: A paused session reports its pause.
      2. Task: Choose the status in order: missing (no values), working, error,
            waiting (a pending pause), stopped (next steps but no pause),
            otherwise done.
      Think about: Why does 'stopped' exist?
      Expected outcome: A session interrupted by a restart reports stopped.
      3. Task: Return the status with the first pending pause, error, stage,
            title, mode, PM, files, agenda, and questionnaire round.
      Expected outcome: The JSON includes files for downloads.
      """
      return self._read_status(slug)
