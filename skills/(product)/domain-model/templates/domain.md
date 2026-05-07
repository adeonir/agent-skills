---
name: {{project-name}}
created: {{YYYY-MM-DD}}
---

# Domain Model — {{Project Name}}

## Bounded Contexts

| Context | Entities | Primary Capability |
|---------|----------|--------------------|
| {{ContextName}} | {{Entity1, Entity2}} | {what this context owns} |

## Entities

### {{EntityName}}

**Type:** Entity | Value Object
**Context:** {{BoundedContextName}}
**Source:** {{FR-N, journey step, or BR-N that introduced this entity}}

#### Attributes

| Attribute | Type | Required | Source |
|-----------|------|----------|--------|
| {{name}} | {{type}} | Yes / No | {{PRD ref}} |

#### Invariants

- `INVARIANT:` {{condition}}. Source: {{BR-N or EC-N}}

#### Lifecycle

```
{state1} --[transition]--> {state2}
  guard: {condition}
{state2} --[transition]--> {state3} (terminal)
```

| State | Description |
|-------|-------------|
| {{state}} | {what it means} |

#### Identity

**Key:** {{natural key field or "surrogate"}}

---

## Relationships

```
{EntityA} --{verb}--> {EntityB}  [{cardinality}]  owner: {root}
```

| Relationship | Cardinality | Owner | Source |
|--------------|-------------|-------|--------|
| {{EntityA verb EntityB}} | 1..* | {{EntityA}} | {{FR-N}} |

## Context Map

```
[ContextA] --upstream--> [ContextB]
[ContextB] --shared kernel-- [ContextC]
```

| Boundary | Type | Translation Needed |
|----------|------|--------------------|
| {{ContextA / ContextB}} | {{upstream/downstream}} | {yes/no — describe} |

## Business Rules Coverage

| Rule ID | Rule Text | Entity | Assignment Type |
|---------|-----------|--------|-----------------|
| BR-1 | {{text}} | {{Entity.lifecycle.state}} | precondition |
| BR-2 | {{text}} | {{Entity}} | invariant |

## Open Questions

- [ ] TBD: {question that needs answering before implementation}

## Processed Gaps

{Empty at creation. Populated when domain-model runs in update mode,
integrating entries from knowledge.md ## Domain Gaps.}

| Gap | Discovered During | Processed On | Change Made |
|-----|-------------------|--------------|-------------|
| {description} | {{feature ID or story}} | {{YYYY-MM-DD}} | {what was updated} |
