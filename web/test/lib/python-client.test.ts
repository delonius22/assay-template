/** Tests for src/lib/python-client.ts (build step 3). Covers: S10.1, S10.3. */
import { describe, it } from "vitest";
import { forwardToPython, serviceHeaders } from "../../src/lib/python-client";

describe("serviceHeaders", () => {
  /**
   * The result has exactly those two keys.
   * Spec: S10.1, S10.3 | Traces to: I17
   * Expected outcome: The result has exactly those two keys.
   */
  it.todo("serviceHeaders step 1: The result has exactly those two keys");
});

describe("forwardToPython", () => {
  /**
   * A request for sessions?x=1 goes to /api/sessions?x=1.
   * Spec: S10.3 | Traces to: I17
   * Expected outcome: A request for sessions?x=1 goes to /api/sessions?x=1.
   */
  it.todo("forwardToPython step 1: A request for sessions?x=1 goes to /api/sessions?x=1");
  /**
   * A browser-sent X-Forwarded-User never reaches Python.
   * Spec: S10.3 | Traces to: I17
   * Expected outcome: A browser-sent X-Forwarded-User never reaches Python.
   */
  it.todo("forwardToPython step 2: A browser-sent X-Forwarded-User never reaches Python");
  /**
   * A 403 from Python reaches the browser as 403.
   * Spec: S10.3 | Traces to: I17
   * Expected outcome: A 403 from Python reaches the browser as 403.
   */
  it.todo("forwardToPython step 3: A 403 from Python reaches the browser as 403");
});
