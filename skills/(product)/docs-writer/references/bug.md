# Bug -- Bug Report

## When to Use

When reporting a bug or defect in the product.

## Workflow

```
structured collection --> drafting
```

No discovery or clarification needed. Collect structured fields directly and draft.

## Step 1: Structured Collection

Collect the following from the user:

1. **What happened?** (actual behavior)
2. **What should have happened?** (expected behavior)
3. **How to reproduce?** (step-by-step)
4. **Environment** (OS, browser, version, etc.)
5. **Workaround?** (any known mitigation)

If the user provides a brief description, ask for the missing fields. Don't ask for fields the user already covered.

## Step 2: Check Existing Context

Look for existing PRD at `.artifacts/docs/prd.md`.

If found: use to understand expected behavior and edge cases. PRD provides journeys (section 5), business rules (section 6), and edge cases (section 7) that help contextualize the bug.

## Drafting

**USE TEMPLATE:** `templates/bug.md`

Fill in fields from user input. Present draft for review before saving.

## Schema

6 sections matching `templates/bug.md`:

| Section | Content |
|---------|---------|
| 1. Description | Expected behavior vs actual behavior |
| 2. Steps to Reproduce | Numbered step-by-step reproduction |
| 3. Environment | OS, browser, device, version, environment |
| 4. Workaround | Known mitigation or "None known" |
| 5. Notes | Additional context, logs, screenshots, related info |
| 6. References | Links to related pitches, scopes, or PRD |

## Guidelines

- Titles should describe the symptom, not the cause: "Login fails with 500 error" not "Fix auth middleware"
- Expected vs actual behavior must be clearly separated
- Reproduction steps should be specific enough for someone else to follow
- Always ask about workarounds -- critical for triage prioritization
- Logs, screenshots, and other attachments go in Notes

## Output

Save to: `.artifacts/docs/bug.md`
