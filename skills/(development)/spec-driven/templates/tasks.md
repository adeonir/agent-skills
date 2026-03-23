---
id: {{ID}}
feature: {{name}}
created: {{YYYY-MM-DD}}
---

# Tasks: {{Feature}}

## Summary

Total: {{count}} | Completed: 0 | Remaining: {{count}}

## Execution Plan

```
T001 --> T002 --> T003
                   ├--> T004 --┐
                   └--> T005 --┼--> T007
                   T006 -------┘
```

## Quality Gates

Run after each task or batch:

- {{lint command}}
- {{typecheck command}}
- {{test command}}

## Tasks

### {{Logical group description}}

- [ ] T001 [P] {{verb}} {{what}}
  - **Done when:** {{verifiable outcome}}

- [ ] T002 [B:T001] {{dependent task}}
  - **Done when:** {{verifiable outcome}}

### {{Next logical group}}

- [ ] T003 [B:T002] {{verb}} {{what}}
  - **Done when:** {{verifiable outcome}}

## Requirements Coverage

| Requirement | Tasks      |
| ----------- | ---------- |
| AC-001      | T001, T002 |
