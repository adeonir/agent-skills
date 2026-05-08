# Entities

Enumerate confirmed entities with attributes, invariants, and lifecycle
states.

## When to Use

Load after discovery confirms the candidate entity list.

> **LOAD FIRST:** [discovery.md](discovery.md) — candidate list must
> exist before enumerating

## Workflow

For each confirmed entity:

### Step 1: Attributes

List all attributes. For each attribute:

- Name and type (string, integer, money, date, ID reference)
- Required vs. optional
- Source (which PRD section defines it)

### Step 2: Invariants

Invariants are rules the entity must always satisfy. Derive from:

- BR-N rules that apply to this entity
- Conditions in user journeys (pre-conditions, post-conditions)
- Edge cases (EC-N) that describe illegal states

Format: `INVARIANT: {condition}. Source: {BR-N or EC-N}`

### Step 3: Lifecycle States

Define the state machine for entities with lifecycle (not value objects):

- States: named statuses the entity passes through
- Transitions: allowed moves between states
- Guards: conditions that must hold for a transition to fire
- Terminal states: states from which no transition is possible

### Step 4: Identity

Define what makes this entity unique:

- Natural key (if stable and meaningful in the domain)
- Surrogate key (if natural key is absent or unstable)

## Quality Gate

Before loading `relationships.md`, verify:

- [ ] Every confirmed entity has attributes, invariants, and lifecycle
- [ ] Every invariant cites a PRD source (BR-N, EC-N, or FR-N)
- [ ] Value objects are noted as such (no lifecycle section needed)
- [ ] No implementation details have leaked in (no table names, no IDs)

## Next Steps

Load [relationships.md](relationships.md).
