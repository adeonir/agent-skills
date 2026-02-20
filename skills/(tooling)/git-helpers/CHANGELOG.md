---
name: git-helpers
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-02-19

### Changed

- Restrict base branch detection to `development` and `main` only
- Subject line focuses on user-observable behavior
- Body guidelines rewritten as HOW from developer perspective, 1-5 items
- Enforce diff-only rule to prevent conversation context leaking into messages

## 2026-02-17

### Changed

- Add closes reference and imperative mood guidelines to PR template
- Expand PR changes list from 3-5 to 3-7 items

## 2026-02-08

### Added

- **Skills Format Migration**: Migrated from plugin format to unified skills format
- **New References**:
  - `commit.md`: Commit message conventions and rules
  - `code-review.md`: Code review scoring and guidelines
  - `guidelines-audit.md`: CLAUDE.md compliance checking
  - `summary.md`: PR description generation
  - `push-pr.md`: Branch push and PR creation workflow
  - `workflow-patterns.md`: Git diff analysis and workflow optimization

### Changed

- Base branch detection now prefers main over master
- Added no-future-references rule to commit guidelines
- Push before create in PR workflow
- Scope rule relaxed for PR titles

---

## 2026-02-04

### Added

- **New Skill**:
  - `git-workflow-patterns`: Standardized patterns for git diff analysis and workflow optimization

### Changed

- **Performance Optimizations**:
  - `git-code-reviewer`: Reduced steps from 25 to 15, consolidated guidelines
  - `git-guidelines-auditor`: Reduced steps from 20 to 12, streamlined prompts
- **Command Improvements**:
  - `git-commit`: More concise prompts, removed redundancy
  - `git-push-pr`: More concise prompts, streamlined guidelines

### Fixed

- Improved token efficiency by 30-40%
- Better consistency between agents and skills

## 2026-02-03

### Added

- **Skills**: New reusable instruction files
  - `conventional-commits`: Commit message guidelines and rules
  - `code-review-guidelines`: Code review best practices and scoring
- **Agent improvements**:
  - Added `temperature: 0.1` for deterministic output
  - Added `steps` limit (20-25) to control cost
  - Added granular `permission.bash` restrictions (only git, find, cat allowed)
- **Command improvements**:
  - Added `agent: build` to `/git-commit`, `/git-push-pr`, `/git-summary`
  - Added `agent: plan` and `subtask: true` to `/git-review`

### Changed

- Installation now includes `skills/` directory
- Updated README with skills documentation

## 2026-02-03

### Changed

- Commands renamed with prefix: `git-commit.md`, `git-review.md`, `git-push-pr.md`, `git-summary.md`
- Agents renamed with prefix: `git-code-reviewer.md`, `git-guidelines-auditor.md`
- Invocation now uses `/git-commit` and `@git-code-reviewer` instead of `/git/commit` and `@git/code-reviewer`
- Simplified installation: files copy directly to `.opencode/commands/` and `.opencode/agents/` without subdirectories

## 2026-01-22

### Changed

- Rename `/details` command to `/summary` for clarity
- Rename `/code-review` command to `/review` for simplicity

## 2026-01-07

### Changed

- `/commit`: never use scope in commit type (`feat:` not `feat(scope):`)
- `/commit`: never add Co-Authored-By or similar attribution lines
- `/push-pr`: allow scope in PR title (`feat:` or `feat(scope):` both valid)
- `/push-pr`: never add Co-Authored-By or similar attribution lines

## 2026-01-03

### Added

- Confidence scoring (0-100) for code review findings
- `guidelines-auditor` agent for CLAUDE.md compliance checking
- `--comment` flag to post review as PR comment via gh cli
- Command prefixes (`/git-helpers:*`) for consistency
- Mermaid workflow diagram in documentation

### Changed

- Rename `/create-pr` to `/push-pr` (more descriptive)
- Code review now outputs to terminal first, asks to save
- Output format includes confidence score per issue: `[score] [file:line]`
- Only report issues with >= 80 confidence

### Fixed

- README.md URL references (claude-code-plugins -> claude-code-extras)

## 2025-12-14

### Fixed

- Support uncommitted changes in code-review command
- Remove command substitution that caused permission errors
- Add detection for staged and unstaged changes when on main branch

## 2025-12-11

### Changed

- Enhance `/details` command with comprehensive PR template
- Add file categorization and structured analysis sections
- Include Technical Flow, Impact Assessment, Priority Review Areas
- Add pre-execution validation for branch checks

## 2025-12-02

### Added

- Initial release
- `/code-review` command for analyzing code changes
- `/commit` command for creating well-formatted commits
- `/details` command for generating PR descriptions
- `/create-pr` command for creating pull requests
- `code-reviewer` agent for quality analysis
