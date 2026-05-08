# Create Issue

Document a unit of internal work that is not user-facing (like a story)
and not a defect (like a bug). Use for infrastructure, refactoring,
tooling, research, CI/CD, documentation, or any chore-type work.

## When to Use

- User wants to file a chore, internal task, or non-feature work item
- User says "create issue", "new issue", "add issue", "chore", "task"
- Work is internal (CI setup, dependency upgrade, refactor) — not a
  user-facing feature and not a defect

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

> When working within an epic: read the epic folder contents before
> drafting — `epic.md` sets the scope and existing artifacts provide
> naming context.

### 1. Identify Epic (optional)

1. Ask the user whether this issue belongs to an epic or is standalone
2. If epic specified, load `.artifacts/epics/{epic-name}/epic.md` for
   context
3. If standalone (no epic): place in `standalone/`

### 2. Draft

Fill the template (below):

- **Name**: kebab-case, descriptive (`upgrade-node-20-actions`,
  `refactor-auth-middleware`, `setup-sentry`)
- **Title**: human-readable title
- **Type**: always `issue`
- **Epic**: parent epic name, or omit for standalone issues
- **Status**: always starts as `planned`
- **Description**: what needs to be done and why — one clear outcome
- **Checklist**: optional breakdown into sub-steps; omit if not needed
- **Rabbit Holes**: optional; known complexities or hidden risks; omit
  for trivial chores
- **References**: link to parent epic, related stories, external docs

### 3. Review

Present the draft to the user. Wait for feedback before saving or
pushing.

### 4. Save or Push

**If tracker configured** (`.artifacts/epics/.config.yml` exists with
`tracker.kind` set and not `none`):
- Ask the user (per session, cached) whether to push to the tracker
- If yes: load [sync.md](sync.md) and dispatch using the draft content;
  pass the parent epic's tracker id (from `epic.md` frontmatter
  `tracker.id`) when applicable — no markdown file is created
- If no: save to `.artifacts/epics/{epic-name}/{issue-name}.md` or
  `.artifacts/epics/standalone/{issue-name}.md`

**If no tracker configured** (config missing or `kind: none`):
- Save to `.artifacts/epics/{epic-name}/{issue-name}.md` or
  `.artifacts/epics/standalone/{issue-name}.md`

If the config is missing, run [sync.md](sync.md) bootstrap before the
first push, then proceed.

## Guidelines

**DO:**
- Use for internal work that has no direct user-facing outcome
- Keep the description focused on one outcome per issue
- Add a checklist when the work has clear sequential sub-steps
- Link to the parent epic when the issue advances an epic's delivery

**DON'T:**
- Use for user-facing features (contrasts: use story for user outcomes)
- Use for defects (contrasts: use bug for defects with repro steps)
- Add acceptance criteria (contrasts: description + checklist is enough)
- Create an issue when a story or bug is the right type (ask if
  ambiguous)

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{issue-name}}
title: {{Issue Title}}
type: issue
epic: {{epic-name or omit for standalone}}
status: planned
created: {{YYYY-MM-DD}}
# tracker block populated by sync.md after first push (omit until then):
# tracker:
#   kind: linear | github-issues | github-projects | jira
#   id: PROJ-123
#   url: https://...
#   last_synced: YYYY-MM-DDTHH:MM:SSZ
---

# {{Issue Title}}

{{What needs to be done and why. One clear outcome.}}

## Checklist

{Remove this section if not needed.}

- [ ] {{Step or sub-task}}

## Rabbit Holes

{Remove this section if not needed.}

- {{Known complexity or hidden risk}}

## References

- **Epic:** {{link to parent epic or "None"}}
- {{link or "None"}}
````

## Error Handling

- Ambiguous type (issue vs bug vs story): ask the user to clarify intent
- Epic not found: list available epics, offer to create one or go
  standalone
- Issue name conflicts: suggest alternative or confirm overwrite
