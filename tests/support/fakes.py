"""A scripted chat model and test settings. No gateway, no API key."""

from collections import Counter
from collections.abc import Callable
from pathlib import Path
from typing import Any

from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from assay.settings import Settings

USAGE = {
    "input_tokens": 1000,
    "output_tokens": 100,
    "total_tokens": 1100,
    "input_token_details": {"cache_read": 800},
}


class ScriptedChat(BaseChatModel):
    """Calls the bound output tool with arguments from script(kind, n).
    Records rejection messages so tests can prove validators fired."""

    script: Callable[[str, int], dict]
    calls: Any = None
    rejections: Any = None
    prompts: Any = None  # (output kind, dynamic prompt) per call
    bound: list[Any] = []

    @property
    def _llm_type(self) -> str:
        """Test helper: llm type."""
        return "scripted"

    def bind_tools(self, tools, tool_choice=None, **kw):
        """Test helper: bind tools."""
        return self.model_copy(update={"bound": list(tools)})

    def _generate(self, messages, stop=None, run_manager=None, **kw):
        """Test helper: generate."""
        last = messages[-1]
        if isinstance(last, ToolMessage) and str(last.content).startswith("Rejected"):
            self.rejections.append(str(last.content))
        kind = self.bound[-1].__name__
        self.calls[kind] += 1
        if self.prompts is not None:
            self.prompts.append((kind, str(messages[1].content)))
        tc = {
            "name": kind,
            "args": self.script(kind, self.calls[kind]),
            "id": f"{kind}-{self.calls[kind]}",
        }
        msg = AIMessage(content="", tool_calls=[tc], usage_metadata=USAGE)
        return ChatResult(generations=[ChatGeneration(message=msg)])


def fake_model(script) -> ScriptedChat:
    """Test helper: fake model."""
    return ScriptedChat(script=script, calls=Counter(), rejections=[], prompts=[])


def make_settings(tmp: Path, **over) -> Settings:
    """Test helper: make settings."""
    base = dict(
        artifacts_dir=tmp / "data",
        database_url="",
        sqlite_path=tmp / "data" / "t.sqlite",
        gateway_url="",
        gateway_key="",
        gateway_headers={},
        models={},
        timeout_s=10,
        cache_mode="explicit",
        retry_attempts=3,
        retry_base_s=0.0,
        retry_cap_s=0.0,
        max_steps=20,
        max_output_retries=3,
        code_roots=(),
        user_header="X-Forwarded-User",
        dev_user="jordan",
        approvers=frozenset({"dana"}),
        team_name="Cards team",
        service_token="svc-token",
    )
    base.update(over)
    return Settings(**base)
