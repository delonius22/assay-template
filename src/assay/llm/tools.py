"""Give agents read-only, sandboxed access to allowlisted code.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C1 Trustworthy output. Agents answer better from code than
from guesses, but code holds secrets. This file owns what may be listed, read, and
searched; it never writes or runs anything.

Why this comes now: Retry exists (step 11). The call loop (step 13) runs these tools
and passes Deps to validators.

Build order: Step 12 of 33.
Previous: src/assay/llm/resilience.py (step 11), which retries transient gateway
errors with backoff.
Next: src/assay/llm/call.py (step 13), which runs the validate-and-retry loop every
agent call goes through.

Build these in order:
    1. ToolError: the error every tool raises.
    2. Deps: the context every tool takes.
    3. ListFiles: first tool schema.
    4. ReadFile: second tool schema.
    5. SearchCode: third tool schema.
    6. roots_from: setup for Deps.
    7. denied: used by every tool.
    8. redact: used by read and search.
    9. resolve: the gate for read and search.
    10. list_files: the first tool.
    11. read_file: the second tool; uses resolve and redact.
    12. search_code: the third tool; uses list_files.
    13. run_tool: the single entry the call loop uses.

Depends on:
    Nothing in this project (foundation root). Placed at step 12 because the call
    loop needs the tool schemas and Deps.
    Standard library: fnmatch, re, dataclasses, pathlib.
    Third-party: pydantic.

Depended on by:
    assay.llm.call: offers and runs the tools. assay.llm.agents: validators read
    Deps. assay.graph.context: builds Deps.

Spec coverage: S4.4 | Traces to: I10, I12
"""

import fnmatch
import re
from dataclasses import dataclass, field
from pathlib import Path

from pydantic import BaseModel, Field, ValidationError

DENY: list[str] = [  # S4.4: never readable, even inside allowed roots
    ".env",
    "*.env",
    ".env.*",
    "*.pem",
    "*.key",
    "*.p12",
    "*.pfx",
    "*.jks",
    "*secret*",
    "*credential*",
    "id_rsa*",
    "*.sqlite",
    "*.db",
    ".git/*",
    "node_modules/*",
]
SECRET_LINE: list[re.Pattern[str]] = [  # S4.4: lines redacted before a model sees them
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(
        r"(?i)\b(password|passwd|pwd|secret|api[_-]?key|token|client[_-]?secret)\b"
        r"\s*[:=]\s*['\"]?[^\s'\"]{6,}"
    ),
    re.compile(r"(?i)\b[a-z][a-z0-9+.-]*://[^/\s:@]+:[^/\s@]+@"),
]
REDACTED = "[line redacted: looks like a credential]"  # S4.4
MAX_BYTES = 60_000  # S4.4: per file read
MAX_HITS = 80  # S4.4: per search
MAX_LIST = 300  # S4.4: per listing


class ToolError(Exception):
    """A tool refusal, sent back to the model as text.

    Problem piece: C1: a model that asks for something forbidden learns why, instead
                   of crashing the call.

    Why it matters: Refusals are expected; raising a distinct error lets the call
                    loop return the message to the model and continue.

    What: An exception whose message is shown to the model.

    Spec: S4.4 | Ticket: — | Traces to: —
    """


@dataclass
class Deps:
    """Per-call context for tools and validators.

    Problem piece: C1: tools and rules see this session's roots and IDs.

    Why it matters: Validators need the session's known IDs and tools need the
                    allowed roots; passing them together keeps the call loop
                    generic.

    What: Allowed roots, known IDs, PRD IDs, feature IDs, and files read so far.

    Spec: S4.4 | Ticket: — | Traces to: —
    """

    roots: dict[str, Path] = field(default_factory=dict)
    known_ids: set[str] = field(default_factory=set)
    prd_ids: set[str] = field(default_factory=set)
    feature_ids: set[str] = field(default_factory=set)
    files_read: list[str] = field(default_factory=list)


class ListFiles(BaseModel):
    """Tool arguments: list readable files matching a glob.

    Problem piece: C1: the shape the model fills to list files.

    Why it matters: The class name and docstring become the tool the model sees, so
                    they must describe it plainly.

    What: A glob pattern whose first segment may be a root name.

    Spec: S4.4 | Ticket: — | Traces to: —
    """

    pattern: str = Field("**/*")


class ReadFile(BaseModel):
    """Tool arguments: read lines from a readable file.

    Problem piece: C1: the shape the model fills to read a file.

    Why it matters: Line ranges keep reads bounded and let the model ask for more
                    only when needed.

    What: A root-prefixed path and an inclusive 1-based line range.

    Spec: S4.4 | Ticket: — | Traces to: —
    """

    path: str
    start_line: int = 1
    end_line: int = 400


class SearchCode(BaseModel):
    """Tool arguments: search readable files for a pattern.

    Problem piece: C1: the shape the model fills to search code.

    Why it matters: Searching finds the relevant file without reading the whole
                    repository.

    What: A regular expression and a glob.

    Spec: S4.4 | Ticket: — | Traces to: —
    """

    regex: str
    glob: str = "**/*"


TOOL_SCHEMAS: list[type[BaseModel]] = [ListFiles, ReadFile, SearchCode]  # S4.4


def roots_from(paths: tuple[Path, ...]) -> dict[str, Path]:
    """Name each allowed root by its folder name.

    Problem piece: C1: short, stable root names in tool paths.

    Why it matters: Absolute paths leak server layout to the model; folder names are
                    enough to address a root.

    What: Maps each root's final folder name to the root. Called as
          roots_from(paths: tuple[Path, ...]) and returns dict[str, Path].

    Spec: S4.4 | Ticket: 09 | Traces to: I10

    Build steps:
    1. Task: Map each path's final folder name to the path.
       Expected outcome: A root /srv/repos/payments is addressed as 'payments'.
    """
    raise NotImplementedError("S4.4: roots_from")


def denied(rel: str, name: str) -> bool:
    """Return True when a path or file name matches the denylist.

    Problem piece: C1: secret-bearing files are never readable (I10).

    Why it matters: A .env inside an allowed root is still a secret; matching both
                    the relative path and the bare name catches it anywhere.

    What: True when either the relative path or the file name matches any DENY
          pattern. Called as denied(rel: str, name: str) and returns bool.

    Spec: S4.4 | Ticket: 09 | Traces to: I10

    Build steps:
    1. Task: Return True when the relative path or the name matches any DENY pattern
             as a shell-style wildcard.
       Expected outcome: '.env' and 'config/.env' are both denied.
    """
    raise NotImplementedError("S4.4: denied")


def redact(text: str) -> str:
    """Replace every credential-looking line with REDACTED.

    Problem piece: C1: a password in an ordinary file never reaches a model (I10).

    Why it matters: The denylist catches secret files, not secrets inside ordinary
                    files such as config.yaml. Redacting whole lines, rather than
                    trying to cut out just the secret, avoids leaking part of a
                    credential through a clever match.

    What: Returns the text with each line matching any SECRET_LINE pattern replaced;
          line count unchanged. Called as redact(text: str) and returns str.

    Spec: S4.4 | Ticket: 09 | Traces to: I10

    Build steps:
    1. Task: Replace each line matching any SECRET_LINE pattern with REDACTED,
             keeping line count.
       Think about: Why keep the line rather than delete it?
       Expected outcome: 'token = abcdef123456' becomes the redaction marker.
    """
    raise NotImplementedError("S4.4: redact")


def resolve(deps: Deps, path: str) -> Path:
    """Map 'root/relative/path' to a real path inside an allowed root.

    Problem piece: C1: no path escapes the allowlist (I10, I12).

    Why it matters: 'payments/../../etc/passwd' looks like it is inside a root until
                    it is resolved. Checking after resolving dots and symlinks is
                    the only reliable check.

    What: Returns an absolute path inside a named root, or raises ToolError
          explaining the refusal. Called as resolve(deps: Deps, path: str) and
          returns Path.

    Spec: S4.4 | Ticket: 09 | Traces to: I10, I12

    Raises:
        ToolError: no roots configured, unknown root, outside the root, or denied by
        policy.

    Build steps:
    1. Task: Refuse when no roots are configured, then split off the root name and
             refuse an unknown root, naming the readable roots.
       Expected outcome: 'elsewhere/x.py' is refused.
    2. Task: Resolve the path fully and refuse it unless it lies inside the root;
             then refuse denied names.
       Think about: Why resolve before checking containment?
       Expected outcome: 'payments/../../etc/passwd' is refused as outside the
                         allowed directories.
    """
    raise NotImplementedError("S4.4: resolve")


def list_files(deps: Deps, pattern: str = "**/*") -> list[str]:
    """Return readable files matching a glob, as 'root/relative' paths.

    Problem piece: C1: let the agent find relevant files.

    Why it matters: An agent cannot read what it cannot find, and listings must
                    never reveal denied files.

    What: Searches one root when the pattern starts with its name, else all roots;
          capped at MAX_LIST.

    Spec: S4.4 | Ticket: 09 | Traces to: I10, I12

    Raises:
        ToolError: no code access configured.

    Build steps:
    1. Task: Choose the roots: just the named root when the pattern starts with one,
             otherwise all roots with the whole pattern.
       Expected outcome: 'payments/**/*.py' searches only payments.
    2. Task: List matching files that are not denied as 'root/relative', stopping at
             MAX_LIST with '... truncated; narrow the pattern'.
       Expected outcome: A root's .env never appears.
    """
    raise NotImplementedError("S4.4: list_files")


def read_file(deps: Deps, path: str, start_line: int = 1, end_line: int = 400) -> str:
    """Return numbered, redacted lines from an allowed file.

    Problem piece: C1: let the agent read code safely.

    Why it matters: Reads must be bounded, redacted, and recorded so the explore
                    validator can tell code was read.

    What: Lines start_line to end_line, prefixed 'N: ', from at most MAX_BYTES;
          records the path read.

    Spec: S4.4 | Ticket: 09 | Traces to: I10, I12

    Raises:
        ToolError: refused path or no such file.

    Build steps:
    1. Task: Resolve the path, refuse a missing file, and read at most MAX_BYTES,
             decoding unreadable bytes with replacement characters.
       Expected outcome: A missing file is refused.
    2. Task: Redact, select the requested line range, record the path as read, and
             number each line from start_line.
       Expected outcome: Reading a file containing a password returns the redaction
                         marker on that line.
    """
    raise NotImplementedError("S4.4: read_file")


def search_code(deps: Deps, regex: str, glob: str = "**/*") -> list[str]:
    r"""Return 'path:line: text' hits for a pattern across readable files.

    Problem piece: C1: find where something is defined or used.

    Why it matters: Searching redacted text only keeps secrets out of hits as well
                    as reads. Bounding the number of hits keeps one broad pattern
                    from flooding the model's context and the bill.

    What: Hits from redacted text, each trimmed to 200 characters, capped at
          MAX_HITS. Called as search_code(deps: Deps, regex: str, glob: str) and
          returns list[str].

    Spec: S4.4 | Ticket: 09 | Traces to: I10, I12

    Raises:
        ToolError: an invalid regular expression.

    Build steps:
    1. Task: Refuse an invalid pattern with 'Bad regex: <reason>'.
       Expected outcome: '(' is refused.
    2. Task: Search each listed file's redacted text, skipping unreadable files, and
             return hits as 'path:line: text', stopping at MAX_HITS with a
             truncation note.
       Expected outcome: Searching 'def \w+' returns a hit like
                         'payments/src/app.py:1: def save()'.
    """
    raise NotImplementedError("S4.4: search_code")


DISPATCH: dict[str, tuple[type[BaseModel], object]] = {  # S4.4
    "ListFiles": (ListFiles, list_files),
    "ReadFile": (ReadFile, read_file),
    "SearchCode": (SearchCode, search_code),
}


def run_tool(name: str, args: dict[str, object], deps: Deps) -> object:
    """Validate a tool call's arguments and run it.

    Problem piece: C1: the model can call only real tools with valid arguments
                   (I12).

    Why it matters: Tool arguments come from a model and must be validated like any
                    external input. A model can name tools that do not exist or pass
                    malformed arguments, and either must come back as a fixable
                    message, not a crash.

    What: Runs the named tool with validated arguments, or raises ToolError. Called
          as run_tool(name: str, args: dict[str, object], deps: Deps) and returns
          object.

    Spec: S4.4 | Ticket: 09 | Traces to: I12

    Raises:
        ToolError: unknown tool or bad arguments.

    Build steps:
    1. Task: Refuse names not in DISPATCH, then validate the arguments against the
             tool's schema, refusing with the validation errors.
       Expected outcome: Calling 'DeleteFile' is refused.
    2. Task: Run the tool with the validated arguments and return its result.
       Expected outcome: A valid ReadFile call returns numbered lines.
    """
    raise NotImplementedError("S4.4: run_tool")
