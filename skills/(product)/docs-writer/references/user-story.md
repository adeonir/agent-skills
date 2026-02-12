# User Story -- Agile Format for User Value

## Workflow

```
discovery --> drafting
```

2-phase workflow. Discovery identifies the persona, action, and benefit. Drafting structures them into the agile format.

## Phase 1: Discovery

**LOAD:** [discovery.md](discovery.md) for shared interview patterns.

**Stage 1 -- Persona & Need:**
- Who is the user? (role, persona, or user type)
- What do they want to accomplish?
- Why is this valuable to them?

**Stage 2 -- Acceptance (if Stage 1 answers are clear enough):**
- How will we know this is done?
- What are the edge cases?
- Any constraints or dependencies?

Minimum 1 stage. Move to drafting when persona, action, and benefit are clear.

## Phase 2: Drafting

**USE TEMPLATE:** `templates/user-story.md`

### Story Format

```
As a [persona], I want [action], so that [benefit].
```

Each part must be specific:

| Part | Bad | Good |
|------|-----|------|
| Persona | "user" | "logged-in customer with active subscription" |
| Action | "search" | "filter search results by date range" |
| Benefit | "find things" | "quickly locate recent transactions" |

### Acceptance Criteria Format

Use WHEN/THEN/SHALL pattern:

```
WHEN [trigger/condition]
THEN [expected outcome]
SHALL [requirement/constraint]
```

Each story should have 2-5 acceptance criteria. Each criterion must be independently verifiable.

## Schema

- **Story ID**: Sequential (US-001, US-002, etc.)
- **Story**: "As a [persona], I want [action], so that [benefit]"
- **Acceptance Criteria**: WHEN/THEN/SHALL conditions
- **Priority**: P1 / P2 / P3
- **Estimate**: Story points or time (optional)
- **Dependencies**: Related stories or prerequisites
- **Notes**: Additional context

## Guidelines

- One user action per story -- if "and" appears in the action, split into multiple stories
- Benefits must describe user value, not implementation details
- Acceptance criteria should be testable by a non-technical person
- If a story is too large (epic), suggest breaking it down

## Output

Save to: `.specs/docs/story-{name}.md`
