# Status Workflow

Status management for spec-driven features.

## When to Use

Auto-loaded as a reference for feature status transitions. Not a direct trigger.

## Status Values (EXACT)

Use ONLY these values in spec.md frontmatter:

| Status | Meaning | When to Use |
|--------|---------|-------------|
| `draft` | Initial state | After `specify` - spec created, may have open questions |
| `ready` | Ready for execution | After `plan` - spec complete, architecture defined |
| `in-progress` | Being executed | After first `execute` task starts |
| `done` | Complete | After `execute` completes all tasks and verification passes |

## Status Transitions

```
draft --[plan]--> ready --[execute]--> in-progress --[execute done]--> done
```

**For Medium scope** (plan/tasks skipped):
```
draft --[execute]--> in-progress --[execute done]--> done
```

## Who Updates What

| Reference | Updates Status | From | To |
|-----------|---------------|------|-----|
| `specify.md` | Yes | - | `draft` |
| `plan.md` | Yes | `draft` | `ready` |
| `tasks.md` | No | - | - |
| `execute.md` | Yes | `draft` or `ready` | `in-progress` |
| `execute.md` | Yes | (all done + verified) | `done` |

## Critical Rules

1. **ONLY use the 4 values above** - never invent new status values
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
status: ready  # <-- ONLY: draft, ready, in-progress, done
branch: "main"
created: "2024-01-15"
---
```

## Common Mistakes to AVOID

- `status: planned` -> Use `ready`
- `status: wip` -> Use `in-progress`
- `status: completed` -> Use `done`
- `status: finished` -> Use `done`
- `status: in_review` -> Use `done` (no separate review status)
- `status: to-review` -> Use `done` (no separate review status)
- `status: pending` -> Use `draft` or `ready`
- `status: archived` -> Use `done` (no archive phase)

## Quick Reference

- Just created feature? -> `draft`
- Plan complete (or skipped for Medium)? -> `ready` (or stay `draft` if Medium)
- Started coding? -> `in-progress`
- All tasks done and verified? -> `done`
