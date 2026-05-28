# Create Epic

Plan a thematic container that groups related stories into a cohesive delivery unit.

## When to Use

- User wants to plan a new feature area or initiative
- User says "create epic", "new epic"
- A PRD or brief exists and needs to be broken into deliverable epics

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

### 1. Discover

Check for existing context before asking questions:

1. Look for `.artifacts/docs/prd.md` -- extract relevant milestones,
   functional requirements, and scope
2. Look for `.artifacts/docs/brief.md` -- extract value proposition
   and target audience
3. If found, summarize what was extracted and confirm with user
4. If not found, ask the user:
   - What problem does this epic solve?
   - Who benefits?
   - What changes for the user when this is done?

### 2. Draft

Fill the template (below) with discovered context:

- **Name**: kebab-case, descriptive (`user-authentication`,
  `payment-processing`)
- **Title**: short human-readable phrase, slug-safe. No commands,
  flags, file paths, parentheses, brackets, or pipes — becomes branch
  name slug downstream.
- **Status**: always starts as `planned`
- **Prose context**: what the epic is about, why it exists, what changes
  for the user -- use a real scenario
- **Stories**: checklist of stories with brief descriptions. Each story
  becomes its own artifact later. **Local-only** — when a tracker is
  configured, adapters strip this section from the body on push so the
  tracker's native child panel (Sub-issues, child issues, etc.) stays
  the single source of truth.
- **Scope**: explicit in/out boundaries. Describe capabilities, not
  technologies (e.g., "secure password storage" not "bcrypt hashing")
- **Rabbit Holes**: known complexities to flag early
- **Acceptance Criteria**: high-level verifiable conditions for the epic
  as a whole (not per-story)
- **References**: links to PRD, design doc, UI design, or other sources

### 3. Save or Push

**If tracker configured** (`.artifacts/epics/.config.yml` exists with
`tracker.kind` set and not `none`):
- Ask the user (per session, cached) whether to push to the tracker
- If yes: load [sync.md](sync.md) and dispatch using the draft content
  directly — no markdown file is created; the tracker is the source of
  truth
- If no: save to `.artifacts/epics/{epic-name}/epic.md`; push later via
  "sync to tracker"

**If no tracker configured** (config missing or `kind: none`):
- Save to `.artifacts/epics/{epic-name}/epic.md`; create the directory
  if it doesn't exist

If the config is missing, run [sync.md](sync.md) bootstrap before the
first push, then proceed.

## Guidelines

**DO:**
- Extract context from existing docs before asking questions
- Write acceptance criteria verifiable without knowing implementation details
- Include scope boundaries -- what's explicitly out helps as much as what's in
- List stories in the epic checklist; create them as separate artifacts later
- Run discover first, even when the user provides context directly
- Hand sizing off to the implementation phase

**DON'T:**
- Include implementation details (contrasts: criteria stay implementation-agnostic)
- Create story artifacts during epic creation (contrasts: list stories in checklist, create on demand later)
- Skip discover (contrasts: run discover first regardless of provided context)
- Add size estimates (contrasts: sizing is an implementation concern)

## Template

ALWAYS use this exact template structure:

````markdown
---
name: {{epic-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: planned
sources: []
# tracker block populated by sync.md after first push (omit until then):
# tracker:
#   kind: linear | github | jira
#   id: PROJ-123
#   url: https://...
#   last_synced: YYYY-MM-DDTHH:MM:SSZ
---

# {{Epic Title}}

## Summary

{{What the epic is about, why it exists, what changes for the user. Use a real scenario to illustrate the problem and the desired outcome.}}

## Stories

<!-- Local-only: stripped by adapters on push to a tracker. Tracker's
native child panel (GitHub Sub-issues, Linear sub-issues, Jira child
issues) is the source of truth for hierarchy once a tracker is wired. -->

- [ ] {{story-name}} — {{brief description of what this story delivers}}
- [ ] {{story-name}} — {{brief description}}

{Stories are linked when created: [001-story-name](001-story-name.md) — description}

## Scope

**In:**

- {{What's included}}

**Out:**

- {{What's explicitly excluded}}

## Acceptance Criteria

- [ ] {{High-level verifiable condition for the epic as a whole}}
- [ ] {{Another testable condition}}

## Rabbit Holes

- {{Known complexity or trap to avoid}}

## References

- **Brief:** {{link or "None"}}
- **PRD:** {{link or "None"}}
- **Design Doc:** {{link or "None"}}
- **UI Design:** {{link or "None"}}
````

## Error Handling

- PRD has multiple milestones: ask which milestone maps to this epic
- User provides vague context: ask clarifying questions, don't assume
- Epic name conflicts with existing: suggest alternative or confirm
  overwrite
