---
name: implement
description: "Implements a spec issue end to end, building each task in a fresh sub-agent and integrating the results on one integration branch, or implements one task of a spec, a standalone task, or a free-form request directly on the current branch. Use when implementing a spec end to end, running its tasks in dependency order, implementing a single task, or implementing a described change. Not for writing or changing the spec, breaking a spec into tasks, reviewing the result against the spec or standards, opening or merging a pull request, or pushing."
argument-hint: "spec [issue] | task [issue or request]"
disable-model-invocation: true
---

# Implement

## Triggers

- **Implement a spec** (`/implement spec [issue]`, "implement every task of this spec") → [implement-spec.md](instructions/implement-spec.md)
- **Implement one task or request** (`/implement task [issue or request]`, "implement this task", "implement this change") → [implement-task.md](instructions/implement-task.md)

If the mode is missing or is neither `spec` nor `task`, ask for it.

## References

- [implementer-brief.md](references/implementer-brief.md) — loaded by the implement spec instruction to dispatch an implementer
- [merger-brief.md](references/merger-brief.md) — loaded by the implement spec instruction when the integration branch moved
