# Create Story

Define a story: a demonstrable slice of user-visible value within an epic,
with acceptance criteria that are verified independently and satisfy a
parent-epic requirement. Enabling work with no demonstrable user outcome is a
Task, not a Story — see [discriminator.md](discriminator.md).

## When to Use

- User wants to detail a story from an epic's checklist
- User says "create story", "new story", "add story"
- User says "edit story", "update story", "change story" — run the edit branch below
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
don't replicate.** Its prose tokens never cross into the story: strip epic
IDs, `§x.x` section numbers, sibling story names, roadmap
language, and any cross-reference that doesn't stand alone. This story
carries one outcome of its own.

The parent epic declares the PRD requirements it owns in its
`## Requirements`. Read that set — it is the menu this story's acceptance
criteria may operationalize. Each `### AC-N` links the requirement it
satisfies on a `**Satisfies**` line (see Acceptance Criteria below):
backward provenance the spec inherits 1:1, the one upstream reference that
crosses, and never in prose. When the story depends on an architectural
decision, record `ADR-NNN` in `## References`, not as a requirement.

### 2. Draft

Fill the template (below):

- **Name**: kebab-case, descriptive, no numeric prefix (`add-pix-payment`,
  `reset-password-flow`) -- the prefix lives in the filename only
- **Title**: short human-readable phrase, slug-safe. No commands,
  flags, file paths, parentheses, brackets, or pipes — becomes branch
  name slug downstream. Declarative — names the deliverable
  (`Reset password flow`), never a narrative outcome (`User can reset
  their password to regain access`). The name is translated from its
  source, not copied: strip any borrowed token — reference or ticket
  codes, section numbers, code identifiers, document or
  sibling-artifact names — which travel in References or the body,
  never the title. The title maps to the tracker's summary field on
  push; outcome prose lives only in the body's Summary section.
- **Epic**: parent epic name (must match an existing epic directory)
- **Status**: always starts as `planned`
- **Prose context**: what this story delivers, who benefits, what
  changes for the user. Keep it focused — one story, one outcome.
  Requirement IDs go on each AC's `Satisfies` line, not the prose; no
  section numbers or stray cross-references here.
- **Out of Scope**: explicit boundaries -- what this story does not
  cover. Remove the section if nothing is ambiguous.
- **Acceptance Criteria**: one or more `### AC-N` blocks, each with a
  single Given/When/Then plus a `**Satisfies**` line naming the parent
  epic requirement it operationalizes (`FR/BR/EC/NFR`; omit the line for
  an AC that maps to no requirement). Validated in Step 3 against rules
  V1-V8. See [ac-validation.md](ac-validation.md).
- **Rabbit Holes**: execution traps specific to this story — edge
  cases, ordering constraints, integration quirks; not implementation
  advice or upstream design notes. A trap belongs to the story whose
  domain owns it, not the story you were authoring when it surfaced —
  being the first story of an initiative does not make it the owner. If
  it affects other stories, relocate it to the sibling that owns the
  domain: the trap moves, it is not cross-referenced
- **Open Questions**: unknowns that seed *this story's* spec discovery;
  omit the section when nothing is undecided. An unknown that gates no AC
  here is not this story's question — it belongs to the story whose
  domain it gates. A foundational decision spanning stories may be kept
  as a blocked open question that suggests an ADR to settle it; a story
  suggests an ADR, never generates one, and never parks the decision on
  whichever story is created first
- **Blocked by**: other stories, bugs, or epics that must finish before
  this story can start, listed in frontmatter `blocked_by` by path. Lets
  the tracker enforce order; leave empty when nothing blocks it.
- **References**: durable pointers the next session follows (parent epic,
  design doc, UI design) plus any `ADR-NNN` the story depends on.
  Canonical in the body; frontmatter `sources:` mirrors the links for sync

**Declare, don't narrate.** The drafting conversation is input, never
content. The body states standing facts in present tense: a resolved
decision enters as fact (`Reset links expire in 15 minutes`), never as
its history (`we discussed 24 hours but the user preferred 15 minutes`).
Strip conversation narrative — "as discussed", "the user confirmed",
"we agreed" — and decision history; an unresolved decision goes to Open
Questions, not the prose.

Record every durable reference (parent epic, design doc, UI design) in
frontmatter `sources:` as you draft -- one entry per source. These are
the pointers the resumption gate relies on.

Apply the resumption gate before proceeding:

> **Resumption gate** — Could a fresh session generate the spec from
> this story and its references, with no chat history? If no, add the
> missing piece (decision, content/copy, constraint, link) before saving.

### 3. Validate Acceptance Criteria

Load [ac-validation.md](ac-validation.md) and run V1-V8 on the drafted AC. Strict by default (V1-V3, V5, V7, V8); V4 is
strict on a duplicate Then with a confirm on `and`-joined Then; V6 surfaces a warning with confirm-to-continue.

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
- Save to markdown and proceed to step 5

**Saving to markdown:**
1. Count existing numbered story files (`NNN-` prefixed) in
   `.artifacts/epics/{epic-name}/`; zero-pad to 3 digits
2. Save to `.artifacts/epics/{epic-name}/{NNN}-{story-name}.md`

If `epic-tracker.kind` is not set, run [sync.md](sync.md) bootstrap first.

### 5. Update Epic Checklist *(markdown only)*

After saving to markdown, update the parent epic's Stories checklist to
replace the plain story name with a linked, numbered entry:

```markdown
- [ ] [003-reset-password-flow](003-reset-password-flow.md) -- brief description
```

## Editing an Existing Story

Creating a story runs the flow above; editing one runs this branch. It changes the body — title, prose, AC, rabbit holes, references — not status (status is set directly, against the tracker or the `status:` field). Create and edit hold the story to the same canonical contract: the template structure, its MUST-NOT boundaries, the AC contract, and requirement linkage — an edit conforms the result, never a free-form rewrite.

1. Load the story (by name, id, or tracker URL) — pull via [sync.md](sync.md) when it carries a `tracker.id`, else read its markdown.
2. Apply the edit as standing fact, not its history — the same **declare, don't narrate** discipline as create.
3. **Re-validate only when the AC block changed** — including a `**Satisfies**` line added, removed, or re-pointed. If it changed, load [ac-validation.md](ac-validation.md), run V1-V8 strict, and loop back on failure. An edit that leaves the AC block untouched skips validation: legacy informal AC is preserved, never retro-rewritten without an explicit edit.
4. Save or push as create does — dispatch through [sync.md](sync.md) when the story has a `tracker.id`, else write the markdown in place.

## Guidelines

**DO:**
- Write acceptance criteria that are testable without knowing
  implementation
- Keep scope tight — one story delivers one demonstrable user outcome, not a horizontal building block
- Reference the parent epic for broader context
- Update the epic's story checklist after creating the story

**DON'T:**
- Add a size field — sizing happens at implementation time
- Include implementation details or technical design
- Carry requirement IDs in prose — link them on each AC's `Satisfies` line; still strip `§x.x` section numbers, sibling names, and roadmap language
- Create stories without a parent epic (ask to create the epic first)

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{story-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: planned
sources: []
blocked_by: []  # paths of artifacts that must finish first (epic-name or epic-name/story-name); omit when nothing blocks this
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

MUST NOT contain: conversation narrative ("as discussed", "we agreed", "the user confirmed"), decision history, `§x.x` section numbers, sibling story names, roadmap language, or implementation details. Requirement IDs (`FR/BR/EC/NFR`) belong on each AC's `Satisfies` line, never the Summary; `ADR-NNN` belongs in References.

## Out of Scope

{Remove this section if nothing is ambiguous.}

- {{What this story explicitly does not cover}}

## Acceptance Criteria

### AC-1

**Given** {{precondition}}
**When** {{action}}
**Then** {{expected outcome}}
**Satisfies** {{parent-epic requirement this AC operationalizes — e.g. FR-3; omit the line when the AC maps to no requirement}}

{Add additional `### AC-N` blocks as needed. Each AC has exactly one Given/When/Then; the `**Satisfies**` line is optional and names one parent-epic requirement (`FR/BR/EC/NFR`).}

## Rabbit Holes

{Remove this section if not needed.}

- {{Execution trap specific to this story — edge case, ordering constraint, or integration quirk}}

MUST NOT contain: implementation advice, upstream design notes, cross-references to other documents, or a trap that belongs to a sibling story's domain (relocate it there).

## Open Questions

{Remove this section if nothing is undecided. Seeds the spec's discovery
— capture what's open so a fresh session knows what to ask, not re-decide.}

- {{Unknown to resolve during specify. A cross-cutting foundational decision may be marked blocked and suggest an ADR to settle it — never generate the ADR here.}}

MUST NOT contain: an unknown that gates no AC in this story (move it to the story whose domain it gates), or an authored ADR (suggest one, never generate it).

## References

{Durable pointers the next session follows to recover context. Canonical
home — travels into the tracker description; frontmatter `sources:`
mirrors these links for sync (markdown only, absent in tracker mode).}

- **Epic:** {{link to parent epic}}
- **Design Doc:** {{link or "None"}}
- **UI Design:** {{link or "None"}}
- **Decisions:** {{ADR-NNN this story depends on, or "None"}}
````

## Error Handling

- Epic doesn't exist: offer to create it first
- Story name conflicts: suggest alternative or confirm overwrite
- Story drafted without AC: ac-validation V1 fires; ask user to add at
  least one `### AC-N` block
