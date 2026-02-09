# Changelog

All notable changes to this skill will be documented in this file.

## v1.0.0 (2026-02-08)

### Added

- **Skills Format Migration**: Migrated from plugin format to unified skills format
- **New References**:
  - `debugging-patterns.md`: Framework-specific debugging patterns (expanded)
  - `log-injection.md`: Targeted log injection patterns (expanded)
  - `log-cleanup.md`: Debug log cleanup (promoted to standalone reference)
- **MCP Strategy**: Runtime detection with explicit fallbacks for console-ninja, chrome-devtools, serena, and context7

---

## v1.4.0 (2026-02-04)

### Added

- **OpenCode Support**: Full migration from Claude Code to OpenCode
- **MCP Integration**: Support for optional MCP servers with automatic fallback
  - console-ninja: Runtime values capture
  - chrome-devtools: Browser inspection
  - serena: Semantic code analysis
  - context7: Documentation search
- **Agent Optimizations**:
  - debug-investigator: 15 steps, MCP-aware with fallback
  - debug-logger: 12 steps, streamlined log injection
- **Automatic MCP Detection**: Command detects available MCPs and adapts workflow

### Changed

- **Workflow**: Enhanced 5-phase workflow with MCP support
- **Tools**: Agents use bash/read/grep/webfetch as fallback when MCPs unavailable
- **Documentation**: Updated README with MCP configuration examples
- **Naming**: Commands and agents use opencode conventions (`/debug`, `@debug-investigator`)

### Migration Notes

- Plugin now requires OpenCode CLI instead of Claude Code
- MCP servers are optional but enhance debugging capabilities
- All functionality works without MCPs using native tools

## v1.3.1 (2026-01-11)

### Added

- YAML frontmatter to debugging skill with name and description
- `context: fork` to debugging skill for conversation context access

## v1.3.0 (2026-01-03)

### Added

- Structured 5-phase workflow (Investigate, Inject, Propose, Verify, Cleanup)
- Confidence scoring for findings (High >= 70, Medium 50-69, Low < 50)
- Structured output format with file:line references
- Automatic cleanup of debug logs after fix verified
- Mermaid workflow diagram in documentation
- "When to Use / When NOT to Use" guidance

### Changed

- bug-investigator now uses confidence scoring
- log-injector handles both injection and cleanup phases
- debug command includes full workflow documentation
- Updated SKILL.md with confidence scoring patterns
- Command prefix changed to `/debug-tools:debug`

## v1.2.1 (2025-12-15)

### Changed

- Remove Serena MCP to avoid duplication with spec-driven plugin
- Update documentation to reference spec-driven for LSP features

## v1.2.0 (2025-12-12)

### Changed

- Simplify agents to role-based style
- Remove hypothesis generation approach in favor of direct investigation
- Reduce total lines from 736 to 320 (56% reduction)

## v1.1.0 (2025-12-11)

### Added

- Serena MCP integration for semantic code analysis

## v1.0.0 (2025-12-11)

### Added

- Initial release
- `/debug` command for starting debugging sessions
- `bug-investigator` agent for code analysis and root cause detection
- `log-injector` agent for targeted debug log insertion
- Console Ninja MCP for runtime values
- Chrome DevTools MCP for browser inspection
- Debugging skill with framework-specific patterns
