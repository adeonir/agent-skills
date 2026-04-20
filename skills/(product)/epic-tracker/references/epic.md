# Create Epic

Plan a thematic container that groups related stories into a cohesive delivery unit.

## When to Use

- User wants to plan a new feature area or initiative
- User says "create epic", "new epic"
- A PRD or brief exists and needs to be broken into deliverable epics

## Workflow

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

**USE TEMPLATE:** `templates/epic.md`

Fill the template with discovered context:

- **Name**: kebab-case, descriptive (`user-authentication`,
  `payment-processing`)
- **Title**: human-readable title
- **Status**: always starts as `planned`
- **Prose context**: what the epic is about, why it exists, what changes
  for the user -- use a real scenario
- **Stories**: checklist of stories with brief descriptions. Each story
  becomes its own artifact later.
- **Scope**: explicit in/out boundaries. Describe capabilities, not
  technologies (e.g., "secure password storage" not "bcrypt hashing")
- **Rabbit Holes**: known complexities to flag early
- **Acceptance Criteria**: high-level verifiable conditions for the epic
  as a whole (not per-story)
- **References**: links to PRD, design doc, figma, or other sources

### 3. Review

Present the draft to the user. Wait for feedback before saving.

### 4. Save

Save to `.artifacts/epics/{epic-name}/epic.md`. Create the directory
if it doesn't exist.

## Guidelines

**DO:**
- Extract context from existing docs before asking questions
- Write acceptance criteria verifiable without knowing implementation details
- Include scope boundaries -- what's explicitly out helps as much as what's in
- List stories in the epic checklist; create them as separate artifacts later
- Run discover first, even when the user provides context directly
- Hand sizing off to spec-driven

**DON'T:**
- Include implementation details (contrasts: criteria stay implementation-agnostic)
- Create story artifacts during epic creation (contrasts: list stories in checklist, create on demand later)
- Skip discover (contrasts: run discover first regardless of provided context)
- Add size estimates (contrasts: sizing is spec-driven's job)

## Error Handling

- PRD has multiple milestones: ask which milestone maps to this epic
- User provides vague context: ask clarifying questions, don't assume
- Epic name conflicts with existing: suggest alternative or confirm
  overwrite
