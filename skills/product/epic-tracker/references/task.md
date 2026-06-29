# Create Task

Document a unit of internal work that is not user-facing (like a story)
and not a defect (like a bug). Use for infrastructure, refactoring,
tooling, research, CI/CD, documentation, or any chore-type work.

## When to Use

- User wants to file a chore, internal task, or non-feature work item
- User says "create task", "new task", "add task", "chore"
- Work is internal (CI setup, dependency upgrade, refactor) — not a
  user-facing feature and not a defect

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

> When working within an epic: read the epic folder contents before
> drafting — `epic.md` sets the scope and existing artifacts provide
> naming context.

### 1. Parse Pasted Context

If the user pasted context (PR link, dependency advisory, config dump,
runbook output, dashboard screenshot, thread excerpt):

1. **Extract signals** — pull out and structure:
   - Links: PR/task URLs, advisory URLs, dashboard URLs, runbook URLs,
     thread permalinks
   - Identifiers: PR number, commit hash, dep version, deployment id
   - Scope hints: services, file paths, or area mentioned
   - Motivation: deadline, blocker, dependency, advisory severity
2. **Populate frontmatter `sources`** with every URL or id detected
3. **Infer the outcome** — what success looks like from the paste
4. **Ask only for gaps** — do not re-ask for fields already in the
   paste

If no context was pasted, proceed to step 2.

### 2. Identify Epic (optional)

1. Ask the user whether this task belongs to an epic or is standalone
2. If epic specified, load `.artifacts/epics/{epic-name}/epic.md` for
   context
3. If standalone (no epic): place in `standalone/`
4. When the task implements PRD requirements, read the PRD for context
   only (via the parent epic's `**PRD:**` link, or directly for a
   standalone task), propose the requirement IDs it satisfies, confirm
   with the user, and record them in `## Requirements`. Pure chores that
   map to no requirement omit the section.

### 3. Draft

Fill the template (below):

- **Name**: kebab-case, descriptive (`upgrade-node-20-actions`,
  `refactor-auth-middleware`, `setup-sentry`)
- **Title**: short human-readable phrase, slug-safe. No commands,
  flags, file paths, parentheses, brackets, or pipes — becomes branch
  name slug downstream. Declarative — names the work
  (`Upgrade CI runner image`), never a narrative outcome (`Builds run
  faster on the new image`). The title maps to the tracker's summary
  field on push; outcome prose lives only in the body's Summary
  section.
- **Type**: always `task`
- **Epic**: parent epic name, or omit for standalone tasks
- **Status**: always starts as `planned`
- **Description**: what needs to be done and why — one clear outcome
- **Requirements**: PRD requirement IDs this task satisfies
  (`FR/BR/EC/NFR`, plus `ADR-NNN` when it depends on a decision); omit
  for chores that map to no requirement
- **Signals**: links and ids from pasted context — PRs, advisories,
  configs, dashboards; omit if empty
- **Checklist**: optional breakdown into sub-steps; omit if not needed
- **Rabbit Holes**: optional; known complexities or hidden risks; omit
  for trivial chores
- **Blocked by**: work that must finish before this task can start,
  listed in frontmatter `blocked_by` by path; leave empty when nothing
  blocks it.
- **References**: link to parent epic, related stories, external docs

Apply the resumption gate before proceeding:

> **Resumption gate** — Could a fresh session resume the work from this
> task and its references, with no chat history? If no, add the missing
> piece (link, advisory, config snippet, signal) before saving.

### 4. Save or Push

**If tracker configured** (`git config --get epic-tracker.kind` returns a value and is not `none`):
- Ask the user (per session, cached) whether to push to the tracker
- If yes: load [sync.md](sync.md) and dispatch using the draft content;
  pass the parent epic's tracker id (from `epic.md` frontmatter
  `tracker.id`) when applicable — no markdown file is created
- If no: save to `.artifacts/epics/{epic-name}/{task-name}.md` or
  `.artifacts/epics/standalone/{task-name}.md`

**If no tracker configured** (`epic-tracker.kind` not set or `none`):
- Save to `.artifacts/epics/{epic-name}/{task-name}.md` or
  `.artifacts/epics/standalone/{task-name}.md`

If `epic-tracker.kind` is not set, run [sync.md](sync.md) bootstrap first.

## Guidelines

**DO:**
- Use for internal work that has no direct user-facing outcome
- Keep the description focused on one outcome per task
- Add a checklist when the work has clear sequential sub-steps
- Link to the parent epic when the task advances an epic's delivery

**DON'T:**
- Use for user-facing features (contrasts: use story for user outcomes)
- Use for defects (contrasts: use bug for defects with repro steps)
- Add acceptance criteria (contrasts: description + checklist is enough)
- Create an task when a story or bug is the right type (ask if
  ambiguous)

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{task-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: planned
sources: []
blocked_by: []  # paths of artifacts that must finish first (epic-name/story-name or standalone/name); omit when nothing blocks this
type: task
epic: {{epic-name or omit for standalone}}
# tracker block populated by sync.md after first push (omit until then):
# tracker:
#   kind: linear | github
#   id: PROJ-123
#   url: https://...
#   last_synced: YYYY-MM-DDTHH:MM:SSZ
---

# {{Task Title}}

## Summary

{{What needs to be done and why. One clear outcome.}}

## Signals

{Source links and identifiers from pasted context. Remove this section if not needed.}

- **Links:** {{PR URLs, advisory URLs, dashboard URLs, runbook URLs}}
- **Identifiers:** {{PR number, commit hash, dep version, deployment id}}

## Checklist

{Remove this section if not needed.}

- [ ] {{Step or sub-task}}

## Requirements

{Remove this section when the task maps to no PRD requirement.}

- {{PRD requirement IDs this task satisfies — e.g. FR-3, NFR-1; add ADR-NNN when it depends on a decision}}

## Rabbit Holes

{Remove this section if not needed.}

- {{Known complexity or hidden risk}}

## References

{Durable pointers the next session follows to recover context. Canonical
home — travels into the tracker description; frontmatter `sources:`
mirrors these links for sync (markdown only, absent in tracker mode).
`## Signals` above holds forensic links, not context pointers.}

- **Epic:** {{link to parent epic or "None"}}
- {{link or "None"}}
````

## Error Handling

- Ambiguous type (task vs bug vs story): ask the user to clarify intent
- Epic not found: list available epics, offer to create one or go
  standalone
- Task name conflicts: suggest alternative or confirm overwrite
