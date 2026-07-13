# Simplicity

The simplest architecture that satisfies the ACs — a ladder for choosing HOW, and the check that a simplification is real before it becomes a decision.

## When to Use

During design, at the Ladder step, when choosing among viable entry points, components, or dependencies — at the self-check before writing, and before verifying a mechanism, to check the premise it serves. Read it whenever a design adds a layer, an abstraction, or a dependency: climb the ladder first.

## The ladder

Every component the design introduces stops at the first rung that satisfies the ACs:

1. **Does it need to exist?** A layer, interface, or config the ACs do not require is speculative — leave it out. An interface with one implementation, a factory for one product, a wrapper that only delegates: not yet.
2. **Does the codebase already have it?** A helper, pattern, or type already here → reuse it, record it as a `reuse` component. The most common over-build is re-implementing what lives a few files over.
3. **Stdlib or language built-in?** Use it before hand-rolling.
4. **Native platform or framework feature?** A framework capability or platform primitive before custom code.
5. **An already-installed dependency?** Use it before adding a new one for what a few lines cover.
6. **Only then** the minimum new code that satisfies the ACs.

Two rungs both hold → take the higher one. The ladder runs after Exploration has traced how the code actually works, never instead of it: the smallest design in the wrong place is a second defect, not a simpler one.

## Each simplification is a claim

"Reuse this helper", "stdlib covers it", "the platform already does this" — each rests on a surface: a type, a signature, an installed dependency's schema, a lifetime guarantee. Verify that surface with the cheapest check that produces the observation — static evidence first, then an existing test, then a one-liner — before recording it as a Decision. A simplification asserted without checking its surface is a hypothesis, not a decision; carry it as a Risk to verify, never as a settled `reuse`.

## Chained necessity

Each piece a design adds can be locally correct and the design still be wrong. When a new component exists only because of the one before it — this contract forces that factory, that factory forces this stub, that path forces a resolver — the chain is the signal: the root decision is wrong, not the last link. Trying to fix the tail (this path or that one, factory or not) only produces the next link.

Stop and return to rung 1 for the decision the chain hangs from, and check it against rung 2 before verifying any mechanism it needs. A check answers *does this work?*, never *should this exist?* — verified on a wrong premise, it reads as rigor and makes the premise harder to challenge, not easier. The signal is the chaining, not the amount of code.

## When NOT to simplify

The ladder chooses among architectures that all satisfy the ACs — it never drops an AC or an NFR to get smaller. Validation at trust boundaries, error handling that prevents data loss, security, and accessibility stay whenever a stated AC or NFR requires them. A simpler design that fails a criterion is not simpler, it is wrong.

## Example

```text
Feature AC: responses for the same input are served from cache within the TTL.

Over-built — a layer the AC does not require:
  CacheProvider interface + InMemoryCacheProvider impl + cache-config module
  → one interface, one implementation, config nobody sets.

Laddered — stop at the rung that satisfies the AC:
  rung 1: a provider abstraction? one impl → not yet.
  rung 3/5: language memoization / an installed util covers TTL caching.
  Decision: memoize the fetch; unbounded key growth is a Risk to verify
  against the schema, not a reason to pre-build eviction.
```
