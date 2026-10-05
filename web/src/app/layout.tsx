/**
 * Wrap every page in the CopilotKit provider.
 *
 * Problem: Bank product managers turn vague asks into delivery work by hand, so questions
 * go unasked, answers go unrecorded, and tickets drift from what was approved. (Full
 * statement: BUILD_ORDER.md, "The problem".)
 *
 * Piece of the problem: C7 Live, standard interaction. Every page shares one CopilotKit
 * connection to /api/copilotkit. This layout owns that provider and the page shell.
 *
 * Why this comes now: The runtime route (5) exists at the URL this provider uses.
 *
 * Build order: Step 9 of 12.
 * Previous: src/components/stage-progress.tsx (step 8), which shows stage and step
 * progress.
 * Next: src/app/page.tsx (step 10), which lists and starts sessions.
 *
 * Build these in order:
 *     1. RootLayout: the only component.
 *
 * Depends on:
 *     Nothing beyond third-party (it references the runtime by URL, not by import).
 *     Node built-ins: none.
 *     Third-party: react, @copilotkit/react-core.
 *
 * Depended on by:
 *     Every page under src/app.
 *
 * Spec coverage: S10.5 | Traces to: I17
 *
 * @packageDocumentation
 */

import { CopilotKit } from "@copilotkit/react-core/v2";
import "@copilotkit/react-core/v2/styles.css";
import type { ReactNode } from "react";

/** Props Next.js passes to the root layout. Spec: S10.5 */
export type RootLayoutProps = { children: ReactNode };

/**
 * Render the page shell inside the CopilotKit provider.
 *
 * Problem piece: C7: one agent connection for the whole app.
 *
 * Why it matters: Hooks only work inside the provider, and one provider means one
 *                 connection and one place to set the runtime URL. Pointing it at the
 *                 same-origin route keeps every call behind the trust boundary.
 *
 * What: An html element with lang en and a body containing the CopilotKit provider,
 *       configured with runtime URL /api/copilotkit, around the page.
 *
 * Spec: S10.5 | Ticket: 14 | Traces to: I17
 *
 * Build steps:
 * 1. Task: Render html (lang en) and body, with the CopilotKit provider using runtime URL
 *          /api/copilotkit around the children.
 *    Think about: Why a same-origin path rather than Python's address?
 *    Expected outcome: Every page can use CopilotKit's hooks.
 *
 * @param props - The page to wrap.
 * @returns The document shell.
 */
export default function RootLayout(props: RootLayoutProps): ReactNode {
  throw new Error("Not implemented: S10.5 RootLayout");
}
