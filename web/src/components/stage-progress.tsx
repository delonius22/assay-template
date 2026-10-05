/**
 * Show a session's stage and its steps as they happen.
 *
 * Problem: Bank product managers turn vague asks into delivery work by hand, so questions
 * go unasked, answers go unrecorded, and tickets drift from what was approved. (Full
 * statement: BUILD_ORDER.md, "The problem".)
 *
 * Piece of the problem: C7 Live, standard interaction. People should see Assay working
 * without refreshing. This component shows the stage from state snapshots and the running
 * step from step events.
 *
 * Why this comes now: It needs nothing beyond the session view's shape; the session page
 * (11) feeds it.
 *
 * Build order: Step 8 of 12.
 * Previous: src/components/pause-card.tsx (step 7), which renders one pause as a card.
 * Next: src/app/layout.tsx (step 9), which wraps every page in the CopilotKit provider.
 *
 * Build these in order:
 *     1. StageProgress: the only component.
 *
 * Depends on:
 *     Nothing in this project (foundation root). Placed at step 8 because the session page
 *     shows it.
 *     Node built-ins: none.
 *     Third-party: react.
 *
 * Depended on by:
 *     src/app/s/[slug]/page.tsx: progress above the cards.
 *
 * Spec coverage: S10.5 | Traces to: I7
 *
 * @packageDocumentation
 */
"use client";

import type { ReactNode } from "react";

/** The session view Python sends in state snapshots (SPECS data shapes). Spec: S10.5 */
export type SessionView = {
  slug: string;
  title: string;
  mode: number;
  pm: string;
  stage: string;
  files: string[];
  agenda: string[];
  q_round: number;
};

/** Props for StageProgress. Spec: S10.5 */
export type StageProgressProps = { view: SessionView | null; runningStep: string | null };

/**
 * Render the stage list, the running step, and the downloads.
 *
 * Problem piece: C7: progress without polling.
 *
 * Why it matters: A two-minute PRD step with no visible progress looks like a hang, and
 *                 people refresh or give up. Showing the stage, the running step, and files
 *                 as they arrive keeps trust.
 *
 * What: Shows the five stages with the current one marked, the running step's name while a
 *       run is active, the agenda items, and a download link per file through the REST
 *       proxy.
 *
 * Spec: S10.5 | Ticket: 14 | Traces to: I7
 *
 * Build steps:
 * 1. Task: Show the stages Intake, Definition of Done, PRD, Spec, and Tickets, marking the
 *          current one; treat 'PRD review' as PRD and 'Done' as all complete.
 *    Expected outcome: Stage 'PRD review' marks PRD as current.
 * 2. Task: While a step runs, show its name in plain words; list agenda items as the gaps
 *          being worked on.
 *    Expected outcome: A running grill_think step shows as 'Asking the next question'.
 * 3. Task: Link each file through /api/assay/sessions/<slug>/files/<name>.
 *    Think about: Why must links go through the proxy, never straight to Python?
 *    Expected outcome: prd.pdf links through the proxy.
 *
 * @param props - The latest session view and the running step, if any.
 * @returns The progress panel.
 */
export function StageProgress(props: StageProgressProps): ReactNode {
  throw new Error("Not implemented: S10.5 StageProgress");
}
