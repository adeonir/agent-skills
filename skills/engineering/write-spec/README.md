# Write Spec

Turn agreed context into a specification of behavior, technical decisions, and tests.

## What It Does

```mermaid
flowchart TD
    A[Read context] --> B[Investigate code]
    B --> C[Draft spec]
    C --> D[Register issue]
    D --> E[Review in tracker]
    E -->|Corrections| C
```

| Phase | Output |
|-------|--------|
| Context | Intended outcome, constraints, and explicit uncertainties |
| Investigation | Grounded decisions, a confirmed test boundary, and answered open questions |
| Specification | Draft spec with problem, solution, user stories, decisions, exclusions, and notes |
| Registration | One tracker issue holding the draft, carrying the `spec` label |
| Review | User-approved spec in its tracker issue |

## Usage

```text
/write-spec turn this conversation into a specification
/write-spec specify the agreed change from the supplied materials
/write-spec update the existing specification with these revised decisions
```

## Output

One tracker issue per spec, registered as a draft and reviewed in the tracker. Without tracker access, the draft in the conversation.

## Requirements

A connected tracker tool or authenticated CLI is required for registration. Without tracker access, the skill reports the blocker and shows the draft in the conversation.
