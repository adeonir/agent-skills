---
name: design-builder
description: >-
  Design-to-code pipeline: extract copy from URLs, extract design tokens
  from images, then build React components or HTML preview variants.
  Use when: extracting content from websites, extracting design systems,
  generating frontend code, previewing design variants, sending to Figma
  via MCP. Triggers on "extract copy", "extract design", "build frontend",
  "generate variants", "export design", "send to Figma".
metadata:
  author: github.com/adeonir
  version: "1.0.1"
---

# Design Builder

Design-to-code pipeline: discover, extract, tokenize, build.

## Workflow

```
discovery --> copy --> design --> frontend / variants / export
```

Each step is independent. Can run isolated or chained.
Discovery is always the first step -- never skip it.

## Discovery

Before any operation, establish project context.

### Step 1: Check Existing Context

Look for existing documents in `.specs/docs/`:

- `prd.md` -- PRD
- `brief.md` -- Brief

If found: read and extract purpose, audience, tone, and key features.
Skip to the relevant trigger operation.

### Step 2: Lightweight Discovery (when no PRD/Brief exists)

Ask up to 4 questions, one stage only:

1. What is the project purpose? (landing page, app, tool, portfolio)
2. Who is the target audience?
3. What is the visual reference? (URLs, screenshots, descriptions)
4. Any brand or style constraints? (colors, fonts, existing guidelines)

If the user answers "I don't know" to any question, mark as TBD and move forward.
Summarize understanding before proceeding.

### Step 3: Route to Operation

**Phase 1 -- Extraction** (how to obtain design tokens):

```
Has URL reference?
  Yes --> Extract copy --> Extract design
  No  --> Has image reference?
    Yes --> Extract design
    No  --> Visual discovery (tone, colors, typography) --> Extract design
```

**Phase 2 -- Building** (what to build -- user chooses):

```
design.json exists --> What to build?
  Preview first    --> Variants --> Frontend or Export
  Build directly   --> Frontend
  Send to Figma    --> Variants --> Export
  External tool    --> Generate prompt (v0, aura.build, replit, etc.)
```

Valid paths after design.json:
- design --> variants --> frontend
- design --> variants --> export
- design --> frontend (directly)
- design --> prompt for external tool

## Artifacts

```
.specs/docs/
├── prd.md                             # PRD (optional)
├── brief.md                           # Brief (optional)
└── {project-name}/
    ├── copy.yaml                      # Structured content
    ├── design.json                    # Design tokens
    ├── variants/
    │   ├── minimal/index.html         # Variant preview
    │   ├── editorial/index.html
    │   ├── startup/index.html
    │   ├── bold/index.html
    │   ├── {custom}/index.html        # Custom variant (if requested)
    │   └── index.html                 # Comparison page
src/                                   # React components (frontend)
```

## Triggers

### Extraction

| Trigger Pattern | Reference |
|-----------------|-----------|
| Extract copy, copy from URL, content from website | [copy.md](references/copy.md) |
| Extract design, design from image, design tokens | [design.md](references/design.md) |

### Building

| Trigger Pattern | Reference |
|-----------------|-----------|
| Build frontend, create components, generate React | [frontend.md](references/frontend.md) |
| Generate variants, preview designs, HTML variants | [variants.md](references/variants.md) |
| Export design, export to Figma, send to Figma | [export.md](references/export.md) |

## Cross-References

```
copy.md ---------> design.md (content informs design)
design.md -------> frontend.md (tokens required)
design.md -------> variants.md (tokens required)
variants.md -----> frontend.md (user picks variant, then builds React)
variants.md -----> export.md (variants required for Figma export)
```

## Required Skills

The `frontend-design` skill is required for **variant generation** and **frontend building**.
It provides design principles to avoid generic AI aesthetics.

Before running any **building** trigger (frontend, variants), check if the skill
is installed by looking for files in `~/.claude/skills/frontend-design/`. If not found,
warn the user and suggest installing it:

```
The frontend-design skill is required but not installed.
Install it: npx skills add https://github.com/anthropics/skills/tree/main/frontend-design
```

Extraction triggers (copy, design) do NOT require this skill.

## Guidelines

- **Project naming**: Ask user for project name. Use kebab-case for directory names.
- **Discovery first**: Always check for existing PRD/Brief before any operation.
  Use them as context when available.
- **Existing artifacts**: Always check for existing copy.yaml, design.json before starting.
  Use them as context when available.
- **Missing prerequisites**: If a required artifact is missing, suggest which step
  to run first (e.g., "Run extract design first to generate design.json").

## Suggestions

After completing any operation, suggest next steps without coupling to specific skills:

- If no PRD/Brief existed: "For more complete product documentation, consider creating a PRD or Brief before the next iteration."
- If variants were generated: "To send a variant to Figma for refinement, run export to Figma."
- Standard next steps per operation (already defined in each reference file).

## Error Handling

- No PRD/Brief: Run lightweight discovery, never block on it
- No copy.yaml: Proceed without it, or suggest running extract copy first
- No design.json: Required for frontend/variants/export -- suggest running extract design
- No frontend-design skill: Required for frontend/variants -- warn and suggest install
- WebFetch fails: Ask user to paste a screenshot instead
