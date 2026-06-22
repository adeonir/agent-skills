# Reliability Framework

Step natures, baselines, tiers, and levers for the compound-reliability analysis.

## When to Use

During Steps 4–6 of the analysis, to classify each step and read the end-to-end
product. Loaded alongside SKILL.md, never on its own.

## Step Natures

| Nature | Examples | Baseline |
|--------|----------|----------|
| Deterministic | git command, API call + lookup table, script | ~99% |
| Conditional | path A/B branch based on state | ~93% |
| Generation (isolated) | schema-validated output, narrow input, no conversation history | ~90% |
| Prompt-driven | instruction guard ("discard X", "block Y") | ~88% |
| Generation (free-form) | unconstrained text output (message, body, summary) | ~82% |

## Tiers

Multiply the per-step baselines for an end-to-end product, then label it:

| Tier | Product |
|------|---------|
| Strong | ≥ ~90% |
| Moderate | ~75–90% |
| Fragile | < ~75% |

Baselines are heuristic and assume step failures are roughly independent; the
product is a transparent calculation over visible inputs, not a hit-rate
prediction. Even 95%/step compounds to ~74% over six steps — step count is
itself a reliability lever.

## Levers

Three levers raise reliability, highest to lowest impact:

1. **Scripts > prompts** — when the work is mechanical, write code. The model
   decides *when*; the script decides *how*.
2. **Idempotence** — read state before writing; running twice produces one change.
3. **Explicit inputs/outputs** — declare what enters, what exits, validate
   deterministically.
