---
name: design-builder
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-04-20

### Changed

- Pair every SKILL.md Guideline DON'T with a concrete DO
- Centralize "ask one question at a time" rule in SKILL.md; drop restatement in structure.md Guidelines
- Drop meta "summarize understanding" instruction in Discovery step 2
- Tone down softening language in aesthetics.md Creative Mandate

## 2026-03-22

### Added

- Structure reference for layout decisions before visual style (create and validate modes)
- Preview reference with guided mode (per-question) and exploratory mode (4 variants)
- Preview server script (Bun) for interactive HTML fragments
- Heuristic validation in design extraction (Nielsen + WCAG AA)
- Discovery checks brainstorming direction and naming research artifacts

### Changed

- Workflow redesigned: discovery --> content --> tokens + validate --> structure --> preview
- Implementation delegated to spec-driven (design-builder stops at approved design)
- SKILL.md rewritten with new triggers, cross-references, and routing
- Design extraction next steps point to structure instead of frontend/variants

### Removed

- Frontend reference (implementation via spec-driven)
- Variants reference (content absorbed into preview reference)
- Export reference (Figma is a preview/wireframe method via MCP, not export step)

## 2026-03-21

### Changed

- Discovery adds "one question at a time" rule
- Frontend loads conventions.md for brownfield projects

## 2026-03-12

### Changed

- Remove allowed-tools and External Content Trust Boundary from SKILL.md
- Simplify error handling language to avoid tool-specific references

## 2026-03-10

### Changed

- Break frontmatter description into multi-line YAML to avoid obfuscation alerts

## 2026-03-02

### Added

- External Content Trust Boundary section in SKILL.md for fetched URL and image sanitization
- Inline trust notes at content ingestion points in copy and design references

## 2026-02-27

### Changed

- Centralize discovery in SKILL.md, references now only ask context-specific questions
- Enhance description with adjacent trigger contexts for better skill matching
- Standardize reference section naming: Process to Workflow, Rules to Guidelines
- Standardize reference closing sections: remove Checklist from frontend.md and variants.md, add Error Handling, merge What to AVOID into Guidelines, convert Fallback to Error Handling
- Add When to Use section to all reference files
- Add Templates section to SKILL.md with links to 2 templates
- Add Context Loading Strategy to SKILL.md
- Merge Suggestions into Guidelines in SKILL.md
- Convert SKILL.md Guidelines to DO/DON'T format
- Default preview port in `export.md` changed from 8081 to 8080

## 2026-02-26

### Added

- `web-standards.md` reference with implementation rules for accessibility, forms, performance, touch, images, hydration, dark mode, and i18n
- Cross-references from frontend.md and variants.md to web-standards.md
- Checklist items for web-standards compliance in frontend.md and variants.md

### Changed

- `frontend.md` accessibility section now delegates to web-standards.md, keeping only design-specific points
- `frontend.md` theme tokens section updated with explicit transition property rule

## 2026-02-25

### Changed

- Update copy and design references for simplified output filenames
- Enhance layout extraction with visual dimension system in design, frontend, and variants references

## 2026-02-20

### Changed

- Output directory migrated from `.specs/docs/{project-name}/` to `.artifacts/design/`
- Remove project-specific subdirectories (copy.yaml, design.json, variants/ now directly under .artifacts/design/)
- All references and templates updated with simplified paths

## 2026-02-19

### Added

- `aesthetics.md` reference with unified design principles (typography, color, motion, spatial composition, backgrounds, visual hierarchy, anti-patterns, responsive behavior, component states, depth and elevation)
- Implementation Concerns section in `frontend.md` (Accessibility, Responsive Implementation, Theme Tokens)

### Changed

- Export workflow now uses Figma MCP server directly instead of HTML intermediary
- Export requires variants as input instead of allowing direct export
- Penpot support and YashiTech extension dependency removed

### Removed

- External `frontend-design` skill dependency absorbed into `aesthetics.md`
- "Required Skills" section and install-check logic from SKILL.md

## 2026-02-13

### Fixed

- Decision tree now separates extraction and building into independent phases
- Variants no longer forced as mandatory step before frontend/export

### Changed

- Templates migrated from yaml/json to markdown format
- Standardize frontmatter metadata across references and templates

### Added

- Prompt generation for external tools (v0, aura.build, replit) as valid building path

## 2026-02-08

### Added

- Migrate from plugin format to unified skills format
- `copy.md` reference for content extraction from URLs
- `design.md` reference for design token extraction from images
- `frontend.md` reference for React component generation
- `variants.md` reference for 4 HTML+CSS layout previews
- `export.md` reference for design tool export (supports Figma, Penpot, and future tools)
- Custom presets support in variants alongside the 4 fixed ones
- Design extraction from description without images by asking about visual direction
- Design principles (60-30-10, visual hierarchy, rhythm rules) incorporated into variants reference

### Changed

- Product planning separated into standalone `docs-writer` skill
- Rename `figma.md` to `export.md` (multi-tool support)
- Reference `frontend-design` skill as external dependency instead of bundled fork
- Output location changed from `./docs/` and `./outputs/` to `.specs/docs/{project-name}/`
- Project types discovered through conversation instead of prefixed
- Variant generation is a separate trigger instead of `--variants` flag on frontend
