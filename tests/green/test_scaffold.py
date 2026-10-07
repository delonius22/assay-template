"""The scaffold installs, imports, compiles, and runs before anything is built."""
import importlib
import pkgutil
import pytest
import re
import subprocess
import sys
from pathlib import Path

from fastapi.testclient import TestClient

import assay
from assay.api.app import Services, create_app, ready
from assay.cli import build_progress
from assay.graph.build import build_graph
from tests.support.fakes import make_settings

ROOT = Path(__file__).resolve().parents[2]


def test_every_module_imports():
    for mod in pkgutil.walk_packages(assay.__path__, "assay."):
        if not mod.name.endswith("__main__"):
            importlib.import_module(mod.name)


def test_graph_compiles_with_every_node():
    assert len(build_graph().compile().get_graph().nodes) == 25     # 23 nodes + start + end


def test_cli_help_runs():
    out = subprocess.run([sys.executable, "-m", "assay", "--help"], capture_output=True, text=True, cwd=ROOT)
    assert out.returncode == 0 and "serve" in out.stdout


def test_every_stub_names_a_real_spec_id():
    specs = set(re.findall(r"\bS\d+\.\d+\b", (ROOT / "SPECS.md").read_text()))
    _, _, stubbed = build_progress()
    assert set(stubbed) <= specs


def test_server_runs_and_names_what_to_build(tmp_path):
    with TestClient(create_app(make_settings(tmp_path))) as c:
        # The scaffold boots; with persistence built (SQLite), the API is live.
        assert c.get("/").status_code == 200
        r = c.get("/api/me")
        assert r.status_code == 200 and "user" in r.json()
    # The not-yet-built guard still names a real spec ID, so any future unbuilt
    # layer fails loudly instead of returning empty state.
    svc = Services(settings=make_settings(tmp_path))
    with pytest.raises(NotImplementedError, match=r"S\d+\.\d+"):
        ready(svc)
