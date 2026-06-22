---
name: skill-reliability
argument-hint: <skill-name>
description: >-
  Analyzes a skill's workflows for compound reliability risks — step count,
  step nature, and variance hotspots. Use when evaluating a skill's hit rate,
  identifying prompt-driven or generation steps that drag end-to-end reliability,
  or finding where scripts, idempotence, or explicit inputs/outputs would help most.
  Invoke as /skill-reliability <skill-name> or when the user asks about steps
  vs reliability, hit rate, or confiabilidade of a specific skill.
---

# Skill Reliability Analysis

Maps a skill's workflow steps through the compound-reliability lens: each step
multiplies risk, and step nature determines baseline variance.

## Triggers

- `/skill-reliability <skill-name>` — analyze a named skill
- "steps vs reliability", "hit rate", "confiabilidade" for a skill → run analysis

## Framework

Step natures and their baseline reliability:

| Nature | Examples | Baseline |
|--------|----------|----------|
| Deterministic | git command, API call + lookup table, script | ~99% |
| Conditional | path A/B branch based on state | ~93% |
| Generation (isolated) | schema-validated output, narrow input, no conversation history | ~90% |
| Prompt-driven | instruction guard ("discard X", "block Y") | ~88% |
| Generation (free-form) | unconstrained text output (message, body, summary) | ~82% |

Multiply the per-step baselines for an end-to-end product, and report it with a
tier label. Always show the per-step baselines that produced it — the product
is only as honest as its visible inputs:

| Tier | Product |
|------|---------|
| Strong | ≥ ~90% |
| Moderate | ~75–90% |
| Fragile | < ~75% |

Baselines are heuristic and assume step failures are roughly independent; the
product is a transparent calculation over visible inputs, not a hit-rate
prediction. As a rule of thumb, even 95%/step compounds to ~74% over six
steps — step count is itself a reliability lever.

Three levers to raise reliability (highest to lowest impact):

1. **Scripts > prompts** — when the work is mechanical, write code. The model
   decides *when*; the script decides *how*.
2. **Idempotence** — read state before writing; running twice produces one change.
3. **Explicit inputs/outputs** — declare what enters, what exits, validate
   deterministically.

## Workflow

### Step 1: Locate Skill

If `$ARGUMENTS` is empty or the user's request is broad ("all skills",
"which skill to start with"), read
[discovery.md](references/discovery.md) first to determine scope and focus.

Otherwise resolve `$ARGUMENTS` to a skill path. Search in order:
1. `skills/` subdirectories of the current repo
2. `.claude/skills/` (project-scoped)
3. `~/.claude/skills/` (global)

If not found, inform the user and stop.

### Step 2: Read Skill Files

Read SKILL.md and all files under `references/` (and `instructions/` if
present). Build a complete picture of every workflow the skill defines.

### Step 3: Map Steps

For each workflow file, list every numbered step:

- **Name** — what the step does
- **Nature** — deterministic / conditional / prompt-driven / generation
- **Baseline** — the nature's value from the Framework table
- **Risk** — low / medium / high (derived from nature and internal complexity)

### Step 4: Assess Compound Reliability

For each workflow: multiply the baselines to get the end-to-end product and its
tier from the Framework table. Report both, and keep the per-step baselines
visible so the number stays auditable.

If the skill chains multiple workflows (e.g., commit → PR → finish), compute the
full-chain product and tier as well.

### Step 5: Identify Top Variance Points

Rank the three steps with the highest variance. For each:

- Why it is high-variance (nature + what can go wrong in practice)
- Which lever applies (scripts / idempotence / explicit I/O)
- What a concrete change would look like

### Step 6: Output Analysis

ALWAYS use this exact template structure:

```text
## <Skill Name>: Reliability Analysis

### Workflow: <filename> — N steps, ~X% (<tier>)

| Step | Nature | Baseline | Risk |
|------|--------|----------|------|
| 1. <name> | deterministic | ~99% | low |
| 2. <name> | generation (free-form) | ~82% | high |

End-to-end: ~99% × … × ~82% ≈ X% (<tier>)

### Full chain (if chained): M total steps, ~Y% (<tier>)

### Top Variance Points

**1. <workflow> Step N — <name>**
<Why this step is high-variance and what can go wrong>
Lever: <scripts / idempotence / explicit I/O>
Change: <concrete description of what to do differently>

**2. ...**

**3. ...**

### Summary
<2–3 sentences on where to focus for the highest reliability gain>
```

## Guidelines

- Use the step-nature table as the classification guide — do not invent new categories
- Prompt-driven guards ("discard X", "block Y instinct") are never as reliable as
  structural isolation; call them out explicitly
- A step with conditional branching counts as one step at the conditional-baseline,
  not multiple steps
- When a workflow chains to another (e.g., SKILL.md → commit.md → Step 3), count
  each numbered sub-step individually
