# Create Story

Define a unit of deliverable work within an epic, with acceptance criteria
that can be verified independently.

## When to Use

- User wants to detail a story from an epic's checklist
- User says "create story", "new story", "add story"
- Breaking down an epic into actionable work items

## Workflow

### 1. Identify Epic

1. If user specifies an epic, load
   `.artifacts/epics/{epic-name}/epic.md`
2. If no epic specified, list available epics and ask which one
3. If no epics exist, ask whether to create the epic first or place
   the story in a new epic

### 2. Draft

**USE TEMPLATE:** `templates/story.md`

Fill the template:

- **Name**: kebab-case, descriptive, no numeric prefix (`add-pix-payment`,
  `reset-password-flow`) -- the prefix lives in the filename only
- **Title**: human-readable title
- **Epic**: parent epic name (must match an existing epic directory)
- **Status**: always starts as `planned`
- **Prose context**: what this story delivers, who benefits, what
  changes for the user. Keep it focused -- one story, one outcome.
- **Acceptance Criteria**: specific, verifiable conditions. These are
  the contract for "done".
- **Rabbit Holes**: known complexities specific to this story
- **References**: link to parent epic, design doc, figma, or other
  sources

### 3. Review

Present the draft to the user. Wait for feedback before saving.

### 4. Save

Determine the next sequence number by counting existing story files in
`.artifacts/epics/{epic-name}/` (exclude `epic.md`). Zero-pad to 3 digits.

Save to `.artifacts/epics/{epic-name}/{NNN}-{story-name}.md`.

Example: if 2 stories exist, the next file is `003-reset-password-flow.md`.

### 5. Update Epic

After saving, update the parent epic's Stories checklist to replace the
plain story name with a linked, numbered entry:

```markdown
- [ ] [003-reset-password-flow](003-reset-password-flow.md) -- brief description
```

## Guidelines

**DO:**
- Write acceptance criteria that are testable without knowing
  implementation
- Keep scope tight -- one story should map to one spec-driven feature
- Reference the parent epic for broader context
- Update the epic's story checklist after creating the story

**DON'T:**
- Add a size field -- spec-driven sizes during handoff
- Include implementation details or technical design
- Create stories without a parent epic (ask to create the epic first)
- Duplicate acceptance criteria from the epic level

## Error Handling

- Epic doesn't exist: offer to create it first
- Story name conflicts: suggest alternative or confirm overwrite
- User provides story without clear acceptance criteria: ask what
  "done" looks like
