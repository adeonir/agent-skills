# Discuss Feature

Resolve gray areas and ambiguities through structured conversation with the user.

## When to Use

- Spec has open questions that block planning or implementation
- Scope is **Complex** and specify detected ambiguous gray areas
- User explicitly asks to discuss a feature's requirements
- Requirements can be interpreted multiple ways

## Output

Creates `.artifacts/features/{ID}-{name}/decisions.md` with user decisions on gray areas.

**USE TEMPLATE:** `templates/decisions.md`

## Workflow

### Step 1: Resolve Feature

1. If ID provided -> use `.artifacts/features/{ID}-{name}/`
2. If no ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

### Step 2: Load Spec

Read `.artifacts/features/{ID}-{name}/spec.md`.

Extract:
- Open Questions section
- Any TBD markers in requirements or acceptance criteria
- Edge cases without clear resolution
- Contradictory or ambiguous requirements

If no gray areas found:
- Inform user the spec has no unresolved ambiguities
- Suggest proceeding to the next phase
- Exit

### Step 3: Categorize Gray Areas

Group ambiguities by type:

| Category | Signal | Example |
|----------|--------|---------|
| Behavior | "It depends", multiple interpretations | "Should expired links show an error or redirect?" |
| Scope | Boundary unclear | "Does 'user management' include role-based access?" |
| Priority | Trade-off without preference | "Performance vs simplicity for caching strategy?" |
| Domain | Missing domain knowledge | "What happens when a subscription lapses mid-billing?" |
| Constraint | Unstated limits | "Is there a max number of items per cart?" |

### Step 4: Structured Discussion

For each gray area, present to user:

```
Gray Area: {description}
Context: {why this matters for the feature}

Options:
(a) {option 1} -- {trade-off}
(b) {option 2} -- {trade-off}
(c) {option 3, if applicable} -- {trade-off}
```

**Discussion principles:**

- Present concrete options, not open-ended questions
- Explain trade-offs for each option (what you gain, what you lose)
- If the user doesn't know, suggest the safest default and mark as "tentative decision -- revisit if needed"
- Group related gray areas together -- resolving one may resolve others
- Don't overwhelm -- discuss 2-3 gray areas at a time, then check if user wants to continue

### Step 5: Record Decisions

For each resolved gray area, record:

- The question / ambiguity
- The decision made
- The rationale (why this option)
- Any caveats or conditions

### Step 6: Generate decisions.md

**USE TEMPLATE:** `templates/decisions.md`

Create `.artifacts/features/{ID}-{name}/decisions.md` with all decisions.

### Step 7: Update spec.md

- Remove resolved items from Open Questions
- Update TBD markers with decisions where applicable
- Add reference to decisions.md in Notes section

### Step 8: Update State

If `.artifacts/state.md` exists, record significant decisions that may affect other features.

### Step 9: Report

Inform user:
- Resolved: {count} gray areas
- Remaining: {count} open questions (if any)
- Created: `decisions.md`
- Next step based on scope:
  - **Large/Complex**: Run `plan`
  - **Medium**: Run `implement`

## Guidelines

- Never resolve ambiguities on behalf of the user -- always ask
- Present options with trade-offs, not just yes/no questions
- If a gray area is too complex for a quick decision, mark as "needs research" and defer to plan phase
- Group related decisions -- don't ask 15 questions one by one
- Tentative decisions are valid -- mark them clearly for future revisit

## Error Handling

- Spec not found: Suggest `specify`
- No gray areas: Inform user spec is clear, suggest next phase
- User unsure on all options: Suggest safest defaults, mark all as tentative
