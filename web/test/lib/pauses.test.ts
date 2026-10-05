/** Tests for src/lib/pauses.ts (build step 4). Covers: S10.6. */
import { describe, it } from "vitest";
import { canApprove, cardFor, validateReply } from "../../src/lib/pauses";

describe("cardFor", () => {
  /**
   * 'approval' returns approval; 'teleport' throws.
   * Spec: S10.6 | Traces to: I18
   * Expected outcome: 'approval' returns approval; 'teleport' throws.
   */
  it.todo("cardFor step 1: 'approval' returns approval; 'teleport' throws");
});

describe("validateReply", () => {
  /**
   * An approval reply without decision yields one problem naming decision.
   * Spec: S10.6 | Traces to: I18
   * Expected outcome: An approval reply without decision yields one problem naming
   *                   decision.
   */
  it.todo(
    "validateReply step 1: An approval reply without decision yields one problem naming decision",
  );
  /**
   * A decision of 'maybe' yields one problem.
   * Spec: S10.6 | Traces to: I18
   * Expected outcome: A decision of 'maybe' yields one problem.
   */
  it.todo("validateReply step 2: A decision of 'maybe' yields one problem");
});

describe("canApprove", () => {
  /**
   * A non-approver gets false.
   * Spec: S10.6 | Traces to: I8
   * Expected outcome: A non-approver gets false.
   */
  it.todo("canApprove step 1: A non-approver gets false");
});
