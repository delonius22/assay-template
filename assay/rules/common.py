"""Rules shared by several agents."""
import re
from typing import Any

from pydantic import BaseModel

ASSERTIONS = [r"\bcomplies with\b", r"\bcompliant with\b", r"\bfully compliant\b", r"\bconforms to\b",
              r"\bin compliance with\b", r"\bmeets (all )?(the )?(regulatory|legal) requirements\b",
              r"\bsatisfies (the )?(regulatory|legal)\b"]
VAGUE = ["properly", "adequately", "fully", "clean", "appropriate", "appropriately",
         "where needed", "as required", "as needed", "sufficient"]
GWT = re.compile(r"^Given .+?,? when .+?,? then .+", re.I | re.S)


def strings(obj: Any) -> list[str]:
    """Every string inside a model, list, dict, or string.

    Spec: S3.1 | Ticket: 02 | Traces to: I4

    Build steps:
    1. Task: If `isinstance(obj, BaseModel)`, replace it with `obj.model_dump()`.
       Expected outcome: models become plain dicts.
    2. Task: If `obj` is a `str`, return `[obj]`.
       Expected outcome: the base case.
    3. Task: If `obj` is a `dict`, return the concatenation of `strings(v)` for each value;
       if a `list` or `tuple`, the concatenation of `strings(v)` for each item.
       Expected outcome: nested strings collected in order.
    4. Task: Return `[]` for anything else (numbers, booleans, None).
       Expected outcome: non-text is ignored.
    """
    raise NotImplementedError("S3.1")


def compliance_claims(obj: Any) -> list[str]:
    """Problems for any text that asserts compliance (only Compliance may conclude).

    Spec: S3.1 | Ticket: 02 | Traces to: I4

    Build steps:
    1. Task: For each `s` in `strings(obj)`, check `any(re.search(p, s, re.I) for p in ASSERTIONS)`.
       Expected outcome: assertions found, including rewordings like "conforms to".
    2. Task: Skip `s` when `"confirm" in s.lower()`.
       Expected outcome: "Reg E: Compliance to confirm" passes.
    3. Task: Return one problem per hit:
       `f"States compliance: '{s[:100]}'. Rewrite it as an area for Compliance to confirm, with an owner."`.
       Expected outcome: the model is told exactly what to rewrite.
    """
    raise NotImplementedError("S3.1")


def one_question(text: str, where: str = "") -> list[str]:
    """A problem when the text asks more than one question.

    Spec: S3.1 | Ticket: 02 | Traces to: I1

    Build steps:
    1. Task: If `text.count("?") > 1`, return
       `[f"{where}Ask exactly one question. Keep the most foundational part."]`.
       Expected outcome: compound questions are rejected.
    2. Task: Otherwise return `[]`.
       Expected outcome: single questions pass.
    """
    raise NotImplementedError("S3.1")


def vague_words(text: str) -> list[str]:
    """The VAGUE words that appear in the text as whole words.

    Spec: S3.1 | Ticket: 04 | Traces to: I1

    Build steps:
    1. Task: Return `[w for w in VAGUE if re.search(rf"\\b{re.escape(w)}\\b", text.lower())]`.
       Expected outcome: "properly tested" yields ["properly"]; "cleanup" yields nothing.
    """
    raise NotImplementedError("S3.1")
