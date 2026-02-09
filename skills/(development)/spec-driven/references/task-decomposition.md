# Task Decomposition Guidelines

Guidelines for breaking features into tasks.

## Task Structure

Each task should be:
- **Atomic**: Completable in one session
- **Testable**: Has verifiable outcome
- **Independent**: Minimal dependencies
- **Traceable**: Maps to requirements

## Task ID Format

```
T001, T002, T003...
```

Sequential, zero-padded, never reused.

## Dependency Markers

| Marker | Meaning |
|--------|---------|
| [P] | Parallel-safe, no dependencies |
| [B:T001] | Blocked by T001 |
| [B:T001,T002] | Blocked by multiple |

## Component Grouping

Group by component:
```markdown
### Authentication

- [ ] T001 [P] Create auth types
- [ ] T002 [B:T001] Implement AuthService
- [ ] T003 [B:T002] Add auth middleware
```

## Natural Order

1. Setup (config, deps)
2. Types (interfaces)
3. Implementation (core logic)
4. Integration (connect)
5. Tests

## Task Description Format

```
- [ ] T001 [P] {verb} {what} in {where}
```

Examples:
- "Create User interface in types/user.ts"
- "Implement login function in auth/service.ts"
- "Add auth middleware in middleware.ts"

## Requirements Coverage

Include coverage table:
```markdown
## Requirements Coverage

| Requirement | Tasks |
|-------------|-------|
| FR-001 | T001, T002 |
| FR-002 | T003 |
```

## Quality Gates

Add to tasks.md:
```markdown
## Quality Gates

Before marking done:
- npm run lint
- npm run typecheck
```
