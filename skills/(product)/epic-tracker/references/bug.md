# Report Bug

Document a defect with structured reproduction steps, severity, and
environment context.

## When to Use

- User wants to report a bug or defect
- User says "create bug", "report bug", "bug report"
- A defect is found during testing or production use

## Workflow

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

**USE TEMPLATE:** `templates/bug.md`

Fill the template:

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

### 5. Save

Save to `.artifacts/epics/{epic-name}/{bug-name}.md` or
`.artifacts/epics/standalone/{bug-name}.md`.

## Guidelines

**DO:**
- Always include steps to reproduce -- even if minimal
- Set severity based on user impact, not technical complexity
- Include the workaround if one exists
- Link to the parent epic when applicable

**DON'T:**
- Guess the severity -- ask the user if unclear
- Include fix suggestions -- that's spec-driven's job
- Skip the environment section for UI bugs
- Create a bug when the user actually wants a story (ask if ambiguous)

## Error Handling

- User can't provide reproduction steps: document what's known, mark
  as "intermittent" in the description
- Severity unclear: default to medium, flag for user review
- Duplicate bug suspected: show existing bugs in the same epic, ask
  if this is a duplicate
