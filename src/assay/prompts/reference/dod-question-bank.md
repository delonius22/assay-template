# DoD question bank

Walk these categories in order. For each, ask one question at a time and
give the recommended answer shown. Adapt the wording to the team. The
recommended level is in brackets.

## 1. Code and review

- Who must approve a change before merge, and may the author approve
  their own? *Recommend: at least one reviewer who is not the author.*
  [Ticket]
- Must the build pass on the merge commit? *Recommend: yes, enforced by
  branch protection.* [Ticket]
- Which static-analysis or lint checks must pass? *Recommend: no new
  findings rated high or above.* [Ticket]

## 2. Testing

- At what level must acceptance criteria be tested? *Recommend: every
  criterion covered by an automated test at the seam named in the spec.*
  [Ticket]
- Must existing regression tests pass? *Recommend: yes, full suite green.*
  [Ticket]
- Who runs user acceptance testing, and when? *Recommend: business owner
  signs UAT once per feature.* [Feature]
- Are performance or load tests needed? *Recommend: only where the spec
  sets a performance target; run once per feature.* [Feature]

## 3. Security

- Which security scans must run, and what blocks a merge? *Recommend:
  dependency and code scans; no new critical or high findings.* [Ticket]
- Are secrets ever allowed in code or configuration? *Recommend: never;
  enforced by a secret scanner.* [Ticket]
- When is a security review or penetration test required? *Recommend:
  once per feature that adds an external interface or new data flow.*
  [Feature]

## 4. Data and privacy

- Can production data be used in development or test environments?
  *Recommend: no; synthetic or masked data only.* [Ticket]
- Must logs be checked for sensitive data? *Recommend: yes; no account
  numbers, personal data, or credentials in logs.* [Ticket]
- Who confirms data classification and retention are implemented as
  specified? *Recommend: data owner, once per feature.* [Feature]

## 5. Audit and controls

- When a story changes customer data, money, or settings, must audit
  events be verified? *Recommend: yes, verified in a test environment.*
  [Ticket]
- If a feature changes an existing control, who signs off? *Recommend:
  the control owner, once per feature.* [Feature]
- Where is evidence kept so an auditor can find it? *Recommend: linked
  from the Jira issue.* [Ticket]

## 6. Accessibility

- What standard applies to customer and staff interfaces? *Recommend: the
  bank's accessibility standard; confirm the WCAG level with the
  accessibility team.* [Ticket, for tickets that change an interface]
- Is assistive-technology testing required? *Recommend: once per feature
  with a new or changed journey.* [Feature]

## 7. Operations and observability

- Must monitoring and alerts be updated when behaviour changes?
  *Recommend: yes.* [Ticket]
- Must the runbook be updated? *Recommend: yes, before release.* [Feature]
- Must a feature flag and rollback path be tested? *Recommend: yes, where
  the spec requires a flag.* [Feature]

## 8. Documentation

- What documentation must change? *Recommend: user-facing help and
  internal procedures, once per feature; ADR when the spec calls for one.*
  [Feature]

## 9. Change management and release

- What approvals are needed to release (change advisory board, release
  manager)? *Recommend: per the bank's change policy; ask who owns it.*
  [Release]
- Must a rollback be rehearsed before production? *Recommend: yes, for
  releases with data migration.* [Release]

## 10. Acceptance and sign-off

- Who accepts a ticket as done? *Recommend: the product owner, against its
  acceptance criteria.* [Ticket]
- Who accepts a feature as done? *Recommend: business owner, after UAT and
  all feature-level items.* [Feature]

## 11. Story level

- Who confirms a story's business goal is met once all its features are
  done? *Recommend: the business owner, against the story's success
  measure.* [Story]
