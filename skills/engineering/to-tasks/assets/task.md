# Task Format

Use `[Task title]` as the issue title and the block below as the issue body. The parent spec and the blocking tasks are native tracker links, never sections of the body. Written as a file, the task uses `[Task title]` as its H1 and ends with a `Parent:` line linking the spec issue and a `Blocked by:` line naming the blocking tasks by their file numbers, or `None`.

ALWAYS use this exact template structure:

```markdown
## What to build

[The end-to-end behavior this task makes work, from the user's perspective, not a layer-by-layer implementation list. For a prefactor or wide-change task, the structural change and the behavior it keeps unchanged.]

## Acceptance criteria

- [ ] [One observable outcome with concrete values that shows this task works. End with `(manual)` when a person meets it outside the repository, such as a setting on the platform.]

## Verification

[How the criteria are verified, as the spec's Testing Decisions set it: the test boundary, or the criteria demonstrated by hand and how.]

```

MUST NOT contain: a parent or blocked-by section in an issue body; specific file paths or implementation code, except a prototype snippet that captures a decision; implementation decisions copied from the spec, which never include its testing decisions; source section numbers or requirement IDs; downstream work, milestones, or releases; conversation narrative.
