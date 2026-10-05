"""Get typed, rule-checked output from any tool-calling model.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C1 Trustworthy output. A model will sometimes return
confident, wrong output. This file forces structured output, checks it against the
rules, and sends problems back until it passes or limits run out; it never decides
what an agent is for.

Why this comes now: Caching (10), retry (11), and tools (12) exist; agents (14) are
specs this loop runs.

Build order: Step 13 of 33.
Previous: src/assay/llm/tools.py (step 12), which gives agents read-only, sandboxed
access to allowlisted code.
Next: src/assay/llm/agents.py (step 14), which defines every agent from prompt
files, output shapes, and rule validators.

Build these in order:
    1. OutputError: the loop's failure.
    2. AgentSpec: the input the loop runs.
    3. CallRecord: the loop's other output.
    4. Limits: the loop's ceilings.
    5. validation_errors: used by call.
    6. call: the public entry.

Depends on:
    assay.domain.models: now. Timestamps call records.
    assay.llm.caching: build_messages, usage_of. Request order and token counts.
    assay.llm.resilience: with_backoff. Every gateway request.
    assay.llm.tools: TOOL_SCHEMAS, Deps, ToolError, run_tool. Code tools and
    validator context.
    Standard library: dataclasses, collections.abc.
    Third-party: langchain-core, pydantic.

Depended on by:
    assay.llm.agents: AgentSpec. assay.graph.context: call, Limits, CallRecord.

Spec coverage: S4.5 | Traces to: I1, I11
"""

from collections.abc import Callable
from dataclasses import asdict, dataclass, field

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from pydantic import BaseModel, ValidationError

from assay.domain.models import now
from assay.llm.caching import build_messages, usage_of
from assay.llm.resilience import with_backoff
from assay.llm.tools import TOOL_SCHEMAS, Deps, ToolError, run_tool

type Validator = Callable[[BaseModel, Deps], list[str]]
OUTPUT_RULE = (  # S4.5: appended to every static prompt
    "\n\nWhen ready, call the {name} tool with the complete output. "
    "If it is rejected, fix every listed problem and call it again."
)


class OutputError(RuntimeError):
    """The model could not produce valid output within the limits.

    Problem piece: C1: a clear failure instead of unchecked output.

    Why it matters: Returning output that failed its rules would defeat the loop;
                    stopping with a named error is the only safe end.

    What: Raised when rejections or steps exceed their limits.

    Spec: S4.5 | Ticket: — | Traces to: —
    """


@dataclass
class AgentSpec:
    """One agent: role, static prompt, output shape, rules, and tools.

    Problem piece: C1: everything the loop needs to run one kind of agent.

    Why it matters: Separating the agent's definition from the loop lets one loop
                    serve every agent and keeps each agent's rules in one place.

    What: Name, role (selects the model), static prompt, output model, validators,
          tool flag, and an optional post-step.

    Spec: S4.5 | Ticket: — | Traces to: —
    """

    name: str
    role: str
    static: str
    output: type[BaseModel]
    validators: list[Validator] = field(default_factory=list)
    tools: bool = False
    post: Callable[[BaseModel, Deps], BaseModel] | None = None


@dataclass
class CallRecord:
    """What one agent call cost and how it went.

    Problem piece: C1: an audit and usage record for every call.

    Why it matters: Tokens, cache reads, retries, and rejections are the evidence
                    that caching works and the rules fire.

    What: Agent, role, model, start time, and counters; dict returns it as plain
          data.

    Spec: S4.5 | Ticket: — | Traces to: —
    """

    agent: str
    role: str
    model: str
    started_at: str
    steps: int = 0
    rejections: int = 0
    transient_retries: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    rejected_for: list[str] = field(default_factory=list)

    def dict(self) -> dict[str, object]:
        """Return the record as plain data.

        Problem piece: C1: records stored in the shared store.

        Why it matters: The store holds plain data, not dataclasses, so the record
                        must convert before saving. Storing the record as plain data
                        keeps the store independent of this class, so old records
                        stay readable after it changes.

        What: Every field of the record as a plain dictionary, ready to save. Called
              as dict() and returns dict[str, object].

        Spec: S4.5 | Ticket: 02 | Traces to: I1

        Build steps:
        1. Task: Return every field as a plain mapping.
           Expected outcome: The result contains all twelve fields.
        """
        raise NotImplementedError("S4.5: dict")


@dataclass
class Limits:
    """Loop limits and retry settings for one call.

    Problem piece: C1: bounded cost.

    Why it matters: Any loop that calls a paid service needs ceilings.

    What: Cache mode, maximum steps and rejections, retry attempts and delays, and
          an injectable sleep.

    Spec: S4.5 | Ticket: — | Traces to: —
    """

    cache_mode: str = "explicit"
    max_steps: int = 40
    max_rejections: int = 3
    retry_attempts: int = 5
    retry_base_s: float = 1.0
    retry_cap_s: float = 30.0
    sleep: Callable[[float], None] | None = None


def validation_errors(exc: ValidationError) -> list[str]:
    """Return readable 'field.path: message' lines from a validation error.

    Problem piece: C1: shape errors the model can fix.

    Why it matters: A raw validation dump is noise to a model; one line per field
                    tells it exactly what to change.

    What: One line per error, the field path joined by dots, then the message.
          Called as validation_errors(exc: ValidationError) and returns list[str].

    Spec: S4.5 | Ticket: 02 | Traces to: I1

    Build steps:
    1. Task: Return one line per error: its location joined with dots, a colon, and
             its message.
       Expected outcome: A missing 'done' field yields 'done: Field required'.
    """
    raise NotImplementedError("S4.5: validation_errors")


def call(
    model: BaseChatModel,
    spec: AgentSpec,
    dynamic: str,
    deps: Deps,
    limits: Limits,
    model_name: str = "",
) -> tuple[BaseModel, CallRecord]:
    """Run one agent until its output passes the schema and every validator.

    Problem piece: C1: the only path from a model's answer to anything that uses it.

    Why it matters: A prompt can ask; only a check can require. Offering the output
                    shape as a tool and forcing a tool call removes free-text
                    replies. Returning each problem to the model lets it repair the
                    answer instead of wasting the attempt. Limits stop a confused
                    model from running up a bill.

    What: Returns validated output and a CallRecord, or raises OutputError after
          max_rejections rejected outputs or max_steps steps.

    Spec: S4.5 | Ticket: 02 | Traces to: I1, I11

    Raises:
        OutputError: still invalid after the limits.

    Build steps:
    1. Task: Offer the code tools (when the agent uses them) and the output shape as
             tools, forcing the model to call a tool every turn; build messages from
             the static prompt plus OUTPUT_RULE and the dynamic text.
       Think about: Why must the output shape be offered as a tool?
       Expected outcome: The model is never asked for free text.
    2. Task: Send each request through retry with backoff, counting every failed
             request in the record, and add each response's token usage to the
             record.
       Expected outcome: One rate limit then success records one transient retry.
    3. Task: Answer every tool call in a response, in order: run code tools and
             return their result or refusal; for the output tool, parse the
             arguments, then run every validator.
       Think about: What breaks if a tool call goes unanswered?
       Expected outcome: Every tool call receives exactly one reply.
    4. Task: On problems, count a rejection, keep up to five reasons, stop with
             OutputError when rejections exceed the limit, and otherwise reply
             'Rejected. Fix every item and call <name> again with the complete
             output:' followed by the problems.
       Expected outcome: An invented source ID is rejected once and fixed on the
                         next turn.
    5. Task: On success, apply the agent's post-step if any, reply 'Accepted.', and
             return the output and record; raise OutputError when steps run out.
       Expected outcome: A valid first answer returns after one step.
    """
    raise NotImplementedError("S4.5: call")
