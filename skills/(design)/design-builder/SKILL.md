---
name: design-builder
description: >-
  Design-to-code pipeline: extract copy from URLs, extract design tokens
  from images, then build React components, HTML preview variants, or
  design-tool-optimized HTML. Use when: extracting content from websites,
  extracting design systems, generating frontend code, previewing design
  variants, exporting to Figma/Penpot. Triggers on "extract copy",
  "extract design", "build frontend", "generate variants", "export design".
metadata:
  author: github.com/adeonir
  version: "1.0.0"
---

# Design Builder

Design-to-code pipeline: extract, tokenize, build.

## Workflow

```
copy --> design --> frontend / variants / export
```

Each step is independent. Can run isolated or chained.
PRD is optional input at any step.

## Artifacts

```
.specs/docs/
├── prd-{project-name}.md              # PRD (optional)
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
    └── export/
        └── index.html                 # HTML optimized for design tools

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
| Export design, export to Figma, export to Penpot | [export.md](references/export.md) |

## Cross-References

```
copy.md ---------> design.md (content informs design)
design.md -------> frontend.md (tokens required)
design.md -------> variants.md (tokens required)
design.md -------> export.md (tokens required)
variants.md -----> frontend.md (user picks variant, then builds React)

External inputs (optional):
docs-writer -----> copy.md (product context)
docs-writer -----> design.md (product context)
```

## Required Skills

The `frontend-design` skill is required for **variant generation**, **frontend building**,
and **design export**. It provides design principles to avoid generic AI aesthetics.

Before running any **building** trigger (frontend, variants, export), check if the skill
is installed by looking for files in `~/.claude/skills/frontend-design/`. If not found,
warn the user and suggest installing it:

```
The frontend-design skill is required but not installed.
Install it: npx skills add https://github.com/anthropics/skills/tree/main/frontend-design
```

Extraction triggers (copy, design) do NOT require this skill.

## Guidelines

- **Project naming**: Ask user for project name. Use kebab-case for directory names.
- **Existing artifacts**: Always check for existing copy.yaml, design.json, and PRD
  before starting. Use them as context when available.
- **Missing prerequisites**: If a required artifact is missing, suggest which step
  to run first (e.g., "Run extract design first to generate design.json").

## Error Handling

- No copy.yaml: Proceed without it, or suggest running extract copy first
- No design.json: Required for frontend/variants/export -- suggest running extract design
- No PRD: Optional at every step, never block on it
- No frontend-design skill: Required for frontend/variants/export -- warn and suggest install
- WebFetch fails: Ask user to paste a screenshot instead
