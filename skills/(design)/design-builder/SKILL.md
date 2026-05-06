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
  "preview the design", "creative variants", "tune design",
  "mockup", "redesign this app", "redesign the landing page",
  "redesign the screen", "modernize this app",
  "brand refresh", "visual prototype",
  "pivot the design", "author DESIGN.md",
  "refresh design tokens", "validate DESIGN.md", "check DESIGN.md",
  "audit design tokens", "push design to external tool". Not for feature
  spec/design.md (use spec-driven), system architecture (use system-design),
  or PR/code review (use git-helpers).
effort: xhigh
---

# Design Builder

**Recommended effort:** xhigh for inputs and preview phases; high for discovery and structure.

Greenfield design pipeline for any digital product: discover, extract content, author `DESIGN.md`, define layout or screen flow, preview, refine.

## Workflow

```
discovery --> copy --> inputs --> structure --> preview --> assets --> final
                                                  ^__|  (tune / comment / apply-across loop)
```

Each step is independent. Can run isolated or chained (`discovery.md` pre-loads before every operation). Assets is optional: auto-invoked after preview approval, or triggered directly. design-builder is greenfield-first — codebase path inside `inputs.md` is an alternative for redesign or migration, not the primary flow. Final design can be served as HTML, pushed to an external design tool when the matching MCP is available, or handed to `spec-driven` for implementation.

## Triggers

| Trigger Pattern | Reference |
|-----------------|-----------|
| Extract copy, copy from URL, web capture, content from website, brief document | [copy.md](references/copy.md) |
| Extract design tokens, author DESIGN.md, refresh design tokens, extract design from images, extract design from codebase, pull design from external design tool | [inputs.md](references/inputs.md) |
| Create a wireframe, layout the page, structure the content, screen flow, organize content, validate this wireframe | [structure.md](references/structure.md) |
| Preview the design, visual mockup, tune the design, comment on the design, creative variants, pivot the design, apply across variants, push the design to an external design tool | [preview.md](references/preview.md) |
| Validate DESIGN.md, check DESIGN.md, audit design tokens, lint the design system | [validate.md](references/validate.md) |
| Redesign this app, modernize this interface, brand refresh on existing product, change the vibe without rebuilding the IA | [redesign.md](references/redesign.md) |
| Generate hero banner, create product image, generate OG card, generate banner, image assets, generate image prompt, prompts for banner | [assets.md](references/assets.md) |

Notes:

- `discovery.md` is not a direct trigger. It loads before every operation — never skip it.
- `aesthetics.md` and `web-standards.md` are not direct triggers. They are auto-loaded by `preview.md`.
- `validate.md` is both a direct trigger (callable on demand) and auto-loaded by `inputs.md` Step 5 as the gate before declaring done.
- `assets.md` is both a direct trigger (callable on demand) and an optional sub-phase auto-invoked by `preview.md` after variant approval.

## Cross-References

```
discovery.md ----------> all refs (pre-loaded before every operation)
brainstorming ---------> design-builder (direction feeds discovery)
docs-writer -----------> design-builder (PRD/Brief feeds discovery)
copy.md ---------------> structure.md (content informs structure)
copy.md ---------------> inputs.md (content informs Voice and Do/Don't prose)
inputs.md -------------> structure.md (tokens inform layout decisions)
inputs.md -------------> preview.md (tokens style the preview)
inputs.md -------------> validate.md (Step 5 gate; auto-loaded before declaring done)
structure.md ----------> preview.md (Layout and Screen Flow shape the variants)
aesthetics.md ---------> preview.md (design principles)
aesthetics.md ---------> redesign.md (Style Axes inform aesthetic direction)
web-standards.md ------> preview.md (implementation rules)
validate.md -----------> DESIGN.md (read-only audit; no patch)
redesign.md -----------> inputs.md (delegates structure-only or aesthetic-only extraction)
redesign.md -----------> preview.md (delegates Exploratory creative variants for the new aesthetic)
redesign.md -----------> validate.md (final gate before declaring done)
preview.md ------------> external design tool (write-only push when MCP is available)
preview.md ------------> assets.md (optional sub-phase after variant approval)
external design tool --> inputs.md (read-only pull when user refreshes from a design-tool file)
inputs.md -------------> assets.md (tokens and prose drive prompts)
assets.md -------------> preview.md (re-render with real assets after generation)
assets.md -------------> spec-driven (approved assets feed implementation)
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
