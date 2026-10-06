"""Prompt caching: static prefix first, changing state last, so the provider
can cache the prefix. Modes: explicit (add cache markers), auto, off."""
from langchain_core.messages import BaseMessage, HumanMessage, SystemMessage


def build_messages(static: str, dynamic: str, mode: str) -> list[BaseMessage]:
    """System message (static, cacheable) then human message (dynamic).

    Spec: S4.2 | Ticket: 02 | Traces to: A2

    Build steps:
    1. Task: When `mode == "explicit"`, build
       `SystemMessage(content=[{"type": "text", "text": static, "cache_control": {"type": "ephemeral"}}])`;
       otherwise `SystemMessage(content=static)`.
       Expected outcome: only the static prefix carries the cache marker.
    2. Task: Return `[system, HumanMessage(content=dynamic)]`.
       Expected outcome: per-call state never enters the cached prefix.
    """
    if mode == "explicit":
        system = SystemMessage(content=[{"type": "text", "text": static, "cache_control": {"type": "ephemeral"}}])
    else:
        system = SystemMessage(content=static)
    return [system, HumanMessage(content=dynamic)]


def usage_of(message) -> dict[str, int]:
    """Token counts from one response, including cache reads when reported.

    Spec: S4.2 | Ticket: 10 | Traces to: A2

    Build steps:
    1. Task: `u = getattr(message, "usage_metadata", None) or {}`;
       `details = u.get("input_token_details") or {}`.
       Expected outcome: missing usage gives empty dicts, not errors.
    2. Task: Return `{"input_tokens": int(u.get("input_tokens", 0)),
       "output_tokens": int(u.get("output_tokens", 0)),
       "cache_read_tokens": int(details.get("cache_read", 0) or 0),
       "cache_write_tokens": int(details.get("cache_creation", 0) or 0)}`.
       Expected outcome: four integers the call record adds up.
    """
    u = getattr(message, "usage_metadata", None) or {}
    details = u.get("input_token_details") or {}
    return {
        "input_tokens": int(u.get("input_tokens", 0)),
        "output_tokens": int(u.get("output_tokens", 0)),
        "cache_read_tokens": int(details.get("cache_read", 0) or 0),
        "cache_write_tokens": int(details.get("cache_creation", 0) or 0),
    }
