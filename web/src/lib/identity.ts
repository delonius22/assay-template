/**
 * Read the signed-in user from the SSO proxy's header.
 *
 * Problem: Bank product managers turn vague asks into delivery work by hand, so questions
 * go unasked, answers go unrecorded, and tickets drift from what was approved. (Full
 * statement: BUILD_ORDER.md, "The problem".)
 *
 * Piece of the problem: C6 People decide. Every action is attributed to a person. This file
 * decides who that is; it never trusts a header the browser could set.
 *
 * Why this comes now: Configuration (step 1) names the header; every route needs the user
 * before forwarding anything.
 *
 * Build order: Step 2 of 12.
 * Previous: src/lib/config.ts (step 1), which reads the web service's configuration.
 * Next: src/lib/python-client.ts (step 3), which forwards calls to the Python service.
 *
 * Build these in order:
 *     1. signedInUser: the only function.
 *
 * Depends on:
 *     src/lib/config.ts: WebConfig. The header name and development user.
 *     Node built-ins: none.
 *     Third-party: none.
 *
 * Depended on by:
 *     Both API routes: the user forwarded to Python.
 *
 * Spec coverage: S10.2 | Traces to: I17, A4
 *
 * @packageDocumentation
 */

import type { WebConfig } from "./config";

/**
 * Return the signed-in user's ID, or refuse.
 *
 * Problem piece: C6: no anonymous answers or approvals.
 *
 * Why it matters: The SSO proxy strips and sets its header on every request (A4), so that
 *                 header is the only identity source to trust. Falling back to the
 *                 development user only when configured keeps local runs working without
 *                 opening a hole in production.
 *
 * What: Returns the trimmed value of the configured header, else the development user, else
 *       throws.
 *
 * Spec: S10.2 | Ticket: 13 | Traces to: I17, A4
 *
 * Build steps:
 * 1. Task: Read the configured header, trim it, and fall back to the development user;
 *          refuse with 'Not signed in' when both are empty.
 *    Think about: What would happen if a deployment set ASSAY_DEV_USER in production?
 *    Expected outcome: A request without the header and without a development user is
 *                      refused.
 *
 * @param headers - The incoming request's headers.
 * @param config - The web configuration.
 * @returns The user ID.
 * @throws An error 'Not signed in' when neither source gives a user.
 */
export function signedInUser(headers: Headers, config: WebConfig): string {
  throw new Error("Not implemented: S10.2 signedInUser");
}
