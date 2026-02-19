# Docs Writer

Generate structured product and technical documents through guided discovery.

## What It Does

Routes document creation requests to type-specific workflows, each with appropriate discovery depth:

```mermaid
flowchart LR
    T[Trigger] --> R{Router}
    R --> PRD[PRD]
    R --> B[Brief]
    R --> I[Issue]
    R --> TK[Task]
    R --> US[User Story]
    R --> RFC[RFC]
    R --> ADR[ADR]
    R --> TDD[TDD]
```

| Type | Workflow | Output |
|------|----------|--------|
| **PRD** | discovery -> analysis -> drafting | `prd.md` |
| **Brief** | discovery -> drafting | `brief.md` |
| **Issue** | classification -> drafting | `issue.md` |
| **Task** | direct drafting | `task.md` |
| **User Story** | discovery -> drafting | `story.md` |
| **RFC** | discovery -> analysis -> drafting | `rfc.md` |
| **ADR** | discovery -> drafting | `adr-{number}-{name}.md` |
| **TDD** | discovery -> analysis -> drafting | `tdd.md` |

## Usage

```
create PRD for my project
create brief for my product
report bug in the login flow
create task to update dependencies
write user story for checkout
create RFC for new auth system
record architecture decision about database choice
create technical design for API gateway
```

The agent detects the document type from the trigger and loads the appropriate workflow.

## Output

All documents are saved to:

```
.specs/docs/{type}.md
```

## Integration

| Skill | How docs-writer connects |
|-------|-------------------------|
| **spec-driven** | Any document can feed into feature initialization |
| **design-builder** | PRD sections inform copy and design extraction |

## Requirements

Works with any agent supporting standard skill format.
