"""Write every markdown artifact from typed state using templates/*.j2.
The Jinja environment and filters are complete; the writers are stubbed."""
from datetime import date
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, StrictUndefined

from ..domain.ids import live, question_ids
from ..domain.models import DodItem, GlossaryTerm
from ..rules.intake import gate
from .csv_export import SPEC_SECTIONS, rows, to_csv
from .pdf import render_pdf

TEMPLATES = Path(__file__).resolve().parent.parent / "templates"
MODES = {1: "1 Greenfield", 2: "2 Existing system", 3: "3 Brief + questionnaire"}
LEVELS = [("ticket", "Ticket level"), ("feature", "Feature level"), ("story", "Story level"),
          ("release", "Release level")]

env = Environment(loader=FileSystemLoader(TEMPLATES), undefined=StrictUndefined,
                  trim_blocks=False, lstrip_blocks=False, keep_trailing_newline=True)
env.filters["cell"] = lambda v: str(v).replace("|", "/").replace("\n", " ").strip()
env.filters["yamlsafe"] = lambda v: '"' + str(v).replace('"', "'") + '"'
env.filters["section_name"] = lambda k: SPEC_SECTIONS.get(k, k)
env.filters["count"] = lambda n, one, many=None: f"{n} {one if n == 1 else (many or one + 's')}"


def template_env() -> Environment:
    """Return the template environment with its filters. (Spec: S6.1 | Ticket: 02 | Traces to: C1)"""
    return env


def write(path: Path, text: str) -> str:
    """Write text (with one trailing newline), creating folders; return the file name. (Complete.)"""
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")
    return path.name


def intake(s, folder: Path) -> list[str]:
   """intake.md (exit gate) and session-log.md.

   Spec: S6.1 | Ticket: 02 | Traces to: C1, I5

   Build steps:
   1. Task: `g = gate(s.log, s.dod_phase == "done")`.
      Expected outcome: the gate items to print.
   2. Task: Return `[write(folder / "intake.md", env.get_template("intake.md.j2").render(s=s, gate=g, modes=MODES)),
      write(folder / "session-log.md", env.get_template("session-log.md.j2").render(s=s))]`.
      Expected outcome: both files rewritten from state.
   """
   g = gate(s.log, s.dod_phase == "done")
   return [write(folder / "intake.md", env.get_template("intake.md.j2").render(s=s, gate=g, modes=MODES)),
           write(folder / "session-log.md", env.get_template("session-log.md.j2").render(s=s))]

def glossary(terms: list[GlossaryTerm], root: Path, team: str) -> None:
   """Spec: S6.1 | Ticket: 02 | Traces to: C1

   Build steps:
   1. Task: `write(root / "glossary.md", env.get_template("glossary.md.j2").render(terms=terms, team=team))`.
      Expected outcome: the shared glossary file, terms sorted by the template.
   """
   write(root / "glossary.md", env.get_template("glossary.md.j2").render(terms=terms, team=team))


def questionnaire(s, folder: Path, form_url: str) -> str:
   """Printable questionnaire for the current round.

   Spec: S6.2 | Ticket: 08 | Traces to: C1

   Build steps:
   1. Task: `ids = question_ids(s.questionnaire, s.q_round)`;
      `name = "questionnaire.md" if s.q_round == 1 else "questionnaire-followup.md"`.
      Expected outcome: the right file for the round.
   2. Task: Return `write(folder / name, env.get_template("questionnaire.md.j2").render(s=s, q=s.questionnaire,
      pairs=list(zip(ids, s.questionnaire.questions)), round=s.q_round, form_url=form_url))`.
      Expected outcome: the file name, for `files`.
   """
   ids = question_ids(s.questionnaire, s.q_round)
   name = "questionnaire.md" if s.q_round == 1 else "questionnaire-followup.md"
   return write(folder / name, env.get_template("questionnaire.md.j2").render(s=s, q=s.questionnaire,
                pairs=list(zip(ids, s.questionnaire.questions)), round=s.q_round, form_url=form_url))


def dod(items: list[DodItem], path: Path, heading: str) -> str:
   """Spec: S6.2 | Ticket: 04 | Traces to: C1

   Build steps:
   1. Task: Return `write(path, env.get_template("dod.md.j2").render(items=items, heading=heading, levels=LEVELS))`.
      Expected outcome: items grouped under Ticket, Feature, Story, and Release headings.
   """
   return write(path, env.get_template("dod.md.j2").render(items=items, heading=heading, levels=LEVELS))

def prd(s, folder: Path) -> list[str]:
   """prd.md (with front matter) and prd.pdf.

   Spec: S6.3 | Ticket: 05 | Traces to: C5, I3

   Build steps:
   1. Task: `core, nar = s.prd_core, s.prd_narrative`; `story_of = {f.id: st.id for st in core.stories for f in st.features}`;
      `entries = live(s.log)`.
      Expected outcome: lookups for the traceability appendix and the tables.
   2. Task: `md = env.get_template("prd.md.j2").render(s=s, core=core, nar=nar, doc_id=s.doc_id,
      today=date.today().isoformat(), fr=list(zip(s.fr_ids, core.functional)), nfr=list(zip(s.nfr_ids, core.non_functional)),
      assumptions=[e for e in entries if e.type == "A"], risks=[e for e in entries if e.type == "R"],
      questions=[e for e in entries if e.type == "Q" and e.status != "Closed"],
      terms=sorted(s.glossary, key=lambda t: t.term), story_of=story_of)`.
      Expected outcome: the full PRD markdown; StrictUndefined fails on any missing variable.
   3. Task: `name = write(folder / "prd.md", md)`; `render_pdf(md, folder / "prd.pdf")`; return `[name, "prd.pdf"]`.
      Expected outcome: both files exist; the PDF shows Approved when `s.approved_by` is set.
   """
   core, nar = s.prd_core, s.prd_narrative
   story_of = {f.id: st.id for st in core.stories for f in st.features}
   entries = live(s.log)
   md = env.get_template("prd.md.j2").render(
       s=s,
       core=core,
       nar=nar,
       doc_id=s.doc_id,
       today=date.today().isoformat(),
       fr=list(zip(s.fr_ids, core.functional)),
       nfr=list(zip(s.nfr_ids, core.non_functional)),
       assumptions=[e for e in entries if e.type == "A"],
       risks=[e for e in entries if e.type == "R"],
       questions=[e for e in entries if e.type == "Q" and e.status != "Closed"],
       terms=sorted(s.glossary, key=lambda t: t.term),
       story_of=story_of,
   )
   name = write(folder / "prd.md", md)
   render_pdf(md, folder / "prd.pdf")
   return [name, "prd.pdf"]


def spec(s, folder: Path) -> str:
   """Spec: S6.4 | Ticket: 06 | Traces to: C1

   Build steps:
   1. Task: Return `write(folder / "spec.md", env.get_template("spec.md.j2").render(s=s, sp=s.spec, seams=s.seams))`.
      Expected outcome: spec.md with numbered sections and the coverage table.
   """
   return write(folder / "spec.md", env.get_template("spec.md.j2").render(s=s, sp=s.spec, seams=s.seams))


def tickets(s, folder: Path) -> list[str]:
   """tickets.csv and agent-prompt.md.

   Spec: S6.6 | Ticket: 07 | Traces to: C1, C6

   Build steps:
   1. Task: `dod_by_level = {lv: [i for i in s.dod_team + s.dod_additions if i.level == lv] for lv, _ in LEVELS}`;
      `csv_text = to_csv(rows(s.prd_core, s.fr_ids, s.tickets, dod_by_level))`;
      `(folder / "tickets.csv").write_text(csv_text, encoding="utf-8")` (create the folder first with
      `folder.mkdir(parents=True, exist_ok=True)`).
      Expected outcome: the CSV, written exactly as generated.
   2. Task: `by_feature` maps each feature ID to its ticket IDs in list order;
      `counts = {"stories": len(s.prd_core.stories), "features": len(s.feature_ids), "tickets": len(s.tickets)}`.
      Expected outcome: the summary the prompt prints.
   3. Task: `prompt = env.get_template("agent-prompt.md.j2").render(s=s, core=s.prd_core, csv_text=csv_text.rstrip(),
      counts=counts, tickets_by_feature={f: by_feature.get(f, []) for f in s.feature_ids})`.
      Expected outcome: instructions, the hierarchy, and the CSV in one prompt.
   4. Task: Return `["tickets.csv", write(folder / "agent-prompt.md", prompt)]`.
      Expected outcome: both names for `files`.
   """
   dod_by_level = {lv: [i for i in s.dod_team + s.dod_additions if i.level == lv] for lv, _ in LEVELS}
   csv_text = to_csv(rows(s.prd_core, s.fr_ids, s.tickets, dod_by_level))
   folder.mkdir(parents=True, exist_ok=True)
   (folder / "tickets.csv").write_text(csv_text, encoding="utf-8")
   by_feature = {f: [t.id for t in s.tickets if f in t.features] for f in s.feature_ids}
   counts = {"stories": len(s.prd_core.stories), "features": len(s.feature_ids), "tickets": len(s.tickets)}
   prompt = env.get_template("agent-prompt.md.j2").render(
       s=s,
       core=s.prd_core,
       csv_text=csv_text.rstrip(),
       counts=counts,
       tickets_by_feature={f: by_feature.get(f, []) for f in s.feature_ids}
   )
   return ["tickets.csv", write(folder / "agent-prompt.md", prompt)]
