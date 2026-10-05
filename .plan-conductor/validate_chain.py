#!/usr/bin/env python3
"""Validate plan-conductor chain artifacts deterministically.

Usage: python3 validate_chain.py [project_root]

Checks (each skipped with a note when its artifact is absent):
  1. SPECS.md parses; S-IDs, I/A/C IDs, decision-log section extracted;
     '## Build order' and '## Data shapes' sections present (may state
     'none' with a reason, but must exist).
  2. Tickets: every Traces-to S-ID exists; every S-ID is covered by a
     ticket or an explicit 'deferred:'; Context capsules <= 25 lines;
     Blocked-by references resolve to real tickets.
  3. Code (any language with a common source extension): every
     'Spec:' line in source cites a real S-ID; S-IDs with no
     implementing function are listed (informational). Python-only:
     every module compiles; 'from __future__ import annotations'
     is banned.
  4. Manifest: stage entries use [x]/[wip]/[ ] markers only.
Exit 0 = all hard checks pass. Exit 1 = failures listed.
"""
import py_compile
import re
import sys
from pathlib import Path

root = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
fails: list[str] = []
notes: list[str] = []


def find_one(*patterns: str) -> Path | None:
    for p in patterns:
        hits = sorted(root.glob(p))
        if hits:
            return hits[0]
    return None


# --- 1. SPECS ---------------------------------------------------------------
specs_path = find_one("SPECS.md", "specs/SPECS.md", "**/SPECS.md")
sids: set[str] = set()
iac: set[str] = set()
if specs_path:
    text = specs_path.read_text(encoding="utf-8")
    sids = set(re.findall(r"\bS\d+\.\d+\b", text)) | set(
        re.findall(r"^## (S\d+):", text, re.M)
    )
    iac = set(re.findall(r"\b[IAC]\d+\b", text))
    if "## Decision log" not in text:
        fails.append(f"{specs_path}: missing '## Decision log' section")
    for section in ("## Build order", "## Data shapes"):
        if section not in text:
            fails.append(
                f"{specs_path}: missing '{section}' section "
                "('none — <reason>' is a valid body; absence is not)"
            )
    if not sids:
        fails.append(f"{specs_path}: no S-IDs found")
else:
    notes.append("SPECS.md not found - spec checks skipped")

# --- 2. Tickets -------------------------------------------------------------
ticket_files = sorted(root.glob(".scratch/*/issues/*.md")) + sorted(
    root.glob("tickets/*.md")
)
covered: set[str] = set()
ticket_ids: set[str] = set()
for tf in ticket_files:
    ticket_ids.add(tf.stem.split("-")[0])
for tf in ticket_files:
    t = tf.read_text(encoding="utf-8")
    traces = set(re.findall(r"\bS\d+(?:\.\d+)?\b", t.split("## Context")[0]))
    covered |= traces
    if specs_path:
        for s in traces:
            if s not in sids and not any(x.startswith(s + ".") for x in sids):
                fails.append(f"{tf.name}: traces to unknown {s}")
    if "**Traces to:**" not in t:
        fails.append(f"{tf.name}: missing '**Traces to:**' line")
    m = re.search(r"## Context\n(.*?)(?:\n## |\Z)", t, re.S)
    if m:
        n = len([ln for ln in m.group(1).strip().splitlines() if ln.strip()])
        if n > 25:
            fails.append(f"{tf.name}: context capsule {n} lines (cap 25) - split the ticket")
    else:
        fails.append(f"{tf.name}: missing '## Context' capsule")
    for ref in re.findall(r"\*\*Blocked by:\*\*\s*([^\n|]+)", t):
        for r in re.findall(r"\b(\d{2})\b", ref):
            if r not in ticket_ids:
                fails.append(f"{tf.name}: blocked by unknown ticket {r}")
if ticket_files and specs_path:
    deferred = set()
    for tf in ticket_files + [specs_path]:
        deferred |= set(
            re.findall(r"deferred:.*?\b(S\d+\.\d+)\b", tf.read_text(encoding="utf-8"))
        ) | set(re.findall(r"\b(S\d+\.\d+)\b.*?deferred:", tf.read_text(encoding="utf-8")))
    leaf_sids = {s for s in sids if "." in s}
    for s in sorted(leaf_sids):
        if s not in covered and s not in deferred:
            fails.append(f"coverage: {s} has no ticket and no 'deferred:' ruling")
elif not ticket_files:
    notes.append("no tickets found - ticket checks skipped")

# --- 3. Docstring Spec: lines ------------------------------------------------
SOURCE_EXTS = (
    ".py", ".ts", ".tsx", ".js", ".jsx", ".go", ".rs", ".java", ".kt",
    ".rb", ".cs", ".swift", ".c", ".h", ".cpp", ".hpp", ".ex", ".exs",
)
code_files = [
    p for p in root.rglob("*")
    if p.suffix in SOURCE_EXTS
    and ".plan-conductor" not in p.parts
    and "scripts" not in p.parts
    and "node_modules" not in p.parts
    and not {".venv", "venv", "env", "site-packages", ".tox"} & set(p.parts)  # local edit: skip virtualenvs
    and "vendor" not in p.parts
    and "target" not in p.parts
]
doc_sids: set[str] = set()
for cf in code_files:
    ctext = cf.read_text(encoding="utf-8", errors="ignore")
    if cf.suffix == ".py":  # language-scoped checks
        if re.search(r"^\s*from\s+__future__\s+import\s+annotations", ctext, re.M):
            fails.append(f"{cf.name}: 'from __future__ import annotations' is banned - remove it")
        try:
            py_compile.compile(str(cf), doraise=True)
        except py_compile.PyCompileError as exc:
            fails.append(f"{cf.name}: does not compile - {exc.exc_type_name}")
    for s in re.findall(r"Spec:\s*(S\d+\.\d+)", ctext):
        doc_sids.add(s)
        if specs_path and s not in sids:
            fails.append(f"{cf.name}: docstring cites unknown {s}")
if specs_path and code_files:
    missing = sorted({s for s in sids if "." in s} - doc_sids)
    if missing:
        notes.append(f"S-IDs with no implementing function yet: {', '.join(missing)}")

# --- 4. Manifest -------------------------------------------------------------
man = root / ".plan-conductor" / "manifest.md"
if man.exists():
    for ln in man.read_text(encoding="utf-8").splitlines():
        if ln.startswith("- [") and not re.match(r"- \[(x|wip| )\] ", ln):
            fails.append(f"manifest: bad status marker: {ln.strip()}")
else:
    notes.append("manifest not found - manifest checks skipped")

# --- report ------------------------------------------------------------------
for n in notes:
    print(f"NOTE  {n}")
if fails:
    for f in fails:
        print(f"FAIL  {f}")
    print(f"\n{len(fails)} failure(s).")
    sys.exit(1)
print("PASS  all hard checks passed")
