---
name: session-notes
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-03-25

### Changed

- Session template: replaced "What Was Done" with "Summary" (outcomes, not tasks)
- Session template: removed git metadata (Branch, PR, Commit) and Files Modified section
- Session reference: guidelines updated to prohibit changelog-style content and git metadata
- Wikilinks must point to existing files -- verify before adding project links
- Orphan wikilinks added to DON'T guidelines

## 2026-03-24

### Added

- Decision note type with reference and template for standalone decision documentation
- New triggers: "decision note", "document decision", "record decision"
- Cross-references: session feeds decision, decision links to project
- Session note type with reference and template for focused single-project work logs
- New triggers: "session note", "obsidian session", "vault session"
- Cross-references: session feeds daily, project feeds session

### Changed

- Session notes now go in `{VaultFolder}/{Project}/Sessions/` subfolder
- Decision notes go in `{VaultFolder}/{Project}/Decisions/` subfolder
- Project overview filename changed from `Overview.md` to `{Name} Overview.md` for unique wikilinks
- Project vault folder is dynamic based on category mapping, not always `Projects/`
- Rename What Was Done to Activities in daily notes
- Replace flat bold-prefix bullets with per-project subsections (`### Project Name`)
- Update daily reference and template to match new structure

## 2026-03-23

### Changed

- Rename Activities to What Was Done with flat bullet format (bold project + one-sentence summary)
- Replace per-project subsections with single-line bold-prefix bullets
- Rename Blockers to Key Decisions, Tomorrow to Open Items
- Simplify observations format from multiple named categories to generic #category pattern
- Remove introductory prose paragraph from daily template
- Update daily reference create and update flows to match new structure

## 2026-03-21

### Added

- "One question at a time" rule in all references that ask user questions

### Changed

- Brag document year from hardcoded to dynamic, path from Brags/Brags YYYY to Brags/YYYY
- Conversation reference rewritten with prose style (aligned with Basic Memory)

### Removed

- Capture reference and template (replaced by Basic Memory)

### Changed

- Add title and type fields to all template frontmatter
- Change tags format from inline list to YAML multiline (one per line)
- Add rich prose context paragraph after H1 in all templates
- Replace References section with Relations using wikilinks only (no relation_type)
- Replace [category] observations with #category hashtags for native Obsidian tag indexing
- Add dynamic tags placeholder to all templates
- Change stack field from string to YAML multiline list
- Centralize English language rule in SKILL.md Writing Style

### Removed

- Remove date field from all template frontmatter
- Remove Language section from daily reference (centralized in SKILL.md)

## 2026-03-20

### Changed

- Replace Obsidian CLI write operations with MCPVault MCP as primary backend
- Use MCPVault tools for all note operations: write_note, read_note, patch_note, search_notes
- Keep Obsidian CLI only for vault discovery (obsidian vaults verbose)
- Centralize vault resolution in SKILL.md (run once per session)
- Simplify all references by removing CLI fallback logic and Write/Edit tool patterns
- Remove mandatory preview and confirmation step before writing
- Remove Content Escaping section from capture reference (no longer needed)
- Simplify daily note update flow: read_note + patch_note instead of Edit tool
- Update vault-structure guide with MCPVault commands

### Added

- Filename Sanitization section in SKILL.md for handling special characters
- Vault Resolution section in SKILL.md for centralized path management

### Removed

- All `which obsidian` availability checks from references
- All `obsidian create`, `obsidian append` commands from references
- Write tool and Edit tool fallback patterns from all references
- Preview and confirm steps from all note creation workflows

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
