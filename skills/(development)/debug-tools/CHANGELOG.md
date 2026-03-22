---
name: debug-tools
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-03-21

### Changed

- Log injection format enforces file:line (never function names)

## 2026-03-10

### Changed

- Restructure from rigid 5-phase sequence to flexible investigate-fix-verify loop
- Add pattern comparison as an investigation technique
- Add fix attempt tracking with escalation after 3 failed attempts
- Add red flags section for detecting off-track debugging
- Reframe log injection and cleanup as optional techniques, not mandatory phases
- Update SKILL.md workflow diagram and guidelines

## 2026-02-27

### Changed

- Generalize log format from JS/TS-only to multi-language (Python, Go, Rust, Ruby)
- Expand log-cleanup grep to cover .py, .go, .rs, .rb, .mjs, .cjs, .vue, .svelte
- Deduplicate confidence scoring table (keep in investigation.md, reference from debugging-patterns.md)
- Replace verbose framework-specific examples with compact common patterns section
- Enhance description with adjacent trigger contexts for better skill matching
- Standardize reference section naming: Process to Workflow
- Standardize reference closing sections: add Error Handling before Task
- Add When to Use section to all reference files
- Convert SKILL.md Guidelines to DO/DON'T format

### Removed

- Framework-specific log examples moved from debugging-patterns to log-injection reference

## 2026-02-25

### Changed

- Remove MCP tool references from SKILL.md and debugging references

## 2026-02-08

### Added

- Migrate from plugin format to unified skills format
- `debugging-patterns.md` reference for framework-specific debugging patterns
- `log-injection.md` reference for targeted log injection patterns
- `log-cleanup.md` reference for debug log cleanup (promoted to standalone reference)
- MCP Strategy with runtime detection and explicit fallbacks for console-ninja, chrome-devtools, serena, and context7

## 2026-02-04

### Added

- Full migration from Claude Code to OpenCode
- Optional MCP integration with automatic fallback (console-ninja, chrome-devtools, serena, context7)
- Automatic MCP detection in command with adapted workflow
- `debug-investigator` agent (15 steps, MCP-aware with fallback)
- `debug-logger` agent (12 steps, streamlined log injection)

### Changed

- Enhance 5-phase workflow with MCP support
- Agents use bash/read/grep/webfetch as fallback when MCPs unavailable
- Update documentation with MCP configuration examples
- Commands and agents use opencode conventions (`/debug`, `@debug-investigator`)

## 2026-01-11

### Added

- YAML frontmatter to debugging skill with name and description
- `context: fork` to debugging skill for conversation context access

## 2026-01-03

### Added

- Structured 5-phase workflow (Investigate, Inject, Propose, Verify, Cleanup)
- Confidence scoring for findings (High >= 70, Medium 50-69, Low < 50)
- Structured output format with file:line references
- Automatic cleanup of debug logs after fix verified
- Mermaid workflow diagram in documentation
- "When to Use / When NOT to Use" guidance

### Changed

- `bug-investigator` now uses confidence scoring
- `log-injector` handles both injection and cleanup phases
- Debug command includes full workflow documentation
- Update SKILL.md with confidence scoring patterns
- Command prefix changed to `/debug-tools:debug`

## 2025-12-15

### Changed

- Remove Serena MCP to avoid duplication with spec-driven plugin
- Update documentation to reference spec-driven for LSP features

## 2025-12-12

### Changed

- Simplify agents to role-based style
- Remove hypothesis generation approach in favor of direct investigation
- Reduce total lines from 736 to 320 (56% reduction)

## 2025-12-11

### Added

- Initial release
- `/debug` command for starting debugging sessions
- `bug-investigator` agent for code analysis and root cause detection
- `log-injector` agent for targeted debug log insertion
- Console Ninja MCP for runtime values
- Chrome DevTools MCP for browser inspection
- Debugging skill with framework-specific patterns
