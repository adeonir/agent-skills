---
name: project-index
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-04-03

### Added

- Documentation for `.agents/knowledge.md` ownership by spec-driven
- Integration note: project-index reads but never writes knowledge.md

## 2026-03-21

### Added

- Custom Hooks section in conventions template
- Project Abstractions table in conventions template
- Inconsistencies section in conventions template
- Mermaid diagrams in architecture template (system overview, component map, data flows)
- Interfaces and APIs section in architecture template
- Module dependencies table in architecture template
- Review notes template (consistency, completeness, recommendations)
- Self-assessment step in summary workflow
- Coverage gaps section in testing template

### Changed

- Size budget removed, replaced with "depth over brevity" guidelines
- Code snippets with source file references required for all conventions
- Custom hooks added to reading priority (position 3)
- Abstractions documented as high priority in convention extraction
- Architecture template uses mermaid for complex diagrams
- Workflows template uses mermaid flowcharts

## 2026-03-10

### Added

- Optional concerns.md for tech debt, risks, and inconsistencies detected during analysis
- Output size budget with target line counts per document (~300 lines / ~12k tokens total)
- Bidirectional integration with spec-driven (preserves discoveries when re-running summary)
- Dedicated root-agents.md reference for AGENTS.md generation (deduplicated from overview and summary)
- Overview consumes docs-writer artifacts (.artifacts/docs/) as context source for richer project.md

### Changed

- Improve brownfield detection with broader signals (manifests, source directories, file count)
- Add reading priority order in deep analysis (config and setup files first, then entry points)
- Add explicit skip list for generated, vendored, and data files
- Add monorepo guidance (workspace structure, shared packages first)
- Restructure convention extraction with required categories table including styling and components
- Add rule to read config files before assuming conventions from dependency names
- Enrich conventions template with styling, state management, async, and components categories
- Enrich integrations template with auth method, config, and environment variables
- Enrich commands template with table format and notes column
- Document size guidelines in summary.md (max 10 table rows, max 7 list items)

## 2026-03-03

### Added

- Initial release extracted from spec-driven skill
- Three commands: initialize, overview, summary
- Overview generates `.agents/project.md` with business context
- Summary generates `.agents/codebase/` with 8 analysis docs (stack, architecture, conventions, testing, integrations, commands, checklist, workflows)
- Auto-generate/update AGENTS.md at project root
- Update mode for summary (merge existing docs instead of overwrite)
