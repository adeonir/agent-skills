# Spec Format

Use `[Work title]` as the issue title and the block below as the issue body.

ALWAYS use this exact template structure:

```markdown
## Problem Statement

[The problem, affected users, and why the outcome matters.]

## Solution

[The expected result from the user's perspective.]

## User Stories

- As [actor], I want [behavior], so that [benefit].
  - Acceptance: [Observable outcome, including relevant limits or failure cases.]

[Cover the agreed behavior without padding the list.]

## Implementation Decisions

[Decisions about modules, interfaces, contracts, data, and relevant interactions. Apply project constraints and describe reuse where relevant. Exclude specific file paths and implementation code. A short prototype-derived state machine, schema, or type shape may appear when it captures a decision more precisely than prose; identify its origin and keep only the decision-bearing parts.]

## Testing Decisions

[The boundary through which tests exercise the behavior, the modules covered, and relevant testing precedent in the repository. Test external behavior rather than implementation details. Describe how to demonstrate the acceptance criteria.]

## Out of Scope

[Explicit exclusions for this unit of work.]

## Further Notes

[Relevant risks, conflicting constraints, assumptions, unverified claims, and unanswered questions. State their consequences; do not present them as settled decisions. Write `None` when there are no additional notes.]

```

MUST NOT contain: source section numbers or requirement IDs; sibling artifact names, downstream tasks, milestones, or releases; implementation steps or file lists; traceability matrices, workflow states, or process gates; conversation narrative.
