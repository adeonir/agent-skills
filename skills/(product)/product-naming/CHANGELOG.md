---
name: product-naming
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-03-11

### Added

- Phase 1 / Phase 2 workflow with implicit transition (research then validation)
- Three entry points: suggest names, evaluate quality, check availability
- Competitor analysis step before name generation in research phase
- Portmanteau and truncation-with-suffix generation styles
- Name variations step for top candidates (suffix swap, vowel swap, abbreviation)
- Dictability test as quality scoring criterion (phone/podcast simulation)
- Trademark check section in validation (INPI and USPTO via web search)
- Estimated domain prices in validation report (pulled from tld-guide.md)
- Separate research-report.md and validation-report.md templates
- Cross-reference with brainstorming skill (bidirectional)
- "What's Next" section in research report template suggesting validation
- Conditional guidance in research template for evaluate-only entry point
- Audience and research report reference in validation template Context section
- Error Handling section in research.md and validation.md references
- Brainstorming row in README.md Integration table

### Fixed

- Merge Entry Points table into Triggers section for consistency with other skills
- Rename "Edge Cases" to "Error Handling" in validation.md for consistency

### Changed

- Rename generation.md to research.md with expanded scope (competitor analysis, variations, scoring)
- Rename evaluation.md to validation.md with narrowed scope (external checks only)
- Move quality scoring from evaluation to research phase
- Update tld-guide.md cross-reference from evaluation.md to validation.md
- Update SKILL.md workflow, triggers, context loading, and error handling for two-phase model
- Update README.md flowchart and usage examples for three entry points
- Domain columns in validation template are now flexible per tld-guide.md
- Social media columns in validation template use platform placeholders

### Removed

- Unified report.md template (replaced by research-report.md and validation-report.md)
- Quality scoring from validation phase (moved to research phase)

## 2026-03-10

### Changed

- Strengthen External Content Trust Boundary with explicit extraction and discard rules
- Break frontmatter description into multi-line YAML to avoid obfuscation alerts

## 2026-03-03

### Changed

- Unify Template A and Template B into single report template
- Simplify report title to "Product Naming" (removed product name suffix)
- Shortlist now uses compact Quality Score format (1-2 lines, no tables)
- Move eliminated names to end of report
- Reorder sections: Shortlist → Recommendation → Availability Summary → Eliminated
- Availability Summary table: remove Status column, add .app TLD column
- Domain check method: prefer whois as primary verification tool

### Removed

- Template A (Name Research) with per-candidate availability tables and comparison matrix
- Template B (Name Validation) with per-candidate detailed quality tables

## 2026-03-02

### Added

- External Content Trust Boundary section in SKILL.md for registrar and social media response sanitization
- Inline trust note at shell command output interpretation in evaluation reference

## 2026-02-28

### Changed

- Domain checks now use shell commands (dig, whois) as primary method with web search as fallback
- Social media checks now use curl HTTP status codes as primary method with web search as fallback
- tld-guide.md "How to Check" section replaced with pointer to evaluation.md to avoid duplication
- SKILL.md guidelines updated to reflect environment-adaptive check strategy
- Error handling expanded with shell rate-limiting and no-tools-available scenarios

### Added

- Reports saved as `.md` files in `.artifacts/docs/` (`{product}-research.md`, `{product}-validation.md`)
- Template B: availability table now matches Template A format (Name + Highlight columns)
- Template B: risk section expanded to bulleted list with context and impact per risk
- Template B: "Recommendation" renamed to "Verdict" with contextual assessment
- Status indicators changed from text markers to traffic light emojis across all files
- SKILL.md output section now references both report templates
- Product Naming skill with two-phase workflow (generation + evaluation)
- Name generation reference with 5 naming styles (real words, compound, invented, prefixed, acronyms)
- Name evaluation reference with domain, social media, and quality checks
- TLD guide reference with pricing and selection logic
- Output template for structured naming reports
- Evals with 20 trigger definitions
