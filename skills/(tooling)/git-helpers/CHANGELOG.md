---
name: git-helpers
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-04-13

### Changed

- Subject must be human readable: prioritize descriptions that tell the story of the change over abstract technical effect; prefer concrete nouns and verbs over framings like "pattern" or "behavior"
- Reevaluating a changelog-style body must attempt a *why* rewrite first; only drop the body when no real context exists, and announce the drop

## 2026-04-12

### Changed

- Finish branch: never use default GitHub merge message; always pass `--subject` citing the PR ID
- Commit body must explain *why*, not restate the diff; added anti-example of changelog-style body

## 2026-03-21

### Added

- Finish branch reference for branch lifecycle (update, merge, cleanup)
- Test plan section in pull request template
- Type of change field in pull request template

### Changed

- Commit body bullets start with lowercase
- Code review output format enforces file:line (never function names)
- Pull request template rewritten (summary with what+why, removed frontmatter)
- Workflow expanded to commit --> review --> summary --> pr --> finish
- Description updated with finish branch and merge triggers

## 2026-03-12

### Changed

- Remove allowed-tools and Data Trust Boundary from SKILL.md

## 2026-03-10

### Changed

- Inline conventional-commits.md into commit.md and delete the separate file
- Rename push-pr.md to create-pull-request.md
- Inline commit format rules and body guidelines directly into commit.md
- Add pre-preview checklist to commit.md Step 4
- Clarify body guideline: "add context the diff alone does not communicate"
- Move pre-commit hook handling from workflow to error handling in commit.md
- Convert all reference guidelines to DO/DON'T format
- Extract PR body format into templates/pull-request.md
- Rename PR_DETAILS.md output to PR_SUMMARY.md
- Add Output section to SKILL.md
- Move Data Trust Boundary above Guidelines in SKILL.md
- Add mermaid diagram to README.md
- Map all description triggers to trigger table entries

### Removed

- conventional-commits.md (inlined into commit.md)
- push-pr.md (renamed to create-pull-request.md)

## 2026-03-02

### Added

- Data Trust Boundary section in SKILL.md for VCS output sanitization
- Inline trust notes at diff ingestion points in commit and code-review references
- Guideline Content Boundary in guidelines-audit reference defining valid vs invalid guideline scope
- Trust language in conventional-commits Source of Truth section

## 2026-02-27

### Changed

- Fix push-pr.md confirmation contradiction (always ask before push/PR)
- Simplify base branch detection to default main with user override
- Deduplicate confidence scoring table (keep in code-review.md, reference from guidelines-audit.md)
- Enhance description with adjacent trigger contexts for better skill matching
- Standardize reference section naming: Process to Workflow
- Standardize reference closing sections: add Guidelines and Error Handling, reorder Task to end
- Add When to Use section to all reference files
- Convert SKILL.md Guidelines to DO/DON'T format

### Removed

- workflow-patterns.md (orphaned reference with generic content)

## 2026-02-25

### Changed

- Reinforce diff as single source of truth for commit message generation
- Remove MCP tool references from code-review reference

## 2026-02-20

### Changed

- Prioritize AGENTS.md/CLAUDE.md for commit conventions before inferring from git log
- Filter merge commits when analyzing git history with `--no-merges` flag
- Clarify scope usage rule: only use if explicitly required by project guidelines

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

- Migrate from plugin format to unified skills format
- `commit.md` reference for commit message conventions and rules
- `code-review.md` reference for code review scoring and guidelines
- `guidelines-audit.md` reference for CLAUDE.md compliance checking
- `summary.md` reference for PR description generation
- `push-pr.md` reference for branch push and PR creation workflow
- `workflow-patterns.md` reference for git diff analysis and workflow optimization

### Changed

- Base branch detection now prefers main over master
- Add no-future-references rule to commit guidelines
- Push before create in PR workflow
- Scope rule relaxed for PR titles

## 2026-02-04

### Added

- `git-workflow-patterns` skill for standardized git diff analysis and workflow optimization

### Changed

- Reduce `git-code-reviewer` steps from 25 to 15, consolidate guidelines
- Reduce `git-guidelines-auditor` steps from 20 to 12, streamline prompts
- `/spec-plan` reduced from 2-3 parallel explorers to 1 comprehensive explorer
- Add automatic stage detection and filtered git diff in `/spec-validate`
- Enhance context passing in `/spec-implement`

### Fixed

- Improve token efficiency by 30-40%
- Better consistency between agents and skills

## 2026-02-03

### Added

- `conventional-commits` skill for commit message guidelines and rules
- `code-review-guidelines` skill for code review best practices and scoring
- `/spec-branch` command for creating feature branch from spec
- `/spec-status` command for detailed status with task progress and next steps
- Agent `temperature` (0.1-0.2) for deterministic output
- Agent `steps` limit (20-25) to control cost
- Granular `permission.bash` restrictions (only git, find, cat allowed)
- `permission.webfetch: allow` for researcher agent
- `agent: build` to `/git-commit`, `/git-push-pr`, `/git-summary`
- `agent: plan` and `subtask: true` to `/git-review`

### Changed

- Commands renamed with prefix: `git-commit.md`, `git-review.md`, `git-push-pr.md`, `git-summary.md`
- Agents renamed with prefix: `git-code-reviewer.md`, `git-guidelines-auditor.md`
- Invocation now uses `/git-commit` and `@git-code-reviewer` instead of `/git/commit` and `@git/code-reviewer`
- Simplify installation: files copy directly to `.opencode/commands/` and `.opencode/agents/` without subdirectories
- Installation now includes `skills/` directory
- Update README with skills documentation

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
