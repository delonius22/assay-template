/**
 * Run one session live: progress, and a card for each pause.
 *
 * Problem: Bank product managers turn vague asks into delivery work by hand, so questions
 * go unasked, answers go unrecorded, and tickets drift from what was approved. (Full
 * statement: BUILD_ORDER.md, "The problem".)
 *
 * Piece of the problem: C7 Live, standard interaction. This is where a PM works through a
 * session. The page connects the 'assay' agent for this session's thread, shows progress,
 * and renders each interrupt as a card.
 *
 * Why this comes now: Pause cards (7), progress (8), and the provider (9) exist.
 *
 * Build order: Step 11 of 12.
 * Previous: src/app/page.tsx (step 10), which lists and starts sessions.
 * Next: src/app/q/[slug]/page.tsx (step 12), which lets a developer answer the
 * questionnaire.
 *
 * Build these in order:
 *     1. SessionPage: the only component.
 *
 * Depends on:
 *     src/components/pause-card.tsx: PauseCard.
 *     src/components/stage-progress.tsx: StageProgress, SessionView.
 *     Node built-ins: none.
 *     Third-party: react, @copilotkit/react-core.
 *
 * Depended on by:
 *     nothing in this project; it is a route Next.js serves at /s/<slug>.
 *
 * Spec coverage: S10.5, S10.6 | Traces to: I7, I8, I18
 *
 * @packageDocumentation
 */
"use client";

import { useAgent, useInterrupt } from "@copilotkit/react-core/v2";
import { type ReactNode, useEffect, useState } from "react";
import { PauseCard } from "../../../components/pause-card";
import { type SessionView, StageProgress } from "../../../components/stage-progress";

/** Props Next.js passes to a dynamic route. Spec: S10.5 */
export type SessionPageProps = { params: Promise<{ slug: string }> };

/**
 * Connect to the session's thread and render progress and pause cards.
 *
 * Problem piece: C7: steps and pauses appear the moment they happen.
 *
 * Why it matters: The session runs on the server whether or not this tab is open (S8.2);
 *                 the page only attaches. Using the slug as the thread ID means reopening
 *                 the page re-attaches, and the server re-sends the open interrupt (S9.4).
 *
 * What: Uses the 'assay' agent with the slug as thread ID, keeps the latest session view
 *       from state snapshots and the running step from step events, loads the profile from
 *       /api/assay/me, and renders StageProgress plus one PauseCard per open interrupt,
 *       resolving through CopilotKit's interrupt hook.
 *
 * Spec: S10.5, S10.6 | Ticket: 14 | Traces to: I7, I8, I18
 *
 * Build steps:
 * 1. Task: Await the slug, attach the 'assay' agent with the slug as thread ID, and start a
 *          run so a waiting session re-sends its interrupt.
 *    Think about: What should reopening a session mid-step show?
 *    Expected outcome: Reopening a waiting session shows the same pause card.
 * 2. Task: Track the latest session view from state snapshots and the running step from
 *          step started and finished events.
 *    Expected outcome: Progress updates without refreshing.
 * 3. Task: Load the profile once from /api/assay/me for the approver rule.
 *    Expected outcome: A non-approver's approval cards have Approve disabled.
 * 4. Task: Use CopilotKit's interrupt hook (its render function receives the open
 *          interrupts and a resolve function) to render one PauseCard per interrupt;
 *          resolving resumes the run.
 *    Expected outcome: Answering a question card shows the next pause.
 *
 * @param props - The route parameters with the slug.
 * @returns The session page.
 */
export default function SessionPage(props: SessionPageProps): ReactNode {
  throw new Error("Not implemented: S10.5 SessionPage");
}
