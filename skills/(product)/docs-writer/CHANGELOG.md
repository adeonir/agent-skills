---
name: docs-writer
---

# Changelog

All notable changes to this skill will be documented in this file.

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

- **Brief**: Lightweight project brief document type (reference + template)
- Document count updated from 7 to 8 types

### Changed

- Refined discovery questions and PRD reference structure
- Updated PRD template with improved frontmatter metadata

## 2026-02-11

### Added

- **Docs Writer Skill**: Generalized document generation with 7 types
- **Router/Dispatcher Pattern**: SKILL.md detects document type from trigger, loads reference on-demand
- **Shared Discovery**: `references/discovery.md` with common interview patterns across all types
- **PRD**: Product Requirements Document (3-phase: discovery -> analysis -> drafting)
- **User Story**: Agile format (discovery -> drafting, WHEN/THEN/SHALL acceptance criteria)
- **Task**: Sprint execution item (direct drafting, structured fields)
- **Issue**: Bug report, feature request, discussion (classification -> drafting, 3 subtypes)
- **RFC**: Request for Comments (discovery -> analysis -> drafting, status lifecycle)
- **ADR**: Architecture Decision Record (discovery -> drafting, sequential numbering)
- **TDD**: Technical Design Document (discovery -> analysis -> drafting)
- **Templates**: One template per document type in `templates/`
- **Cross-References**: Integration with spec-driven and design-builder skills
