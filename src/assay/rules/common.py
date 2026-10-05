"""Hold the text rules several agents share.

Problem: Bank product managers turn vague asks into delivery work by hand, so
questions go unasked, answers go unrecorded, and tickets drift from what was
approved. (Full statement: BUILD_ORDER.md, "The problem".)

Piece of the problem: C1 Trustworthy output. Some rules apply to every agent's text:
never assert compliance, ask one question at a time, never use unverifiable words.
This file owns those checks; it never decides what happens when they fail.

Why this comes now: IDs exist (step 3). Every stage-specific rule file after this
one reuses these checks, so they come first among the rules.

Build order: Step 4 of 33.
Previous: src/assay/domain/ids.py (step 3), which assigns every log, question, DoD,
requirement, and ticket ID.
Next: src/assay/rules/intake.py (step 5), which holds the intake entry rules and the
11-item exit gate.

Build these in order:
    1. strings: the walker compliance_claims needs.
    2. compliance_claims: builds on strings.
    3. one_question: independent; used by three agents.
    4. vague_words: independent; used by the DoD rules.

Depends on:
    Nothing in this project (foundation root for the rules). Placed at step 4
    because every other rule file imports from here.
    Standard library: re.
    Third-party: pydantic.

Depended on by:
    assay.llm.agents: the agent validators. assay.graph.nodes: the stage gates.
    assay.rules.dod, prd, spec, tickets.

Spec coverage: S3.1 | Traces to: I1, I4
"""

import re

from pydantic import BaseModel

ASSERTIONS: list[str] = [  # S3.1: phrases that assert compliance
    r"\bcomplies with\b",
    r"\bcompliant with\b",
    r"\bfully compliant\b",
    r"\bconforms to\b",
    r"\bin compliance with\b",
    r"\bmeets (all )?(the )?(regulatory|legal) requirements\b",
    r"\bsatisfies (the )?(regulatory|legal)\b",
]
VAGUE: list[str] = [  # S3.1: words no one can verify
    "properly",
    "adequately",
    "fully",
    "clean",
    "appropriate",
    "appropriately",
    "where needed",
    "as required",
    "as needed",
    "sufficient",
]
GWT = re.compile(r"^Given .+?,? when .+?,? then .+", re.I | re.S)  # S3.6: criterion shape


def strings(obj: object) -> list[str]:
    """Return every piece of text inside a model, list, dict, or string.

    Problem piece: C1: text-wide checks must see every string an agent produced.

    Why it matters: A compliance claim can hide in any nested field: a risk row, a
                    requirement, a narrative paragraph. Checking only top-level text
                    would let the claim through, so every text rule first collects
                    all strings.

    What: Walks a value recursively and returns its strings in order; non-text
          values are ignored. Called as strings(obj: object) and returns list[str].

    Spec: S3.1 | Ticket: 02 | Traces to: I4

    Build steps:
    1. Task: Treat a model as its plain-data form, return a string as itself, and
             collect from every value of a mapping and every item of a list or
             tuple.
       Think about: Which kinds of values should contribute nothing?
       Expected outcome: A model holding a list of rows yields every row's text and
                         no numbers.
    """
    raise NotImplementedError("S3.1: strings")


def compliance_claims(obj: object) -> list[str]:
    """Return a problem for every text that asserts regulatory compliance.

    Problem piece: C1: only Compliance may say a regulation is met (I4).

    Why it matters: A generated PRD that says 'conforms to Reg E' reads as a finding
                    the bank relied on. If Compliance never confirmed it, that
                    sentence is a liability. The rule flags any assertion unless the
                    same text defers to Compliance with the word 'confirm'.

    What: Takes any value; returns one problem per string that matches ASSERTIONS
          without 'confirm'. Called as compliance_claims(obj: object) and returns
          list[str].

    Spec: S3.1 | Ticket: 02 | Traces to: I4

    Build steps:
    1. Task: Check every collected string against each ASSERTIONS pattern, ignoring
             case.
       Expected outcome: 'The design conforms to Reg E.' produces one problem.
    2. Task: Skip any string that contains the word 'confirm', and word each problem
             as: States compliance: '<first 100 characters>'. Rewrite it as an area
             for Compliance to confirm, with an owner.
       Think about: Why is 'confirm' the escape, rather than 'Compliance'?
       Expected outcome: 'Reg E applicability: Compliance to confirm.' produces no
                         problem.
    """
    raise NotImplementedError("S3.1: compliance_claims")


def one_question(text: str, where: str = "") -> list[str]:
    """Return a problem when text asks more than one question.

    Problem piece: C1 and C6: one question at a time, so each answer can shape the
                   next.

    Why it matters: A compound question gets a partial answer and loses the
                    dependency between its parts. Counting question marks is crude
                    but reliable for model output.

    What: Returns a problem prefixed by 'where' when the text has more than one
          question mark.

    Spec: S3.1 | Ticket: 02 | Traces to: I1

    Build steps:
    1. Task: Return 'Ask exactly one question. Keep the most foundational part.'
             prefixed by 'where' when the text has more than one question mark;
             otherwise nothing.
       Expected outcome: 'What problem? Who has it?' produces one problem.
    """
    raise NotImplementedError("S3.1: one_question")


def vague_words(text: str) -> list[str]:
    """Return the VAGUE words found in text as whole words.

    Problem piece: C1 and C6: quality checks people can verify.

    Why it matters: 'Code is clean' cannot be checked by two people and agreed.
                    Rejecting such words forces a Definition of Done item to state a
                    condition someone can test.

    What: Returns each VAGUE word that appears as a whole word, ignoring case.
          Called as vague_words(text: str) and returns list[str].

    Spec: S3.1 | Ticket: 04 | Traces to: I1

    Build steps:
    1. Task: Return the VAGUE words present as whole words, ignoring case.
       Think about: Why must 'cleanup' not match 'clean'?
       Expected outcome: 'Properly tested' yields properly; 'cleanup done' yields
                         nothing.
    """
    raise NotImplementedError("S3.1: vague_words")
