"""call(): typed, rule-checked output from any tool-calling model (I1, D3)."""
from dataclasses import asdict, dataclass, field
from typing import Callable

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from pydantic import BaseModel, ValidationError

from ..domain.models import now
from .caching import build_messages, usage_of
from .resilience import with_backoff
from .tools import TOOL_SCHEMAS, Deps, ToolError, run_tool

Validator = Callable[[BaseModel, Deps], list[str]]


class OutputError(RuntimeError):
    """The model could not produce valid output within the limits."""


@dataclass
class AgentSpec:
    name: str
    role: str                 # selects the model: ASSAY_MODEL_<ROLE>
    static: str               # instructions + references: identical on every call (cacheable)
    output: type[BaseModel]
    validators: list[Validator] = field(default_factory=list)
    tools: bool = False
    post: Callable[[BaseModel, Deps], BaseModel] | None = None


@dataclass
class CallRecord:
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

    def dict(self) -> dict:
        return asdict(self)


@dataclass
class Limits:
    cache_mode: str = "explicit"
    max_steps: int = 40
    max_rejections: int = 3
    retry_attempts: int = 5
    retry_base_s: float = 1.0
    retry_cap_s: float = 30.0
    sleep: Callable[[float], None] | None = None   # tests inject a no-op


OUTPUT_RULE = ("\n\nWhen ready, call the {name} tool with the complete output. "
               "If it is rejected, fix every listed problem and call it again.")


def validation_errors(exc: ValidationError) -> list[str]:
    """Readable 'field.path: message' lines from a Pydantic error. (Helper; complete.)"""
    return [f"{'.'.join(str(p) for p in e['loc'])}: {e['msg']}" for e in exc.errors()]


def call(model: BaseChatModel, spec: AgentSpec, dynamic: str, deps: Deps,
         limits: Limits, model_name: str = "") -> tuple[BaseModel, CallRecord]:
    """Run one agent until it returns output that passes the schema and every validator.

    Spec: S4.5 | Ticket: 02 | Traces to: I1, I11

    Build steps:
    1. Task: `rec = CallRecord(agent=spec.name, role=spec.role, model=model_name, started_at=now())`;
       `out_name = spec.output.__name__`; `tools = ([*TOOL_SCHEMAS] if spec.tools else []) + [spec.output]`;
       `bound = model.bind_tools(tools, tool_choice="any")`.
       Expected outcome: the model must call a tool every turn; the output schema is the last tool.
    2. Task: `msgs = build_messages(spec.static + OUTPUT_RULE.format(name=out_name), dynamic, limits.cache_mode)`.
       Expected outcome: static prefix first (cacheable), dynamic last.
    3. Task: Define `invoke()` that returns `bound.invoke(msgs)` and increments `rec.transient_retries` before
       re-raising any exception. Build `backoff = dict(attempts=limits.retry_attempts, base_s=limits.retry_base_s,
       cap_s=limits.retry_cap_s)`, adding `sleep=limits.sleep` when it is not None.
       Expected outcome: every gateway request goes through retry with backoff (I11).
    4. Task: Loop `for _ in range(limits.max_steps)`: `rec.steps += 1`; `ai = with_backoff(invoke, **backoff)`;
       add each value of `usage_of(ai)` onto the matching `rec` field with `setattr`; `msgs.append(ai)`.
       If `not ai.tool_calls`, append `HumanMessage(f"Respond by calling a tool. Use {out_name} for your answer.")`
       and continue.
       Expected outcome: tokens and cache reads accumulate per call.
    5. Task: For EACH `tc` in `ai.tool_calls` (every call needs a ToolMessage with `tool_call_id=tc["id"]`):
       if `tc["name"] == out_name`: `out = spec.output.model_validate(tc["args"])` then
       `problems = [p for v in spec.validators for p in v(out, deps)]`; on `ValidationError as exc` use
       `validation_errors(exc)`. With problems: `rec.rejections += 1`, extend `rec.rejected_for` with
       `problems[:5]`, raise `OutputError(...)` when `rec.rejections > limits.max_rejections`, else append
       `ToolMessage("Rejected. Fix every item and call " + out_name + " again with the complete output:\\n- " + "\\n- ".join(problems), tool_call_id=tc["id"])`.
       Without problems: `final = spec.post(out, deps) if spec.post else out` and append `ToolMessage("Accepted.", ...)`.
       Otherwise run `result = run_tool(tc["name"], tc["args"], deps)` (on `ToolError as exc` use
       `f"Error: {exc}"`) and append `ToolMessage(str(result), tool_call_id=tc["id"])`.
       Expected outcome: rule problems go back to the model verbatim; code tools answer.
    6. Task: After the inner loop, `return final, rec` when `final` was set. After the outer loop, raise
       `OutputError(f"{spec.name}: no valid output within {limits.max_steps} steps.")`.
       Expected outcome: validated output, or a clear failure; never unchecked output.
    """
    raise NotImplementedError("S4.5")
