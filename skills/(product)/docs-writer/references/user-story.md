# User Story -- Agile Format for User Value

## When to Use

When writing user stories for development planning.

## Workflow

```
[clarification] --> drafting
```

Direct drafting with optional clarification. The user comes with the persona, action, and benefit -- only clarify when input is incomplete.

## Step 1: Check Existing Context

Look for existing PRD at `.artifacts/docs/prd.md`.

If found: read and use as context for drafting. PRD provides personas (section 3), scope (section 4), journeys (section 5), and business rules (section 6) that inform story writing. Less clarification needed.

If no PRD exists: rely on user input and clarify more proactively.

## Step 2: Clarification (when input is incomplete)

Evaluate the user's input (and PRD context if available) against the sufficiency criteria below. If all criteria are met, skip directly to drafting. If gaps exist, ask only about the gaps.

### Persona & Need

**Sufficient when:**
- Persona is specific enough to distinguish from other user types
- Action is a single, clear interaction
- Benefit describes user value, not system behavior

**Clarify when:**
- Generic "user" → "What role or context are they in? Describe a specific person."
- Action too broad → "Can you break this down? What's the specific interaction?"
- Benefit is implementation detail → "That's how, not why. What value does the user get?"

### Acceptance Criteria

**Sufficient when:**
- 2-5 verifiable acceptance criteria exist
- Key edge cases identified or noted as TBD

**Clarify when:**
- Criteria too vague → "What does 'working' look like? Walk me through the scenario."
- Missing edge cases → "What happens when [boundary condition]?"

## Drafting

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

Use checklist format as default. Each criterion must be independently verifiable:

```
- [ ] Search results display within 2 seconds
- [ ] Empty state shows "No results found" with suggested terms
- [ ] Minimum 3 characters required to trigger search
```

For complex behavioral flows, use Given/When/Then:

```
- [ ] Given a logged-in user with items in cart, When they click "checkout", Then they see the payment form with saved address pre-filled
```

Each story should have 2-5 acceptance criteria.

## Schema

7 sections matching `templates/user-story.md`:

| Section | Content |
|---------|---------|
| 1. Story | "As a [persona], I want [action], so that [benefit]" |
| 2. Context | Why this story exists, problem it solves, parent epic/journey |
| 3. Acceptance Criteria | 2-5 verifiable conditions (checklist or Given/When/Then) |
| 4. Technical Notes | Constraints and implementation hints (when applicable) |
| 5. Out of Scope | What this story explicitly does not cover |
| 6. Dependencies | Related stories or prerequisites |
| 7. References | Links to PRD, TDD, Figma, blockers |

## Guidelines

- One user action per story -- if "and" appears in the action, split into multiple stories
- Benefits must describe user value, not implementation details
- Acceptance criteria should be testable by a non-technical person
- If a story is too large (epic), suggest breaking it down
- Definition of Done belongs at team level, not per-story -- don't duplicate it
- Technical tasks and spikes don't need "As a..." framing -- use the right format for the work type

## Output

Save to: `.artifacts/docs/story.md`
