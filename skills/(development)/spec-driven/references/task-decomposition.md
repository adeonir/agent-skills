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

## Commit Boundary Grouping

Group tasks by logical commit boundaries. Each group must be self-contained -- after completing all tasks in a group, the codebase is stable and committable. The group heading describes the commit scope.

```markdown
### Auth types and service

- [ ] T001 [P] Create auth types
- [ ] T002 [B:T001] Implement AuthService

### Auth middleware

- [ ] T003 [B:T002] Add auth middleware
- [ ] T004 [B:T003] Protect routes with auth middleware
```

Criteria for a good group:
- **Cohesive**: All tasks serve the same logical purpose
- **Complete**: No half-implemented features -- the group leaves the code in a working state
- **Minimal**: Don't bundle unrelated changes just to reduce commits

## Natural Order

1. Setup (config)
2. Types (interfaces)
3. Implementation (core logic)
4. Integration (connect)
5. Tests

Dependencies (packages) are installed within the task that first requires them, not in a separate setup task. This keeps each commit group self-contained.

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
