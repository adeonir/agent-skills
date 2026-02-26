---
name: docs-writer
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-02-25

### Changed

- Replace fixed discovery stages with adaptive deepening across all document types
- Apply adaptive discovery to remaining types (adr, issue, rfc, tdd, user-story)

## 2026-02-20

### Changed

- Output directory migrated from `.specs/docs/` to `.artifacts/docs/`
- All document types now save to unified `.artifacts/docs/` location

## 2026-02-19

### Changed

- Output filenames simplified from `{type}-{project-name}` to `{type}` only

## 2026-02-17

### Changed

- Remove frontmatter and title placeholders from document templates

## 2026-02-13

### Added

- Brief document type with reference and template (lightweight project brief)
- Document count updated from 7 to 8 types

### Changed

- Refine discovery questions and PRD reference structure
- Update PRD template with improved frontmatter metadata

## 2026-02-11

### Added

- Docs Writer skill with generalized document generation for 7 types
- Router/dispatcher pattern in SKILL.md (detects document type from trigger, loads reference on-demand)
- `discovery.md` shared reference with common interview patterns across all types
- PRD type with 3-phase workflow (discovery, analysis, drafting)
- User Story type with agile format (discovery, drafting, WHEN/THEN/SHALL acceptance criteria)
- Task type for sprint execution items (direct drafting, structured fields)
- Issue type for bug reports, feature requests, discussions (classification, drafting, 3 subtypes)
- RFC type for Request for Comments (discovery, analysis, drafting, status lifecycle)
- ADR type for Architecture Decision Records (discovery, drafting, sequential numbering)
- TDD type for Technical Design Documents (discovery, analysis, drafting)
- Templates for all document types in `templates/`
- Cross-references with spec-driven and design-builder skills
