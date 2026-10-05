# Assay web app

Next.js with CopilotKit. Holds the UI and the CopilotKit runtime; calls the Python service
over AG-UI and REST with the service token and the signed-in user (ADR 0001).

Start at `BUILD_ORDER.md`, step 1. `npm ci`, then `npm run typecheck`, `npm run lint`,
`npm test`. Environment: `ASSAY_PYTHON_URL`, `ASSAY_SERVICE_TOKEN`, `ASSAY_USER_HEADER`
(default `x-forwarded-user`), and `ASSAY_DEV_USER` for local runs only.

`.npmrc` turns off npm's automatic peer installs (D16); required peers are pinned in
`package.json`. Pages are stubs, so `next build` succeeds only once they are built.
