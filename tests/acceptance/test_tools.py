"""Ticket 09: sandboxed code tools and the explore agent (S4.4, S4.6)."""

from collections import Counter
from typing import Any

import pytest
from langchain_core.language_models import BaseChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult

from assay.llm.agents import agent
from assay.llm.call import Limits, call
from assay.llm.tools import Deps, ToolError, list_files, read_file, redact, run_tool, search_code

MAP = {
    "components": ["Alert Preferences"],
    "data_flow": "API to store",
    "data_stores": ["prefs"],
    "tests": "None",
}


@pytest.fixture
def deps(tmp_path):
    """Test helper: deps."""
    root = tmp_path / "payments"
    (root / "src").mkdir(parents=True)
    (root / "src" / "app.py").write_text("def save_threshold():\n    password = 'hunter2hunter2'\n")
    (root / ".env").write_text("API_KEY=secret\n")
    return Deps(roots={"payments": root})


def test_reads_are_confined_and_redacted(deps):
    """Reads are confined and redacted.

    Spec: S4.4 | Traces to: I10
    Expected outcome: .env and ../ paths are refused and a password line is redacted.
    """
    assert "payments/src/app.py" in list_files(deps, "payments/**/*.py")
    assert "payments/.env" not in list_files(deps)
    text = read_file(deps, "payments/src/app.py")
    assert "save_threshold" in text and "hunter2" not in text and "redacted" in text
    for bad in ["payments/.env", "payments/../../etc/passwd", "elsewhere/x.py"]:
        with pytest.raises(ToolError):
            read_file(deps, bad)
    assert deps.files_read == ["payments/src/app.py"]


def test_search_and_dispatch(deps):
    """Search and dispatch.

    Spec: S4.4 | Traces to: I12
    Expected outcome: search returns path:line hits and unknown tools are refused.
    """
    assert search_code(deps, r"def \w+")[0].startswith("payments/src/app.py:1:")
    with pytest.raises(ToolError):
        run_tool("DeleteFile", {}, deps)
    with pytest.raises(ToolError):
        run_tool("ReadFile", {"nope": 1}, deps)
    assert redact("token = abcdef123456") == "[line redacted: looks like a credential]"


def test_no_roots_means_no_code_access():
    """No roots means no code access.

    Spec: S4.4 | Traces to: I10
    Expected outcome: listing without roots is refused.
    """
    with pytest.raises(ToolError):
        list_files(Deps())


class Explorer(BaseChatModel):
    """Map without reading (rejected), read a file, then map again."""

    bound: list[Any] = []
    seen: list[str] = []

    @property
    def _llm_type(self) -> str:
        """Test helper: llm type."""
        return "explorer"

    def bind_tools(self, tools, tool_choice=None, **kw):
        """Test helper: bind tools."""
        return self.model_copy(update={"bound": list(tools)})

    def _generate(self, messages, stop=None, run_manager=None, **kw):
        """Test helper: generate."""
        self.seen.extend(str(m.content) for m in messages if isinstance(m, ToolMessage))
        n = sum(1 for m in messages if isinstance(m, AIMessage)) + 1
        calls = (
            [{"name": "ReadFile", "args": {"path": "payments/src/app.py"}, "id": "r"}]
            if n == 2
            else [{"name": "CurrentStateMap", "args": MAP, "id": f"m{n}"}]
        )
        return ChatResult(
            generations=[ChatGeneration(message=AIMessage(content="", tool_calls=calls))]
        )


def test_explore_must_read_code_first(deps):
    """Explore must read code first.

    Spec: S4.6 | Traces to: I1
    Expected outcome: a map before reading is rejected once, then accepted with files_read.
    """
    model = Explorer()
    out, rec = call(
        model, agent("explore"), "Map the alerts code.", deps, Limits(sleep=lambda s: None)
    )
    assert out.files_read == ["payments/src/app.py"] and rec.rejections == 1
    assert any("Read the relevant code" in s for s in model.seen)
