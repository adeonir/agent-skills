# Status and Listing

List features and show detailed status.

## When to Use

When listing features or checking the status of a specific feature.

## Commands

### List All Features

```
list features
show specs
```

### Show Specific Feature

```
show status
status of auth feature
```

## Workflow

### List Features

1. Scan `.artifacts/features/`
2. Read spec.md frontmatter from each
3. Group by status
4. Display table

**Output:**
```markdown
## Features

### In Progress
| ID | Feature | Scope | Branch | Created |
|----|---------|-------|--------|---------|
| 003 | auth | large | feat/auth | 2024-01-15 |

### Ready
| ID | Feature | Scope | Branch | Created |
|----|---------|-------|--------|---------|
| 002 | payments | complex | feat/payments | 2024-01-10 |

### Done
| ID | Feature | Scope | Branch | Created |
|----|---------|-------|--------|---------|
| 001 | onboarding | medium | - | 2024-01-01 |

Total: 3 features
```

Also check `.artifacts/quick/` for quick mode tasks:

```markdown
### Quick Tasks
| ID | Task | Status |
|----|------|--------|
| 001 | fix-login-redirect | done |
| 002 | update-env-config | done |
```

### Show Status

1. Resolve feature (ID, branch, or single)
2. Read spec.md, plan.md, tasks.md (whichever exist)
3. Parse task progress (if tasks.md exists)
4. Determine next action

**Output:**
```markdown
## Feature: 003-auth

| Property | Value |
|----------|-------|
| Status | in-progress |
| Type | greenfield |
| Scope | large |
| Branch | feat/auth |
| Created | 2024-01-15 |

### Artifacts
| File | Status |
|------|--------|
| spec.md | Present |
| decisions.md | Present |
| plan.md | Present |
| tasks.md | Present |

### Progress
[=========> ] 45% (5/11 tasks)

Completed:
- [x] T001 - Setup auth types
- [x] T002 - Create login form

Remaining:
- [ ] T006 - Add session persistence
- [ ] T007 - Write tests

### Next Step
Run `execute` to continue.
```

## Guidelines

**DO:**
- Show all features regardless of status
- Keep status reports factual, not interpretive
- Always include the next recommended action
- Show scope to help user understand the pipeline depth

**DON'T:**
- Modify feature status from this command -- use execute
- Filter features by status unless explicitly requested
- Add interpretation or commentary to status reports

## Error Handling

- No features: Suggest `specify`
- Feature not found: List available
