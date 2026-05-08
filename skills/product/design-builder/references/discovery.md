# Discovery

Establishes project context and routes to the correct operation reference.

## When to Use

Load at the start of every operation — before any trigger reference is loaded.

## Workflow

### Step 1 — Check Existing Context

Look for:

- `<project-root>/DESIGN.md` — already-authored visual identity
- `.artifacts/docs/prd.md` — PRD
- `.artifacts/docs/brief.md` — Brief
- `.artifacts/brainstorm/` — direction artifacts
- `.artifacts/docs/*-research.md` — naming research
- `.artifacts/design/copy.yaml` — extracted content payload

If found, read and extract purpose, audience, tone, key features, and any
existing tokens. Skip to the relevant trigger operation.

### Step 2 — Lightweight Discovery

Ask one question at a time:

1. Project type: landing-page, website, web-app, or mobile-app?
2. Source on hand: URL, images, brief document, codebase, design-tool file,
   or text description?
3. Visual references or constraints?

### Step 3 — Route to Trigger

Load only the reference matching the activated trigger:

| Trigger intent | Reference | Auto-loads |
|----------------|-----------|------------|
| Content extraction | `copy.md` | — |
| Visual identity / DESIGN.md | `inputs.md` | `validate.md` (Step 5) |
| Structure / wireframe | `structure.md` | — |
| Preview / refinement | `preview.md` | `aesthetics.md`, `web-standards.md` |
| Validation only | `validate.md` | — |
| Redesign | `redesign.md` | — |
| Asset generation | `assets.md` | — |

Never load multiple operation references simultaneously.

Project type routes behavior in all subsequent steps:

- **page-based** (landing-page, website): section-oriented questions and presets
- **screen-based** (web-app, mobile-app): screen-flow and navigation questions,
  app-oriented presets
