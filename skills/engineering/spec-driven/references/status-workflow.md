# Status Workflow

Status management for spec-driven features.

## When to Use

Auto-loaded as a reference for feature status transitions. Not a direct trigger.

## Status Values (EXACT)

Use ONLY these values in spec.md frontmatter:

| Status | Meaning | When to Use |
|--------|---------|-------------|
| `draft` | Initial state | After `specify` - spec created, may have open questions |
| `ready` | Ready for implementation | After `design` - spec complete, architecture defined |
| `in-progress` | Being implemented | After first `implement` task starts |
| `to-review` | Implementation complete, awaiting Goals/Success audit | After `implement` finishes all tasks and per-task verify passes |
| `done` | Complete | After `audit` confirms Goals and Success Criteria are met |

## Status Transitions

```
draft --[design]--> ready --[implement]--> in-progress --[implement done]--> to-review --[audit]--> done
```

**For Medium scope** (design/tasks skipped):
```
draft --[implement]--> in-progress --[implement done]--> to-review --[audit]--> done
```

## Who Updates What

| Reference | Updates Status | From | To |
|-----------|---------------|------|-----|
| `specify.md` | Yes | - | `draft` |
| `design.md` | Yes | `draft` | `ready` |
| `tasks.md` | No | - | - |
| `implement.md` | Yes | `draft` or `ready` | `in-progress` |
| `implement.md` | Yes | (all tasks done + per-task verify passed) | `to-review` |
| `verify.md` | No (only marks AC `[x]` in spec.md body) | - | - |
| `audit.md` | Yes | `to-review` | `done` |
| `validate.md` | No (may revert AC/Goal/Success `[x]` if UAT reproves) | - | - |

## Critical Rules

1. **ONLY use the 5 values above** - never invent new status values
2. **Check current status before updating** - read spec.md frontmatter first
3. **Update at the END of the phase** - after completing all steps of that reference
4. **Never skip status** - follow the flow (exceptions: Medium scope can go draft -> in-progress)

## Frontmatter Format

```yaml
---
id: "001"
feature: "auth"
type: "greenfield"
scope: "large"
status: ready  # <-- ONLY: draft, ready, in-progress, to-review, done
branch: "main"
created: "2024-01-15"
---
```

## Common Mistakes to AVOID

- `status: planned` -> Use `ready`
- `status: wip` -> Use `in-progress`
- `status: completed` -> Use `done`
- `status: finished` -> Use `done`
- `status: in_review` -> Use `to-review`
- `status: pending` -> Use `draft` or `ready`
- `status: archived` -> Use `done` (no archive phase)

## Quick Reference

- Just created feature? -> `draft`
- Design complete (or skipped for Medium)? -> `ready` (or stay `draft` if Medium)
- Started coding? -> `in-progress`
- All tasks done, per-task verify passed? -> `to-review`
- Goals and Success Criteria audited and met? -> `done`
