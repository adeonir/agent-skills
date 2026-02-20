# Status and Listing

List features and show detailed status.

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

## Process

### List Features

1. Scan `.artifacts/features/`
2. Read spec.md frontmatter from each
3. Group by status
4. Display table

**Output:**
```markdown
## Features

### In Progress
| ID | Feature | Branch | Created |
|----|---------|--------|---------|
| 003 | auth | feat/auth | 2024-01-15 |

### Ready
| ID | Feature | Branch | Created |
|----|---------|--------|---------|
| 002 | payments | feat/payments | 2024-01-10 |

### Done
| ID | Feature | Branch | Created |
|----|---------|--------|---------|
| 001 | onboarding | - | 2024-01-01 |

Total: 3 features
```

### Show Status

1. Resolve feature (ID, branch, or single)
2. Read spec.md, plan.md, tasks.md
3. Parse task progress
4. Determine next action

**Output:**
```markdown
## Feature: 003-auth

| Property | Value |
|----------|-------|
| Status | in-progress |
| Type | greenfield |
| Branch | feat/auth |
| Created | 2024-01-15 |

### Artifacts
| File | Status |
|------|--------|
| spec.md | Present |
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
Run `implement` to continue.
```

## Error Handling

- No features: Suggest `initialize`
- Feature not found: List available
