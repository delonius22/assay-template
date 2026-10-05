"""Provide the command line: serve the app and report build progress.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C6 People decide. Operators start the app and developers see
what is left to build. This file owns those commands.

Why this comes now: The app (31) exists.

Build order: Step 32 of 33.
Previous: src/assay/api/app.py (step 31), which serves the REST API and the AG-UI
endpoint.
Next: src/assay/__main__.py (step 33), which runs the command line.

Build these in order:
    1. build_progress: used by 'check'.
    2. main: the entry.

Depends on:
    assay.settings: load_settings, missing_config. Configuration status.
    Standard library: argparse, importlib, inspect, pkgutil, re.
    Third-party: uvicorn (imported inside main).

Depended on by:
    assay.__main__: the entry point.

Spec coverage: S8.3 | Traces to: I9
"""

import argparse
import importlib
import inspect
import pkgutil
import re

import assay
from assay.settings import load_settings, missing_config


def build_progress() -> tuple[int, int, list[str]]:
    """Count stubbed functions and list their spec IDs.

    Problem piece: C6: developers see what is left.

    Why it matters: A skeleton is built over weeks; a count by spec ID shows
                    progress and the next work at a glance.

    What: Stubbed count, total count, and stubbed spec IDs sorted numerically; skips
          the entry module and vendored code.

    Spec: S8.3 | Ticket: 02 | Traces to: I9

    Build steps:
    1. Task: Import every module in the package except the entry module and vendored
             code, and examine every function and method defined in it.
       Think about: Why must importing the entry module be avoided?
       Expected outcome: Running check does not start the CLI twice.
    2. Task: Count functions whose body raises NotImplementedError and collect their
             spec IDs, sorted by section then item.
       Expected outcome: A fresh skeleton reports every function as stubbed.
    """
    raise NotImplementedError("S8.3: build_progress")


def main(argv: list[str] | None = None) -> int:
    """Run the 'serve' or 'check' command.

    Problem piece: C6: one command to run or inspect Assay.

    Why it matters: 'serve' must use one worker because session locks live in memory
                    (A3); 'check' must never print secret values.

    What: 'serve' runs uvicorn in factory mode on create_app with one worker;
          'check' prints progress and missing configuration names.

    Spec: S8.3 | Ticket: 02 | Traces to: I9, A3

    Build steps:
    1. Task: Parse 'serve' (host, default 127.0.0.1; port, default 8000) and
             'check'.
       Expected outcome: '--help' lists both commands.
    2. Task: For 'serve', import uvicorn inside the command and run
             assay.api.app:create_app as a factory with one worker.
       Expected outcome: The server starts on the given port.
    3. Task: For 'check', print 'Build progress: <done> of <total> functions
             implemented.', the stubbed IDs, and the missing configuration names, or
             which spec to build first when settings are stubbed; return 0.
       Expected outcome: A fresh skeleton prints that S1.1 must be built first.
    """
    raise NotImplementedError("S8.3: main")
