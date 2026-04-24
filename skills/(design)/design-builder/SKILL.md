---
name: design-builder
description: >-
  Greenfield design pipeline for any digital product (landing pages,
  websites, web apps, mobile apps): extract content, author a single-file
  visual identity at the project root (DESIGN.md, tokens plus rationale),
  define layout or screen flow, preview and refine designs, push to an
  external design tool when available. Use when building pages or app
  screens from references, images, briefs, or an existing codebase;
  defining layout or screen flow; previewing and tuning designs;
  authoring or refreshing DESIGN.md from a source.
when_to_use: >-
  Triggers on "extract copy", "extract design", "extract from codebase",
  "web capture", "wireframe", "screen flow", "layout the page",
  "preview the design", "UI variants", "tune design", "mockup",
  "redesign the landing page", "redesign the screen", "visual prototype",
  "UI design review", "author DESIGN.md", "refresh design tokens",
  "push design to external tool". Not for feature spec/design.md
  (use spec-driven), system architecture (use system-design), or PR/code
  review (use git-helpers).
effort: xhigh
---

# Design Builder

**Recommended effort:** xhigh for inputs and preview phases; high for discovery and structure.

Greenfield design pipeline for any digital product: discover, extract content, author `DESIGN.md`, define layout or screen flow, preview, refine.

## Workflow

```
discovery --> copy --> inputs --> structure --> preview --> final
                                                  ^__|  (tune / comment / apply-across loop)
```

Each step is independent. Can run isolated or chained. Discovery is always the first step — never skip it.

design-builder is greenfield-first: it assumes no existing codebase. The codebase path inside `inputs.md` is an alternative for redesign or migration work, not the primary flow.

Project type routes behavior in later steps:

- **page-based** (landing-page, website): section-oriented questions and presets
- **screen-based** (web-app, mobile-app): screen-flow and navigation questions, app-oriented presets

Final design can be served as HTML via the preview server, or pushed to an external design tool when the matching MCP is available, or handed to `spec-driven` for implementation.

### Discovery

Before any operation, establish project context.

**Step 1 — Check existing context.** Look for:

- `<project-root>/DESIGN.md` — already-authored visual identity
- `.artifacts/docs/prd.md` — PRD
- `.artifacts/docs/brief.md` — Brief
- `.artifacts/brainstorm/` — brainstorming direction
- `.artifacts/docs/*-research.md` — naming research
- `.artifacts/design/copy.yaml` — extracted content payload

If found, read and extract purpose, audience, tone, key features, and any existing tokens. Skip to the relevant trigger operation.

**Step 2 — Lightweight discovery (when no context exists).** Ask one question at a time:

1. Project type: landing-page, website, web-app, or mobile-app?
2. Source on hand: URL, images, brief document, codebase, design-tool file, or text description?
3. Visual references or constraints?

## Context Loading Strategy

Load only the reference matching the current trigger. For preview operations, also load `aesthetics.md` and `web-standards.md` as auto-loaded dependencies.

**Never simultaneous:**

- Multiple operation references (e.g., `copy.md` + `structure.md`)

## Triggers

### Content

| Trigger Pattern | Reference |
|-----------------|-----------|
| Extract copy, copy from URL, web capture, content from website, brief document | [copy.md](references/copy.md) |

### Visual Identity (DESIGN.md)

| Trigger Pattern | Reference |
|-----------------|-----------|
| Extract design tokens, author DESIGN.md, refresh design tokens, extract design from images, extract design from codebase, pull design from external design tool | [inputs.md](references/inputs.md) |

### Structure

| Trigger Pattern | Reference |
|-----------------|-----------|
| Wireframe a screen, layout the page, structure the content, screen flow, organize content, validate this wireframe | [structure.md](references/structure.md) |

### Preview and Refinement

| Trigger Pattern | Reference |
|-----------------|-----------|
| Preview the design, UI variants, visual mockup, UI design review, tune the design, comment on the design, push the design to an external design tool | [preview.md](references/preview.md) |

Notes:

- `aesthetics.md` and `web-standards.md` are not direct triggers. They are auto-loaded by `preview.md`.

## Cross-References

```
brainstorming ---------> design-builder (direction feeds discovery)
product-naming --------> design-builder (name feeds discovery)
docs-writer -----------> design-builder (PRD/Brief feeds discovery)
copy.md ---------------> structure.md (content informs structure)
copy.md ---------------> inputs.md (content informs Voice and Do/Don't prose)
inputs.md -------------> structure.md (tokens inform layout decisions)
inputs.md -------------> preview.md (tokens style the preview)
structure.md ----------> preview.md (Layout and Screen Flow shape the variants)
aesthetics.md ---------> preview.md (design principles)
web-standards.md ------> preview.md (implementation rules)
preview.md ------------> external design tool (write-only push when MCP is available)
external design tool --> inputs.md (read-only pull when user refreshes from a design-tool file)
design-builder --------> spec-driven (approved design feeds implementation)
```

## Guidelines

**DO:**

- Ask one question at a time when gathering context from the user
- Treat `<project-root>/DESIGN.md` as the source of truth for visual identity
- Patch DESIGN.md section by section so each phase preserves the others' work
- Route preset and decision sets by project type
- Auto-load `aesthetics.md` and `web-standards.md` for every preview run
- Use ultrathink for inputs and preview phases — token and visual choices cascade
- Treat external design-tool files as user-owned — read or push only when the user asks and the matching MCP is available

**DON'T:**

- Skip discovery (contrasts: always run discovery first)
- Rewrite the whole DESIGN.md when only one section or block changed (contrasts: section-scoped patch)
- Mix operations in one turn (contrasts: route to the single matching reference)
- Create files in an external design tool (contrasts: treat those files as user-owned; only push when the file already exists)
- Block on a missing optional MCP (contrasts: fall back to HTML preview or another input source)

## Output

### Templates

| Context | Template |
|---------|----------|
| Copy extraction output | [copy.md](templates/copy.md) |
| DESIGN.md visual identity (output filename uppercase) | [design.md](templates/design.md) |

### Artifacts

```
<project-root>/
└── DESIGN.md             # Visual identity: tokens (frontmatter) + rationale (prose)

.artifacts/design/
├── copy.yaml             # Structured content (sections or screens), optional
└── preview/
    ├── guided/           # Per-question decisions
    ├── variants/         # Complete variants per preset
    └── components/       # Isolated component previews (optional)
```

External design-tool files (when used) live at the user's path of choice and are user-owned. Skill never creates them.

## Error Handling

- No project type set: ask before routing operations
- No DESIGN.md at project root: route to inputs to author it; only structure and preview require it as a prerequisite
- DESIGN.md malformed (invalid YAML frontmatter, duplicate section heading): report the parse error, ask user to fix or regenerate
- Required external context missing (PRD, brief): prompt user before proceeding
- Conflicting inputs (PRD says one thing, images another): ask user which is authoritative
- Optional MCP unavailable: skip the path that needs it, offer the HTML fallback

## Compact Instructions

Preserve:

- Current phase and loaded reference file
- Project type (page-based or screen-based), name, purpose, audience
- Path to `DESIGN.md` and which sections were patched in the current session
- Open user decisions, pending approvals, and refinement-loop state (tune sliders in flight, comments awaiting resolution)

Drop:

- Raw tool outputs and intermediate extraction results
- Scratch reasoning and discarded design directions

`DESIGN.md`, `copy.yaml`, and preview HTML files persist on disk and survive compaction. Re-read them on resume rather than reconstructing from memory.
