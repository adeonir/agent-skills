# system-design

Guided system design from problem to architecture blueprint.

## Installation

```bash
npx skills add adeonir/agent-skills --skill system-design
```

## What It Does

```mermaid
flowchart LR
    D[discovery] -->|problem framed| R[requirements]
    R -->|NFRs clear| T[trade-offs]
    T -->|decisions resolved| A[architecture]
    A -->|blueprint approved| O[output]
    O -->|handoff| DW[docs-writer]
    O -->|handoff| SD[spec-driven]
    R -->|unclear| D
```

| Phase | Output |
|-------|--------|
| Discovery | Problem framing, scope, constraints |
| Requirements | Functional + non-functional requirements |
| Trade-offs | Visual comparison tables with recommendations |
| Architecture | Component diagram, data flow, patterns |
| Output | `system-brief.md` in `.artifacts/docs/` |

## Usage

```
design a notification system for a web app with 50k users
architecture for image upload and processing with AI moderation
how should I structure an API that needs to scale from 100 to 10,000 req/s
my monolith is struggling under load — help me plan the migration
```

## Output

System brief saved to `.artifacts/docs/system-brief.md`.

## Integration

| Skill | Connection |
|-------|-----------|
| docs-writer | Brief feeds TDD (component design) or ADR (trade-off decisions) |
| spec-driven | Architecture constraints feed feature specification |
| brainstorming | Brainstorm output can initiate a system design session |
