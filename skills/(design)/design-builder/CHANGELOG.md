# Changelog

All notable changes to this skill will be documented in this file.

## v1.0.0 (2026-02-08)

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

- Product planning separated into standalone `prd-writer` skill
- `figma.md` renamed to `export.md` (supports Figma, Penpot, and future tools)
- frontend-design skill referenced as external dependency instead of bundled fork
- Output location changed from `./docs/` and `./outputs/` to `.specs/docs/{project-name}/`
- Project types discovered through conversation instead of prefixed
- Variant generation is a separate trigger instead of `--variants` flag on frontend
