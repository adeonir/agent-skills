# Discovery

Establish the available context and route one design-brief operation.

## When to Use

Load before every operation.

## Workflow

1. Scan the project root for `DESIGN.md`, then scan `docs/design/moodboard.md`, `docs/product/PRODUCT.md`, `docs/product/PRD.md`, and `docs/product/brainstorm.md`. Do not look for an older DESIGN.md path or schema.
2. Read found artifacts as claims to check, not authority to inherit. Extract only the product context, stated register, visual intent, constraints, and current tokens that the selected operation needs. Strip upstream IDs, milestones, feature names, and roadmap language from every design output.
3. Identify the source on hand: codebase, URL, HTML/CSS, images, design-tool file, or text description.
4. Identify the requested operation from the user's vocabulary:

| Vocabulary or state | Route |
|---|---|
| no visual reference, explore, find a look, not sure how it should feel | `direction` |
| author, create, extract, codify, refresh, rebrand, evolve, sync | `design` |
| assess, audit current identity, what is consistent or drifted | `identity-assessment` |
| preview, tune, comment, inspect visually | `preview` |
| validate, lint, check DESIGN.md | `validate` |
| export tokens | `export` |
| compare versions, token diff, regressions | `diff` |

5. Classify the field internally:
   - **Greenfield** — no identity must be preserved. A supplied visual reference gives the direction; route directly to design. Only product context or a vague feeling means direction is absent; route to direction first.
   - **Brownfield** — an existing identity must be described, preserved, changed, or reconciled. Run identity assessment before any mutation.
6. Classify the brownfield intent when the request names it:

| Intent | Meaning |
|---|---|
| `inherit` | Codify the confirmed current identity. |
| `refresh` | Preserve its DNA and make the smallest sufficient improvement. |
| `rebrand` | Replace the identity while preserving product surfaces and structure. |
| `evolve` | Compare the identity with stated product intent and recommend the required scale of change. |
| `sync` | Accept implementation values as truth for drifted token groups without introducing a direction. |

7. When the request is ambiguous between refresh and rebrand, carry both into identity assessment. Recommend one after examining whether the existing DNA still serves the stated intent, then wait for confirmation.
8. Determine surfaces by context and take the dominant register from `PRODUCT.md` when present. Ask only when neither the artifacts nor the request settle a load-bearing surface, register exception, source conflict, or intended operation.
9. Hand the selected instruction: operation, field, explicit or pending intent, surfaces, register, source, and found artifacts. Never load two operation instructions together.

Preview, validate, export, and diff route directly after the scan. Brownfield design routes through identity assessment first.

## Error Handling

- If the only found identity uses an older path, treat the root `DESIGN.md` as absent.
- If two sources claim the same token value, ask which source is authoritative before assessment or authoring.
- If a required source cannot be read, ask for another source and do not infer its contents.
