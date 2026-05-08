# Rules

Assign every PRD business rule (BR-N) to entity lifecycle states.
Validate full coverage.

## When to Use

Load after relationships and bounded contexts are stable. The bounded
context structure must exist before rules can be assigned.

## Workflow

### Step 1: Rule Inventory

List all BR-N rules from the PRD. For each:

- Rule ID (BR-N)
- Rule text (verbatim from PRD)
- Applicable entities (which entities are involved)

### Step 2: Assign to Entity Lifecycle

For each rule, identify the lifecycle state or transition it governs
and assign as:

- Precondition: must hold before a transition fires
- Postcondition: must hold after a transition fires
- Invariant: must always hold regardless of state

Format:
```
BR-1: Order.lifecycle.checkout.precondition
BR-2: Payment.lifecycle.authorized.invariant
```

### Step 3: Coverage Check

Verify every BR-N from the PRD is assigned:

- List unassigned BRs — these are gaps
- For each gap: determine if it maps to an undiscovered entity (return
  to `entities.md`) or a missing invariant (add it)

### Step 4: Edge Case Coverage

For each EC-N from the PRD:

- Identify which entity state it represents
- Ensure the lifecycle includes this state or transition
- Flag ECs with no entity home as open questions

## Quality Gate

Before loading `output.md`, verify:

- [ ] Every BR-N has an entity assignment
- [ ] Every EC-N has an entity lifecycle home
- [ ] No gaps remain (or gaps are documented as open questions)
- [ ] Invariant lists in entities reflect all assigned BRs

## Next Steps

Load [output.md](output.md).
