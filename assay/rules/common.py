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
   """Every string inside a model, list, dict, or string"""
   if isinstance(obj, BaseModel):
      obj = obj.model_dump()
   if isinstance(obj, str):
      return [obj]
   if isinstance(obj, dict):
      return [s for v in obj.values() for s in strings(v)]
   if isinstance(obj, (list, tuple)):
      return [s for v in obj for s in strings(v)]
   return []


def compliance_claims(obj: Any) -> list[str]:
   """Problems for any text that asserts compliance (only Compliance may conclude)."""
   return [s for s in strings(obj) if any(re.search(p, s, re.I) for p in ASSERTIONS) and "confirm" not in s.lower()]


def one_question(text: str, where: str = "") -> list[str]:
    """A problem when the text asks more than one question."""
    # Check if the text contains more than one question mark
    return [f"{where}Ask exactly one question. Keep the most foundational part."] if text.count("?") > 1 else []


def vague_words(text: str) -> list[str]:
   """The VAGUE words that appear in the text as whole words."""
   return [w for w in VAGUE if re.search(rf"\b{re.escape(w)}\b", text.lower())]
