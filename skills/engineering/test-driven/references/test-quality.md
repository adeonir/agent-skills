# Test Quality

The checks a test passes before the change is reported done.

## When to Use

Load to self-check the tests a change touched, and to brief the reviewer of those tests.

## Checks

Every test:

- Asserts something. A test the runner reports with no assertions fails.
- Traces to an acceptance criterion or a listed edge case in the source of truth.
- Fails under a plausible wrong implementation.
- Asserts each field the source names for a returned object, an event, or a stored record.

## Anti-patterns

- **Implementation-coupled:** mocks an internal collaborator, tests a private method, or verifies through a side channel, such as querying the database instead of reading through the interface. It breaks on a refactor that keeps behavior.
- **Tautological:** the expected value is recomputed the way the code computes it, so the test passes by construction.
- **Shallow:** passes under a plausible wrong implementation. "No error thrown" as the only assertion, a call count or spy where the criterion names a resulting state, or only the happy path when the source lists edge cases.
- **Unanchored:** asserts behavior the source of truth does not ask for.
- **Framework test:** asserts behavior of a library or the framework, not of the change.

A tautological assertion and its fix:

```typescript
// Tautological: recomputes the total the way the code does
expect(calculateTotal(items)).toBe(items.reduce((sum, i) => sum + i.price, 0));

// Anchored: a known literal from the source of truth
expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
```
