Use this template as written:
# Spec Format

Use `[Work title]` as the issue title and the block below as the issue body. Include `Reference` only when a related document exists, and `Current Behavior` only when the work changes existing behavior. For a repository file, link its URL on the repository host's default branch.

ALWAYS use this exact template structure:

```markdown
## Problem Statement

[The problem, affected users, and why the outcome matters.]

## Current Behavior

[The existing behavior this work changes, in one to three lines, read from the code.]

## Solution

[The expected result from the user's perspective.]

## User Stories

1. As [actor], I want [behavior], so that [benefit].
   - Acceptance: [The observable outcome of one path, with concrete values.]
   - Acceptance: [The observable outcome of one failure case or limit, with concrete values.]

[Cover all aspects of the agreed behavior: every actor, path, and failure case or limit the context names. Add no story the context does not support. Write one behavior per acceptance line. Acceptance covers behavior the project owns, configures, or composes.]

## Implementation Decisions

[Decisions about modules, interfaces, contracts, data, and relevant interactions. Respect the project's conventions and architecture decisions. When a decision reuses an existing module or pattern, name it. When the work replaces a module the project owns, name the module and its tests for removal. For a contract, name the errors the caller must handle. For a contestable decision, name the rejected option in one sentence. Exclude specific file paths and implementation code. A short prototype-derived state machine, schema, or type shape may appear when it captures a decision more precisely than prose; identify its origin and keep only the decision-bearing parts.]

## Testing Decisions

[The boundary through which tests exercise the behavior, stated as: tests exercise [behavior] only through [boundary], not implementation details. The modules covered, and relevant testing precedent in the repository.]

## Out of Scope

[Explicit exclusions for this unit of work. Write `None` when there are none.]

## Further Notes

[Assumptions, including unverified claims, and risks. State their consequences; do not present them as settled decisions. Write `None` when there are none.]

## Reference

[Link to each related document.]
```

MUST NOT contain: source section numbers or requirement IDs; sibling artifact names outside `Reference`; a supplied material's name or provenance; downstream tasks, milestones, or releases; implementation steps or file lists; traceability matrices, workflow states, or process gates; conversation narrative.
