# Spec Format

Use `[Work title]` as the issue title and the block below as the issue body. Include `Reference` only when a related document exists, and `Current Behavior` only when the work changes existing behavior. For a repository file, link its URL on the repository host; if the file is not on the remote, ask the user before registering.

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
   - Acceptance: [One observable outcome with concrete values, including relevant limits or failure cases.]

[Cover the agreed behavior without padding the list. Write one behavior per acceptance line, observable through the test boundary or the manual demonstration in Testing Decisions. Leave out an absence that only reading configuration shows, such as a removed dependency.]

## Implementation Decisions

[Decisions about modules, interfaces, contracts, data, and relevant interactions. Apply project constraints. When a decision reuses an existing module or pattern, name it. For a contract, name the errors the caller must handle. For a contestable decision, name the rejected option in one sentence. Exclude specific file paths and implementation code. A short prototype-derived state machine, schema, or type shape may appear when it captures a decision more precisely than prose; identify its origin and keep only the decision-bearing parts.]

## Testing Decisions

[The boundary through which tests exercise the behavior, the modules covered, and relevant testing precedent in the repository. For each external dependency, the seam where a test replaces it, or that it has no seam. Test external behavior rather than implementation details. Quote each acceptance criterion demonstrated by hand, and for each surface those criteria share, one pass through it in the local environment that demonstrates them, as what a person sees while using the product, such as "press the button; it compresses and settles back". Name a developer tool, a playback rate, or a media-feature emulation only for an outcome no one can see without it. List the one-time setup a person does before the demonstration, such as registering an OAuth app with the local callback address.]

## Out of Scope

[Explicit exclusions for this unit of work.]

## Further Notes

[Relevant risks, conflicting constraints, assumptions, unverified claims, and unanswered questions; never setup steps. State their consequences; do not present them as settled decisions. Write `None` when there are no additional notes.]

## Reference

[Link to each related document.]

```

MUST NOT contain: source section numbers or requirement IDs; sibling artifact names outside `Reference`; downstream tasks, milestones, or releases; implementation steps or file lists; traceability matrices, workflow states, or process gates; conversation narrative.
