"""tickets.csv: each story, then each feature followed by its tickets (C6).
Columns are the contract in SPECS ## Data shapes."""
import csv
import io
import re

from ..domain.models import DodItem, PRDCore, Ticket

SPEC_SECTIONS = {"modules": "3.1 Modules", "interfaces": "3.2 Interfaces", "data": "3.3 Data",
                 "key_flows": "3.4 Key flows", "integrations": "3.5 Integrations",
                 "security": "4 Security", "nfr_design": "5 Non-functional design",
                 "observability": "6 Observability", "rollout": "7 Rollout", "testing": "8 Testing"}
COLUMNS = ["Level", "ID", "Parent ID", "Title", "Description", "Acceptance Criteria",
           "Definition of Done", "Requirements", "Spec Sections", "Priority", "Size", "Type",
           "Depends On", "Unblocks", "Sources"]
RANK = {"Must have": 0, "Should have": 1, "Could have": 2, "Won't have": 3}


def story_title(text: str) -> str:
    """'As a customer, I want low-balance alerts, so that…' -> 'Low-balance alerts'.

    Spec: S6.5 | Ticket: 07 | Traces to: C6

    Build steps:
    1. Task: `m = re.search(r"I want (?:to )?(.+?),? so that", text, re.I | re.S)`;
       `goal = (m.group(1) if m else text).strip()`.
       Expected outcome: the goal clause, or the whole text when the pattern fails.
    2. Task: Return `goal[:1].upper() + goal[1:]`.
       Expected outcome: sentence case.
    """
    raise NotImplementedError("S6.5")


def dod_cell(items: list[DodItem]) -> str:
    """One DoD checklist cell. (Complete.)"""
    return "\n".join(f"[ ] {d.id} {d.statement} (evidence: {d.evidence})" for d in items)


def top_priority(priorities: list[str]) -> str:
    """The highest MoSCoW priority in a list. (Complete.)"""
    return min(priorities, key=lambda p: RANK[p]) if priorities else ""


def rows(core: PRDCore, fr_ids: list[str], tickets: list[Ticket], dod: dict[str, list[DodItem]]) -> list[dict]:
    """CSV rows in order: story, then each feature followed by its tickets.

    Spec: S6.5 | Ticket: 07 | Traces to: C6, I15

    Build steps:
    1. Task: Build `reqs_by_feature` mapping feature ID -> list of (FR ID, priority) from `zip(fr_ids, core.functional)`.
       Expected outcome: each feature's requirements and priorities.
    2. Task: For each story `st`: append `{"Level": "Story", "ID": st.id, "Parent ID": "", "Title": story_title(st.text),
       "Description": st.text, "Definition of Done": dod_cell(dod["story"]), "Priority": top_priority(<priorities of
       all its features' requirements>)}`.
       Expected outcome: one story row.
    3. Task: For each feature `f` in `st.features`: append `{"Level": "Feature", "ID": f.id, "Parent ID": st.id,
       "Title": f.name, "Description": f.summary, "Definition of Done": dod_cell(dod["feature"]),
       "Requirements": " ".join(its FR IDs), "Priority": top_priority(its priorities)}`.
       Expected outcome: features directly after their story.
    4. Task: Directly after each feature, for each ticket `t` with `t.feature_id == f.id` (list order): Description is
       `t.user_story` (Ticket), f"Question: {t.question} Timebox: {t.timebox}" (Spike), or
       f"Enabler. Unblocks {', '.join(t.unblocks_ids)}." (Enabler), plus f"\\nNotes: {t.notes}" when present;
       Acceptance Criteria is `"\\n".join(f"{k}. {c}" for k, c in enumerate(t.acceptance_criteria, 1))`;
       Definition of Done `dod_cell(dod["ticket"])`; Requirements `" ".join(t.requirements)`;
       Spec Sections `"; ".join(SPEC_SECTIONS[r] for r in t.spec_refs)`; Priority, Size, Type from the ticket;
       Depends On `" ".join(t.depends_on_ids)`; Unblocks `" ".join(t.unblocks_ids)`; Sources `" ".join(t.sources)`;
       Level "Ticket", Parent ID `f.id`.
       Expected outcome: tickets in build order under their feature.
    5. Task: Return the list of row dicts.
       Expected outcome: ready for to_csv().
    """
    raise NotImplementedError("S6.5")


def to_csv(rows_: list[dict]) -> str:
    """CSV text with every column, multi-line cells quoted.

    Spec: S6.5 | Ticket: 07 | Traces to: C1

    Build steps:
    1. Task: `buf = io.StringIO()`; `w = csv.DictWriter(buf, fieldnames=COLUMNS, lineterminator="\\n")`; `w.writeheader()`.
       Expected outcome: the header row.
    2. Task: For each row, `w.writerow({c: r.get(c, "") for c in COLUMNS})`.
       Expected outcome: missing cells are empty; newlines inside cells are quoted by the csv module.
    3. Task: Return `buf.getvalue()`.
       Expected outcome: the CSV text.
    """
    raise NotImplementedError("S6.5")
