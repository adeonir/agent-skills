---
name: design-builder
description: >-
  Greenfield design pipeline for any digital product (landing pages,
  websites, web apps, mobile apps): extract content and tokens, define
  structure or screen flow, preview and refine designs, sync iterations,
  package handoff. Use when building pages or app screens from references,
  images, briefs, or an existing codebase; defining layout or screen flow;
  previewing and tuning designs; syncing changes from Pencil or
  implementation back to tokens and structure; packaging a handoff bundle
  for another agent or developer. Triggers on "extract copy", "extract
  design", "extract from codebase", "web capture", "wireframe", "layout",
  "structure", "screen flow", "preview", "variants", "tune design",
  "mockup", "redesign", "create prototype", "design review", "sync
  design", "sync tokens", "handoff design", "package design".
---

# Design Builder

**Recommended effort:** xhigh for preview, design extraction, and sync phases;
high for discovery, structure, and handoff.

Greenfield design pipeline for any digital product: discover, extract,
structure, preview, refine, sync, handoff.

## Workflow

```
discovery --> content --> tokens --> structure --> preview --> final
                                                     ^__|  (tune / comment / apply-across loop)

sync:    pen or implementation code  -->  design.json + structure.md
handoff: collected artifacts         -->  single bundle for external use
```

Each step is independent. Can run isolated or chained. Discovery is always
the first step — never skip it.

design-builder is greenfield-first: it assumes no existing codebase. The
"extract from codebase" path in `design.md` is an alternative for redesign
or migration work, not the primary flow.

Project type routes behavior in later steps:

- **page-based** (landing-page, website): section-oriented questions and presets
- **screen-based** (web-app, mobile-app): screen-flow and navigation questions, app-oriented presets

Design final can be: HTML standalone, Paper/Pencil/Figma via MCP, input
for `spec-driven` (implementation), or a handoff bundle for external use.

### Discovery

Before any operation, establish project context.

**Step 1 — Check existing context.** Look for:

- `.artifacts/docs/prd.md` — PRD
- `.artifacts/docs/brief.md` — Brief
- `.artifacts/brainstorm/` — brainstorming direction
- `.artifacts/docs/*-research.md` — naming research

If found, read and extract purpose, audience, tone, and key features. Skip
to the relevant trigger operation.

**Step 2 — Lightweight discovery (when no context exists).** Ask one question
at a time:

1. What is the project purpose? (landing page, website, web app, mobile app, other)
2. Who is the target audience?
3. What is the visual reference? (URLs, screenshots, brief documents, descriptions, existing codebase for redesigns)
4. Any brand or style constraints? (colors, fonts, existing guidelines)

Lock in project type early — it routes later steps into page-based or
screen-based flows. If the user answers "I don't know" to any question,
mark as TBD and move forward.

**Step 3 — Route to operation.**

Phase 1 — Extraction (how to obtain content and tokens):

```
Has URL reference?
  Yes --> Extract copy (full page or captured region) --> Extract design
  No  --> Has image reference?
    Yes --> Extract design (from images)
    No  --> Has existing codebase for redesign?
      Yes --> Extract design (from codebase)
      No  --> Visual discovery (tone, colors, typography) --> Extract design
```

Phase 2 — Structure and Preview (design the experience):

```
tokens + validate complete --> Structure --> Preview --> Design final
                                                ^_______|  (refinement loop)
```

Phase 3 — Sync and Handoff (optional, post-approval):

```
Derivative changed (pen or code) --> Sync (propagate to source of truth)
External implementer needs package --> Handoff (bundle + intent)
```

## Context Loading Strategy

Load only the reference matching the current trigger. For preview operations,
also load `aesthetics.md` and `web-standards.md` as auto-loaded dependencies.

**Never simultaneous:**

- Multiple operation references (e.g., `copy.md` + `structure.md`)

## Triggers

### Extraction

| Trigger Pattern | Reference |
|-----------------|-----------|
| Extract copy, copy from URL, web capture, content from website, brief document | [copy.md](references/copy.md) |
| Extract design, design from image, design tokens, extract from codebase | [design.md](references/design.md) |

### Structure

| Trigger Pattern | Reference |
|-----------------|-----------|
| Wireframe, layout, structure, screen flow, organize content | [structure.md](references/structure.md) |

### Preview and Refinement

| Trigger Pattern | Reference |
|-----------------|-----------|
| Preview, variants, mockup, design review, tune design, comment on design | [preview.md](references/preview.md) |

### Sync

| Trigger Pattern | Reference |
|-----------------|-----------|
| Sync design, sync tokens, update design.json, propagate changes | [sync.md](references/sync.md) |

### Handoff

| Trigger Pattern | Reference |
|-----------------|-----------|
| Handoff design, package design, bundle for developer | [handoff.md](references/handoff.md) |

### Auto-Loaded (not direct triggers)

- `aesthetics.md` — loaded by `preview.md` as design principles
- `web-standards.md` — loaded by `preview.md` as implementation rules

## Cross-References

```
brainstorming ---------> design-builder (direction feeds discovery)
product-naming --------> design-builder (name feeds discovery)
copy.md ---------------> structure.md (content informs structure)
design.md -------------> structure.md (tokens inform visual hierarchy)
design.md -------------> preview.md (tokens style the preview)
structure.md ----------> preview.md (structure + tokens = preview)
aesthetics.md ---------> preview.md (design principles)
web-standards.md ------> preview.md (implementation rules)
preview.md ------------> sync.md (iterations in derivatives trigger sync)
sync.md <-------------- design.pen, implementation (derivatives flow back)
sync.md ---------------> design.json, structure.md (source of truth)
handoff.md <----------- all artifacts (collects and points, never embeds)
design-builder --------> spec-driven (approved design feeds implementation)
spec-driven -----------> sync.md (implementation changes propagate back)
```

## Guidelines

**DO:**
- Ask one question at a time when gathering context from the user
- Ask user for project name and use kebab-case for directory names
- Lock in project type during discovery — it routes later steps
- Check for existing context before any operation (PRD, brief, brainstorm, naming)
- Check for existing `copy.yaml`, `design.json`, `structure.md` before starting
- Run lightweight discovery when no prior context exists
- Validate coherence with structure before preview, even when a wireframe exists
- Treat `design.json` and `structure.md` as source of truth — use sync to reconcile derivatives
- Suggest next steps and missing prerequisites after each operation

**DON'T:**
- Skip discovery (contrasts: check for existing context or run lightweight discovery)
- Ignore existing artifacts when they are available (contrasts: check for existing artifacts)
- Block on missing PRD/Brief (contrasts: run lightweight discovery)
- Skip structure (contrasts: validate coherence with structure before preview)
- Silently overwrite `design.json` or `structure.md` with derivative state (contrasts: use sync with explicit conflict resolution)
- Use page-based questions or presets for a web-app or mobile-app (contrasts: route by project type)

## Output

### Templates

| Context | Template |
|---------|----------|
| Copy extraction output | [copy.md](templates/copy.md) |
| Design tokens output | [design.md](templates/design.md) |
| Handoff bundle output | [handoff.md](templates/handoff.md) |

### Artifacts

```
.artifacts/design/
├── copy.yaml              # Structured content (sections or screens)
├── design.json            # Design tokens (validated)
├── structure.md           # Layout or screen-flow decisions
├── design.pen             # Pencil iteration surface (optional)
├── handoff.md             # Handoff bundle (optional)
└── preview/               # Preview session output
    ├── guided/            # Per-question decisions (guided mode)
    ├── variants/          # Complete variants (exploratory mode)
    └── components/        # Isolated component previews (optional)
```

## Error Handling

- No PRD/Brief: run lightweight discovery, never block on it
- No `copy.yaml`: proceed without it, or suggest running extract copy first
- No `design.json`: required for structure/preview — suggest running extract design
- No `structure.md`: required for preview — suggest running structure first
- Reference URL unavailable: ask user to paste a screenshot or use a captured-region path
- Project type unclear: ask the user before routing — page-based and screen-based differ throughout
- Derivative out of sync with `design.json`/`structure.md`: suggest running sync before further work
