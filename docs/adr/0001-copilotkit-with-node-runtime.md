# CopilotKit frontend with a Node.js runtime service

Status: accepted | Date: 2026-10-05

## Context

Assay's browser UI was one HTML page served by the Python app, with no build
step (C2). The team chose CopilotKit as the frontend, to use AG-UI's standard
human-in-the-loop interrupts and live progress instead of polling.
CopilotKit's supported production path is React → CopilotKit Runtime
(Node.js) → AG-UI agent. Connecting React directly to a Python AG-UI endpoint
exists only as `agents__unsafe_dev_only`: unsupported, with no server-side
middleware, and authentication left entirely to the caller.

## Decision

Add one Next.js service that holds both the React UI and the CopilotKit
runtime route. It sits behind the bank's SSO proxy and forwards the
signed-in user's ID to the Python service on every call. The Python service
remains the only component that calls models or touches Postgres, and it
accepts AG-UI calls only from the Node service.

## Consequences

- Easier: standard interrupts rendered by CopilotKit; live progress; any
  AG-UI client can drive Assay later.
- Harder: two services to approve, deploy, monitor, and secure; a
  JavaScript build and dependency audit in CI; a trust boundary between Node
  and Python that must be enforced.
- Given up: the single-page, no-build frontend (C2).

## Alternatives

- Keep the plain page and switch its transport to AG-UI: no second service,
  but no CopilotKit components. Rejected by the user's frontend ruling.
- Connect React directly to Python (`agents__unsafe_dev_only`): unsupported
  in production and pushes authentication into browser code. Rejected.
