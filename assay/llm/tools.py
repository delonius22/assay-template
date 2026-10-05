"""Read-only codebase tools for agents (I10).

Three layers: an allowlist of directories, a denylist of secret-bearing
names, and redaction of credential-looking lines before text reaches a model.
"""
import fnmatch
import re
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

DENY = [".env", "*.env", ".env.*", "*.pem", "*.key", "*.p12", "*.pfx", "*.jks", "*secret*",
        "*credential*", "id_rsa*", "*.sqlite", "*.db", ".git/*", "node_modules/*"]
SECRET_LINE = [
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|token|client[_-]?secret)\b"
               r"\s*[:=]\s*['\"]?[^\s'\"]{6,}"),
    re.compile(r"(?i)\b[a-z][a-z0-9+.-]*://[^/\s:@]+:[^/\s@]+@"),
]
REDACTED = "[line redacted: looks like a credential]"
MAX_BYTES = 60_000
MAX_HITS = 80
MAX_LIST = 300


class ToolError(Exception):
    """Sent back to the model as the tool result so it can correct itself."""


@dataclass
class Deps:
    """Per-call context for tools and validators."""
    roots: dict[str, Path] = field(default_factory=dict)
    known_ids: set[str] = field(default_factory=set)
    prd_ids: set[str] = field(default_factory=set)
    feature_ids: set[str] = field(default_factory=set)
    files_read: list[str] = field(default_factory=list)


class ListFiles(BaseModel):
    """List readable files matching a glob, e.g. 'payments/**/*.py'. Paths start with a root name."""
    pattern: str = Field("**/*")


class ReadFile(BaseModel):
    """Read lines from a file (1-based, inclusive). Path starts with a root name."""
    path: str
    start_line: int = 1
    end_line: int = 400


class SearchCode(BaseModel):
    """Search readable files for a regular expression. Returns 'path:line: text'."""
    regex: str
    glob: str = "**/*"


TOOL_SCHEMAS = [ListFiles, ReadFile, SearchCode]


def roots_from(paths: tuple[Path, ...]) -> dict[str, Path]:
    """Name each allowed root by its folder name. (Helper; complete.)"""
    return {p.name: p for p in paths}


def denied(rel: str, name: str) -> bool:
    """True when a path or file name matches the denylist.

    Spec: S4.4 | Ticket: 09 | Traces to: I10

    Build steps:
    1. Task: Return `any(fnmatch.fnmatch(rel, d) or fnmatch.fnmatch(name, d) for d in DENY)`.
       Expected outcome: `.env`, keys, and credential files are refused wherever they sit.
    """
    raise NotImplementedError("S4.4")


def redact(text: str) -> str:
    """Replace every credential-looking line with REDACTED.

    Spec: S4.4 | Ticket: 09 | Traces to: I10

    Build steps:
    1. Task: For each `line` in `text.splitlines()`, keep it unless
       `any(p.search(line) for p in SECRET_LINE)`, in which case use `REDACTED`.
       Expected outcome: passwords in ordinary files never reach a model.
    2. Task: Return the lines joined with "\\n".
       Expected outcome: line numbers are preserved.
    """
    raise NotImplementedError("S4.4")


def resolve(deps: Deps, path: str) -> Path:
    """Map 'rootname/relative/path' to a real path inside an allowed root, or raise ToolError.

    Spec: S4.4 | Ticket: 09 | Traces to: I10, I12

    Build steps:
    1. Task: If `not deps.roots`, raise `ToolError("No code access is configured for this deployment.")`.
       Expected outcome: code access is off by default.
    2. Task: Split `root_name, _, rel = path.partition("/")`; `root = deps.roots.get(root_name)`;
       if None raise `ToolError(f"Unknown root '{root_name}'. Readable roots: {sorted(deps.roots)}")`.
       Expected outcome: only named roots are reachable.
    3. Task: `p = (root / rel).resolve()`; if `root not in p.parents and p != root` raise
       `ToolError(f"'{path}' is outside the allowed directories.")`.
       Expected outcome: `../` escapes are refused AFTER resolving symlinks and dots.
    4. Task: If `denied(p.relative_to(root).as_posix(), p.name)` raise
       `ToolError(f"'{path}' is not readable by policy.")`. Return `p`.
       Expected outcome: a safe absolute path.
    """
    raise NotImplementedError("S4.4")


def list_files(deps: Deps, pattern: str = "**/*") -> list[str]:
    """Readable files matching a glob, as 'root/relative' paths, capped at MAX_LIST.

    Spec: S4.4 | Ticket: 09 | Traces to: I10

    Build steps:
    1. Task: If `not deps.roots`, raise `ToolError("No code access is configured for this deployment.")`.
       Expected outcome: consistent with resolve().
    2. Task: `root_name, _, rest = pattern.partition("/")`; when `root_name in deps.roots` search only that
       root with glob `rest`, else search every root with the whole `pattern`.
       Expected outcome: 'payments/**/*.py' searches one root.
    3. Task: For each `p` from `root.glob(glob or "**/*")` with `p.is_file()` and not
       `denied(p.relative_to(root).as_posix(), p.name)`, append `f"{name}/{p.relative_to(root).as_posix()}"`.
       Expected outcome: denied files never appear in listings.
    4. Task: Stop at MAX_LIST entries and append "… truncated; narrow the pattern". Return the list.
       Expected outcome: bounded output (I12).
    """
    raise NotImplementedError("S4.4")


def read_file(deps: Deps, path: str, start_line: int = 1, end_line: int = 400) -> str:
    """Numbered lines from an allowed file, redacted, capped at MAX_BYTES.

    Spec: S4.4 | Ticket: 09 | Traces to: I10, I12

    Build steps:
    1. Task: `p = resolve(deps, path)`; if `not p.is_file()` raise `ToolError(f"No such file: {path}")`.
       Expected outcome: only real, allowed files are read.
    2. Task: `text = redact(p.read_bytes()[:MAX_BYTES].decode("utf-8", errors="replace"))`.
       Expected outcome: bounded and redacted before anything else sees it.
    3. Task: `lines = text.splitlines()[max(start_line - 1, 0):end_line]`; append `path` to `deps.files_read`.
       Expected outcome: the explore validator can see that code was read.
    4. Task: Return `"\\n".join(f"{i}: {l}" for i, l in enumerate(lines, start_line))`.
       Expected outcome: line-numbered text.
    """
    raise NotImplementedError("S4.4")


def search_code(deps: Deps, regex: str, glob: str = "**/*") -> list[str]:
    """'path:line: text' hits for a regex across readable files, capped at MAX_HITS.

    Spec: S4.4 | Ticket: 09 | Traces to: I10, I12

    Build steps:
    1. Task: `pat = re.compile(regex)`; on `re.error as e` raise `ToolError(f"Bad regex: {e}")`.
       Expected outcome: a bad pattern is reported to the model, not crashed on.
    2. Task: For each `rel` in `list_files(deps, glob)` (skip entries starting with "…"), read
       `redact(resolve(deps, rel).read_text(encoding="utf-8", errors="ignore"))`, skipping on `OSError` or `ToolError`.
       Expected outcome: only allowed, redacted text is searched.
    3. Task: For each line where `pat.search(line)`, append `f"{rel}:{n}: {line.strip()[:200]}"`.
       Expected outcome: hits with locations.
    4. Task: Stop at MAX_HITS and append "… truncated; narrow the search". Return the hits.
       Expected outcome: bounded output.
    """
    raise NotImplementedError("S4.4")


DISPATCH = {"ListFiles": (ListFiles, list_files), "ReadFile": (ReadFile, read_file),
            "SearchCode": (SearchCode, search_code)}


def run_tool(name: str, args: dict, deps: Deps):
    """Validate arguments and run one code tool by name.

    Spec: S4.4 | Ticket: 09 | Traces to: I12

    Build steps:
    1. Task: If `name not in DISPATCH` raise `ToolError(f"Unknown tool {name}.")`.
       Expected outcome: the model cannot invent tools.
    2. Task: `schema, fn = DISPATCH[name]`; `parsed = schema.model_validate(args)`; on `ValidationError as e`
       raise `ToolError(f"Bad arguments: {e.errors()}")`.
       Expected outcome: arguments are validated at the boundary.
    3. Task: Return `fn(deps, **parsed.model_dump())`.
       Expected outcome: the tool's result, sent back to the model.
    """
    raise NotImplementedError("S4.4")
