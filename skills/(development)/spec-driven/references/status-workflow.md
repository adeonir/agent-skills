# Status Workflow

Status management for spec-driven features.

## Status Values (EXACT)

Use ONLY these values in spec.md frontmatter:

| Status | Meaning | When to Use |
|--------|---------|-------------|
| `draft` | Initial state | After `initialize` - spec created, needs review |
| `ready` | Ready for planning | After `plan` - spec complete, open questions resolved |
| `in-progress` | Being implemented | After first `implement` task starts |
| `to-review` | Implementation done | After all tasks complete, ready for validation |
| `done` | Validated | After `validate` passes |
| `archived` | Moved to docs | After `archive` (feature directory can be deleted) |

## Status Transitions

```
draft --[plan]--> ready --[implement]--> in-progress --[all tasks done]--> to-review --[validate]--> done --[archive]--> archived
```

## Who Updates What

| Reference | Updates Status | From | To |
|-----------|---------------|------|-----|
| `initialize.md` | Yes | - | `draft` |
| `plan.md` | Yes | `draft` | `ready` |
| `tasks.md` | No | - | - |
| `implement.md` | Yes | `ready` | `in-progress` |
| `implement.md` | Yes | (tasks done) | `to-review` |
| `validate.md` | Yes | `to-review` | `done` |
| `archive.md` | No (requires `done`) | - | - |

## Critical Rules

1. **ONLY use the 6 values above** - never invent new status values
2. **Check current status before updating** - read spec.md frontmatter first
3. **Update at the END of the phase** - after completing all steps of that reference
4. **Never skip status** - follow the flow: draft → ready → in-progress → to-review → done → archived

## Frontmatter Format

```yaml
---
id: "001"
feature: "auth"
type: "greenfield"
status: ready  # <-- ONLY: draft, ready, in-progress, to-review, done, archived
branch: "main"
created: "2024-01-15"
---
```

## Common Mistakes to AVOID

❌ `status: planned` → Use `ready`
❌ `status: wip` → Use `in-progress`
❌ `status: completed` → Use `done`
❌ `status: finished` → Use `done`
❌ `status: in_review` → Use `to-review`
❌ `status: pending` → Use `draft` or `ready`

## Quick Reference

- Just created feature? → `draft`
- Spec reviewed and complete? → `ready`
- Started coding? → `in-progress`
- All tasks done, need review? → `to-review`
- Validated and working? → `done`
- Moved to docs/features/? → `archived`
