# Skill Architecture Patterns

Reference inventory of reusable skill structures. Use it when choosing how to organize a new skill or refactor an existing one.

## Inventory

| Pattern | Structure | Use when |
|---------|-----------|----------|
| One job | `SKILL.md` contains one complete procedure. Optional modes, references, assets, or scripts support that procedure. | Requests lead to the same end result, even when depth or execution strategy varies. |
| Multiple jobs | `SKILL.md` routes each job to its own instruction. Shared references, assets, or scripts are optional. | The skill handles distinct end-to-end outcomes that may share context or outputs. |

## Pattern structures

### One job

- `SKILL.md`: contains the entrypoint and complete procedure. Use `## Quick start` to begin; add a `## Workflow` when the sequence needs to be explicit.
- Steps: give each action, input, completion condition, and any stop, branch, or loop-back condition.
- Progress checklist: optional; use it to track a procedure with several steps.
- Modes: optional; keep them in the same job when they produce the same outcome. Put substantial mode-specific guidance in references loaded by `SKILL.md`.
- References: optional; use for a focused rubric or substantial guidance loaded at a named step.
- Assets and scripts: optional; use templates for reusable artifacts and scripts for deterministic operations.
- `README.md` and `agents/openai.yaml`: provide user-facing documentation and host metadata.

### Multiple jobs

- `SKILL.md`: declares triggers and routes each job to one instruction. Add a workflow map when jobs can be chained or share an artifact.
- `instructions/<job>.md`: one complete procedure per job.
- Shared references: optional; use for intake, vocabulary, rubrics, or constraints used by multiple instructions.
- Assets: optional; use a template when one job creates an artifact that another job reads or updates.
- Scripts: optional; use for deterministic operations shared by or specific to a job.
- `README.md` and `agents/openai.yaml`: provide user-facing documentation and host metadata.

## Choosing a structure

- Count end-to-end outcomes first. Keep one outcome in one job, even when it has modes or phases; split distinct outcomes into separate jobs.
- For one job, keep the procedure in `SKILL.md` unless its size or mode-specific detail calls for references.
- For multiple jobs, create one instruction per job and route to them from `SKILL.md`.
- Add shared references only for substantial guidance that multiple steps need; keep short constraints inline.
- Add an asset when procedures create or update a reusable artifact. Add a script when deterministic processing improves reliability.

## File contents

Use the following content pattern for each file type. Treat the headings as a guide; include a section only when the skill needs it. Repository rules in `AGENTS.md` and `.agents/rules/` remain the source for required authoring conventions.

### `SKILL.md`

The entrypoint identifies the skill, routes the request, and gives the selected procedure enough context to start. Keep procedures in this file only for a one-job skill; for several jobs, route to `instructions/`. After the title, use `## Triggers` to route several jobs or `## Quick start` to begin one job. A one-job file then contains its workflow; a routing file contains the routes and a compact workflow map.

```markdown
---
name: skill-name
description: "Capability and trigger contexts."
---

# Skill Title

One sentence stating what the skill does and when to use it.

## Triggers

- **Request type** (recognizable phrases) → [instruction](instructions/job.md)

## References

- [reference.md](references/reference.md) — which instruction loads it and what it provides

## Workflow

Describe the route or sequence. For several jobs, show how the instructions relate. For one job, give the steps here or route to its procedure.
```

Use `## Triggers` for several jobs and point each trigger to one instruction. Use `## Quick start` for a one-job skill that begins its procedure directly. Add a `## Workflow` section when a sequence or route map helps the agent choose or complete the procedure. State whether procedures are independent or can be chained when that affects use.

### `instructions/<job>.md`

Each instruction is one complete procedure. It states its result, loads required references before relying on them, and gives executable steps in order.

```markdown
# Job Title

One-line description of the result.

## Load first

Read [reference.md](../references/reference.md) for the rules used below.

## When to Use

State any operational condition that must be checked after the entrypoint routes here.

## Workflow

Copy this checklist and tick it off:

Progress:
- [ ] Step 1: [observable milestone]
- [ ] Step 2: [observable milestone]
- [ ] Step 3: Report the result

**Step 1. [Verb].** State the action, required input, and completion condition.

**Step 2. [Verb].** State the next action and any branch, stop, or return condition.
```

Use `## When to Use` when the routed procedure has its own state gate or optional path. Make each step produce a checkable result. Put retries and loop-backs next to the step that can trigger them. A progress checklist is useful for multi-step work; keep it aligned with the actual workflow.

### `references/<topic>.md`

A reference supplies material an instruction loads at a named step. It carries no trigger and does not replace a procedure.

```markdown
# Reference Title

One-line description of what this reference provides.

## When to Use

Name the instruction or decision this reference supports.

## [Topic]

State the shared constraint, rubric, vocabulary, or lookup material.
```

Keep a reference focused. When two instructions need the same substantial constraint, put it in one reference and tell both instructions to load it. Keep a short constraint inline when a reference would add more overhead than clarity.

### `assets/<template>.md`

An asset is reusable input or output material, such as a document template. The instruction that uses it names whether to read or write it and how to fill it. Mark copyable templates as strict or flexible, and keep operational steps in the instruction rather than the asset.

### `scripts/<tool>`

Use a script for deterministic work such as parsing, validation, or formatting. The instruction says when to run it, what input it accepts, and what output or failure means. The script handles its own errors; do not make the reader infer success from silence.
