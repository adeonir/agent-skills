---
name: domain-model
description: >-
  Translates product requirements into a formal domain language: entities,
  invariants, relationships, and bounded contexts. Use when a PRD exists
  and a shared domain vocabulary is needed before architecture or
  implementation, or when an implementation surfaces a domain gap that
  requires updating the model. Triggers: "build domain model", "define
  entities", "map domain", "bounded contexts", "domain language", "what
  are the entities", "entity relationships", "invariants for", "update
  domain model", "domain gap found". Not for implementation data models,
  system architecture, or product requirements.
---

# Domain Model

Translate PRD business rules and user journeys into a formal domain model:
entities, invariants, relationships, and bounded contexts.

## Workflow

```
discovery --> entities --> relationships --> rules --> output
  ^___________________|  (loop: new entity may reshape relationships)
```

Discovery reads the PRD. Entities, relationships, and rules build on it.
Output produces the domain artifact and hands off downstream.

## Triggers

- **Build the model** ("build domain model", "define entities",
  "model the domain") → [discovery.md](references/discovery.md)
- **Enumerate entities** with attributes, invariants, lifecycle →
  [entities.md](references/entities.md)
- **Map relationships** with cardinalities and bounded contexts →
  [relationships.md](references/relationships.md)
- **Assign business rules** ("validate BR coverage", "assign rules") →
  [rules.md](references/rules.md)
- **Produce artifact** ("output", "produce domain.md") →
  [output.md](references/output.md)
- **Update mode** ("update domain model", "domain gap found", "spec found
  violation") → [discovery.md](references/discovery.md) (update mode)

## Guidelines

- Read the PRD before any other action — the model derives from it
- Trace every entity back to at least one PRD journey or FR
- Assign every BR-N to one or more entity lifecycle states
- Mark invariants explicitly — they are the enforcement contracts
- Group entities into bounded contexts before handoff

## Anti-Pattern: Implementation Leakage

Do not mix implementation data models (table names, ORM classes, column
types, foreign keys) with domain concepts. The domain model lives at the
business abstraction level — entities, lifecycle states, invariants. File
paths and code grounding belong to downstream implementation specs, not
here. When uncertain, ask: would a non-engineer stakeholder recognize this
language? If no, it has leaked.

## Anti-Pattern: Premature Finality

The domain model is never final. When implementation surfaces a gap (a
behavior that contradicts an invariant, an unanticipated state, an
entity not in the model), enter update mode rather than patching the
artifact silently. The model and the running system must stay in sync.
