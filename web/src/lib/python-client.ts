/**
 * Forward calls to the Python service with the service token and the user.
 *
 * Problem: Bank product managers turn vague asks into delivery work by hand, so questions
 * go unasked, answers go unrecorded, and tickets drift from what was approved. (Full
 * statement: BUILD_ORDER.md, "The problem".)
 *
 * Piece of the problem: C7 Live, standard interaction. Browsers never reach Python (I17).
 * This file is the one place that adds the trust headers and forwards; it never decides
 * what to call.
 *
 * Why this comes now: Configuration (1) and identity (2) exist; both routes forward through
 * this.
 *
 * Build order: Step 3 of 12.
 * Previous: src/lib/identity.ts (step 2), which reads the signed-in user.
 * Next: src/lib/pauses.ts (step 4), which maps pauses to cards and checks replies.
 *
 * Build these in order:
 *     1. serviceHeaders: used by both forwarding paths.
 *     2. forwardToPython: the REST path.
 *
 * Depends on:
 *     src/lib/config.ts: WebConfig. URL and token.
 *     Node built-ins: none.
 *     Third-party: none.
 *
 * Depended on by:
 *     src/app/api/copilotkit/route.ts: headers for the AG-UI agent.
 *     src/app/api/assay/[...path]/route.ts: REST forwarding.
 *
 * Spec coverage: S10.1, S10.3 | Traces to: I17
 *
 * @packageDocumentation
 */

import type { WebConfig } from "./config";

/**
 * Return the headers that prove a call comes from this service and name the user.
 *
 * Problem piece: C7: Python can trust the user only on calls from here.
 *
 * Why it matters: Python accepts a user header only alongside the shared token (S9.6);
 *                 building both in one function means no route can forget one of them.
 *
 * What: X-Assay-Service-Token set to the configured token and X-Forwarded-User set to the
 *       user.
 *
 * Spec: S10.1, S10.3 | Ticket: 13 | Traces to: I17
 *
 * Build steps:
 * 1. Task: Return exactly two headers: X-Assay-Service-Token with the token and
 *          X-Forwarded-User with the user.
 *    Expected outcome: The result has exactly those two keys.
 *
 * @param user - The signed-in user.
 * @param config - The web configuration.
 * @returns The two headers.
 */
export function serviceHeaders(user: string, config: WebConfig): Record<string, string> {
  throw new Error("Not implemented: S10.1 serviceHeaders");
}

/**
 * Forward one REST call to Python and return its response unchanged.
 *
 * Problem piece: C7: the browser reaches Python's REST API only through here.
 *
 * Why it matters: Copying the browser's headers would forward any user header a browser
 *                 chose to send, which is exactly the impersonation I17 forbids. Only the
 *                 method, the body, the content type, and the trust headers may cross.
 *
 * What: Sends the same method and body to the Python URL plus path, with the content type
 *       and service headers only, and returns Python's status, body, and content type.
 *
 * Spec: S10.3 | Ticket: 13 | Traces to: I17
 *
 * Build steps:
 * 1. Task: Build the target address from the Python URL, '/api/', the path, and the
 *          original query string.
 *    Expected outcome: A request for sessions?x=1 goes to /api/sessions?x=1.
 * 2. Task: Send the same method and, for methods with a body, the same body, carrying only
 *          the content type and the service headers.
 *    Think about: Which incoming headers must never be copied, and why?
 *    Expected outcome: A browser-sent X-Forwarded-User never reaches Python.
 * 3. Task: Return Python's status, body, and content type unchanged so downloads and errors
 *          pass through.
 *    Expected outcome: A 403 from Python reaches the browser as 403.
 *
 * @param request - The browser's request.
 * @param path - The path under Python's /api, such as sessions/alerts.
 * @param user - The signed-in user.
 * @param config - The web configuration.
 * @returns Python's response, status preserved.
 */
export async function forwardToPython(
  request: Request,
  path: string,
  user: string,
  config: WebConfig,
): Promise<Response> {
  throw new Error("Not implemented: S10.3 forwardToPython");
}
