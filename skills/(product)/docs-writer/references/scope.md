# Scope -- Technical Work Item

## When to Use

When creating a technical work item that belongs to a pitch (feature).

## Workflow

```
drafting (direct)
```

No discovery needed. Scopes are concrete slices of work within a pitch. The user already knows what needs to be done. Collect structured fields and draft.

Ask the user for the scope details. If they provide a brief description, fill in reasonable defaults and present for review.

### Required Fields

1. **Title**: What this scope covers (descriptive, not action-oriented)
2. **Description**: What needs to happen and why
3. **Parent Pitch**: Which pitch this scope belongs to (or "standalone")

### Optional Fields

4. **Scope In**: What's included in this slice
5. **Scope Out**: What's excluded from this slice

## Drafting

**USE TEMPLATE:** `templates/scope.md`

Fill in fields from user input. Present draft for review before saving.

## Guidelines

**DO:**
- Define a slice of work, not a full feature -- that is the pitch's job
- Make each scope an integrated piece (frontend + backend together when possible)
- Keep scopes small enough to finish in a few days, large enough to be meaningful
- Mark scopes without a parent pitch as standalone work (maintenance, refactoring, etc.)

**DON'T:**
- Add acceptance criteria -- validation happens at the pitch level
- Make scopes so large they become features
- Split frontend and backend into separate scopes when they belong together

## Output

Save to: `.artifacts/docs/scope.md`
