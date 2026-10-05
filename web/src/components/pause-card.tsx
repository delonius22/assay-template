/**
 * Render one pause as a card a person can act on.
 *
 * Problem: Bank product managers turn vague asks into delivery work by hand, so questions
 * go unasked, answers go unrecorded, and tickets drift from what was approved. (Full
 * statement: BUILD_ORDER.md, "The problem".)
 *
 * Piece of the problem: C6 People decide. Each pause kind gets its own wording and
 * controls. This component renders a card and resolves the interrupt; it never talks to
 * Python directly.
 *
 * Why this comes now: Pause logic (4) exists; the session page (11) renders these cards.
 *
 * Build order: Step 7 of 12.
 * Previous: src/app/api/assay/[...path]/route.ts (step 6), which proxies REST calls to
 * Python.
 * Next: src/components/stage-progress.tsx (step 8), which shows stage and step progress.
 *
 * Build these in order:
 *     1. PauseCard: the only component.
 *
 * Depends on:
 *     src/lib/pauses.ts: cardFor, validateReply, canApprove, Me, ResponseSchema.
 *     Node built-ins: none.
 *     Third-party: react, @copilotkit/react-core (types).
 *
 * Depended on by:
 *     src/app/s/[slug]/page.tsx: one card per open interrupt.
 *
 * Spec coverage: S10.6 | Traces to: I8, I18
 *
 * @packageDocumentation
 */
"use client";

import type { Interrupt } from "@copilotkit/react-core/v2";
import { type ReactNode, useState } from "react";
import { canApprove, cardFor, type Me, type ResponseSchema, validateReply } from "../lib/pauses";

/** Props for PauseCard. Spec: S10.6 */
export type PauseCardProps = {
  interrupt: Interrupt;
  me: Me;
  resolve: (payload: Record<string, unknown>) => void;
};

/**
 * Render the card for one interrupt and resolve it with a valid reply.
 *
 * Problem piece: C6: a person answers, approves, or requests changes in context.
 *
 * Why it matters: The card is where a PM acts on each pause. Choosing the card by reason
 *                 keeps the domain wording; validating against the response schema before
 *                 resolving catches mistakes at once; disabling Approve for non-approvers
 *                 keeps the UI honest (I8).
 *
 * What: Picks the card by the interrupt's reason, shows its message and metadata, collects
 *       the reply fields its kind needs, shows validation problems, and calls resolve with
 *       a payload matching the response schema.
 *
 * Spec: S10.6 | Ticket: 14 | Traces to: I8, I18
 *
 * Build steps:
 * 1. Task: Choose the card from the interrupt's reason and show its message; for question
 *          kinds show the recommended answer and reason from metadata, and prefill the
 *          answer with the recommendation.
 *    Expected outcome: A question card shows the recommended answer prefilled.
 * 2. Task: Collect the fields the kind's reply needs: text for questions and map review, a
 *          decision with optional change text for approval, seams, and ticket review, the
 *          brief fields for brief fixes, and nothing for waiting.
 *    Think about: Which kinds share a reply shape, and why?
 *    Expected outcome: An approval card offers Approve and Request changes.
 * 3. Task: Before resolving, validate against the response schema and show each problem;
 *          resolve only when there are none.
 *    Expected outcome: Submitting an empty answer shows a problem and does not resolve.
 * 4. Task: Disable Approve, with a short reason, when the person may not approve.
 *    Expected outcome: A non-approver sees Approve disabled.
 *
 * @param props - The interrupt, the signed-in profile, and the resolve function.
 * @returns The card.
 */
export function PauseCard(props: PauseCardProps): ReactNode {
  throw new Error("Not implemented: S10.6 PauseCard");
}
