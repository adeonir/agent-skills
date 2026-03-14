# Issue -- Work Item

## When to Use

When creating a work item that belongs to an epic (or stands alone for maintenance, refactoring, etc.).

## Workflow

```
drafting (direct)
```

No discovery needed. Issues are concrete units of work within an epic. The user already knows what needs to be done. Collect structured fields and draft.

Ask the user for the issue details. If they provide a brief description, fill in reasonable defaults and present for review.

### Required Fields

1. **Title**: What this issue covers (descriptive, not action-oriented)
2. **Description**: What needs to happen and why
3. **Context**: Why this work matters -- link to the epic or broader goal
4. **Parent Epic**: Which epic this issue belongs to (or "standalone")

### Optional Fields

5. **Scope In**: What's included in this slice
6. **Scope Out**: What's excluded from this slice

## Drafting

**USE TEMPLATE:** `templates/issue.md`

Fill in fields from user input. Present draft for review before saving.

## Guidelines

**DO:**
- Define a unit of work, not a full feature -- that is the epic's job
- Make each issue an integrated piece (frontend + backend together when possible)
- Keep issues small enough to finish in a few days, large enough to be meaningful
- Include context that links back to the epic or explains motivation
- Mark issues without a parent epic as standalone work (maintenance, refactoring, etc.)

**DON'T:**
- Add acceptance criteria -- validation happens at the epic level
- Make issues so large they become features
- Split frontend and backend into separate issues when they belong together

## Output

Save to: `.artifacts/docs/issue.md`
