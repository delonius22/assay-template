# Build Order — Assay web app (Next.js + CopilotKit)

The Python service has its own build order in `../BUILD_ORDER.md`; build it first (ticket 12).

## The problem
Bank product managers turn vague asks into delivery work by hand, so questions go unasked, answers go unrecorded, and tickets drift from what was approved. Solved, for this app, means a PM and developers work through a whole session in the
browser, seeing each step and pause as it happens, while browsers never reach the Python service.

### What must be true for it to be solved
- **C6 People decide: the right people answer, approve, and correct at every stage.** (steps 2, 4, 7, 10, 12)
- **C7 Live, standard interaction: people see progress and pauses as they happen, through a standard agent protocol.** (steps 1, 3, 4, 5, 6, 8, 9, 11)

These are the Python service's capabilities C6 and C7; C1 to C5 live entirely in Python.

## How to use this skeleton
Start at step 1. In each file: read the file comment, then build the functions in its
"Build these in order" list. For each function, read Problem piece / Why it matters / What,
work through the build steps, then turn its `it.todo` entries into real tests and make them
pass. When the file's tests pass, follow its `Next:` pointer. Once a function is implemented
and tested, delete its Build steps block; keep Problem piece, Why it matters, and What.

Toolchain baseline: TypeScript 7.0.2 (native compiler); Node.js 24 Active LTS; Next.js 16.3;
React 19.3; CopilotKit 1.77 (`@copilotkit/react-core/v2`); AG-UI client 1.0.2; Vitest 5.0.3;
Biome 2.5.
Spec ID scheme: verbatim IDs from ../SPECS.md (S10.1 to S10.7).

## Sequence
| Step | Module | Capability | Builds | Depends on | Unlocks |
|---|---|---|---|---|---|
| 1 | src/lib/config.ts |  | Read the web service's configuration once. | — (start of project) | 2, 3, 5, 6 |
| 2 | src/lib/identity.ts |  | Read the signed-in user from the SSO proxy's header. | src/lib/config.ts | 5, 6 |
| 3 | src/lib/python-client.ts |  | Forward calls to the Python service with the service token and the user. | src/lib/config.ts | 5, 6 |
| 4 | src/lib/pauses.ts |  | Map pauses to cards and check replies before sending. | — (foundation root) | 7 |
| 5 | src/app/api/copilotkit/route.ts |  | Serve the CopilotKit runtime, with Assay registered as an AG-UI agent. | src/lib/config.ts, src/lib/identity.ts, src/lib/python-client.ts | — |
| 6 | src/app/api/assay/[...path]/route.ts |  | Proxy REST calls to the Python service. | src/lib/config.ts, src/lib/identity.ts, src/lib/python-client.ts | — |
| 7 | src/components/pause-card.tsx |  | Render one pause as a card a person can act on. | src/lib/pauses.ts | 11 |
| 8 | src/components/stage-progress.tsx |  | Show a session's stage and its steps as they happen. | — (foundation root) | 11 |
| 9 | src/app/layout.tsx |  | Wrap every page in the CopilotKit provider. | — (foundation root) | — |
| 10 | src/app/page.tsx |  | List sessions and start a new one. | — (foundation root) | — |
| 11 | src/app/s/[slug]/page.tsx |  | Run one session live: progress, and a card for each pause. | src/components/pause-card.tsx, src/components/stage-progress.tsx | — |
| 12 | src/app/q/[slug]/page.tsx |  | Let a developer answer the current questionnaire round. | — (foundation root) | — |

## Assumptions
- Next.js's convention wins over the generic TypeScript reference: `moduleResolution: "bundler"`
  and extensionless relative imports, because Next compiles the app with its own bundler.
- `.npmrc` sets `legacy-peer-deps=true`: CopilotKit 1.77's channel packages declare an optional
  Vitest 4 peer that crashes npm's resolver beside Vitest 5 (D16). Remove when CopilotKit updates.
- Pages and components are plain functions returning ReactNode; tests for them are `it.todo`
  lists without imports, because rendering them needs a DOM environment chosen at build time.
- A4: the SSO proxy sets the configured user header on every request to this service.

## Open questions
- none for this app; OQ-1 (cancelled resume entries) is tracked in ../BUILD_ORDER.md.
