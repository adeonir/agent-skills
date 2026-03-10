---
name: project-index
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-03-10

### Added

- Optional concerns.md for tech debt, risks, and inconsistencies detected during analysis
- Output size budget with target line counts per document (~300 lines / ~12k tokens total)
- Bidirectional integration with spec-driven (preserves discoveries when re-running summary)
- Dedicated root-agents.md reference for AGENTS.md generation (deduplicated from overview and summary)
- Overview consumes docs-writer artifacts (.artifacts/docs/) as context source for richer project.md

### Changed

- Improve brownfield detection with broader signals (manifests, source directories, file count)
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
