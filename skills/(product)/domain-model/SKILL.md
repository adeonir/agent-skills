---
name: domain-model
description: >-
  Translate product requirements into a formal domain language: entities,
  invariants, relationships, and bounded contexts. Use when a PRD exists
  and you need a shared domain vocabulary before system design, or when
  spec-driven surfaces a domain gap that requires updating the model.
when_to_use: >-
  Triggers on "build domain model", "define entities", "map domain",
  "bounded contexts", "domain language", "what are the entities",
  "model the domain", "domain model for", "entity relationships",
  "invariants for", "update domain model", "domain gap found",
  "spec found domain violation". Not for implementation data models
  (use spec-driven design.md), system architecture (use system-design),
  or product requirements (use docs-writer).
effort: xhigh
---

# Domain Model

**Recommended effort:** xhigh for discovery and entity mapping phases;
high once entities are clear and relationships are being mapped.

Translate PRD business rules and user journeys into a formal domain model:
entities, invariants, relationships, and bounded contexts. Use ultrathink
during entity mapping and rules assignment.

## Workflow

```
discovery --> entities --> relationships --> rules --> output
  ^___________________|  (loop: new entity may reshape relationships)
```

Discovery reads the PRD. Entities, relationships, and rules build on it.
Output produces the domain artifact and hands off downstream.

## Triggers

| Trigger Pattern | Reference |
|-----------------|-----------|
| Build domain model, model the domain, define entities | [discovery.md](references/discovery.md) |
| Enumerate entities, attributes, invariants, lifecycle | [entities.md](references/entities.md) |
| Entity relationships, cardinalities, bounded contexts | [relationships.md](references/relationships.md) |
| Business rules, assign rules to entities, validate BRs | [rules.md](references/rules.md) |
| Output, produce domain.md, handoff | [output.md](references/output.md) |
| Update domain model, domain gap, spec found violation | [discovery.md](references/discovery.md) (update mode) |

Notes:

- `discovery.md` is always the entry point for both new and update mode.
- `entities.md` loads after discovery confirms candidate entities.
- `relationships.md` loads after entities are enumerated.
- `rules.md` loads after relationships are stable.
- `output.md` loads when the user approves the model.

## Cross-References

```
discovery.md -----> entities.md      (candidates confirmed → enumerate)
entities.md ------> relationships.md (entities stable → map relations)
relationships.md -> rules.md         (structure stable → assign BRs)
rules.md ---------> output.md        (all BRs covered → produce artifact)
domain-model -----> docs-writer      (PRD BRs and journeys as input)
domain-model -----> system-design    (bounded contexts inform services)
domain-model -----> spec-driven      (entities+rules as impl contracts)
domain-model -----> epic-tracker     (entity lifecycle informs story scope)
spec-driven ------> domain-model     (domain gaps trigger update mode)
```

## Guidelines

**DO:**
- Read the PRD before any other action — the model derives from it
- Trace every entity back to at least one PRD journey or FR
- Assign every BR-N to one or more entity lifecycle states
- Mark invariants explicitly — they are the enforcement contracts
- Group entities into bounded contexts before handoff to system-design
- Use update mode when spec-driven reports a domain gap

**DON'T:**
- Invent entities not grounded in the PRD (contrasts: trace every entity
  to a PRD journey or FR)
- Mix implementation data models with domain concepts (contrasts: stay at
  business abstraction level; spec-driven handles file:line grounding)
- Leave any PRD BR-N unassigned to an entity (contrasts: assign every
  BR to an entity lifecycle)
- Skip bounded context grouping (contrasts: group entities before handoff)
- Treat the domain model as final (contrasts: use update mode when
  spec-driven surfaces a gap)

## Output

Domain model saved to `.artifacts/docs/domain.md`. Create the directory
if it does not exist.

Handoff options:
- `system-design` — bounded contexts inform service boundaries
- `spec-driven` — entities and rules become implementation contracts
- `epic-tracker` — entity lifecycle states can scope story definition

## Error Handling

- No PRD artifact found: ask user to provide the PRD path or run
  docs-writer first
- PRD has no BR-N IDs: continue with informal rules, flag for
  traceability
- Entity candidate is ambiguous (value object vs. entity): decide based
  on whether it has its own lifecycle; document the decision
- Bounded context boundary is unclear: flag as open question, do not guess
- Update mode — entity not found: create it, note it as an addition
- Update mode — rule conflicts with existing invariant: surface conflict
  to user before updating

## Compact Instructions

Preserve:
- Current phase, confirmed entity list with invariants
- Bounded context grouping (even if partial)
- Unassigned BRs list and open questions

Drop:
- Full PRD transcript
- Intermediate reasoning on rejected entity candidates
- Raw tool outputs
