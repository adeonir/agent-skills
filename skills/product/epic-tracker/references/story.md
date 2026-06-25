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

Read the parent epic for scope and naming context only. **Translate,
don't replicate.** Its tokens never cross into the story: strip epic IDs,
upstream document codes (§x.x, EC-N, ADR-NNN), sibling story names,
milestone language, and any cross-reference that doesn't stand alone.
Do not copy epic-level acceptance criteria. This story carries one
outcome of its own.

### 2. Draft

Fill the template (below):

- **Name**: kebab-case, descriptive, no numeric prefix (`add-pix-payment`,
  `reset-password-flow`) -- the prefix lives in the filename only
- **Title**: short human-readable phrase, slug-safe. No commands,
  flags, file paths, parentheses, brackets, or pipes — becomes branch
  name slug downstream. Declarative — names the deliverable
  (`Reset password flow`), never a narrative outcome (`User can reset
  their password to regain access`). The title maps to the tracker's
  summary field on push; outcome prose lives only in the body's
  Summary section.
- **Epic**: parent epic name (must match an existing epic directory)
- **Status**: always starts as `planned`
- **Prose context**: what this story delivers, who benefits, what
  changes for the user. Keep it focused — one story, one outcome.
  No upstream IDs, section numbers, or cross-references.
- **Out of Scope**: explicit boundaries -- what this story does not
  cover. Remove the section if nothing is ambiguous.
- **Acceptance Criteria**: one or more `### AC-N` blocks, each with a
  single Given/When/Then. Validated in Step 4 against rules V1-V7. See
  [ac-validation.md](ac-validation.md).
- **Rabbit Holes**: execution traps specific to this story — edge
  cases, ordering constraints, integration quirks; not implementation
  advice or upstream design notes
- **Open Questions**: unknowns that seed the spec's discovery; omit the
  section when nothing is undecided
- **Blocked by**: other stories, bugs, or epics that must finish before
  this story can start, listed in frontmatter `blocked_by` by path. Lets
  the tracker enforce order; leave empty when nothing blocks it.
- **References**: durable pointers the next session follows (parent epic,
  design doc, UI design). Canonical in the body; frontmatter `sources:`
  mirrors the links for sync

Record every durable reference (parent epic, design doc, UI design) in
frontmatter `sources:` as you draft -- one entry per source. These are
the pointers the resumption gate relies on.

Apply the resumption gate before proceeding:

> **Resumption gate** — Could a fresh session generate the spec from
> this story and its references, with no chat history? If no, add the
> missing piece (decision, content/copy, constraint, link) before saving.

### 3. Validate Acceptance Criteria

Load [ac-validation.md](ac-validation.md) and run V1-V7 on the drafted AC. Strict by default (V1-V5, V7); V6 surfaces a
warning with confirm-to-continue.

If any strict rule fails: surface the structured error (AC id, rule name,
suggested fix), do not proceed to save or push. Loop back to Draft until
the user fixes the AC.

### 4. Save or Push

**If tracker configured** (`git config --get epic-tracker.kind` returns a value and is not `none`):
- Ask the user (per session, cached) whether to push to the tracker
- If yes: load [sync.md](sync.md) and dispatch using the draft content;
  pass the parent epic's tracker id (from `epic.md` frontmatter
  `tracker.id`) so the story is linked — no markdown file is created
- If no: save to markdown and proceed to step 5

**If no tracker configured** (`epic-tracker.kind` not set or `none`):
- Save to markdown and proceed to step 6

**Saving to markdown:**
1. Count existing story and task files in `.artifacts/epics/{epic-name}/`
   (exclude `epic.md`); zero-pad to 3 digits
2. Save to `.artifacts/epics/{epic-name}/{NNN}-{story-name}.md`

If `epic-tracker.kind` is not set, run [sync.md](sync.md) bootstrap first.

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
- Keep scope tight — one story should map to one implementation feature
- Reference the parent epic for broader context
- Update the epic's story checklist after creating the story

**DON'T:**
- Add a size field — sizing happens at implementation time
- Include implementation details or technical design
- Carry upstream IDs, section numbers, or doc-internal codes (§x.x, EC-N, ADR-NNN) — translate to plain language
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
blocked_by: []  # paths of artifacts that must finish first (epic-name/story-name); omit when nothing blocks this
epic: {{epic-name}}
type: story
# tracker block populated by sync.md after first push (omit until then):
# tracker:
#   kind: linear | github
#   id: PROJ-123
#   url: https://...
#   last_synced: YYYY-MM-DDTHH:MM:SSZ
---

# {{Story Title}}

## Summary

{{What this story delivers, who benefits, what changes for the user. One story, one outcome.}}

MUST NOT contain: upstream IDs (§x.x, EC-N, ADR-NNN), sibling story names, epic-level acceptance criteria, roadmap language, or implementation details.

## Out of Scope

{Remove this section if nothing is ambiguous.}

- {{What this story explicitly does not cover}}

## Acceptance Criteria

### AC-1

**Given** {{precondition}}
**When** {{action}}
**Then** {{expected outcome}}

{Add additional `### AC-N` blocks as needed. Each AC has exactly one Given/When/Then.}

## Rabbit Holes

{Remove this section if not needed.}

- {{Execution trap specific to this story — edge case, ordering constraint, or integration quirk}}

MUST NOT contain: implementation advice, upstream design notes, or cross-references to other documents.

## Open Questions

{Remove this section if nothing is undecided. Seeds the spec's discovery
— capture what's open so a fresh session knows what to ask, not re-decide.}

- {{Unknown to resolve during specify}}

## References

{Durable pointers the next session follows to recover context. Canonical
home — travels into the tracker description; frontmatter `sources:`
mirrors these links for sync (markdown only, absent in tracker mode).}

- **Epic:** {{link to parent epic}}
- **Design Doc:** {{link or "None"}}
- **UI Design:** {{link or "None"}}
````

## Error Handling

- Epic doesn't exist: offer to create it first
- Story name conflicts: suggest alternative or confirm overwrite
- Story drafted without AC: ac-validation V1 fires; ask user to add at
  least one `### AC-N` block
