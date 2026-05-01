---
name: context-audit
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-04-30

### Added

- Explicit context-snapshot prompt asking the user to paste `/context` output before scoring, so MCP estimates use real numbers when available
- Filter 3 exception: rules that overlap with a skill trigger are not flagged as redundant; triggers are heuristic, rules are deterministic
- Skill description+when_to_use cap check (1,536 chars); deducts when frontmatter exceeds the harness truncation limit

### Changed

- Soften CLAUDE.md size penalty: `> 200 lines` now -5 (was -10), `> 500 lines` now -10 (was -20); the file may be load-bearing in spec-heavy repos
- Replace SKILL.md body-length deduction with description+when_to_use char check; skill bodies load on invocation, not at session start

### Removed

- Drop `autocompact_percentage_override` checks, deductions, and report references; key is not part of the current Claude Code settings schema
- Drop the `Long SKILL.md files` deduction; long bodies are informational only (invocation latency, not per-session tokens)

## 2026-04-28

### Added

- Initial release
- Deterministic scanner for MCP servers, slash commands, hooks, agents, skills, CLAUDE.md (with `@import` resolution), settings keys, and missing deny rules
- Heuristic pre-filter for Default, Vague, and Bandaid rule patterns; emits `flagged_rules[]` per instruction file
- Drift detection across runs, with baseline persisted to `.claude/.audit-baseline.json`
- Five-filter reconciliation workflow (Default, Contradiction, Redundancy, Bandaid, Vague)
- Per-scanner inspection reference loaded only on troubleshooting
- Scoring with deduction caps and Top 3 ranking formula (savings divided by effort weight)
- Report template with worked example
- MCP-to-CLI mapping for playwright, github, filesystem, gcloud, kubectl, and others
- Project marker (package.json, Cargo.toml, etc.) to deny-pattern recommendations
- Inspired by "The Claude Code Context Cleanup Guide" PDF by Bradley Bonanno (2026)
