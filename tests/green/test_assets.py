"""Shipped-complete assets: prompts, templates, UI, PDF renderer (decision D6)."""
from pathlib import Path

from assay.llm import agents as A
from assay.render.markdown import TEMPLATES, env
from assay.render.pdf import render_pdf

UI = Path(A.__file__).resolve().parents[1] / "api" / "static" / "index.html"
PAUSE_KINDS = ["question", "dod_question", "map_review", "brief_fix", "await_answers", "approval", "seams",
               "ticket_review"]


def test_prompts_load_and_prefixes_are_stable():
    assert A.PRD_CORE.static == A.PRD_NARRATIVE.static           # one cache entry for both PRD agents
    for spec in [*A.GRILL.values(), A.EXPLORE, A.BRIEF, A.QUESTIONNAIRE, A.RECONCILE, A.DOD,
                 A.PRD_CORE, A.SEAMS, A.SPEC, A.TICKETS]:
        assert spec.static.startswith("# Rules for every task")
    assert "NFR- ID must be covered" in A.TICKETS.static        # decision D5


def test_every_template_compiles():
    names = sorted(p.name for p in TEMPLATES.glob("*.j2"))
    assert len(names) == 8
    for n in names:
        env.get_template(n)


def test_ui_handles_every_pause_kind():
    html = UI.read_text()
    for kind in PAUSE_KINDS:
        assert f'"{kind}"' in html, kind


def test_pdf_renderer_produces_a_pdf(tmp_path):
    md = ("---\ntitle: Test\ndoc_id: PRD-1\nversion: \"0.1\"\nstatus: For review\n"
          "classification: Internal\napprovers:\n  - name: A\n    role: B\n---\n\n# 1. Summary\n\nText.\n\n"
          "| ID | Requirement |\n|---|---|\n| FR-01 | Must work. |\n")
    out = tmp_path / "t.pdf"
    render_pdf(md, out)
    assert out.read_bytes()[:4] == b"%PDF"
