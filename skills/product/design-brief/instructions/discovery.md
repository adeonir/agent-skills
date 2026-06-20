# Discovery

Establishes project context and routes to the correct operation reference.

## When to Use

Load at the start of every operation — before any trigger reference is loaded.

## Workflow

### Step 1: Check Existing Context

Look for:

- `docs/design/DESIGN.md` — already-authored visual identity
- `docs/design/moodboard.md` — locked visual direction (feeds token authoring)
- `docs/product/prd.md` — PRD
- `docs/product/brief.md` — Brief
- `docs/product/brainstorm.md` — strategic direction

If found, read and extract purpose, audience, tone, key features, and any
existing tokens. Tokens in `DESIGN.md` live in the YAML frontmatter at the top
of the file — parse that block as the authoritative state. A `moodboard.md` with
`status: locked` is a settled visual direction: treat it as a given direction
for token authoring. Skip to the relevant trigger operation.

### Step 2: Lightweight Discovery

Ask one question at a time:

1. Project surfaces, named by context (landing, dashboard, form, checkout…), and the register of each — brand (the design is the product) or product (the design serves a task)?
2. Source on hand: URL, images, brief document, codebase, vanilla HTML/CSS,
   design-tool file, or text description?
3. Visual references or constraints?

### Step 3: Classify Field

Infer field from source and intent — no explicit question to the user:

- **Greenfield** — no existing visual identity to preserve. Source is
  inspiration, not constraint. Typical sources: reference images, brand
  URL used as reference, text description. No legacy tokens; `DESIGN.md`
  starts from scratch. Greenfield splits on whether a direction is
  **given** or **absent**: a reference (images, URL, text description) or a
  locked `moodboard.md` is a given direction — route straight to token
  authoring, which extracts it. When only audience, PRD, or a vague feeling
  exists with no reference, the direction is absent — route to `direction.md`
  first to explore and lock a mood.
- **Brownfield** — existing visual identity must be honored, refactored,
  or replaced. Typical sources: codebase, vanilla HTML/CSS export,
  external design-tool file. Legacy tokens exist; `DESIGN.md` may
  already exist.

Within brownfield, three implicit sub-modes — detect by user vocabulary,
do not ask:

| Sub-mode | Trigger phrases | Skill behavior |
|----------|-----------------|----------------|
| inherit | "extract tokens", "document our current system", "audit design" | Pull legacy as-is, preserve names and roles |
| refresh | "modernize", "polish", "tighten", "tune" | Keep DNA, tighten scale, refresh prose |
| rebrand | "rebrand", "new identity", "brand refresh", "change the vibe" | Replace identity, preserve product surfaces and structure |

Partial cases (codebase defines colors but no typography) stay brownfield;
gaps are filled via images or description without flipping the field.

### Step 4: Route to Trigger

Load only the reference matching the activated trigger:

| Trigger intent | Reference | Auto-loads |
|----------------|-----------|------------|
| Mood exploration (direction absent, no reference) | `direction.md` | `aesthetics.md`, `brand.md` / `product.md` |
| Visual identity / DESIGN.md | `design.md` | `aesthetics.md`, `brand.md` / `product.md`, `validate.md` |
| Token preview / tune (DESIGN.md exists) | `preview.md` | `anti-patterns.md` |
| Validation only | `validate.md` | — |
| Reconcile / drift sync | `reconcile.md` | `validate.md` |

Never load multiple operation references simultaneously.

The surfaces present in the source route behavior in subsequent steps, each
under a register (brand or product). A project may carry several — route by every
surface it has, named by context, not a single declared type:

- **brand surfaces** (landing, campaign, portfolio, about): section-oriented,
  conversion-facing questions
- **product surfaces** (dashboard, settings, forms, data tables): screen-flow,
  navigation, and state questions
- **storefronts straddle**: the marketing / catalog shell is brand, the
  checkout / account flow is product (see
  [../references/brand.md](../references/brand.md) /
  [../references/product.md](../references/product.md))
