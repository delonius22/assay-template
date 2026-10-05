/**
 * List sessions and start a new one.
 *
 * Problem: Bank product managers turn vague asks into delivery work by hand, so questions
 * go unasked, answers go unrecorded, and tickets drift from what was approved. (Full
 * statement: BUILD_ORDER.md, "The problem".)
 *
 * Piece of the problem: C6 People decide. A PM starts here. This page lists sessions and
 * starts new ones through the REST proxy.
 *
 * Why this comes now: The REST proxy (6) and layout (9) exist.
 *
 * Build order: Step 10 of 12.
 * Previous: src/app/layout.tsx (step 9), which wraps every page in the CopilotKit provider.
 * Next: src/app/s/[slug]/page.tsx (step 11), which runs one session live.
 *
 * Build these in order:
 *     1. SessionsPage: the only component.
 *
 * Depends on:
 *     Nothing in this project by import; it calls the REST proxy route by URL.
 *     Node built-ins: none.
 *     Third-party: react, next.
 *
 * Depended on by:
 *     nothing in this project; it is a route Next.js serves at /.
 *
 * Spec coverage: S10.4 | Traces to: I12
 *
 * @packageDocumentation
 */
"use client";

import Link from "next/link";
import { type ReactNode, useEffect, useState } from "react";

/**
 * Render the session list and the new-session form.
 *
 * Problem piece: C6: a PM finds their sessions and starts new ones.
 *
 * Why it matters: Starting a session needs the right inputs for the mode, especially the
 *                 brief for mode 3, and the server's validation messages must reach the PM
 *                 verbatim so they can fix them.
 *
 * What: Lists sessions from /api/assay/sessions with title, stage, and status, linking each
 *       to /s/<slug>; a form takes title, slug, mode, and for mode 3 the ask, why, and
 *       outcome, then posts to /api/assay/sessions and opens the new session.
 *
 * Spec: S10.4 | Ticket: 14 | Traces to: I12
 *
 * Build steps:
 * 1. Task: Load the sessions and show each with its title, stage, and status, linking to
 *          its session page.
 *    Expected outcome: A new session appears at the top of the list.
 * 2. Task: Offer a form for title, slug (3 to 40 lowercase letters, digits, or hyphens),
 *          and mode, showing the brief fields only for mode 3.
 *    Expected outcome: Choosing mode 3 shows ask, why, and outcome.
 * 3. Task: Post the form, show Python's error message on refusal, and open the session on
 *          success.
 *    Expected outcome: A duplicate slug shows the server's 409 message.
 *
 * @returns The page.
 */
export default function SessionsPage(): ReactNode {
  throw new Error("Not implemented: S10.4 SessionsPage");
}
