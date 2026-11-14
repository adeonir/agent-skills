# Task Format

Use `[Task title]` as the issue title and the block below as the issue body. The parent spec and the blocking tasks are native tracker links, never sections of the body.

ALWAYS use this exact template structure:

```markdown
## What to build

[The end-to-end behavior this task makes work, from the user's perspective, not a layer-by-layer implementation list. For a prefactor or wide-change task, the structural change and the behavior it keeps unchanged.]

## Acceptance criteria

- [ ] [One observable outcome with concrete values.]

```

MUST NOT contain: a setup step as an acceptance criterion; a step in a published environment; a parent or blocked-by section in an issue body; specific file paths or implementation code, except a prototype snippet that captures a decision; implementation decisions copied from the spec, which never include its testing decisions; source section numbers or requirement IDs; downstream work, milestones, or releases; conversation narrative.
