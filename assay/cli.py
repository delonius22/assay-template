"""Command line: `assay serve` runs the web app; `assay check` reports configuration
and build progress. (Complete.)"""
import argparse
import importlib
import inspect
import pkgutil
import re

import assay


def build_progress() -> tuple[int, int, list[str]]:
    """Count functions still raising NotImplementedError, by S-ID."""
    stubbed, total, ids = 0, 0, set()
    for mod in pkgutil.walk_packages(assay.__path__, "assay."):
        if mod.name.endswith("__main__"):
            continue                       # importing it would re-run the CLI
        m = importlib.import_module(mod.name)
        for _, obj in inspect.getmembers(m):
            fns = [obj] if inspect.isfunction(obj) else (
                [f for _, f in inspect.getmembers(obj, inspect.isfunction)] if inspect.isclass(obj) else [])
            for f in fns:
                if getattr(f, "__module__", "") != mod.name:
                    continue
                try:
                    src = inspect.getsource(f)
                except (OSError, TypeError):
                    continue                   # generated methods (dataclasses) have no source
                total += 1
                if hit := re.search(r'raise NotImplementedError\("(S\d+\.\d+)"\)', src):
                    stubbed += 1
                    ids.add(hit.group(1))
    return stubbed, total, sorted(ids, key=lambda x: [int(n) for n in x[1:].split(".")])


def main(argv=None) -> None:
    ap = argparse.ArgumentParser(prog="assay", description="Grill an idea into a PRD, a spec, and a tickets CSV.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sv = sub.add_parser("serve", help="Run the web app (one worker).")
    sv.add_argument("--host", default="127.0.0.1")
    sv.add_argument("--port", type=int, default=8000)
    sub.add_parser("check", help="Show configuration problems and which S-IDs are still stubbed.")
    a = ap.parse_args(argv)

    if a.cmd == "serve":
        import uvicorn
        uvicorn.run("assay.api.app:create_app", factory=True, host=a.host, port=a.port, workers=1)
        return

    stubbed, total, ids = build_progress()
    print(f"Build progress: {total - stubbed} of {total} functions implemented.")
    if ids:
        print("Still stubbed: " + ", ".join(ids))
    try:
        from .settings import load_settings, missing_config
        missing = missing_config(load_settings())
        print("Configuration: " + ("complete." if not missing else "missing " + ", ".join(missing)))
    except NotImplementedError as exc:
        print(f"Configuration: not checkable yet; build {exc} first.")


if __name__ == "__main__":
    main()
