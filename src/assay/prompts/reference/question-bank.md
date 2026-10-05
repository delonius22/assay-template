# Question bank

Use this as a coverage checklist, not a script. Pick the questions that
matter for this initiative, rephrase them in its own terms, and always add
a recommended answer. Owner shows who normally answers.

## 1. Problem and need — owner: PM / Business

- What problem does this solve, and for whom? How do we know it is real
  (complaints, incident counts, audit finding, lost revenue)?
- What happens if we do nothing for twelve months?
- Is the stated need actually a solution in disguise? What is the
  underlying problem?

## 2. Outcome and success — owner: PM / Business

- What will be measurably different when this is done?
- What is the baseline today, and what is the target?
- Who signs off that the outcome was achieved?

## 3. Users and parties — owner: PM, with Operations

- Which customer segments are affected (retail, small business, commercial,
  wealth)? Any vulnerable-customer considerations?
- Which staff roles use or support it (branch, contact centre, operations,
  fraud, collections)?
- Which third parties or vendors are involved?

## 4. Scope — owner: PM

- What is explicitly out of scope?
- What is deferred to a later phase, and why?
- Which channels: mobile, web, branch, contact centre, API partners?

## 5. Journeys — owner: PM with Developer

- Walk the main journey step by step. What does the user see and do?
- At each step, what can fail, and what happens then?
- What happens on timeout, duplicate submission, or partial completion?
- What does the customer see when the system is down?

## 6. Data — owner: Data, Developer

- What data is created, read, changed, or deleted?
- Does it include personal, financial, or authentication data? What is the
  bank's classification for it?
- Where is the system of record? Will data be copied anywhere new?
- How long must it be retained, and how is it deleted?
- Does data leave the bank (vendor, cloud region, partner)?

## 7. Integrations — owner: Architecture, Developer

- Which internal systems does this call or feed (core banking, card
  processor, general ledger, CRM, data warehouse)?
- Which external services? What are their availability and contract terms?
- What happens when a dependency is slow or down?
- Are there batch cut-off times or settlement windows to respect?

## 8. Non-functional needs — owner: Architecture, Operations, Security

- Availability target and support hours. Is this customer-facing 24/7?
- Expected volume now and at peak (month-end, payday, holidays).
- Response-time expectations users will notice.
- Authentication and authorisation: who may do what? Is step-up
  authentication or dual approval (maker-checker) needed?
- What must be written to an audit trail, and who reviews it?
- Accessibility standard required for customer and staff interfaces.
- Disaster recovery: recovery time and recovery point expectations.

## 9. Risk, control, and regulation — owner: Compliance, Risk, InfoSec

Agents flag areas; they never conclude. Each flagged area gets an owner and
a `Q-` entry marked "Compliance to confirm".

- Does this change a customer disclosure, fee, rate, or term?
- Does it affect money movement, payments, or account balances?
- Does it involve credit decisions, eligibility, or pricing by customer?
- Does it touch identity verification, fraud, or anti-money-laundering
  monitoring?
- Does it change an existing control, reconciliation, or approval step?
- Does it introduce a new vendor or move data to a new location?
- Does it use a model or automated decision that affects customers?

Example regulatory areas a US bank's Compliance team may consider, as
prompts only: consumer privacy (GLBA), electronic fund transfers (Reg E),
fair lending (ECOA / Reg B), unfair or deceptive practices (UDAAP), BSA/AML,
card data (PCI DSS, an industry standard), and accessibility. Applicability
depends on jurisdiction, product, and charter. Never state that any of
these applies or is satisfied.

## 10. Rollout — owner: PM, Operations, Developer

- Pilot group or big-bang? Who goes first?
- Feature flag, and who controls it?
- Rollback plan and the trigger for using it.
- Staff training, procedures, and customer communication needed.
- Support model after launch: who is on call?

## 11. Delivery risk — owner: PM, Developer

- What are we least sure about technically? Can we spike it early?
- What external approvals could block release (architecture board, change
  advisory board, security review, vendor due diligence)?
- Fixed dates and why they are fixed.
