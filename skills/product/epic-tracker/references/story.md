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

Fill the template (below):

- **Name**: kebab-case, descriptive, no numeric prefix (`add-pix-payment`,
  `reset-password-flow`) -- the prefix lives in the filename only
- **Title**: human-readable title
- **Epic**: parent epic name (must match an existing epic directory)
- **Status**: always starts as `planned`
- **Prose context**: what this story delivers, who benefits, what
  changes for the user. Keep it focused -- one story, one outcome.
- **Acceptance Criteria**: one or more `### AC-N` blocks, each with a
  single Given/When/Then. Validated in Step 4 against rules V1-V7. See
  [ac-validation.md](ac-validation.md).
- **Rabbit Holes**: known complexities specific to this story
- **References**: link to parent epic, design doc, UI design, or
  other sources

### 3. Review

Present the draft to the user. Wait for feedback before saving.

### 4. Validate Acceptance Criteria

Load [ac-validation.md](ac-validation.md) and run V1-V7 on the drafted AC. Strict by default (V1-V5, V7); V6 surfaces a
warning with confirm-to-continue.

If any strict rule fails: surface the structured error (AC id, rule name,
suggested fix), do not proceed to save or push. Loop back to Review until
the user fixes the AC.

### 5. Save or Push

**If tracker configured** (`.artifacts/epics/.config.yml` exists with
`tracker.kind` set and not `none`):
- Ask the user (per session, cached) whether to push to the tracker
- If yes: load [sync.md](sync.md) and dispatch using the draft content;
  pass the parent epic's tracker id (from `epic.md` frontmatter
  `tracker.id`) so the story is linked — no markdown file is created
- If no: save to markdown and proceed to step 6

**If no tracker configured** (config missing or `kind: none`):
- Save to markdown and proceed to step 6

**Saving to markdown:**
1. Count existing story and task files in `.artifacts/epics/{epic-name}/`
   (exclude `epic.md`); zero-pad to 3 digits
2. Save to `.artifacts/epics/{epic-name}/{NNN}-{story-name}.md`

If the config is missing, run [sync.md](sync.md) bootstrap before the
first push, then proceed.

### 6. Update Epic Checklist *(markdown only)*

After saving to markdown, update the parent epic's Stories checklist to
replace the plain story name with a linked, numbered entry:

```markdown
- [ ] [003-reset-password-flow](003-reset-password-flow.md) -- brief description
```

## Guidelines

**DO:**
- Write acceptance criteria that are testable without knowing
  implementation
- Keep scope tight — one story should map to one implementation feature
- Reference the parent epic for broader context
- Update the epic's story checklist after creating the story

**DON'T:**
- Add a size field — sizing happens at implementation time
- Include implementation details or technical design
- Create stories without a parent epic (ask to create the epic first)
- Duplicate acceptance criteria from the epic level

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{story-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: planned
sources: []
epic: {{epic-name}}
type: story
# tracker block populated by sync.md after first push (omit until then):
# tracker:
#   kind: linear | github-issues | github-projects | jira
#   id: PROJ-123
#   url: https://...
#   last_synced: YYYY-MM-DDTHH:MM:SSZ
---

# {{Story Title}}

## Summary

{{What this story delivers, who benefits, what changes for the user. One story, one outcome.}}

## Acceptance Criteria

### AC-1

**Given** {{precondition}}
**When** {{action}}
**Then** {{expected outcome}}

{Add additional `### AC-N` blocks as needed. Each AC has exactly one Given/When/Then.}

## Rabbit Holes

{Remove this section if not needed.}

- {{Known complexity specific to this story}}

## References

- **Epic:** {{link to parent epic}}
- **Design Doc:** {{link or "None"}}
- **UI Design:** {{link or "None"}}
````

## Error Handling

- Epic doesn't exist: offer to create it first
- Story name conflicts: suggest alternative or confirm overwrite
- Story drafted without AC: ac-validation V1 fires; ask user to add at
  least one `### AC-N` block
