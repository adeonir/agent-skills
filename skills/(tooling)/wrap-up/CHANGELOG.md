---
name: wrap-up
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-04-16

### Changed

- Removed dependency on `memory-notes` skill — BM syntax rules, tool signatures, and search-before-create logic now inline in bm-notes.md
- Removed dependency on `session-notes` skill — Obsidian templates (daily, session, decision), syntax rules, tool signatures, and filename sanitization now inline in obsidian-notes.md
- Wrap-up now depends only on MCPs (BM MCP, MCPVault MCP) and the `auto-memory` skill
- Cross-References and Guidelines in SKILL.md updated to reflect direct MCP calls

### Fixed

- Obsidian notes now follow the complete template (frontmatter + all sections), no longer missing Key Decisions, Learnings, Open Items, Observations, or Relations
- Daily note no longer reverts to changelog style — enforced outcomes-and-decisions guidance with no contradictory bullets
- Obsidian observations no longer leak BM `[brackets]` format — `#hashtags` enforced with explicit DON'T rule

## 2026-04-08

### Changed

- Renamed categories to match directory names: `work` -> `jobs`, `freelance` -> `freelances`, `personal` -> `personals`
- Unified all BM projects to `main` (removed `work` and `ventures` projects)
- BM prefix now matches category name directly (`ventures/` instead of `products/`)
- Added entity-linking guidelines to bm-notes.md (link to `entities/`, create entities for recurring technologies)

## 2026-04-06

### Fixed

- Clarified that BM writes must invoke memory-notes skill (via Skill tool), not call write_note MCP directly
- Clarified that Obsidian writes must invoke session-notes skill (via Skill tool), not call Obsidian MCP directly
- Added top-level guideline in SKILL.md enforcing skill invocation over direct MCP calls
- Updated cross-references to specify "invoke via Skill tool, not MCP"

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
