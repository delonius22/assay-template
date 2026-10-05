/** Tests for src/lib/config.ts (build step 1). Covers: S10.1, S10.2. */
import { describe, it } from "vitest";
import { loadWebConfig } from "../../src/lib/config";

describe("loadWebConfig", () => {
  /**
   * With only URL and token set, the user header is x-forwarded-user.
   * Spec: S10.1, S10.2 | Traces to: I17
   * Expected outcome: With only URL and token set, the user header is x-forwarded-user.
   */
  it.todo("loadWebConfig step 1: With only URL and token set, the user header is x-forwarded-user");
  /**
   * A missing token throws an error naming ASSAY_SERVICE_TOKEN.
   * Spec: S10.1, S10.2 | Traces to: I17
   * Expected outcome: A missing token throws an error naming ASSAY_SERVICE_TOKEN.
   */
  it.todo("loadWebConfig step 2: A missing token throws an error naming ASSAY_SERVICE_TOKEN");
});
