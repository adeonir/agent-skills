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
| 003 | auth | large | feat/auth | YYYY-MM-DD |

### Ready
| ID | Feature | Scope | Branch | Created |
|----|---------|-------|--------|---------|
| 002 | payments | complex | feat/payments | YYYY-MM-DD |

### To Review
| ID | Feature | Scope | Branch | Created |
|----|---------|-------|--------|---------|
| 004 | checkout | medium | feat/checkout | YYYY-MM-DD |

### Done
| ID | Feature | Scope | Branch | Created |
|----|---------|-------|--------|---------|
| 001 | onboarding | medium | - | YYYY-MM-DD |

Total: 4 features
```

Group order matches status flow: In Progress -> Ready -> To Review -> Done.
Draft features appear before Ready when present.

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
2. Read spec.md, design.md, tasks.md (whichever exist)
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
| Created | YYYY-MM-DD |

### Artifacts
| File | Status |
|------|--------|
| spec.md | Present |
| decisions.md | Present |
| design.md | Present |
| tasks.md | Present |

### Progress
[=========> ] 45% (5/11 tasks)

Completed:
- [x] T-1 - Setup auth types
- [x] T-2 - Create login form

Remaining:
- [ ] T-6 - Add session persistence
- [ ] T-7 - Write tests

### Next Step
Run `implement` to continue.
```

Next-step rules by status:

| Status | Next Step |
|--------|-----------|
| `draft` | Run `design` (or `implement` for Medium scope) |
| `ready` | Run `implement` |
| `in-progress` | Run `implement` to continue |
| `to-review` | Run `audit` to validate Goals/Success Criteria (and optionally `validate` for UAT) |
| `done` | Feature closed |

## Guidelines

**DO:**
- Show all features regardless of status
- Keep status reports factual, not interpretive
- Always include the next recommended action
- Show scope to help user understand the pipeline depth

**DON'T:**
- Modify feature status from this command -- use implement
- Filter features by status unless explicitly requested
- Add interpretation or commentary to status reports

## Error Handling

- No features: Suggest `specify`
- Feature not found: List available
