---
name: session-notes
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-03-14

### Changed

- Rewrite daily reference with separate create and update flows
- Add Edit tool flow for updating existing daily notes (append only adds to end of file)
- Infer project name from current working directory
- Mark only Activities as required section, rest are optional
- Add natural language bullet point style with examples
- Add Basic Memory integration for context gathering (optional, skipped if unavailable)
- Default daily notes to English, Portuguese with proper accents if user writes in Portuguese

## 2026-03-12

### Changed

- Simplify template frontmatter: remove `type` field, rename `created` to `date`
- Simplify brag template: consolidate to 3 sections (Impact, Technical, Growth)
- Simplify company template: remove `size`, `industry`, `source` from frontmatter
- Simplify challenge template: remove `challenge-type`, rename `technologies` to `stack`
- Update project template: remove `status`, add `stack`, fix mixed-language placeholder
- Remove `{{source}}` from conversation template tags
- Replace dynamic title in daily template with date format
- Replace Morning section in daily template with project subtopics in Activities
- Remove `period` from brag template frontmatter
- Add mid-file editing guideline to SKILL.md for direct vault file edits
- Update daily reference to ask user about activities instead of defaulting to git log
- Update all references to match template changes
- Remove allowed-tools and External Content Trust Boundary from SKILL.md
- Remove dynamic content pattern from context loading strategy

## 2026-03-10

### Added

- External Content Trust Boundary section in SKILL.md for URL capture sanitization

### Changed

- Break frontmatter description into multi-line YAML to avoid obfuscation alerts

## 2026-03-09

### Changed

- Switch filenames from kebab-case to Title Case (e.g., `My Project.md`)
- Switch wiki-links from `[[note-name]]` to `[[Note Name]]`
- Update all references and templates to match new naming conventions

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
- Safety rule: never overwrite or delete existing vault files
