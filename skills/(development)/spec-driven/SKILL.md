---
name: spec-driven
description: >-
  Specification-driven development with structured phases: Initialize, Plan, Tasks, Implement+Validate.
  Creates structured feature specs with traceability to requirements.
  Use when: starting projects, planning features, implementing with verification,
  or tracking decisions across sessions. Triggers on "map codebase", "initialize",
  "initialize project", "create feature", "plan", "tasks", "implement",
  "validate", "archive".
metadata:
  author: github.com/adeonir
  version: "1.0.0"
---

# Spec-Driven Development

Structured development workflow: Initialize -> Plan -> Tasks -> Implement + Validate.

## Workflow

```
initialize --> plan --> tasks --> implement --> validate --> archive
```

## Project Structure

```
.artifacts/
├── project/
│   ├── PROJECT.md          # Vision, goals, constraints
│   ├── ROADMAP.md          # Planned features, milestones
│   └── CHANGELOG.md        # Feature implementation history
├── codebase/               # Brownfield analysis (optional)
│   ├── STACK.md
│   ├── ARCHITECTURE.md
│   ├── CONVENTIONS.md
│   ├── STRUCTURE.md
│   ├── TESTING.md
│   └── INTEGRATIONS.md
├── research/               # Research cache (optional)
│   └── {topic}.md
└── features/
    └── {ID}-{name}/
        ├── spec.md         # WHAT: Requirements
        ├── plan.md         # HOW: Architecture
        └── tasks.md        # WHEN: Tasks

docs/
└── features/
    └── {name}.md           # Consolidated implementation
```

## Context Loading Strategy

**Base load (~15k tokens):**
- PROJECT.md (context)
- Current feature spec.md

**On-demand:**
- codebase/*.md (brownfield)
- plan.md (implementing)
- tasks.md (executing)
- research/*.md (new technologies)

**Never simultaneous:**
- Multiple feature specs
- Archived features

## Triggers

### Project-Level
| Trigger Pattern | Reference |
|-----------------|-----------|
| Initialize project, setup project | [project-init.md](references/project-init.md) |
| Create roadmap, plan features | [roadmap.md](references/roadmap.md) |
| Map codebase, analyze codebase | [codebase-mapping.md](references/codebase-mapping.md) |

### Feature-Level
| Trigger Pattern | Reference |
|-----------------|-----------|
| Create new feature, new feature | [initialize.md](references/initialize.md) (greenfield) |
| Modify feature, improve feature | [initialize.md](references/initialize.md) (brownfield) |
| Create technical plan | [plan.md](references/plan.md) |
| Research technology, cache research | [research.md](references/research.md) |
| Create tasks | [tasks.md](references/tasks.md) |
| Implement task | [implement.md](references/implement.md) |
| Validate | [validate.md](references/validate.md) |
| Archive | [archive.md](references/archive.md) |
| List features, show status | [status-specs.md](references/status-specs.md) |

### Guidelines
| Trigger Pattern | Reference |
|-----------------|-----------|
| How to write specs | [spec-writing.md](references/spec-writing.md) |
| How to decompose tasks | [task-decomposition.md](references/task-decomposition.md) |
| Codebase exploration | [codebase-exploration.md](references/codebase-exploration.md) |
| Research patterns | [research.md](references/research.md) |
| Baseline discovery | [baseline-discovery.md](references/baseline-discovery.md) |
| Extract from PRD/docs | [doc-extraction.md](references/doc-extraction.md) |
| Coding principles | [coding-principles.md](references/coding-principles.md) |
| Status workflow, when to update status | [status-workflow.md](references/status-workflow.md) |

## Cross-References

```
project-init.md ----> roadmap.md
project-init.md ----> codebase-mapping.md
initialize.md ------> plan.md (when spec complete)
plan.md ------------> tasks.md
plan.md ------------> research.md (if new tech)
tasks.md -----------> implement.md
implement.md -------> coding-principles.md (loaded before coding)
implement.md -------> validate.md
validate.md --------> implement.md (if issues)
validate.md --------> archive.md (if passed)
```

## Guidelines

- Content separation: spec=WHAT, plan=HOW, tasks=WHEN
- Status flow: draft -> ready -> in-progress -> to-review -> done -> archived
- Feature IDs: sequential (001, 002), never reused
- Research cache: Reusable across features in .artifacts/research/
- Archive generates: docs/features/{name}.md (no ID)

## Error Handling

- No .artifacts/: Suggest initialize project first
- Spec not found: List available features
- Open questions blocking architecture: Resolve before planning
- Plan not found: Suggest plan before tasks
- Tasks not found: Suggest tasks before implement
