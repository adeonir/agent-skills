---
id: {{ID}}
feature: {{name}}
created: {{YYYY-MM-DD}}
---

# Tasks: {{Feature}}

## Summary

Total: {{count}} | Completed: 0 | Remaining: {{count}}

## Quality Gates

Run after each implementation batch (1 or more tasks):

- {{lint command}}
- {{typecheck command}}

## Tasks

### {{Logical group description}}

- [ ] T001 [P] {{verb}} {{what}} in {{where}}
- [ ] T002 [B:T001] {{dependent task}}

### {{Next logical group}}

- [ ] T003 [B:T002] {{verb}} {{what}} in {{where}}

## Requirements Coverage

| Requirement | Tasks      |
| ----------- | ---------- |
| FR-001      | T001, T002 |
