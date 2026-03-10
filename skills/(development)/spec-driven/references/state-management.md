# State Management

Persist decisions, blockers, lessons, and deferred ideas across sessions.

## When to Use

- After making significant decisions during any phase
- When a blocker is identified
- When a lesson is learned (something that worked or didn't)
- When an idea should be deferred for later
- When resuming work and needing context from previous sessions
- Explicitly triggered: "record decision", "log blocker", "add deferred idea"

## File Location

`.artifacts/state.md`

**USE TEMPLATE:** `templates/state.md`

## Workflow

### Reading State

Before starting work on any feature:

1. Check if `.artifacts/state.md` exists
2. If exists: scan for relevant decisions, active blockers, and deferred ideas related to the current work
3. If not exists: skip (will be created on first write)

### Writing State

After any phase completion or when significant information arises:

1. If `.artifacts/state.md` doesn't exist, create it from template
2. Add entry to the appropriate section
3. Use consistent date format (YYYY-MM-DD)

### Sections

#### Decisions

Record technical and product decisions that affect the project. Each entry includes:
- Date
- Decision made
- Rationale (why)
- Context (which feature or phase triggered it)

#### Blockers

Track active blockers preventing progress. Each entry includes:
- Date identified
- Description
- Impact (what is blocked)
- Status: `active` or `resolved`
- Resolution (when resolved)

#### Lessons

Things learned during development. Each entry includes:
- Date
- What happened
- Takeaway (what to do differently or repeat)

#### Deferred

Ideas, improvements, or features explicitly deferred for later. Each entry includes:
- Date
- Description
- Reason for deferring
- Priority suggestion (when to revisit)

## When to Update

| Event | Section | Action |
|-------|---------|--------|
| Architecture decision in plan phase | Decisions | Record decision + rationale |
| Gray area resolved in discuss | Decisions | Record decision + context |
| Dependency unavailable | Blockers | Add with impact description |
| Blocker resolved | Blockers | Update status to resolved |
| Quick fix reveals tech debt pattern | Lessons | Record pattern + suggestion |
| Quality gate catches recurring issue | Lessons | Record issue + prevention |
| Out-of-scope idea during specify | Deferred | Record with priority suggestion |
| Feature scope narrowed | Deferred | Move cut items here |

## Guidelines

- Keep entries concise -- one or two lines per entry
- Always include date and context
- Don't duplicate information already in spec.md or plan.md -- state.md is for cross-cutting concerns
- Review state.md at the start of each new feature for relevant context
- Resolved blockers stay in the file (for history) but are marked as resolved
- State is persistent -- don't delete entries, only add and update status

## Error Handling

- No .artifacts/: Create it and state.md from template
- State.md corrupted: Recreate from template, note loss of history
