---
title: {{system-name}} — System Design Brief
created: {{YYYY-MM-DD}}
---

# {{System Name}} — System Design Brief

## Problem

{{one paragraph: what problem is being solved, who it affects, why it matters}}

## Users and Usage Patterns

{{who uses the system and how — main actions, expected session shape}}

## Scope

**In scope:** {{what this design covers}}

**Out of scope:** {{what this design explicitly excludes}}

## Functional Requirements

{numbered list of concrete, verifiable requirements:}
1. {{FR-01: requirement}}
2. {{FR-02: requirement}}

## Non-Functional Requirements

| Attribute | Target |
|-----------|--------|
| Scale | {{e.g., 10,000 concurrent users; 500 req/s peak}} |
| Latency | {{e.g., p99 < 300ms for read operations}} |
| Availability | {{e.g., 99.9% uptime, RTO < 15min}} |
| Consistency | {{strong / eventual — with rationale}} |
| Data retention | {{e.g., 90 days; GDPR applicable}} |

## Constraints

**Hard constraints:** {{must-haves that cannot be traded}}

**Soft constraints / preferences:** {{preferences that can be revisited}}

## Key Decisions

{one subsection per resolved trade-off:}

### {{Decision Name}}

| Criterion | {{Option A}} | {{Option B}} |
|-----------|-------------|-------------|
| {{criterion}} | {{value}} | {{value}} |
| Recommendation | - | X |

**Chosen:** {{option}} — {{one-sentence rationale tied to a specific NFR}}

## Architecture

### Pattern

{{name the architectural pattern(s) in use}}

### Component Diagram

```
{ASCII block diagram}
```

### Components

| Component | Role | Technology (if decided) |
|-----------|------|------------------------|
| {{name}} | {{what it does}} | {{stack or TBD}} |

### Main Flows

**Happy path:** {{step-by-step through the primary use case}}

**Failure path:** {{what happens when a critical component is unavailable}}

**Scale path:** {{how the system handles 10x load}}

### Observability

| Component | Key Metrics | Key Logs |
|-----------|-------------|----------|
| {{name}} | {{metrics}} | {{what to log}} |

## Open Questions

{list of unknowns deferred during design:}
- {{question}} — {{owner or context}}

## Handoff

{indicate next step:}
- [ ] docs-writer → TDD for component-level planning
- [ ] docs-writer → ADR for decision {{name}}
- [ ] spec-driven → feature implementation
- [ ] No handoff — brief is sufficient
