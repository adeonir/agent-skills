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

1. Project surfaces: marketing pages, app screens, commerce (catalog + checkout), or a combination?
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
| Mood exploration (direction absent, no reference) | `direction.md` | `aesthetics.md`, `presets.md` |
| Visual identity / DESIGN.md | `design-brief.md` | `validate.md` |
| Token preview / tune (DESIGN.md exists) | `preview.md` | `aesthetics.md`, `anti-patterns.md` |
| Validation only | `validate.md` | — |
| Reconcile / drift sync | `reconcile.md` | `validate.md` |

Never load multiple operation references simultaneously.

The surface kinds present in the source route behavior in subsequent steps.
A project may carry several — route by every surface it has, not a single
declared type:

- **marketing / content surfaces**: section-oriented questions and presets
- **app / dashboard screens**: screen-flow and navigation questions,
  app-oriented presets
- **storefront / commerce surfaces**: product catalog, PLP/PDP, cart and
  checkout flows, trust-signal presets
