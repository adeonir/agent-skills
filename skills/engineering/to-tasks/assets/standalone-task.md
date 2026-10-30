# Standalone Task Format

Use `[Task title]` as the issue title and the block below as the issue body. The task has no parent spec. The blocking issues are native tracker links, never sections of the body.

ALWAYS use this exact template structure:

```markdown
## Summary

[One or two sentences: the work this task does and the outcome it leaves behind.]

## Acceptance Criteria

- [ ] [One observable outcome with concrete values that shows this task works.]
```

MUST NOT contain: a parent or blocked-by section; specific file paths or implementation code, except a prototype snippet that captures a decision; source section numbers or requirement IDs; downstream work, milestones, or releases; conversation narrative.
