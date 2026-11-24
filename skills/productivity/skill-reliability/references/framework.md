# Reliability Framework

Step natures, baselines, tiers, and levers for the compound-reliability analysis.

## Step Natures

| Nature | Examples | Baseline |
|--------|----------|----------|
| Deterministic | git command, API call + lookup table, script | ~99% |
| Conditional | path A/B branch based on state | ~93% |
| Generation (isolated) | schema-validated output, narrow input, no conversation history | ~90% |
| Prompt-driven | instruction guard ("discard X", "block Y") | ~88% |
| Generation (free-form) | unconstrained text output (message, body, summary) | ~82% |

## Tiers

Multiply the per-decision baselines for an end-to-end product, then label it:

| Tier | Product |
|------|---------|
| Strong | ≥ ~90% |
| Moderate | ~75–90% |
| Fragile | < ~75% |

Classify a step by its **decision**, not by its presence. A step that runs a fixed command, reads a file, or verifies a named condition is a checkpoint and carries no baseline of its own. A step that asks the model to choose — which branch, which wording, which file — carries the baseline of that choice. Count only decisions in the product.

Baselines are heuristic and assume decisions fail roughly independently; the product is a transparent calculation over visible inputs, not a hit-rate prediction. Six discretionary decisions at ~95% each compound to ~74%; six checkpoints add no risk.

## Levers

Three levers raise reliability, highest to lowest impact:

1. **Scripts > prompts** — when the work is mechanical, write code. The model decides *when*; the script decides *how*.
2. **Idempotence** — read state before writing; running twice produces one change.
3. **Explicit inputs/outputs** — declare what enters, what exits, validate deterministically.

A lever applies only where the model cannot do the work unaided. Every suggestion names why it cannot; when it can, the change belongs in the instruction, not in a script or a merged step.
