# Create Task

Document a general unit of actionable work — anything that is not a user
story with acceptance criteria and not a defect. Commonly infrastructure,
refactoring, tooling, research, CI/CD, or documentation. A task is defined
by form, not audience: no user-story frame, no acceptance criteria,
measured by a Definition of Done.

## When to Use

- User wants to file a task, chore, or general work item
- User says "create task", "new task", "add task", "chore"
- Work is not framed as a user story with acceptance criteria and is not
  a defect — measured by a Definition of Done, whatever its audience

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

A task carries no requirement IDs and no acceptance criteria — it is
AC-less work measured by its `## Definition of Done`. Work that delivers
a PRD requirement and needs verifiable acceptance criteria is a story,
not a task. When the type is unclear, see [discriminator.md](discriminator.md).

### 3. Draft

Fill the template (below):

- **Name**: kebab-case, descriptive (`upgrade-node-20-actions`,
  `refactor-auth-middleware`, `setup-sentry`)
- **Title**: short human-readable phrase, slug-safe. No commands,
  flags, file paths, parentheses, brackets, or pipes — becomes branch
  name slug downstream. Declarative — names the work
  (`Upgrade CI runner image`), never a narrative outcome (`Builds run
  faster on the new image`). The name is translated from its source,
  not copied: strip any borrowed token — reference or ticket codes,
  section numbers, code identifiers, document or sibling-artifact
  names — which travel in References or the body, never the title. The
  title maps to the tracker's summary field on push; outcome prose
  lives only in the body's Summary section.
- **Type**: always `task`
- **Epic**: parent epic name, or omit for standalone tasks
- **Status**: always starts as `planned`
- **Description**: what needs to be done and why — one clear outcome
- **Signals**: links and ids from pasted context — PRs, advisories,
  configs, dashboards; omit if empty
- **Definition of Done**: the conditions that mark the task complete —
  its done-contract; verifiable items, not sub-step narration
- **Rabbit Holes**: optional; known complexities or hidden risks; omit
  for trivial chores
- **Blocked by**: work that must finish before this task can start,
  listed in frontmatter `blocked_by` by path; leave empty when nothing
  blocks it.
- **References**: link to parent epic, related stories, external docs,
  and any `ADR-NNN` the task depends on

**Declare, don't narrate.** The collected answers and pasted context
are input, never content. The body states standing facts in present
tense: a resolved decision enters as fact (`CI runs on the Node 20
image`), never as its history (`we discussed staying on Node 18 but
decided to upgrade`). Strip conversation narrative — "as discussed",
"the user confirmed", "we agreed" — and decision history.

**Translate, don't replicate.** Sources (advisory, PR, design doc, ADR,
epic) stay read-only. Extract only what maps to this task, then
translate into its own language: strip reference and ticket codes,
`§x.x` section numbers, code identifiers, document and sibling-artifact
names. The task carries the facts, not the source's tokens — reference
codes travel in References, source links in Signals.

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
- Use for general actionable work that isn't a user story with AC or a defect
- Keep the description focused on one outcome per task
- Write a Definition of Done — the verifiable conditions that mark the task complete
- Link to the parent epic when the task advances an epic's delivery

**DON'T:**
- Use for work that delivers a PRD requirement with acceptance criteria (contrasts: that's a story)
- Use for defects (contrasts: use bug for defects with repro steps)
- Add acceptance criteria — a task is AC-less (contrasts: description + Definition of Done is enough; AC belongs to a story)
- Create a task when a story or bug is the right type (ask if
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
epic: {{epic-name or omit for standalone}}
type: task
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

MUST NOT contain: conversation narrative ("as discussed", "we agreed", "the user confirmed"), decision history, `§x.x` section numbers, document or reference codes, sibling-artifact names, or code identifiers and mechanism walkthroughs (`store.publish()`, "the write-through compares..."). Reference codes (`ADR-NNN`, ticket ids) travel in References; source links and ids in Signals.

## Signals

{Source links and identifiers from pasted context. Remove this section if not needed.}

- **Links:** {{PR URLs, advisory URLs, dashboard URLs, runbook URLs}}
- **Identifiers:** {{PR number, commit hash, dep version, deployment id}}

## Definition of Done

- [ ] {{condition that marks this task complete — verifiable, not sub-step narration}}

## Rabbit Holes

{Remove this section if not needed.}

- {{Known complexity or hidden risk}}

MUST NOT contain: implementation advice, upstream design notes, or cross-references to other documents.

## References

{Durable pointers the next session follows to recover context. Canonical
home — travels into the tracker description; frontmatter `sources:`
mirrors these links for sync (markdown only, absent in tracker mode).
`## Signals` above holds forensic links, not context pointers.}

- **Epic:** {{link to parent epic or "None"}}
- **Decisions:** {{ADR-NNN this task depends on, or "None"}}
- {{link or "None"}}
````

## Error Handling

- Ambiguous type (task vs bug vs story): ask the user to clarify intent
- Epic not found: list available epics, offer to create one or go
  standalone
- Task name conflicts: suggest alternative or confirm overwrite
