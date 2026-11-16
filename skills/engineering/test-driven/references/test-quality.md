# Test Quality

The anti-patterns a test avoids while the loop writes it.

## When to Use

Load before writing the first test of the loop, and apply on every cycle.

## Anti-patterns

- **Implementation-coupled:** mocks an internal collaborator, tests a private method, asserts on call counts or call order, or verifies through a side channel, such as querying the database instead of reading through the interface. It breaks on a refactor that keeps behavior. Mock only at system boundaries: external APIs, time, and randomness. For the database and the file system, use the repository's test instance when one exists.
- **Tautological:** the expected value is recomputed the way the code computes it, so the test passes by construction.
- **Horizontal slicing:** writing all the tests first, then all the code. Tests written in bulk verify imagined behavior: they test the shape of things instead of the behavior a caller sees, and they fix the test structure before the code exists. Write one test, then the code that passes it, and let each cycle respond to what the previous one taught.

A side-channel assertion and its fix:

```typescript
// Implementation-coupled: bypasses the interface to verify
await createUser({ name: "Alice" });
const row = await db.query("SELECT * FROM users WHERE name = ?", ["Alice"]);
expect(row).toBeDefined();

// Through the interface: reads back what the caller can read
const user = await createUser({ name: "Alice" });
expect((await getUser(user.id)).name).toBe("Alice");
```

A tautological assertion and its fix:

```typescript
// Tautological: recomputes the total the way the code does
expect(calculateTotal(items)).toBe(items.reduce((sum, i) => sum + i.price, 0));

// Anchored: a known literal from the source of truth
expect(calculateTotal([{ price: 10 }, { price: 5 }])).toBe(15);
```
