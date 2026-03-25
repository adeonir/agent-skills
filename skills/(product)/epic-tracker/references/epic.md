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
- Write acceptance criteria that are verifiable without knowing
  implementation details
- Include scope boundaries -- what's explicitly out helps as much as
  what's in
- List stories even if they'll be created later -- the checklist is
  the roadmap

**DON'T:**
- Include implementation details -- that's spec-driven's job. No
  technology names, frameworks, or patterns in the epic.
- Create story artifacts during epic creation -- just list them
- Skip the discover phase even if the user provides context directly
- Add size estimates -- spec-driven handles sizing

## Error Handling

- PRD has multiple milestones: ask which milestone maps to this epic
- User provides vague context: ask clarifying questions, don't assume
- Epic name conflicts with existing: suggest alternative or confirm
  overwrite
