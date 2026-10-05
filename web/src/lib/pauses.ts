/**
 * Map pauses to cards and check replies before sending.
 *
 * Problem: Bank product managers turn vague asks into delivery work by hand, so questions
 * go unasked, answers go unrecorded, and tickets drift from what was approved. (Full
 * statement: BUILD_ORDER.md, "The problem".)
 *
 * Piece of the problem: C6 People decide and C7 Live, standard interaction. Each pause kind
 * needs its own wording, and replies must match the pause's response schema (I18). This
 * file owns that logic; it renders nothing.
 *
 * Why this comes now: It is pure logic with no dependencies beyond types; the pause card
 * (7) and session page (11) use it.
 *
 * Build order: Step 4 of 12.
 * Previous: src/lib/python-client.ts (step 3), which forwards calls to the Python service.
 * Next: src/app/api/copilotkit/route.ts (step 5), which serves the CopilotKit runtime.
 *
 * Build these in order:
 *     1. cardFor: the smallest piece.
 *     2. validateReply: used when a card submits.
 *     3. canApprove: used by approval cards.
 *
 * Depends on:
 *     Nothing in this project (foundation root). Placed at step 4 because the pause card
 *     needs it before it can render.
 *     Node built-ins: none.
 *     Third-party: none.
 *
 * Depended on by:
 *     src/components/pause-card.tsx: card choice and reply checks.
 *     src/app/s/[slug]/page.tsx: approver rule.
 *
 * Spec coverage: S10.6 | Traces to: I8, I18
 *
 * @packageDocumentation
 */

/** The pause kinds Python sends as interrupt reasons (SPECS data shapes). Spec: S10.6 */
export const PAUSE_KINDS = [
  "question",
  "dod_question",
  "map_review",
  "brief_fix",
  "await_answers",
  "approval",
  "seams",
  "ticket_review",
] as const;

/** One pause kind. Spec: S10.6 */
export type PauseKind = (typeof PAUSE_KINDS)[number];

/** The signed-in person's profile from Python's /api/me. Spec: S10.6 */
export type Me = { user: string; approver: boolean };

/** A JSON schema as sent in an interrupt's responseSchema. Spec: S10.6 */
export type ResponseSchema = {
  type?: string;
  required?: string[];
  properties?: Record<string, { type?: string; enum?: string[]; minLength?: number }>;
};

/**
 * Return the card kind for an interrupt reason.
 *
 * Problem piece: C6: each pause shown in its own words.
 *
 * Why it matters: Schema-generated forms lose the domain wording a PM needs ('Approve the
 *                 PRD' versus a bare checkbox). Choosing the card by reason keeps the
 *                 wording, while the schema still validates.
 *
 * What: Returns the reason as a PauseKind when it is one of PAUSE_KINDS; throws for
 *       anything else so an unknown pause is never silently shown as the wrong card.
 *
 * Spec: S10.6 | Ticket: 14 | Traces to: I18
 *
 * Build steps:
 * 1. Task: Return the reason when it is listed in PAUSE_KINDS; otherwise throw an error
 *          naming it.
 *    Think about: Why fail loudly rather than fall back to a generic card?
 *    Expected outcome: 'approval' returns approval; 'teleport' throws.
 *
 * @param reason - The interrupt's reason.
 * @returns The matching kind.
 * @throws An error naming an unknown reason.
 */
export function cardFor(reason: string): PauseKind {
  throw new Error("Not implemented: S10.6 cardFor");
}

/**
 * Return the problems that would make Python refuse a reply.
 *
 * Problem piece: C7: a person fixes a bad reply before sending (I18).
 *
 * Why it matters: Python validates every reply (S9.3), but a round trip to learn that a
 *                 required field is empty wastes the person's time. Checking the same
 *                 schema here gives the message at once; the server check stays
 *                 authoritative.
 *
 * What: Checks required fields are present and non-empty, enum fields hold an allowed
 *       value, and minimum string lengths are met; returns one message per problem, empty
 *       when valid.
 *
 * Spec: S10.6 | Ticket: 14 | Traces to: I18
 *
 * Build steps:
 * 1. Task: Report each required field that is missing or an empty string, naming the field.
 *    Expected outcome: An approval reply without decision yields one problem naming
 *                      decision.
 * 2. Task: Report enum fields outside their allowed values and strings shorter than their
 *          minimum length.
 *    Think about: Why is this check only a convenience, never the guard?
 *    Expected outcome: A decision of 'maybe' yields one problem.
 *
 * @param schema - The interrupt's response schema.
 * @param payload - The reply about to be sent.
 * @returns Problem messages; empty when the reply is valid.
 */
export function validateReply(schema: ResponseSchema, payload: Record<string, unknown>): string[] {
  throw new Error("Not implemented: S10.6 validateReply");
}

/**
 * Return whether this person may approve.
 *
 * Problem piece: C6: the UI never invites an action the server will refuse (I8).
 *
 * Why it matters: Python refuses approvals by non-approvers with 403; offering an enabled
 *                 Approve button that always fails teaches people the app is broken.
 *
 * What: True when the signed-in person's profile from Python's /api/me marks them an
 *       approver; false otherwise.
 *
 * Spec: S10.6 | Ticket: 14 | Traces to: I8
 *
 * Build steps:
 * 1. Task: Return the profile's approver flag.
 *    Expected outcome: A non-approver gets false.
 *
 * @param me - The signed-in person's profile from Python's /api/me.
 * @returns Whether Approve is enabled.
 */
export function canApprove(me: Me): boolean {
  throw new Error("Not implemented: S10.6 canApprove");
}
