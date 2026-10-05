/**
 * Read the web service's configuration once.
 *
 * Problem: Bank product managers turn vague asks into delivery work by hand, so questions
 * go unasked, answers go unrecorded, and tickets drift from what was approved. (Full
 * statement: BUILD_ORDER.md, "The problem".)
 *
 * Piece of the problem: C7 Live, standard interaction. The Node service must know where
 * Python is, the token that proves calls come from it, and which header carries the user.
 * This file owns that shape and how it is read; it never calls anything.
 *
 * Why this comes now: Nothing depends on anything earlier, and every route reads this
 * configuration.
 *
 * Build order: Step 1 of 12.
 * Previous: none. This is the start of the project.
 * Next: src/lib/identity.ts (step 2), which reads the signed-in user.
 *
 * Build these in order:
 *     1. loadWebConfig: the only function.
 *
 * Depends on:
 *     Nothing in this project. This module is the start of the project. Build it first.
 *     Node built-ins: none.
 *     Third-party: none.
 *
 * Depended on by:
 *     src/lib/identity.ts, src/lib/python-client.ts, both API routes: every setting.
 *
 * Spec coverage: S10.1, S10.2 | Traces to: I17, A4
 *
 * @packageDocumentation
 */

/**
 * Everything the web service is configured with.
 *
 * Problem piece: C7. Where Python lives and how calls are trusted.
 * Why it matters: Reading environment variables in many places invites one route to disagree with another.
 * What: Python base URL, service token, SSO user header name, and an optional development user.
 * Spec: S10.1, S10.2 | Ticket: 13 | Traces to: I17
 */
export type WebConfig = {
  pythonUrl: string;
  serviceToken: string;
  userHeader: string;
  devUser: string;
};

/**
 * Return the web configuration from environment variables.
 *
 * Problem piece: C7: one trusted configuration for every route.
 *
 * Why it matters: The service token is what lets Python trust this service (I17); a missing
 *                 token must stop the service at startup rather than let it run and fail on
 *                 every call. Taking the environment as a parameter keeps the function
 *                 testable.
 *
 * What: Reads ASSAY_PYTHON_URL, ASSAY_SERVICE_TOKEN, ASSAY_USER_HEADER (default
 *       x-forwarded-user), and ASSAY_DEV_USER; refuses a missing URL or token.
 *
 * Spec: S10.1, S10.2 | Ticket: 13 | Traces to: I17
 *
 * Build steps:
 * 1. Task: Read the four variables, defaulting the user header to x-forwarded-user and the
 *          development user to empty.
 *    Expected outcome: With only URL and token set, the user header is x-forwarded-user.
 * 2. Task: Refuse a missing ASSAY_PYTHON_URL or ASSAY_SERVICE_TOKEN with an error that
 *          names the variable.
 *    Think about: Why must the message name the variable but never print the token?
 *    Expected outcome: A missing token throws an error naming ASSAY_SERVICE_TOKEN.
 *
 * @param env - The environment, usually the process environment.
 * @returns The validated configuration.
 * @throws An error naming the missing variable, never its value.
 */
export function loadWebConfig(env: Record<string, string | undefined>): WebConfig {
  throw new Error("Not implemented: S10.1 loadWebConfig");
}
