---
name: wrap-up
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-04-01

### Fixed

- Obsidian session notes path now includes Sessions/ subfolder consistently
- Session and debrief notes are always created; decision notes are optional by context

## 2026-03-25

### Changed

- Obsidian notes: removed git metadata rules, aligned language to outcomes/decisions (not steps taken)
- Debrief must have its own title describing what was learned/decided, not reuse session title
- Debrief template placeholder updated to reflect naming convention
- Moved debrief and decision templates inline into bm-notes.md, removed templates/ directory
- Daily note update now reads existing note first and consolidates bullets instead of appending

## 2026-03-24

### Added

- Decision note template (templates/decision.md) with Context + Decisions required sections
- Conditional decision note creation step in bm-notes.md (step 5)
- Initial skill creation with SKILL.md, references, and templates
- Path detection from ~/Developer/{category}/{project}/ with mapping table
- Auto-memory update step (references/auto-memory.md)
- BM session and debrief note creation (references/bm-notes.md)
- Obsidian session and daily note creation (references/obsidian-notes.md)
- Category-to-system mapping table (references/mapping.md)
- Debrief note template for BM (templates/debrief.md)

### Changed

- Debrief template now uses `## Context` heading for body prose
- Reference bm-notes.md uses template files instead of inline examples
- Added memory-notes guidance on body context to bm-notes.md
- Decision notes are now required for formats, conventions, and reusable patterns
