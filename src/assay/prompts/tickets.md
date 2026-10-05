# Task: cut tickets for every feature

The PRD's stories and features are fixed. Produce the tickets that build
them, as one list in BUILD ORDER.

- Vertical slices: each ticket delivers behaviour a tester can see end to end.
  "Create the table" is not a ticket; "Customer saves a threshold" is.
- The first ticket is the thinnest end-to-end path (a tracer bullet).
- Riskiest work early. Add a spike (with a question and a timebox) before
  any ticket that cannot be estimated.
- Enablers only when unavoidable, and each names the later tickets it unblocks.
- depends_on may point only to EARLIER tickets in the list.
- Sizes XS, S, or M. Split anything larger.
- Three to seven Given/When/Then acceptance criteria per ticket, covering
  failure paths, permissions, and audit where relevant.
- Trace every ticket to FR-/NFR- IDs and the spec sections it builds on.
- Every FR- and NFR- ID must be covered by a ticket, or listed in uncovered with a reason.
- If reviewer feedback is given, address every point and return the complete revised plan.
