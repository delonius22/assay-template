/**
 * Serve the CopilotKit runtime, with Assay registered as an AG-UI agent.
 *
 * Problem: Bank product managers turn vague asks into delivery work by hand, so questions
 * go unasked, answers go unrecorded, and tickets drift from what was approved. (Full
 * statement: BUILD_ORDER.md, "The problem".)
 *
 * Piece of the problem: C7 Live, standard interaction. CopilotKit's React hooks talk to
 * this runtime; the runtime talks to Python over AG-UI. This file owns that bridge and adds
 * the trust headers (ADR 0001).
 *
 * Why this comes now: Configuration (1), identity (2), and the service headers (3) exist.
 *
 * Build order: Step 5 of 12.
 * Previous: src/lib/pauses.ts (step 4), which maps pauses to cards and checks replies.
 * Next: src/app/api/assay/[...path]/route.ts (step 6), which proxies REST calls to Python.
 *
 * Build these in order:
 *     1. createRuntime: the helper the route uses.
 *     2. POST: the route itself.
 *
 * Depends on:
 *     src/lib/config.ts: loadWebConfig, WebConfig.
 *     src/lib/identity.ts: signedInUser.
 *     src/lib/python-client.ts: serviceHeaders.
 *     Node built-ins: none.
 *     Third-party: @copilotkit/runtime, @ag-ui/client.
 *
 * Depended on by:
 *     src/app/layout.tsx: the runtime URL /api/copilotkit.
 *
 * Spec coverage: S10.1, S10.2 | Traces to: I17, A4
 *
 * @packageDocumentation
 */

import { HttpAgent } from "@ag-ui/client";
import {
  CopilotRuntime,
  copilotRuntimeNextJSAppRouterEndpoint,
  ExperimentalEmptyAdapter,
} from "@copilotkit/runtime";
import { loadWebConfig, type WebConfig } from "../../../lib/config";
import { signedInUser } from "../../../lib/identity";
import { serviceHeaders } from "../../../lib/python-client";

/**
 * Return a CopilotKit runtime with Assay registered as an AG-UI agent for one user.
 *
 * Problem piece: C7: the agent CopilotKit's hooks connect to.
 *
 * Why it matters: The agent must call Python's /agui endpoint with the service token and
 *                 this request's user. Building the runtime per request is what lets each
 *                 call carry the right user; a shared runtime would carry whoever came
 *                 first.
 *
 * What: A runtime whose single agent, named 'assay', is an AG-UI HTTP agent pointed at the
 *       Python URL plus /agui, with the service headers for this user.
 *
 * Spec: S10.1 | Ticket: 13 | Traces to: I17
 *
 * Build steps:
 * 1. Task: Create an AG-UI HTTP agent for the Python URL plus '/agui' carrying the service
 *          headers for this user.
 *    Think about: Why must the headers be built per request?
 *    Expected outcome: The agent's requests carry X-Assay-Service-Token.
 * 2. Task: Create a runtime whose agents map has that agent under the name 'assay'.
 *    Expected outcome: The React side can address the agent as 'assay'.
 *
 * @param config - The web configuration.
 * @param user - The signed-in user.
 * @returns The configured runtime.
 */
export function createRuntime(config: WebConfig, user: string): CopilotRuntime {
  throw new Error("Not implemented: S10.1 createRuntime");
}

/**
 * Handle one CopilotKit request.
 *
 * Problem piece: C7: every hook call reaches Python as the signed-in user.
 *
 * Why it matters: This route is the only door between browsers and the agent. Resolving the
 *                 user from the SSO header before creating the runtime guarantees no
 *                 request is forwarded anonymously.
 *
 * What: Loads configuration, resolves the user (401 when not signed in), and serves the
 *       request through CopilotKit's Next.js App Router endpoint with an empty service
 *       adapter, at /api/copilotkit.
 *
 * Spec: S10.1, S10.2 | Ticket: 13 | Traces to: I17, A4
 *
 * Build steps:
 * 1. Task: Load the configuration from the process environment and resolve the user,
 *          answering 401 'Not signed in' on failure.
 *    Expected outcome: A request without the SSO header gets 401.
 * 2. Task: Serve the request through CopilotKit's App Router endpoint helper with the
 *          runtime for this user, an empty service adapter (the agent does its own model
 *          calls), and the endpoint path /api/copilotkit.
 *    Think about: Why does this runtime need no model adapter of its own?
 *    Expected outcome: A hook request reaches Python's /agui as the signed-in user.
 *
 * @param request - The incoming request.
 * @returns The runtime's response, or 401.
 */
export async function POST(request: Request): Promise<Response> {
  throw new Error("Not implemented: S10.1 POST");
}
