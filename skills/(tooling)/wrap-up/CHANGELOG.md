---
name: wrap-up
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-04-21

### Added

- Auto-memory optimization routine now runs at the end of the auto-memory step — scans all memory files for duplicates, staleness, broken index pointers, and oversized entries

## 2026-04-20

### Added

- Vault discovery via `.notes/` symlink in the repo root, with a bootstrap flow that prompts for the vault path and adds `.notes` to `.git/info/exclude`
- Shared `wrap-up.yml` registry at the vault root keyed by repo absolute path, with fields `name`, `bm.project`, `bm.path`, `obsidian.path`, `tags`
- Project bootstrap flow that prompts for name, BM project/path, Obsidian path, and base tags, appending the entry under the existing `projects` key
- Base tags from the project entry applied to every note (session, decision, daily)
- Downstream refs append context tags per note on top of base tags
- `note_type` set on every BM write (`session`, `decision`) for native filtering
- Permalink documented as the `identifier` format for `edit_note`

### Changed

- Project resolution rewritten around `.notes/` symlink and `wrap-up.yml` lookup instead of path parsing
- BM and Obsidian notes now consume paths and base tags from the mapping output
- Obsidian daily note path remains `Daily/YYYY-MM-DD.md` regardless of project
- Session note now carries facts and reasoning together — one BM write per session instead of two
- `write_note` examples use `directory` (real MCP param) instead of `folder`
- Obsidian session and decision templates are now prose-first, with observations and relations woven inline and standalone sections kept only as fallback
- Obsidian daily Activities now uses one prose paragraph per project instead of 3-5 bullets

### Removed

- Hardcoded path detection
- Category-to-system mapping table
- Debrief note type — absorbed into the session note
- Rule requiring `title` to match `# Heading` (not enforced by BM MCP)
- `# H1` heading from all Obsidian notes — frontmatter `title` is the canonical heading
- Obsidian session `## Summary`, `## Key Decisions`, and `## Learnings` sections — absorbed into the prose body
- Obsidian daily `## Key Decisions` and `## Learnings` sections — content moves into Activities prose

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

- Renamed categories to match directory names
- Unified all BM projects under `main`
- BM prefix now matches category name directly
- Added entity-linking guidelines (link to `entities/`, create entities for recurring technologies)

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
- Path-based project detection with category mapping table
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
