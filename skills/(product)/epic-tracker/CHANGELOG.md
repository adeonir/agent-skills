---
name: epic-tracker
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-04-23

### Changed

- Triggers "overview", "status", "start story", and "create bug" removed (collided with spec-driven and project-index)
- "Not for" routing added to spec-driven ("implement story S###") and project-index (project-wide overview)

## 2026-04-22

### Changed

- Story files now use a zero-padded 3-digit numeric prefix (`001-story-name.md`) for visual ordering in file explorers
- Epic checklist entries updated to linked format when story is created

## 2026-04-20

### Changed

- Pair every Guideline DON'T with a concrete DO in SKILL.md and epic.md

## 2026-03-25

### Added

- Initial skill creation with SKILL.md, references, and templates
- Epic, story, bug, and release artifact types
- Discover phase checks for existing PRD/brief before creating epics
- Status tracking in frontmatter for all artifacts
- Handoff reference for spec-driven bridge
- Overview reads artifacts directly (no index file)
