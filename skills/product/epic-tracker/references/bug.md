# Report Bug

Document a defect with structured reproduction steps, severity, and
environment context.

## When to Use

- User wants to report a bug or defect
- User says "create bug", "report bug", "bug report"
- A defect is found during testing or production use

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

> When working within an epic: read the epic folder contents before
> collecting information — `epic.md` sets the scope and existing artifacts
> provide naming context.

### 1. Collect Information

Ask the user for (skip what's already provided):

1. **What happened vs what should happen** -- expected and actual
   behavior
2. **Steps to reproduce** -- ordered steps to trigger the bug
3. **Severity** -- critical (system down), high (major feature broken),
   medium (workaround exists), low (cosmetic/minor)
4. **Environment** -- browser, OS, device, app version, environment
   (optional, ask only if relevant)
5. **Workaround** -- any known mitigation
6. **Related epic** -- which epic this bug belongs to, if any

### 2. Determine Location

- If the bug relates to an epic: save in that epic's folder
- If standalone (no epic): save in `standalone/`
- If unsure: ask the user

### 3. Draft

Fill the template (below):

- **Name**: kebab-case, descriptive (`broken-pix-redirect`,
  `login-timeout-error`)
- **Title**: human-readable title describing the defect
- **Epic**: parent epic name, or omit for standalone bugs
- **Type**: always `bug`
- **Status**: always starts as `planned`
- **Severity**: critical, high, medium, or low
- **Description**: expected vs actual behavior, impact statement
- **Steps to Reproduce**: numbered, specific steps
- **Environment**: table of relevant environment details (optional)
- **Workaround**: known mitigation or "None known"
- **References**: link to parent epic, related stories, logs

### 4. Review

Present the draft to the user. Wait for feedback before saving.

### 5. Save or Push

**If tracker configured** (`.artifacts/epics/.config.yml` exists with
`tracker.kind` set and not `none`):
- Ask the user (per session, cached) whether to push to the tracker
- If yes: load [sync.md](sync.md) and dispatch using the draft content;
  the adapter adds `bug` label and severity labels (Jira uses the native
  `Bug` issue type) — no markdown file is created
- If no: save to `.artifacts/epics/{epic-name}/{bug-name}.md` or
  `.artifacts/epics/standalone/{bug-name}.md`

**If no tracker configured** (config missing or `kind: none`):
- Save to `.artifacts/epics/{epic-name}/{bug-name}.md` or
  `.artifacts/epics/standalone/{bug-name}.md`

If the config is missing, run [sync.md](sync.md) bootstrap before the
first push, then proceed.

## Guidelines

**DO:**
- Always include steps to reproduce -- even if minimal
- Set severity based on user impact, not technical complexity
- Include the workaround if one exists
- Link to the parent epic when applicable

**DON'T:**
- Guess the severity -- ask the user if unclear
- Include fix suggestions — implementation is a downstream concern
- Skip the environment section for UI bugs
- Create a bug when the user actually wants a story (ask if ambiguous)

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{bug-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: planned
sources: []
epic: {{epic-name or omit for standalone}}
type: bug
severity: {{critical/high/medium/low}}
# tracker block populated by sync.md after first push (omit until then):
# tracker:
#   kind: linear | github-issues | github-projects | jira
#   id: PROJ-123
#   url: https://...
#   last_synced: YYYY-MM-DDTHH:MM:SSZ
---

# {{Bug Title}}

## Summary

{{Brief one-sentence description of the defect.}}

## Expected

{{What should happen}}

## Actual

{{What actually happens}}

## Impact

{{Who is affected and how severely}}

## Steps to Reproduce

1. {{First action}}
2. {{Next step}}
3. {{Step where the bug manifests}}

## Environment

| Field | Value |
|-------|-------|
| Browser | {{e.g., Chrome 122}} |
| OS | {{e.g., macOS 15}} |
| Device | {{e.g., Desktop / iPhone 15}} |
| Version | {{App version or commit hash}} |
| Environment | {{Production / Staging / Local}} |

## Workaround

{{Known mitigation, or "None known"}}

## References

- **Epic:** {{link to parent epic, or "None"}}
- **Related stories:** {{links or "None"}}
````

## Error Handling

- User can't provide reproduction steps: document what's known, mark
  as "intermittent" in the description
- Severity unclear: default to medium, flag for user review
- Duplicate bug suspected: show existing bugs in the same epic, ask
  if this is a duplicate
