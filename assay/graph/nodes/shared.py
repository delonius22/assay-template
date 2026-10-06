"""Helpers used by several stages."""
from ...render import markdown as md
from ..context import AppContext
from ..state import AssayState


def reply(value) -> tuple[str, str]:
    """Split a resume value into (text, user).

    Spec: S5.3 | Ticket: 02 | Traces to: I12

    Build steps:
    1. Task: If `isinstance(value, dict)`, return
       `(str(value.get("text", "")).strip(), str(value.get("user") or "unknown"))`.
       Expected outcome: web replies carry the SSO user.
    2. Task: Otherwise return `(str(value).strip(), "unknown")`.
       Expected outcome: plain strings (tests, scripts) still work.
    """
    raise NotImplementedError("S5.3")


def write_intake(s: AssayState, c: AppContext) -> list[str]:
    """Rewrite intake.md and session-log.md (and the glossary) so files match state.

    Spec: S6.1 | Ticket: 02 | Traces to: C1, D2

    Build steps:
    1. Task: `names = md.intake(s, c.folder(s))`.
       Expected outcome: intake.md and session-log.md written; their names returned.
    2. Task: If `s.glossary`, call `md.glossary(s.glossary, c.settings.artifacts_dir, c.settings.team_name)`.
       Expected outcome: the shared glossary file is current.
    3. Task: Return `names`.
       Expected outcome: callers add them to `files`.
    """
    raise NotImplementedError("S6.1")


def files(s: AssayState, *names: str) -> list[str]:
    """The session's generated files plus new names, sorted, without blanks. (Complete.)"""
    return sorted(set(s.files) | {n for n in names if n})


def glossary_text(s: AssayState) -> str:
    """Glossary lines for prompts. (Complete.)"""
    return "\n".join(f"- {t.term}: {t.definition}" for t in s.glossary) or "(no glossary yet)"
