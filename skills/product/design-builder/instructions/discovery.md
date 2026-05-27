# Discovery

Establishes project context and routes to the correct operation reference.

## When to Use

Load at the start of every operation — before any trigger reference is loaded.

## Workflow

### Step 1: Check Existing Context

Look for:

- `docs/design/DESIGN.md` — already-authored visual identity
- `.artifacts/docs/prd.md` — PRD
- `.artifacts/docs/brief.md` — Brief
- `.artifacts/brainstorm/` — direction artifacts
- `.artifacts/docs/*-research.md` — naming research
- `docs/design/copy.yaml` — extracted content payload

If found, read and extract purpose, audience, tone, key features, and any
existing tokens. Tokens in `DESIGN.md` live in the YAML frontmatter at the top
of the file — parse that block as the authoritative state. Skip to the
relevant trigger operation.

### Step 2: Lightweight Discovery

Ask one question at a time:

1. Project type: landing-page, website, web-app, mobile-app, or e-commerce?
2. Source on hand: URL, images, brief document, codebase, vanilla HTML/CSS,
   design-tool file, or text description?
3. Visual references or constraints?

### Step 3: Classify Field

Infer field from source and intent — no explicit question to the user:

- **Greenfield** — no existing visual identity to preserve. Source is
  inspiration, not constraint. Typical sources: reference images, brand
  URL used as reference, text description. No legacy tokens; `DESIGN.md`
  starts from scratch.
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
| Content extraction | `copy.md` | — |
| Visual identity / DESIGN.md | `design.md` | `validate.md` |
| Structure / wireframe | `structure.md` | — |
| Preview / refinement | `preview.md` | `aesthetics.md`, `web-standards.md` |
| Validation only | `validate.md` | — |
| Redesign (anchor + new reference) | `redesign.md` | — |
| Reconcile / drift sync | `reconcile.md` | `validate.md` |

Never load multiple operation references simultaneously.

Project type routes behavior in all subsequent steps:

- **page-based** (landing-page, website): section-oriented questions and presets
- **screen-based** (web-app, mobile-app): screen-flow and navigation questions,
  app-oriented presets
- **commerce-based** (e-commerce): product catalog, PLP/PDP, cart and checkout
  flows, trust-signal presets
