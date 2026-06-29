# Edit Story

Update an existing Story body (title, prose, AC, rabbit holes, references)
with diff-based AC re-validation. AC text changes re-run V1-V8 strict;
edits that don't touch AC text skip validation (legacy tolerance).

## When to Use

- User says "edit story", "update story body", "change story"
- User wants to change a Story's prose, AC, rabbit holes, or references
- Status-only changes route to [status.md](status.md), not here

This ref does not handle status transitions. `status.md` owns the status
field; edits here are body-level.

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

### 1. Identify Story

1. If user specifies a Story (by name, id, or tracker URL), load it.
2. If `tracker.id` is present in the artifact, source of truth is the
   tracker -- load via [sync.md](sync.md) pull direction.
3. Otherwise, read the markdown at `.artifacts/epics/{epic-name}/{NNN}-{story-name}.md`.
4. If ambiguous, list candidate Stories and ask which one.

### 2. Capture Edit

Present the current body to the user. Capture the proposed edit (full
revised body or a targeted section change). Hold the edit in memory; do
not write yet.

If the edit touches the title, keep it declarative — it names the
deliverable and maps to the tracker's summary field; narrative outcome
prose belongs only in the body's Summary section (see the Title rules
in [story.md](story.md)).

### 3. Diff AC Section

Extract the AC section from the pre-edit body and the post-edit body:

- Find `## Acceptance Criteria` heading.
- Read until the next `## ` heading or end of document.
- Normalize whitespace (collapse runs of blank lines, strip trailing
  spaces).
- Compare pre vs post by string equality. The `**Satisfies**` line is
  part of the AC block — adding, removing, or re-pointing it is an
  AC-text change.

Two branches:

**Branch 1 -- AC text unchanged:**
- The user touched only title, prose, rabbit holes, or references.
- No validation runs.
- Proceed to Step 4 (Save or Push).
- Covers AC-5 from the spec (legacy tolerance for stories created before
  Gherkin enforcement, when AC stays untouched).

**Branch 2 -- AC text changed:**
- The user added, removed, or modified AC text in any way.
- Load [ac-validation.md](ac-validation.md) and run V1-V8 strict against
  the new AC section.
- If any strict rule fails: surface the structured error, do not save
  or push, loop back to Step 2 (Capture Edit) until the user fixes the
  AC.
- If validation passes: proceed to Step 4.
- Covers AC-6 from the spec (any AC text change triggers full
  validation, regardless of pre-edit format).

### 4. Save or Push

**If tracker configured** (`git config --get epic-tracker.kind` returns a value and is not `none`) and the Story has a `tracker.id`:
- Load [sync.md](sync.md) push direction; dispatch the edit to the
  matching adapter.
- The adapter updates the tracker entity in place; no markdown file is
  created.

**If no tracker configured or Story is markdown-only:**
- Write the edited body to the existing markdown file at its current
  path. Update no other frontmatter fields.

If the edit changed status, route through [status.md](status.md) first;
this ref handles body only.

## Guidelines

**DO:**
- Diff the AC section before deciding whether to validate
- Run V1-V8 strict only when AC text actually changed
- Preserve legacy informal AC when the user did not touch them
- Keep status updates routed through `status.md`, not this ref
- Loop back to Capture Edit on validation failure rather than partial-saving

**DON'T:**
- Validate on every edit indiscriminately (contrasts: diff first, validate only when AC changed)
- Retroactively rewrite legacy AC into Gherkin without an explicit user edit (contrasts: preserve untouched AC)
- Mix status changes into body edits (contrasts: route status through status.md)
- Save or push partial edits when validation fails (contrasts: loop back to Capture Edit)

## Error Handling

- Story not found: list candidates from the epic or standalone area; ask
  user to clarify.
- Tracker unavailable mid-edit: surface the error; cache the proposed
  edit in memory; suggest retry once MCP returns.
- Validation fails on Branch 2: emit the structured error from
  `ac-validation.md`, return user to Step 2.
- Edit removes the AC section entirely: V1 fires (zero `### AC-N`
  blocks); reject the edit.
- Edit converts legacy informal AC into Gherkin: Branch 2 runs full
  validation; the conversion either passes or the user iterates.
- Concurrent tracker change since last sync: surface conflict via
  `sync.md` conflict detection before applying the edit.

## Outcomes

- On successful save: artifact reflects the edit; further status updates
  route through `status.md`.
- On successful push: tracker entity updated; `tracker.last_synced`
  refreshed in markdown frontmatter when a local cache exists.
