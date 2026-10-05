/** Tests for src/lib/identity.ts (build step 2). Covers: S10.2. */
import { describe, it } from "vitest";
import { signedInUser } from "../../src/lib/identity";

describe("signedInUser", () => {
  /**
   * A request without the header and without a development user is refused.
   * Spec: S10.2 | Traces to: I17, A4
   * Expected outcome: A request without the header and without a development user is
   *                   refused.
   */
  it.todo(
    "signedInUser step 1: A request without the header and without a development user is refused",
  );
});
