# To Spec

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
| Investigation | Grounded implementation and testing decisions |
| Specification | Draft spec with problem, solution, user stories, decisions, exclusions, and notes |
| Registration | One tracker issue holding the draft, carrying the `spec` label |
| Review | User-approved spec in its tracker issue |

## Usage

```text
/to-spec turn this conversation into a specification
/to-spec specify the agreed change from the supplied materials
/to-spec update the existing specification with these revised decisions
```

## Output

One tracker issue per spec, registered as a draft and reviewed in the tracker. Without tracker access, a markdown file in the project at a path the user confirms, or the conversation when the user declines the file.

## Requirements

A connected tracker tool or authenticated CLI is required for registration. Without tracker access, the skill reports the blocker and offers the markdown file.
