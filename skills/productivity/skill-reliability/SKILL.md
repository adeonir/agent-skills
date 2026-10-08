---
name: skill-reliability
argument-hint: "[skill-name]"
description: "Analyzes a skill's end-to-end reliability: trigger precision plus compound workflow risk, with verifiable fixes applied on confirmation. Use when evaluating a skill's hit rate, checking whether a description fires on the right requests, finding steps that drag reliability, or deciding where scripts, idempotence, or explicit inputs and outputs help most. Not for general skill authoring, structure audits, or running evals."
---

# Skill Reliability Analysis

## Triggers

- `/skill-reliability [skill-name]` — analyze a named skill
- "steps vs reliability", "hit rate", "trigger precision" for a skill → run analysis

## Model

Scores a skill's reliability as two factors and proposes verifiable fixes. A skill is only useful when it fires and finishes:

```text
P(useful) = P(triggers correctly) × P(workflow completes | triggered)
```

Step 3 scores the first factor (trigger reliability); Steps 4–5 score the second (compound workflow reliability). See [framework.md](references/framework.md) for step natures, baselines, tiers, and the three reliability levers.

## Workflow

The commands below write a bundled script as `<this-skill>/scripts/<name>`. Resolve `<this-skill>` to the directory this `SKILL.md` was read from; `<skill-dir>` is the skill under analysis, resolved in Step 1.

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Locate the skill
- [ ] Step 2: Read the skill files
- [ ] Step 3: Score trigger reliability
- [ ] Step 4: Map the steps
- [ ] Step 5: Assess compound reliability
- [ ] Step 6: Identify the top variance points
- [ ] Step 7: Output the analysis
- [ ] Step 8: Apply the confirmed fixes
```

**Step 1. Locate the skill.** If `$ARGUMENTS` is empty or the request is broad ("all skills", "which skill to start with"), read [discovery.md](references/discovery.md) first to set scope. Otherwise resolve `$ARGUMENTS` to a skill path, searching in order: `skills/` subdirectories of the current repo, then `.claude/skills/`, then `~/.claude/skills/`. If not found, inform the user and stop. Done when `<skill-dir>` is a path containing a `SKILL.md`.

**Step 2. Read the skill files.** Read SKILL.md and all files under `references/` (and `instructions/` if present). Done when you can name every workflow the skill defines.

**Step 3. Score trigger reliability.** Run the deterministic linter first:

```bash
python3 <this-skill>/scripts/trigger_lint.py <skill-dir>
```

Then follow [trigger-eval.md](references/trigger-eval.md): probe the name + description with explicit, implicit, negative, and ambiguous requests, reason fire-vs-should-fire, and draft a description fix when a probe misses. If the held-out re-test fails, return to the rewrite. Done when you hold a verdict (Clean / Leaky / Narrow) and any rewrite with its held-out re-test result.

**Step 4. Map the steps.** Enumerate the workflows and their numbered steps deterministically:

```bash
python3 <this-skill>/scripts/inventory.py <skill-dir>
```

For each step assign Nature, Baseline, and Risk from [framework.md](references/framework.md). If the inventory misses a workflow you read in Step 2, add its steps by hand and say so. Done when every inventoried step has a Nature, Baseline, and Risk.

**Step 5. Assess compound reliability.** Multiply the baselines into the end-to-end product and tier; feed the values to `inventory.py --product "<b1> <b2> …"` for the deterministic arithmetic. Keep the per-step baselines visible so the number stays auditable. For a chained skill (commit → PR → finish), compute the full-chain product too. Done when each workflow has a product and tier.

**Step 6. Identify the top variance points.** Rank the three highest-variance steps. Write each as a labelled block:

- **Failure mode** — what concretely goes wrong (an observed bad output, not "it varies")
- **Why it varies** — the nature plus its internal complexity
- **Lever** — scripts / idempotence / explicit I/O
- **Suggestion** — the concrete fix; for a trigger fix, a ready-to-paste description rewrite
- **Expected gain** — the baseline shift and its effect on the workflow product

If a Suggestion has no verification, return to Step 5 and rework it. Done when each block carries all five labels.

**Step 7. Output the analysis.** Produce the report with the strict template in [output-template.md](references/output-template.md). Done when the report matches the template.

**Step 8. Apply the confirmed fixes.** Apply a change only after the user confirms it. Write a description rewrite directly to the target's SKILL.md. Implement a workflow or script change on request, one at a time, re-running its verification check after each. Do not apply a change whose verification step from Step 7 you cannot state. Done when each confirmed change is applied and its verification check passed.

## Guidelines

- Classify steps only with the [framework.md](references/framework.md) natures — do not invent categories
- Prompt-driven guards ("discard X", "block Y") never match structural isolation; call them out
- A conditional branch counts as one step at the conditional baseline, not several
- Count each numbered sub-step of a chained workflow individually
- Trigger reliability gates the chain: a Leaky or Narrow verdict caps P(useful) regardless of the workflow score
- Every suggestion carries an expected gain and a verification step; never propose a change you cannot verify
