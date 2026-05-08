# Relationships

Map relationships between entities: cardinalities, direction, and
bounded context grouping.

## When to Use

Load after entities are enumerated and their invariants are confirmed.
Entity enumeration must be complete before relationships can be mapped.

## Workflow

### Step 1: Pairwise Relationships

For each entity pair that interacts in the PRD (journeys, BRs):

- Name the relationship verb (owns, belongs to, contains, references)
- Cardinality: one-to-one, one-to-many, many-to-many
- Direction: unidirectional or bidirectional
- Ownership: which side is the aggregate root (if applicable)

Format:
```
EntityA --{verb}--> EntityB  [1..*]  owner: EntityA
```

### Step 2: Aggregate Roots

Identify aggregate roots:

- An aggregate root is the entity through which all access to a cluster
  of entities passes
- Cluster entities that can only exist within the lifecycle of their root
- Mark the aggregate root in the relationship map

### Step 3: Bounded Contexts

Group entities and their relationships into bounded contexts:

- A bounded context is a boundary within which the domain model is
  consistent and unambiguous
- Name each context after the primary capability it owns
- List which entities belong to each context
- Identify context boundaries — where two contexts share an entity,
  mark the shared concept and the translation needed

### Step 4: Context Map

Produce a context map showing:

- Each bounded context as a named box
- Relationships between contexts (upstream/downstream, shared kernel,
  anti-corruption layer)

## Quality Gate

Before loading `rules.md`, verify:

- [ ] All entity pairs from PRD journeys have a named relationship
- [ ] All aggregate roots are identified
- [ ] All entities are assigned to a bounded context
- [ ] Context map shows inter-context relationships

## Next Steps

Load [rules.md](rules.md).
