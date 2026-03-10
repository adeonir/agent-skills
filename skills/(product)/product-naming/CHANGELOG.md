---
name: product-naming
---

# Changelog

All notable changes to this skill will be documented in this file.

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
