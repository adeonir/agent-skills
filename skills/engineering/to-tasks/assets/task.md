# Task Format

Use `[Task title]` as the issue title and the block below as the issue body. The parent spec and the blocking tasks are native tracker links, never sections of the body. Written as a file, the task uses `[Task title]` as its H1 and ends with a `Parent:` line linking the spec issue and a `Blocked by:` line naming the blocking tasks by their file numbers, or `None`.

ALWAYS use this exact template structure:

```markdown
## What to build

[The end-to-end behavior this task makes work, from the user's perspective, not a layer-by-layer implementation list. For a prefactor or wide-change task, the structural change and the behavior it keeps unchanged.]

## Manual setup

- [A one-time step a person does in the local environment before the criteria can be met, such as registering an OAuth app with the local callback address. Omit the section when there is none.]

## Acceptance criteria

### Tested

- [ ] [One observable outcome with concrete values that a test at the spec's test boundary checks.]

### Demonstrated by hand

- [ ] [One observable outcome with concrete values that a person demonstrates in the local environment because no test covers it, written as what the person sees while using the product. Omit the list when there is none.]

## Verification

[How the criteria are verified, as the spec's Testing Decisions set it: the test boundary for the tested criteria, and one pass through the product that shows the criteria demonstrated by hand in the local environment. Carry the intent of the spec's demonstration, not its wording. Name a developer tool, a playback rate, or a media-feature emulation only for an outcome no one can see without it.]

```

MUST NOT contain: a setup step as an acceptance criterion; a step in a published environment; a parent or blocked-by section in an issue body; specific file paths or implementation code, except a prototype snippet that captures a decision; implementation decisions copied from the spec, which never include its testing decisions; source section numbers or requirement IDs; downstream work, milestones, or releases; conversation narrative.
