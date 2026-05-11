# Output

Produce the system brief and ask the user what to do next.

## When to Use

Load after the architecture is confirmed by the user.

> Before writing artifacts, ensure `.artifacts` is excluded locally:
> `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

## System Brief

Save to `.artifacts/docs/system.md`. Create the directory if it
does not exist.

ALWAYS use this exact template structure:

````markdown
---
name: {{system-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: draft
sources:
  - .artifacts/docs/prd.md
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
- [ ] Technical Design Document for component-level planning
- [ ] Architecture Decision Record for decision {{name}}
- [ ] Implementation specs — feature work using this architecture
- [ ] No handoff — brief is sufficient
````

The brief is the source of truth for the design session. It is input for
the next step — not the final deliverable.

## Handoff

After saving the brief, ask directly:

> "Brief saved to `.artifacts/docs/system-brief.md`. What's next?
> - **Technical Design Document** — component-level planning
> - **Implementation specs** — start a feature from this architecture
> - **Nothing for now** — brief is enough"

Wait for the user's answer. Pass the relevant section of the brief as
context to the next step:

- TDD: pass the Architecture section (components, data flow, patterns)
- Implementation: pass the Architecture section and the Functional Requirements

## Quality Gate

Before delivering the brief:

- [ ] All sections are complete (no empty sections)
- [ ] Trade-off decisions reference the requirements that drove them
- [ ] Architecture diagram matches the component list
- [ ] Open questions are listed with owner or context

## Error Handling

- `.artifacts/docs/` does not exist: create it before saving
- User wants to change a decision after output: return to trade-offs
  and propagate the change through architecture before regenerating
