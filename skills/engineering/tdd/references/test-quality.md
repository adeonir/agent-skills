# Test Quality

The anti-patterns a test avoids while the loop writes it.

## When to Use

Load before writing the first test of the loop, and apply on every cycle.

## Anti-patterns

- **Implementation-coupled:** mocks an internal collaborator, tests a private method, asserts on call counts or call order, or verifies through a side channel, such as querying the database instead of reading through the interface. It breaks on a refactor that keeps behavior. Mock only at system boundaries: external APIs, time, and randomness. For the database and the file system, use the repository's test instance when one exists.
- **Tautological:** the expected value is recomputed the way the code computes it, so the test passes by construction.
- **Nondeterministic:** depends on timing, test order, or global state the test does not set up, so it passes or fails with no change in behavior. Control time and randomness through the boundary mocks, and set up every piece of state the test reads.
- **Throwaway:** proves the change once and has no reason to stay in the suite afterward. Write a test the suite keeps, one that guards behavior a caller relies on.
