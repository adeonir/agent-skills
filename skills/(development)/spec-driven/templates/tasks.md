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
  - **Tests:** {{unit|integration|e2e|none}}
  - **Gate:** {{quick|full|build}}
  - **Done when:** {{verifiable outcome}}; gate passes, no tests deleted

- [ ] T002 [B:T001] {{dependent task}}
  - **Tests:** {{unit|integration|e2e|none}}
  - **Gate:** {{quick|full|build}}
  - **Done when:** {{verifiable outcome}}; gate passes, no tests deleted

### {{Next logical group}}

- [ ] T003 [B:T002] {{verb}} {{what}}
  - **Tests:** {{unit|integration|e2e|none}}
  - **Gate:** {{quick|full|build}}
  - **Done when:** {{verifiable outcome}}; gate passes, no tests deleted

## Requirements Coverage

| Requirement | Tasks      |
| ----------- | ---------- |
| AC-001      | T001, T002 |
