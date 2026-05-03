# Create Story

Define a unit of deliverable work within an epic, with acceptance criteria
that can be verified independently.

## When to Use

- User wants to detail a story from an epic's checklist
- User says "create story", "new story", "add story"
- Breaking down an epic into actionable work items

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

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

### 4. Save or Push

**If tracker configured** (`.artifacts/epics/.config.yml` exists with
`tracker.kind` set and not `none`):
- Ask the user (per session, cached) whether to push to the tracker
- If yes: load [sync.md](sync.md) and dispatch using the draft content;
  pass the parent epic's tracker id (from `epic.md` frontmatter
  `tracker.id`) so the story is linked — no markdown file is created
- If no: save to markdown and proceed to step 5

**If no tracker configured** (config missing or `kind: none`):
- Save to markdown and proceed to step 5

**Saving to markdown:**
1. Count existing story and task files in `.artifacts/epics/{epic-name}/`
   (exclude `epic.md`); zero-pad to 3 digits
2. Save to `.artifacts/epics/{epic-name}/{NNN}-{story-name}.md`

If the config is missing, run [sync.md](sync.md) bootstrap before the
first push, then proceed.

### 5. Update Epic Checklist *(markdown only)*

After saving to markdown, update the parent epic's Stories checklist to
replace the plain story name with a linked, numbered entry:

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
