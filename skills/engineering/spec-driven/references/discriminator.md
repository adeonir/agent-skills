# Discriminator

The WHAT / HOW / WHEN boundary between spec, design, and tasks — what each phase answers, what enters, what stays out, and the signals that a concern leaked into the wrong artifact.

## When to Use

At the self-check step of specify, design, and tasks, to confirm the artifact carries only its own concern. Also read whenever content feels like it might belong to a neighbor phase.

## The boundary

| Phase | Answers | Enters | Stays out |
|-------|---------|--------|-----------|
| **Spec** | WHAT + WHY | observable behavior, ACs, goals, edge cases, assumptions, intent-why | tech, file path, component, algorithm, architecture, implementation order |
| **Design** | HOW | architecture, components, files, interface contracts (signatures), data model, non-obvious technical decisions, error strategy, risks | function bodies, tests, step sequences, commit order |
| **Tasks** | WHEN / ORDER | atomic steps, dependencies, per-task tests, gates, commit boundary | new architecture (already in design), behavior (already in spec) |

## The observability test

If the user or caller observes it → WHAT (enters the spec). If it is an internal choice → HOW (stays out, goes to design). Precise observable results — status, error semantics, a field present in the response, a state transition, limits, priorities — are WHAT. Tech, library, file path, component/function/class name, internal data structure, algorithm, and design-mechanism rationale are HOW.

## Where WHY lives, without bloat

- **Macro why** → Overview.
- **Story why** → the `...so that {benefit}` clause.
- **Non-obvious AC why** → an optional `(because …)` inline.
- **Technical trade-off / decision** → `design.md ## Decisions`.
- **Gray-area decision** → `discuss.md`.
- **Project-level decision** → `CONTEXT.md`.

## Spec self-check — three questions

1. Does any AC or edge case name a tech, file, or component/function? → rewrite as behavior.
2. Does every AC have an observable, *precise* result (not vague)?
3. Is any "goal" an implementation task in disguise?

## Leak signals

- `When Y, then Z` in the design → leaked from spec (that is an AC).
- `step 1: create X; step 2: create Y` in the design → leaked from tasks.
- New architecture introduced in tasks → leaked from design.
- An AC restated in the design → design references `AC-N` via traceability, never copies it.
