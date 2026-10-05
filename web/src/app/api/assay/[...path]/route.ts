/**
 * Proxy REST calls to the Python service.
 *
 * Problem: Bank product managers turn vague asks into delivery work by hand, so questions
 * go unasked, answers go unrecorded, and tickets drift from what was approved. (Full
 * statement: BUILD_ORDER.md, "The problem".)
 *
 * Piece of the problem: C7 Live, standard interaction. Session lists, questionnaires,
 * downloads, and usage are plain REST. This route forwards them with the trust headers; it
 * adds no behaviour.
 *
 * Why this comes now: Forwarding (3) and identity (2) exist; the pages need these calls.
 *
 * Build order: Step 6 of 12.
 * Previous: src/app/api/copilotkit/route.ts (step 5), which serves the CopilotKit runtime.
 * Next: src/components/pause-card.tsx (step 7), which renders one pause as a card.
 *
 * Build these in order:
 *     1. GET: reads first.
 *     2. POST: then writes.
 *
 * Depends on:
 *     src/lib/config.ts: loadWebConfig.
 *     src/lib/identity.ts: signedInUser.
 *     src/lib/python-client.ts: forwardToPython.
 *     Node built-ins: none.
 *     Third-party: none.
 *
 * Depended on by:
 *     src/app/page.tsx, src/app/s/[slug]/page.tsx, src/app/q/[slug]/page.tsx: every REST
 *     call.
 *
 * Spec coverage: S10.3 | Traces to: I17
 *
 * @packageDocumentation
 */

import { loadWebConfig } from "../../../../lib/config";
import { signedInUser } from "../../../../lib/identity";
import { forwardToPython } from "../../../../lib/python-client";

/** Route parameters Next.js passes to a catch-all segment. Spec: S10.3 */
export type RouteContext = { params: Promise<{ path: string[] }> };

/**
 * Forward a GET to Python's REST API.
 *
 * Problem piece: C7: reads reach Python only through the trust boundary.
 *
 * Why it matters: Downloads and status reads carry no body, but they still need the user,
 *                 because Python attributes and authorises every call.
 *
 * What: Resolves the user (401 when missing), joins the path segments, and forwards to
 *       Python's /api with the same query string.
 *
 * Spec: S10.3 | Ticket: 13 | Traces to: I17
 *
 * Build steps:
 * 1. Task: Resolve the user (401 'Not signed in' on failure), await the path segments, join
 *          them with '/', and forward.
 *    Expected outcome: GET /api/assay/sessions reaches Python's /api/sessions.
 *
 * @param request - The incoming request.
 * @param context - The catch-all path segments.
 * @returns Python's response, or 401.
 */
export async function GET(request: Request, context: RouteContext): Promise<Response> {
  throw new Error("Not implemented: S10.3 GET");
}

/**
 * Forward a POST to Python's REST API.
 *
 * Problem piece: C7: writes reach Python only through the trust boundary.
 *
 * Why it matters: Starting sessions, replying, and submitting answers change state, so they
 *                 must carry the user exactly like reads, and their bodies must pass
 *                 through unchanged.
 *
 * What: Resolves the user (401 when missing), joins the path segments, and forwards the
 *       method and body to Python's /api.
 *
 * Spec: S10.3 | Ticket: 13 | Traces to: I17
 *
 * Build steps:
 * 1. Task: Resolve the user (401 on failure), join the path segments, and forward with the
 *          body.
 *    Expected outcome: POST /api/assay/sessions creates a session as the signed-in user.
 *
 * @param request - The incoming request.
 * @param context - The catch-all path segments.
 * @returns Python's response, or 401.
 */
export async function POST(request: Request, context: RouteContext): Promise<Response> {
  throw new Error("Not implemented: S10.3 POST");
}
