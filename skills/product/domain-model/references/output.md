# Output

Produce the domain artifact and hand off downstream.

## When to Use

Load after all BR-N rules are assigned and the quality gate passes.

> Before writing artifacts, ensure `.artifacts` is excluded locally:
> `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

## Artifact

Save to `.artifacts/docs/domain.md`. Create the directory if it does
not exist.

ALWAYS use this exact template structure:

````markdown
---
name: {{project-name}}
created: {{YYYY-MM-DD}}
updated: {{YYYY-MM-DD}}
status: draft
sources:
  - .artifacts/docs/prd.md
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

{Empty at creation. Populated when running in update mode, integrating
entries from knowledge.md ## Domain Gaps.}

| Gap | Discovered During | Processed On | Change Made |
|-----|-------------------|--------------|-------------|
| {description} | {{feature ID or story}} | {{YYYY-MM-DD}} | {what was updated} |
````

## Update Mode

When running in update mode (triggered by an implementation surfacing a
domain gap):

1. Read `.agents/knowledge.md` `## Domain Gaps` section
2. For each gap entry, update the relevant entity or rule in the artifact
3. Append each processed gap to `## Processed Gaps` in `domain.md`
4. Clear processed rows from `knowledge.md ## Domain Gaps`

The queue lives in `knowledge.md`; the artifact holds the historical
record.

## Handoff

After saving, ask directly:

> "Domain model saved to `.artifacts/docs/domain.md`. What's next?
> - **Architecture** — bounded contexts inform service boundaries
> - **Implementation specs** — entities and rules become contracts
> - **Lifecycle planning** — entity lifecycle states scope story definition
> - **Nothing for now** — model is enough"

## Quality Gate

Before presenting the artifact:

- [ ] All sections complete (no empty sections)
- [ ] Every entity has at least one invariant
- [ ] Every BR-N appears in exactly one lifecycle assignment
- [ ] Bounded context map is present
- [ ] No implementation concepts (table names, column types, ORM models)

## Error Handling

- `.artifacts/docs/` does not exist: create it before saving
- User wants to add an entity after output: return to entity enumeration,
  propagate through relationships and rules before regenerating
- Update mode — `## Domain Gaps` not found in knowledge.md: note the
  section does not exist yet; ask user to describe the gap directly
