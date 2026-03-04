---
name: session-notes
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-03-04

### Added

- Initial release with 7 note types: Projects, Companies, Challenges, Brags, Daily, Conversations, and Captures
- Templates and references for each note type workflow
- Obsidian Flavored Markdown guide (`guides/markdown.md`)
- Vault structure guide (`guides/vault-structure.md`)
- Cross-references between note types with dependency flows
- Integration with Obsidian CLI (`parameter=value` syntax, `silent` by default)
- CLI fallback: Write tool when Obsidian CLI is unavailable
- Preview and confirm step before writing any note
- Template sync guideline (skill repo as source of truth, vault `Templates/` for manual use)
