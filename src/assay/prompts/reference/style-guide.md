# PRD style guide

The reader is a business owner, a risk or compliance reviewer, or an
executive. They are expert in banking and short on time. Write for them.

## Language

- **Plain words.** Prefer "send", "check", "store", "show" over
  "dispatch", "validate", "persist", "render".
- **Short sentences.** Aim for 25 words or fewer. One idea per sentence.
- **Active voice.** "The system sends an alert," not "An alert is sent."
- **Name the actor.** Say who does each thing: the customer, the
  contact-centre agent, the system.
- **Glossary terms only.** Use the canonical terms from `CONTEXT.md`. If a
  technical term is unavoidable, define it in the glossary in one plain
  sentence.
- **No code, no schemas, no endpoint or table names, no library names.**
  These go in the spec.
- **No hype.** Do not write "seamless", "robust", "cutting-edge",
  "world-class", or "best-in-class". State what the thing does.

## Requirement wording

| Word | Meaning |
|---|---|
| **must** | Mandatory. Release cannot proceed without it. |
| **should** | Expected. Omitting it needs a recorded reason. |
| **may** | Optional. |

Priority uses MoSCoW: Must have, Should have, Could have, Won't have (this
release). "Won't have" items also appear in Out of scope.

Each requirement must be testable. "The alert should be fast" fails.
"The customer must receive the alert within two minutes of the balance
falling below their threshold, in 99% of cases" passes.

## Evidence and certainty

- Cite source IDs in the **Source** column of every requirement table and
  in the traceability appendix. Keep IDs out of narrative prose.
- Label assumptions as assumptions. Never present a suspected cause or an
  estimate as a fact.
- For regulation, write "Compliance to confirm" unless the session log
  shows a named person confirmed it.

## Layout

- Lead each section with the point, then the detail.
- Use tables for requirements, risks, stakeholders, and measures.
- Use bullets for short parallel items; use prose for reasoning.
- Keep the executive summary to one page: problem, outcome, scope,
  cost of delay, decisions needed.
