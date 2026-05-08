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
T-1 --> T-2 --> T-3
                 ├--> T-4 --┐
                 └--> T-5 --┼--> T-7
                 T-6 -------┘
```

## Quality Gates

Run after each task or batch:

- {{lint command}}
- {{typecheck command}}
- {{test command}}

## Tasks

### S-1 [P1] {{Story Title}}

- [ ] T-1 [P] {{verb}} {{what}}
  - **Tests:** {{unit|integration|e2e|none}}
  - **Gate:** {{quick|full|build}}
  - **Done when:** {{verifiable outcome}}; gate passes, no tests deleted
  - **Satisfaction sketch:** {{one line: why this implementation actually moves the criterion}}

- [ ] T-2 [B:T-1] {{dependent task}}
  - **Tests:** {{unit|integration|e2e|none}}
  - **Gate:** {{quick|full|build}}
  - **Done when:** {{verifiable outcome}}; gate passes, no tests deleted
  - **Satisfaction sketch:** {{one line: why this implementation actually moves the criterion}}

### S-2 [P2] {{Story Title}}

- [ ] T-3 [B:T-2] {{verb}} {{what}}
  - **Tests:** {{unit|integration|e2e|none}}
  - **Gate:** {{quick|full|build}}
  - **Done when:** {{verifiable outcome}}; gate passes, no tests deleted
  - **Satisfaction sketch:** {{one line: why this implementation actually moves the criterion}}
  - **Candidate trace:** (investigation tasks only -- omit otherwise)
    | Candidate | Evidence For | Evidence Against | Status |
    |-----------|--------------|------------------|--------|
    | {{name}} | {{observation}} | {{observation}} | {{chosen / ruled out}} |

## Requirements Coverage

| Story | Tasks         |
|-------|---------------|
| S-1   | T-1, T-2      |
| S-2   | T-3           |

| Requirement | Tasks      |
| ----------- | ---------- |
| AC-1        | T-1, T-2   |
