"""Run the command line with 'python -m assay'.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C6 People decide. The entry point. It holds one line of glue
and nothing else.

Why this comes now: The CLI (32) exists.

Build order: Step 33 of 33.
Previous: src/assay/cli.py (step 32), which provides the command line.
Next: none. This is the final step; the project is complete when its tests pass.

Build these in order:

Depends on:
    assay.cli: main. The command line.
    Standard library: none.
    Third-party: none.

Depended on by:
    nothing in this project; this is the entry point.

Spec coverage: — | Traces to: I9

Build steps:
1. Task: Run main and exit with its return code when executed as a module.
   Expected outcome: 'python -m assay --help' prints both commands.
"""

from assay.cli import main

if __name__ == "__main__":
    raise SystemExit(main())
