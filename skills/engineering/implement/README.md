# Implement

Implement a spec, one of its tasks, or a standalone task, building each task in a fresh sub-agent and integrating the results on one branch.

## What It Does

```mermaid
flowchart TD
    A[Read target and relations] --> B[Prepare integration branch]
    B --> C[Rebuild state from the checklist]
    C --> D[Investigate when tasks need it]
    D --> E[Dispatch ready tasks]
    E --> F[Integrate each finished task]
    F -->|Integration branch moved| E
    F -->|Tasks unblocked| E
    F -->|Nothing ready| G[Report]
```

| Phase | Output |
|-------|--------|
| Target | Spec and tasks with their native blocking links |
| Branch | One integration branch per spec, reused across runs |
| State | Each task integrated, resumed, or pending, with integration tracked in `.artifacts/implement/[spec-id]/checklist.md` |
| Investigation | Notes in `.artifacts/implement/[spec-id]/`, when a task needs them |
| Dispatch | One fresh implementer per ready task, in its own worktree, with the task set to in progress |
| Integration | Integration branch fast-forwarded to each verified task, with the checklist line ticked, the task set to in review when it has a criterion left to a manual step and to done otherwise, unless it is standalone, and the task branch deleted |
| Report | Tasks with commits and verification, blockers, tasks not started, and criteria left to a manual step, with an offer of a step-by-step manual procedure |

## Usage

```text
/implement spec implement every task of this spec issue
/implement task implement this task of the spec
/implement task implement this standalone task that has no spec
```

## Output

Local commits on the integration branch `[spec-id]-[slug]`, one branch per task until it is integrated, tracker statuses set to in progress on dispatch, the spec with its first task, and in review or done on integration except for a standalone task, and the checklist, investigation notes, and manual steps (`manual.md`) in `.artifacts/implement/[spec-id]/`. Nothing is pushed, and the main checkout is never switched.

## Requirements

A connected tracker tool or authenticated CLI with sub-issues and blocking links, git with worktree support, and sub-agents.
