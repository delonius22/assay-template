# Traceability — Assay web app

Spec IDs are taken verbatim from ../SPECS.md section S10. PRD trace is the section's "Traces to" line.

| Spec ID | Clause summary | PRD trace | File | Function(s) | Test(s) |
|---|---|---|---|---|---|
| S10.1 | The CopilotKit runtime route registers Assay as an AG-UI agent pointing at the Python endpoint, attaching the  | I17, I18, C7 | src/app/api/copilotkit/route.ts, src/lib/config.ts, src/lib/python-client.ts | POST, createRuntime, loadWebConfig, serviceHeaders | test/app/api/copilotkit/route.test.ts, test/lib/config.test.ts, test/lib/python-client.test.ts |
| S10.2 | Read the signed-in user from the SSO proxy header; refuse when missing, except for a development user set in c | I17, I18, C7 | src/app/api/copilotkit/route.ts, src/lib/config.ts, src/lib/identity.ts | POST, loadWebConfig, signedInUser | test/app/api/copilotkit/route.test.ts, test/lib/config.test.ts, test/lib/identity.test.ts |
| S10.3 | A REST proxy route forwards session, questionnaire, download, and usage calls to Python with the service token | I17, I18, C7 | src/app/api/assay/[...path]/route.ts, src/lib/python-client.ts | GET, POST, forwardToPython, serviceHeaders | test/app/api/assay/[...path]/route.test.ts, test/lib/python-client.test.ts |
| S10.4 | The sessions page lists sessions and starts a new one (title, slug, mode, brief for mode 3) | I17, I18, C7 | src/app/page.tsx | SessionsPage | test/app/page.test.ts |
| S10.5 | The session page connects the agent for the session's thread, shows stage progress from snapshots and step eve | I17, I18, C7 | src/app/layout.tsx, src/app/s/[slug]/page.tsx, src/components/stage-progress.tsx | RootLayout, SessionPage, StageProgress | test/app/layout.test.ts, test/app/s/[slug]/page.test.ts, test/components/stage-progress.test.ts |
| S10.6 | Pause cards render each pause kind from the interrupt's reason and response schema and resolve it with a match | I17, I18, C7 | src/app/s/[slug]/page.tsx, src/components/pause-card.tsx, src/lib/pauses.ts | PauseCard, SessionPage, canApprove, cardFor, validateReply | test/app/s/[slug]/page.test.ts, test/components/pause-card.test.ts, test/lib/pauses.test.ts |
| S10.7 | The questionnaire page lets a developer answer the current round and submit through the REST proxy | I17, I18, C7 | src/app/q/[slug]/page.tsx | QuestionnairePage | test/app/q/[slug]/page.test.ts |
