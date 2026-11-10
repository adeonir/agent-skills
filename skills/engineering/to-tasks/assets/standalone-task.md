# Standalone Task Format

Use `[Task title]` as the issue title and the block below as the issue body. The task has no parent spec. The blocking issues are native tracker links, never sections of the body. Written as a file, the task uses `[Task title]` as its H1 and ends with a `Blocked by:` line naming the blocking issues, or `None`.

ALWAYS use this exact template structure:

```markdown
## Summary

[One or two sentences: the work this task does and the outcome it leaves behind.]

## Manual setup

- [A one-time step a person does in the local environment before the criteria can be met, such as registering an OAuth app with the local callback address. Omit the section when there is none.]

## Acceptance Criteria

### Tested

- [ ] [One observable outcome with concrete values that a test checks.]

### Demonstrated by hand

- [ ] [One observable outcome with concrete values that a person demonstrates in the local environment because no test covers it. Omit the list when there is none.]

## Verification

[How the criteria are verified: the test for the tested criteria, and how to demonstrate each criterion demonstrated by hand in the local environment.]
```

MUST NOT contain: a setup step as an acceptance criterion; a step in a published environment; a parent or blocked-by section in an issue body; specific file paths or implementation code, except a prototype snippet that captures a decision; source section numbers or requirement IDs; downstream work, milestones, or releases; conversation narrative.
