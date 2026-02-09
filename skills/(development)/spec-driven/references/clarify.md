# Clarify Requirements

Resolve ambiguities in specification.

## When to Use

- Spec has [NEEDS CLARIFICATION] markers
- Requirements are unclear
- Before planning

## Process

### Step 1: Resolve Feature

1. If ID provided -> use `.specs/features/{ID}-{name}/`
2. If no ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

### Step 2: Scan for Clarifications

Search for `[NEEDS CLARIFICATION: ...]` markers.

If none found:
- Inform spec is clear
- Suggest `plan`

### Step 3: Present Questions

For each clarification:
- Show context
- Ask specific question
- Offer options if applicable

### Step 4: Update Spec

Replace marker with clarified content:

Before:
```markdown
- [ ] FR-003: [NEEDS CLARIFICATION: What is the timeout?]
```

After:
```markdown
- [ ] FR-003: Timeout must be 30 seconds
```

### Step 5: Check for New Questions

Sometimes clarification reveals new questions.

If new questions found:
- Mark them
- Continue process

### Step 6: Report

Show summary:
- Clarifications resolved: {count}
- New questions: {count}

If all clear:
- Suggest `plan`

## Error Handling

- Spec not found: Suggest `initialize`
- User unsure: Keep as [NEEDS CLARIFICATION], move on
