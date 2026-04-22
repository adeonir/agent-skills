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

### S001 [P1] {{Story Title}}

- [ ] T001 [P] {{verb}} {{what}}
  - **Tests:** {{unit|integration|e2e|none}}
  - **Gate:** {{quick|full|build}}
  - **Done when:** {{verifiable outcome}}; gate passes, no tests deleted

- [ ] T002 [B:T001] {{dependent task}}
  - **Tests:** {{unit|integration|e2e|none}}
  - **Gate:** {{quick|full|build}}
  - **Done when:** {{verifiable outcome}}; gate passes, no tests deleted

### S002 [P2] {{Story Title}}

- [ ] T003 [B:T002] {{verb}} {{what}}
  - **Tests:** {{unit|integration|e2e|none}}
  - **Gate:** {{quick|full|build}}
  - **Done when:** {{verifiable outcome}}; gate passes, no tests deleted

## Requirements Coverage

| Story | Tasks            |
|-------|------------------|
| S001  | T001, T002       |
| S002  | T003             |

| Requirement | Tasks      |
| ----------- | ---------- |
| AC-001      | T001, T002 |
