---
name: system-design
description: >-
  Guided system design from problem to architecture. Starts from the
  problem, not the document. Runs interactive discovery, elicits
  non-functional requirements, produces visual trade-off tables, and maps
  components. Agnostic to domain, stack, and experience level. Use when
  designing a new system, planning architecture, choosing between
  technical approaches, or facing scale/consistency/reliability decisions.
  Triggers: "design a system", "architecture for", "how should I
  structure", "system for X", "what architecture", "scale this", "handle
  X users", "microservices vs monolith", "how to store", "real-time
  notifications", "event-driven", "distributed system", "system design
  interview". Not for feature design specs, technical design documents,
  or visual UI design.
---

# System Design

Interactive system design from problem framing to architecture blueprint.
Start from the problem — requirements, trade-offs, and components follow.

## Workflow

```
discovery --> requirements --> trade-offs --> architecture --> output
  ^______________|  (loop until requirements are clear)
```

Discovery and requirements iterate: ask, deepen, confirm. Trade-offs and
architecture are sequential once requirements are stable.

## Triggers

- **Problem framing** ("design a system", "how should I structure",
  "architecture for") → [discovery.md](references/discovery.md)
- **Requirements** ("constraints", "scale", "SLA", "non-functional",
  "what numbers") → [requirements.md](references/requirements.md)
- **Trade-offs** ("compare options", "SQL vs NoSQL", "sync vs async",
  "monolith vs microservices") → [trade-offs.md](references/trade-offs.md)
- **Architecture mapping** ("components", "data flow", "diagram",
  "blueprint") → [architecture.md](references/architecture.md)
- **Produce brief** ("output", "save the brief", "handoff") →
  [output.md](references/output.md)

Always start at discovery, even when the user provides requirements
upfront. Load each subsequent reference only when its phase begins.

## Guidelines

- Start every session with discovery, even when requirements seem clear
- Ask one question at a time during discovery and requirements
- Present trade-offs as tables with an explicit recommendation
- State the reasoning behind every architectural recommendation
- Mark unknowns as open questions rather than filling gaps with assumptions
- Acknowledge the user's experience level and adjust vocabulary accordingly

## Anti-Pattern: Premature Architecture

Producing component diagrams before key decisions are resolved hides the
reasoning that should justify the diagram. Resolve trade-offs first; the
architecture follows from them. When the user pushes for a diagram early,
sketch the open decisions instead and invite them to walk through one.

## Anti-Pattern: Preference as Constraint

A user who states "we use Postgres" is sharing a preference, not closing
the trade-off. Note the preference, run the comparison anyway, and confirm
or challenge it based on the table. Hard constraints are external
(compliance, existing infra, team skill); preferences are internal and
revisitable.

## Anti-Pattern: Prose-Only Decisions

Every significant architectural decision must produce a comparison table
with a recommendation row. Decisions written only in prose hide the
criteria, can't be audited, and lose the link to the requirement they
serve. The only exception: a single-option decision under hard
constraints — state it as a one-line note.
