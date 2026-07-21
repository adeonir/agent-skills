# Discovery

Establishes project context and routes to the correct operation reference.

## When to Use

Load at the start of every operation — before any trigger reference is loaded. Step 1's artifact scan runs always; Steps 2–4 classify and route, and matter only when the route depends on classification (`direction`, `design`). `validate` and `preview` route from the trigger alone — for them, discovery is the Step 1 scan, and their own prerequisite checks already cover the DESIGN.md lookup.

## Workflow

### Step 1: Check Existing Context

Look for:

- `docs/design/DESIGN.md` — already-authored visual identity
- `docs/design/moodboard.md` — locked visual direction (feeds token authoring)
- `docs/product/PRD.md` — PRD
- `docs/product/PRODUCT.md` — positioning (register, anti-references, principles, personality)
- `docs/product/brainstorm.md` — strategic direction

If found, read and extract purpose, audience, tone, key features, and any existing tokens. From `PRODUCT.md`, read the default register, anti-references, principles, and personality as context to translate into tokens — never copy its prose verbatim into `DESIGN.md`. Tokens in `DESIGN.md` live in the YAML frontmatter at the top of the file — parse that block as the authoritative state. A `moodboard.md` with `status: locked` is a settled visual direction: treat it as a given direction for token authoring. Skip to the relevant trigger operation.

### Step 2: Lightweight Discovery

Ask one question at a time:

1. Project surfaces, named by context (landing, dashboard, form, checkout…). Register comes from `PRODUCT.md`'s default when present; ask it per surface only when no `PRODUCT.md` exists or a surface diverges from the default — brand (the design is the product) or product (the design serves a task)?
2. Source on hand: URL, images, brief document, codebase, vanilla HTML/CSS, design-tool file, or text description?
3. Visual references or constraints?

### Step 3: Classify Field

Infer field from source and intent — no explicit question to the user:

- **Greenfield** — no existing visual identity to preserve. Source is inspiration, not constraint. Typical sources: reference images, brand URL used as reference, text description. No legacy tokens; `DESIGN.md` starts from scratch. Greenfield splits on whether a direction is **given** or **absent**: a reference (images, URL, text description) or a locked `moodboard.md` is a given direction — route straight to token authoring, which extracts it. When only audience, PRD, or a vague feeling exists with no reference, the direction is absent — route to `direction.md` first to explore and lock a mood.
- **Brownfield** — existing visual identity must be honored, refactored, or replaced. Typical sources: codebase, vanilla HTML/CSS export, external design-tool file. Legacy tokens exist; `DESIGN.md` may already exist.

Within brownfield, five implicit sub-modes — detect by user vocabulary, do not ask:

| Sub-mode | Trigger phrases | Skill behavior |
|----------|-----------------|----------------|
| inherit | "extract tokens", "document our current system", "audit design" | Pull legacy as-is, preserve names and roles |
| refresh | "modernize", "polish", "tighten", "tune" | Keep DNA, tighten scale, refresh prose |
| rebrand | "rebrand", "new identity", "brand refresh", "change the vibe" | Replace identity, preserve product surfaces and structure |
| evolve | "evolve", "does our design still fit", "align the design to the strategy", "rethink the direction against the PRD" | Extract the current identity, diff it against the stated intent (`PRODUCT.md` / PRD), propose a delta and recommended direction before authoring |
| sync | "sync design from implementation", "update DESIGN.md from code", "reconcile drift", "refresh design tokens from this codebase" | Implementation is the source of truth for drifted values; diff against `DESIGN.md` and patch the drifted groups, narrative sections untouched. Requires an existing `DESIGN.md` — without one, the ask is inherit |

When the ask does not name a sub-mode ("redesign this", "it feels dated", "overhaul"), diagnose rather than default. An identity whose DNA still serves the stated intent → `refresh` (preserve the palette and type DNA, evolve within it); an identity that no longer fits → `rebrand` (replace it, preserve the product surfaces). Bias toward refresh when the system is sound — defaulting to overhaul is where a brand's real palette gets replaced by a generic one (AI-slop color) for no reason.

Partial cases (codebase defines colors but no typography) stay brownfield; gaps are filled via images or description without flipping the field.

### Step 4: Route to Trigger

Route to the operation the trigger names — the trigger table lives in SKILL.md's Quick start. What discovery hands downstream is the classification: field, sub-mode, surfaces, register. `design.md` picks its flow from that hand-off — greenfield author, or the brownfield sub-mode detected above.

Never load multiple operation references simultaneously.

Register loading follows the surfaces: a project under one register reads only its register file downstream; a project whose surfaces span both registers reads both — [../references/brand.md](../references/brand.md) and [../references/product.md](../references/product.md) define the surface lists and the straddle cases.
