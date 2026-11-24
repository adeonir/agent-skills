---
name: implement
description: "Implements a spec issue end to end, building each task in a fresh sub-agent and integrating the results on one integration branch, or implements one task of a spec, a standalone task, or a free-form request directly on the current branch. Use when implementing a spec end to end, running its tasks in dependency order, implementing a single task, or implementing a described change. Not for writing or changing the spec, breaking a spec into tasks, reviewing the result against the spec or standards, opening or merging a pull request, or pushing."
argument-hint: "spec [issue] | task [issue or request]"
disable-model-invocation: true
metadata:
  inspired-by:
    - "implement — https://github.com/mattpocock/skills/blob/main/skills/engineering/implement/SKILL.md"
    - "implement-spec — https://github.com/mattpocock/skills/blob/main/skills/engineering/implement-spec/SKILL.md"
    - "incremental-implementation — https://github.com/addyosmani/agent-skills/blob/main/skills/incremental-implementation/SKILL.md"
    - "tlc-implement — https://github.com/tech-leads-club/agent-skills/blob/main/packages/skills-catalog/skills/(development)/tlc-implement/SKILL.md"
---

# Implement

Implement work from a spec or a single task, end to end.

## Triggers

- **Implement a spec** — the whole spec should run (`/implement spec [issue]`, "implement every task of this spec") → [implement-spec.md](references/implement-spec.md) · each task in a fresh sub-agent, integrated on one branch
- **Implement one task or request** — a single task or a described change (`/implement task [issue or request]`, "implement this task") → [implement-task.md](references/implement-task.md) · the change on the current branch

If the mode is missing or is neither `spec` nor `task`, ask for it.

A spec run ends with its report, and its procedure no longer applies. A later request in the same session works on the integration branch directly, with no worktree.
