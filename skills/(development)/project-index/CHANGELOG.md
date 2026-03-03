---
name: project-index
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-03-03

### Added

- Initial release extracted from spec-driven skill
- Three commands: initialize, overview, summary
- Overview generates `.agents/project.md` with business context
- Summary generates `.agents/codebase/` with 8 analysis docs (stack, architecture, conventions, testing, integrations, commands, checklist, workflows)
- Auto-generate/update AGENTS.md at project root
- Update mode for summary (merge existing docs instead of overwrite)
