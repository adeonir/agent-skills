---
name: design-builder
description: >-
  Product-engineer design pipeline: extract content and tokens, define
  structure, preview and approve designs. Use when building pages from
  reference URLs or screenshots, extracting design systems, defining
  page structure, previewing designs, or redesigning sites. Triggers on
  "extract copy", "extract design", "wireframe", "layout", "structure",
  "preview", "variants", "mockup", "build from reference", "redesign
  this", "create prototype", "design review".
---

# Design Builder

Product-engineer design pipeline: discover, extract, structure, preview, approve.

## Workflow

```
discovery --> content --> tokens + validate --> structure --> preview --> design final
```

Each step is independent. Can run isolated or chained.
Discovery is always the first step -- never skip it.

Design final can be: HTML standalone, Paper/Pencil/Figma via MCP, or input
for spec-driven (implementation).

## Context Loading Strategy

Load only the reference matching the current trigger. For preview operations,
also load `aesthetics.md` and `web-standards.md` as auto-loaded dependencies.

**Never simultaneous:**
- Multiple operation references (e.g., copy.md + structure.md)

## Triggers

### Extraction

| Trigger Pattern | Reference |
|-----------------|-----------|
| Extract copy, copy from URL, content from website | [copy.md](references/copy.md) |
| Extract design, design from image, design tokens | [design.md](references/design.md) |

### Structure

| Trigger Pattern | Reference |
|-----------------|-----------|
| Wireframe, layout, structure, organize content | [structure.md](references/structure.md) |

### Preview

| Trigger Pattern | Reference |
|-----------------|-----------|
| Preview, variants, mockup, design review | [preview.md](references/preview.md) |

### Auto-Loaded (not direct triggers)

- `aesthetics.md` -- loaded by `preview.md` as design principles
- `web-standards.md` -- loaded by `preview.md` as implementation rules

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
design-builder --------> spec-driven (approved design feeds implementation)
```

## Discovery

Before any operation, establish project context.

### Step 1: Check Existing Context

Look for existing documents:

- `.artifacts/docs/prd.md` -- PRD
- `.artifacts/docs/brief.md` -- Brief
- `.artifacts/brainstorm/` -- brainstorming direction
- `.artifacts/docs/*-research.md` -- naming research

If found: read and extract purpose, audience, tone, and key features.
Skip to the relevant trigger operation.

### Step 2: Lightweight Discovery (when no context exists)

Ask one question at a time:

1. What is the project purpose? (landing page, app, tool, portfolio)
2. Who is the target audience?
3. What is the visual reference? (URLs, screenshots, descriptions)
4. Any brand or style constraints? (colors, fonts, existing guidelines)

If the user answers "I don't know" to any question, mark as TBD and move forward.

### Step 3: Route to Operation

**Phase 1 -- Extraction** (how to obtain design tokens):

```
Has URL reference?
  Yes --> Extract copy --> Extract design
  No  --> Has image reference?
    Yes --> Extract design
    No  --> Visual discovery (tone, colors, typography) --> Extract design
```

**Phase 2 -- Structure and Preview** (design the experience):

```
tokens + validate complete --> Structure --> Preview --> Design final
```

## Templates

| Context | Template |
|---------|----------|
| Copy extraction output | [copy.md](templates/copy.md) |
| Design tokens output | [design.md](templates/design.md) |

## Artifacts

```
.artifacts/design/
├── copy.yaml              # Structured content
├── design.json            # Design tokens (validated)
├── structure.md           # Layout decisions
└── preview/               # Preview session output
    ├── guided/            # Per-question decisions (guided mode)
    └── variants/          # 4 HTML variants (exploratory mode)
```

## Guidelines

**DO:**
- Ask one question at a time when gathering context from the user
- Ask user for project name and use kebab-case for directory names
- Check for existing context before any operation (PRD, brief, brainstorm, naming)
- Check for existing copy.yaml, design.json, structure.md before starting
- Run lightweight discovery when no prior context exists
- Validate coherence with structure before preview, even when a wireframe exists
- Suggest next steps and missing prerequisites after each operation

**DON'T:**
- Skip discovery (contrasts: check for existing context or run lightweight discovery)
- Ignore existing artifacts when they are available (contrasts: check for existing artifacts)
- Block on missing PRD/Brief (contrasts: run lightweight discovery)
- Skip structure (contrasts: validate coherence with structure before preview)

## Error Handling

- No PRD/Brief: Run lightweight discovery, never block on it
- No copy.yaml: Proceed without it, or suggest running extract copy first
- No design.json: Required for structure/preview -- suggest running extract design
- No structure.md: Required for preview -- suggest running structure first
- Reference URL unavailable: ask user to paste a screenshot instead
