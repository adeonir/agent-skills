<!-- Feature design doc. ALWAYS use this exact template structure. Remove an optional section, or an optional subsection, that has no content. Delete every comment and replace every square-bracket slot before writing the file. -->

---
name: [feature-slug]
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
status: proposed
sources: []
---

# Feature Design Doc: [Feature Name]

## Context

[A summary of what will be built.]

## Proposed Solution

[The flow, the components involved, and what changes in the system, with every decision taken and its reason. Enough detail for a new session to implement from this document alone. Record error handling only where the design decides it.]

### Data Changes

<!-- Optional. -->

[Schema changes and migrations.]

### Contracts

<!-- Optional. -->

[APIs, events, and interfaces between parts of the system.]

## Alternatives & Trade-offs

<!-- Optional: only when a real alternative was weighed or the solution has a relevant cost. -->

- **Cost of this solution:** [what going ahead gives up]
- **[Alternative not selected]:** [the reason]

## Rollout

<!-- Optional: only when the release needs more than shipping directly. -->

- [Feature flag, gradual migration, or rollback.]

## Tests

<!-- Optional: only when testing goes beyond the project standard. -->

- [What is tested beyond the standard.]

## References

- [Typed reference to a related document that exists, such as the feature PRD or an ADR.]

MUST NOT contain: goals, non-goals, a scope list, requirements, acceptance criteria, edge-case lists, a task list, tracker User Stories, implementation sequence, duplicated feature PRD content, or conversation narrative ("as discussed", "we agreed", "the user confirmed").
