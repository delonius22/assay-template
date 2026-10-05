# Assay glossary

## Session
One initiative's journey from first question to exported tickets, identified by its slug. In AG-UI terms, a session is a thread. Distinct from: run, step.
Decided: 2026-10-05, during AG-UI grill.

## Run
One execution of a session from a start or a resume until the next pause, the finish, or an error. A session has many runs. Distinct from: session, step.
Decided: 2026-10-05, during AG-UI grill.

## Step
One graph node executing inside a run, such as one grill turn or writing the PRD. Distinct from: stage, run.
Decided: 2026-10-05, during AG-UI grill.

## Stage
A phase of a session that a person recognises: Intake, Definition of Done, PRD, Spec, Tickets. A stage contains many steps. Distinct from: step.
Decided: 2026-10-05, during AG-UI grill.

## Pause
A point where a session waits for a person: a question, an approval, a review, or waiting for answers. In AG-UI terms, a pause is an interrupt. Distinct from: error, finish.
Decided: 2026-10-05, during AG-UI grill.

## Story
A business goal written "As a..., I want..., so that...". Contains features. Distinct from: ticket.
Decided: 2026-10-05 (D1).

## Feature
A business capability that delivers part of a story. Contains tickets. Distinct from: component, module.
Decided: 2026-10-05 (D1).

## Ticket
A buildable, testable slice of one feature, listed in build order. Distinct from: story, task.
Decided: 2026-10-05 (D1, D8).
