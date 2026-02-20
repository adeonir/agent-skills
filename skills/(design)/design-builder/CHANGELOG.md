---
name: design-builder
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-02-19

### Added

- `aesthetics.md` reference with unified design principles (typography, color, motion, spatial composition, backgrounds, visual hierarchy, anti-patterns, responsive behavior, component states, depth and elevation)
- `frontend.md` section: Implementation Concerns (Accessibility, Responsive Implementation, Theme Tokens)

### Removed

- External `frontend-design` skill dependency absorbed into `aesthetics.md`
- "Required Skills" section and install-check logic from SKILL.md

## 2026-02-19

### Changed

- Export workflow now uses Figma MCP server directly instead of HTML intermediary
- Export requires variants as input instead of allowing direct export
- Penpot support and YashiTech extension dependency removed

## 2026-02-13

### Fixed

- Decision tree now separates extraction and building into independent phases
- Variants no longer forced as mandatory step before frontend/export

### Changed

- Templates migrated from yaml/json to markdown format
- Standardized frontmatter metadata across references and templates

### Added

- Prompt generation for external tools (v0, aura.build, replit) as valid building path

## 2026-02-08

### Added

- **Skills Format Migration**: Migrated from plugin format to unified skills format
- **New References**:
  - `copy.md`: Content extraction from URLs (from copy-extractor agent + copy command)
  - `design.md`: Design token extraction from images (from design-extractor agent + design command)
  - `frontend.md`: React component generation (from frontend-builder agent + frontend command)
  - `variants.md`: 4 HTML+CSS layout previews (from variants-builder agent + frontend --variants)
  - `export.md`: Design tool export (from figma-builder agent + figma command, renamed for multi-tool support)
- **Custom Presets**: Variants now support user-defined custom presets alongside the 4 fixed ones
- **Style from Description**: Design extraction works without images by asking about visual direction
- **Design Principles**: 60-30-10, visual hierarchy, and rhythm rules incorporated into variants.md

### Changed

- Product planning separated into standalone `docs-writer` skill
- `figma.md` renamed to `export.md` (supports Figma, Penpot, and future tools)
- frontend-design skill referenced as external dependency instead of bundled fork
- Output location changed from `./docs/` and `./outputs/` to `.specs/docs/{project-name}/`
- Project types discovered through conversation instead of prefixed
- Variant generation is a separate trigger instead of `--variants` flag on frontend
