---
name: skill-reliability
argument-hint: <skill-name>
description: >-
  Analyzes a skill's end-to-end reliability — trigger precision plus compound
  workflow risk (step count, step nature, variance hotspots) — and proposes
  verifiable fixes it can apply on confirmation. Use when evaluating a skill's
  hit rate, checking whether a description fires on the right requests, finding
  prompt-driven or generation steps that drag reliability, or deciding where
  scripts, idempotence, or explicit inputs/outputs help most. Invoke as
  /skill-reliability with a skill name, or when the user asks about steps vs
  reliability, hit rate, trigger precision, or confiabilidade of a specific skill.
---

# Skill Reliability Analysis

Scores a skill's reliability as two factors — trigger precision and compound
workflow risk — and proposes verifiable fixes.

## Triggers

- `/skill-reliability <skill-name>` — analyze a named skill
- "steps vs reliability", "hit rate", "trigger precision", "confiabilidade" for
  a skill → run analysis

## Model

A skill is only useful when it fires AND finishes:

```text
P(useful) = P(triggers correctly) × P(workflow completes | triggered)
```

Step 3 scores the first factor (trigger reliability); Steps 4–5 score the second
(compound workflow reliability). See [framework.md](references/framework.md) for
step natures, baselines, tiers, and the three reliability levers.

## Workflow

### Step 1: Locate Skill

If `$ARGUMENTS` is empty or the request is broad ("all skills", "which skill to
start with"), read [discovery.md](references/discovery.md) first to set scope.
Otherwise resolve `$ARGUMENTS` to a skill path, searching in order: `skills/`
subdirectories of the current repo, then `.claude/skills/`, then
`~/.claude/skills/`. If not found, inform the user and stop.

### Step 2: Read Skill Files

Read SKILL.md and all files under `references/` (and `instructions/` if present).
Build a complete picture of every workflow the skill defines.

### Step 3: Trigger Reliability

Run the deterministic linter first:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/trigger_lint.py <skill-dir>
```

Then follow [trigger-eval.md](references/trigger-eval.md): probe the
name + description with explicit, implicit, negative, and ambiguous requests,
reason fire-vs-should-fire, and draft a description fix when a probe misses.
Produce a verdict (Clean / Leaky / Narrow) and any rewrite.

### Step 4: Map Steps

Enumerate the workflows and their numbered steps deterministically:

```bash
python3 ${CLAUDE_SKILL_DIR}/scripts/inventory.py <skill-dir>
```

For each step assign Nature, Baseline, and Risk from
[framework.md](references/framework.md).

### Step 5: Assess Compound Reliability

Multiply the baselines into the end-to-end product and tier; feed the values to
`inventory.py --product "<b1> <b2> …"` for the deterministic arithmetic. Keep the
per-step baselines visible so the number stays auditable. For a chained skill
(commit → PR → finish), compute the full-chain product too.

### Step 6: Identify Top Variance Points

Rank the three highest-variance steps. Write each as a labelled block:

- **Failure mode** — what concretely goes wrong (an observed bad output, not "it varies")
- **Why it varies** — the nature plus its internal complexity
- **Lever** — scripts / idempotence / explicit I/O
- **Suggestion** — the concrete fix; for a trigger fix, a ready-to-paste description rewrite
- **Expected gain** — the baseline shift and its effect on the workflow product

### Step 7: Output Analysis

Produce the report with the strict template in
[output-template.md](references/output-template.md).

### Step 8: Apply Fixes

Apply a change only after the user confirms it.

- Description rewrite → write it directly to the target's SKILL.md.
- Workflow or script change → implement on request, one at a time, re-running
  its verification check after each.

Do not apply a change whose verification step (Step 7) you cannot state.

## Guidelines

- Classify steps only with the [framework.md](references/framework.md) natures — do not invent categories
- Prompt-driven guards ("discard X", "block Y") never match structural isolation; call them out
- A conditional branch counts as one step at the conditional baseline, not several
- Count each numbered sub-step of a chained workflow individually
- Trigger reliability gates the chain: a Leaky or Narrow verdict caps P(useful) regardless of the workflow score
- Every suggestion carries an expected gain and a verification step; never propose a change you cannot verify
