---
name: spec-driven
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-02-20

### Changed

- Output directory migrated from `.specs/` to `.artifacts/specs/`
- Research cache location updated to `.artifacts/specs/research/`
- All references and templates updated with new paths

## 2026-02-11

### Removed

- Session state management (STATE.md template and session-state.md reference)
- State generation steps from project initialization

## 2026-02-11

### Added

- Templates for all artifacts (PROJECT, ROADMAP, CHANGELOG, spec, plan, tasks, archive)
- `status-workflow.md` reference with exact status values

### Changed

- References simplified by extracting output schemas into templates

## 2026-02-08

### Added

- **Skills Format Migration**: Migrated from plugin format to unified skills format
- **New References**:
  - `project-init.md`: Project initialization workflow
  - `roadmap.md`: Feature planning and milestones
  - `codebase-mapping.md`: Comprehensive codebase analysis
  - `baseline-discovery.md`: Brownfield baseline analysis
  - `doc-extraction.md`: PRD/document extraction
  - `research.md`: Research caching with MCP support
- **Content Separation**: Enforced CRITICAL separation between spec/plan/tasks
- **Feature Resolution**: Consistent feature lookup by ID or branch in all references
- **coding-principles.md**: Behavioral principles loaded before implementation (simplicity, surgical changes, anti-patterns)
- **Acceptance criteria format**: WHEN/THEN/SHALL pattern in spec-writing.md
- **Priority levels**: P1/P2/P3 on user stories (P1=must deliver, P2=should have, P3=nice to have)
- **Data Model Definition**: Entities, relationships, API contracts in plan.md
- **Mermaid diagram recommendations**: In Data Flow and Relationships sections of plan.md
- **Pre-implementation checklist**: Assumptions, files, success criteria, risk check in implement.md
- **Edge case verification**: Error states, boundaries, concurrency, permissions in validate.md
- **Inline Q&A**: Ambiguity resolution during initialization (3-5 questions, max 2 rounds)
- **Open Questions section**: Replaces [NEEDS CLARIFICATION] markers in spec.md template

### Changed

- Expanded `plan.md` with Requirements Traceability, Test Strategy, Codebase Patterns
- Expanded `codebase-exploration.md` with 4-phase process and output template
- Expanded `validate.md` Full Mode with Pattern Compliance and gap categories
- Expanded `implement.md` with 3-phase per-task process (Before/During/After)
- Task size guidelines (Small/Medium/Large) added to `tasks.md`
- Archive changelog entries now use dates only (no feature IDs)
- Research cache location changed to `.artifacts/research/`
- **validate.md**: Simplified from 4 separate modes to single adaptive validation
- **validate.md**: Unified output format with categorized checks table
- **initialize.md**: Ambiguities resolved inline during init, not in separate clarify phase
- **plan.md**: Added Step 5 (Data Model Definition) before component design
- **implement.md**: Loads coding-principles.md in Before (Preparation) step
- **project-init.md**: "Load Existing Context" replaces "Check MCP Memory Bank"
- **doc-extraction.md**: Conflicting requirements go to "Open Questions" instead of markers

### Removed

- **clarify.md**: Entire file deleted (clarifications happen inline during initialization)
- **clarify phase**: Removed from workflow, triggers table, cross-references, and examples
- **[NEEDS CLARIFICATION] markers**: Replaced with inline Q&A and Open Questions section
- **MCP Strategy sections**: Removed from plan.md, implement.md, codebase-exploration.md, research.md
- **MCP tool names**: Removed Serena/Context7 references from all references (tool-agnostic)

---

## 2026-02-04

### Added

- **New Skills**:
  - `codebase-exploration`: Standardized patterns for codebase analysis
  - `output-templates`: Pre-defined templates for plan.md and tasks.md
  - `validation-checklists`: Structured checklists by validation mode
  - `research-cache`: Caching strategies with TTL and automatic invalidation
- **Optional MCP Support**:
  - `serena`: Semantic code analysis and symbol navigation
  - Automatic MCP detection in `/spec-plan` command
  - Fallback to native tools (grep, read, glob) when MCPs unavailable
  - Updated `spec-explorer` and `spec-implementer` agents to use MCPs when available

### Changed

- **Performance Optimizations**:
  - `spec-explorer`: Reduced steps from 30 to 25, with directive prompts and explicit file content reading
  - `spec-architect`: Reduced steps from 30 to 20, removed redundancies
  - `spec-tasker`: Reduced steps from 15 to 10, streamlined process
  - `spec-implementer`: Reduced steps from 50 to 35, optimized quality gates
  - `spec-validator`: Reduced steps from 25 to 15, added automatic mode detection
  - `spec-researcher`: Added YAML metadata for cache management

- **Command Improvements**:
  - `/spec-plan`: Reduced from 2-3 parallel explorers to 1 comprehensive explorer
  - `/spec-validate`: Added automatic stage detection and filtered git diff
  - `/spec-implement`: Enhanced context passing

### Fixed

- Status workflow consistency across all commands

## 2026-02-03

### Added

- **Skills**: New reusable instruction files
  - `spec-writing`: Specification writing guidelines
  - `task-decomposition`: Task breakdown and dependency mapping
- **New commands**:
  - `/spec-branch`: Create feature branch from spec and link them together
  - `/spec-status`: Show detailed status with task progress and next steps
- **Agent improvements**:
  - Added `temperature` (0.1-0.2) for deterministic output
  - Added `steps` limit (10-50 depending on agent) to control cost
  - Added granular `permission.bash` restrictions where applicable
  - Added `permission.webfetch: allow` for researcher agent
- **Command improvements**:
  - Added `agent: build` to `/spec-init`, `/spec-implement`, `/spec-archive`
  - Added `agent: plan` to `/spec-clarify`, `/spec-plan`, `/spec-tasks`, `/spec-specs`, `/spec-status`
  - Added `subtask: true` to `/spec-validate` for isolated context

### Changed

- Installation now includes `skills/` directory
- Updated README with skills documentation and new commands

## 2026-02-03

### Changed

- Commands renamed with prefix: `spec-init.md`, `spec-plan.md`, `spec-tasks.md`, etc.
- Agents renamed with prefix: `spec-researcher.md`, `spec-explorer.md`, `spec-architect.md`, etc.
- Invocation now uses `/spec-init` and `@spec-architect` instead of `/spec/init` and `@spec/architect`
- Updated all internal references in commands and agents
- Simplified installation: files copy directly to `.opencode/commands/` and `.opencode/agents/` without subdirectories

## 2026-01-31

### Added

- Test Infrastructure Discovery step in `explorer` agent
  - Discovers test framework via config files (jest, vitest, pytest, etc.)
  - Locates test directories, shared utilities, fixtures, helpers, and mocks
  - Documents how to run tests and finds reference tests for similar features
- Test Strategy section in `architect` plan output
  - Existing Infrastructure table (framework, directory, utilities, run command)
  - Reference Tests table (patterns to follow from similar features)
  - New Tests table (components, files, scenarios)

### Changed

- Task grouping is now a flat list with adjacency-based grouping (blank lines between groups)
  - No more section headers (Foundation, Implementation, etc.)
  - Related tasks (types, implementation, tests) are always adjacent
  - Component-specific deps belong next to the code that uses them
- `/plan` command no longer runs inline validation (removed Step 8)
  - Suggests `/spec-driven:validate` as optional step in the report
- `architect` process now analyzes test patterns from explorer output

### Removed

- Inline plan validation step from `/plan` command (use `/spec-driven:validate` instead)
- Category-based task sections (Foundation, Implementation, Documentation)
- Generic "Testing: {strategy}" field from architect Considerations

## 2026-01-25

### Changed

- `/init` now enforces strict content separation between spec.md and plan.md
  - spec.md: WHAT to build (requirements, acceptance criteria)
  - plan.md: HOW to build (architecture, files, implementation)
  - tasks.md: WHEN to build (ordered tasks with dependencies)
- Brownfield baseline now describes behavior only, no file paths or code
- Task grouping by component: related tasks (types, implementation, tests if any) are grouped together for atomic commits
- Quality gates run after each task, not as separate final tasks
- Removed assumption that all projects have tests

### Fixed

- spec.md was including implementation details (file paths, code, technology choices)
- Tasks were being separated from related work (e.g., component far from its tests)

## 2026-01-18

### Added

- Quality Gates in tasks.md output
  - Detects lint/typecheck scripts from package.json
  - Adds instruction to run quality checks after each task
- Implementer now runs quality gates after each task, tries `--fix` flag first, then fixes remaining manually

### Changed

- `/tasks` command now reads package.json to detect quality gate commands

## 2026-01-18

### Added

- Project Conventions Discovery step in `explorer` agent
  - Identifies wrapper libraries/abstractions the project uses
  - Documents patterns that MUST be followed (with reference files)
  - Documents what to avoid (e.g., direct access when abstraction exists)
- "Project conventions" as mandatory output item in explorer analysis

### Changed

- Rule 4 in explorer now emphasizes explicit documentation of conventions

## 2026-01-12

### Added

- Brownfield support in `/init` command
  - Auto-detects greenfield vs brownfield based on keywords and codebase analysis
  - Generates Baseline section for brownfield specs (related files, current behavior, modification points)
  - New `type: greenfield | brownfield` field in spec.md frontmatter
- Multi-mode validation in `/validate` command
  - Mode Spec: validates spec structure (after /init)
  - Mode Plan: + documentation compliance (after /plan)
  - Mode Tasks: + requirements coverage (after /tasks)
  - Mode Full: + code validation (after /implement)
  - Auto-detects mode based on available artifacts

### Changed

- Consolidated `plan-validator` and `spec-validator` into unified `validator` agent
- Renamed agents for consistency:
  - `web-researcher` -> `researcher`
  - `code-explorer` -> `explorer`
  - `code-architect` -> `architect`
  - `task-generator` -> `tasker`
  - `implement-agent` -> `implementer`
  - `spec-archiver` -> `archiver`
- Reduced agent count from 8 to 7
- `/validate` can now run at any workflow phase (not just after /implement)

### Removed

- `plan-validator` agent (merged into `validator`)
- `spec-validator` agent (merged into `validator`)

## 2026-01-12

### Added

- `plan-validator` agent to validate plan.md against project documentation
- Plan validation step in `/plan` command (Step 8)
- Auto-correction loop: re-generates plan until documentation consistency achieved (max 3 iterations)
- User prompt when max iterations reached with remaining inconsistencies

### Changed

- `/plan` command now has 10 steps (was 9)

## 2026-01-12

### Fixed

- `/init` now systematically reads all files in referenced @path
- `/init` extracts rules, constraints, and examples from documentation
- `code-architect` re-reads referenced docs before implementation decisions
- `code-architect` marks undocumented decisions as `[NOT DOCUMENTED - needs verification]`

## 2026-01-07

### Fixed

- Status update timing in `/plan` command: now sets `ready` only after plan is generated

## 2026-01-07

### Changed

- Renamed status values for consistency:
  - `planning` -> `ready`
  - `review` -> `to-review`
- Status lifecycle: `draft` -> `ready` -> `in-progress` -> `to-review` -> `done` -> `archived`

## 2026-01-05

### Changed

- `/archive` now generates centralized changelog at `docs/CHANGELOG.md`
- Feature docs (`docs/features/*.md`) no longer include changelog section
- Changelog uses Keep a Changelog format (Added/Changed/Removed/Fixed/Deprecated/Security)

## 2026-01-05

### Added

- Requirements Traceability in `code-architect` agent
  - New "Requirements Mapping" step in process
  - Mandatory "Requirements Traceability" table in plan.md output
- Requirements Coverage in `task-generator` agent
  - New "Extract Requirements" step to read spec.md
  - New "Verify Requirements Coverage" step
  - Mandatory "Requirements Coverage" table in tasks.md output
- `/tasks` command now passes spec.md to task-generator agent

### Changed

- Task categories renamed for clarity:
  - "Setup & Dependencies" -> "Foundation"
  - "Core Implementation" -> "Implementation"
  - "Testing & Validation" -> "Validation"
  - "Polish & Documentation" -> "Documentation"
- `code-architect` must map every FR-xxx to components
- `task-generator` must ensure every FR-xxx has at least one task

## 2026-01-03

### Added

- Documentation Discovery phase in `code-explorer` agent
  - Scans READMEs in related directories
  - Finds architecture docs, diagrams (mermaid, dbml, puml, drawio)
  - Checks related specs and CLAUDE.md for conventions
- Documentation Review phase in `code-architect` agent
  - Extracts implicit requirements from diagrams
  - Verifies plan completeness against documentation
- Documentation Context section in plan.md template
- Planning Completeness validation in `spec-validator` agent
  - Detects unplanned files created during implementation
  - Reports planning gaps for future improvements

### Changed

- `code-explorer` now includes documentation findings in output
- `code-architect` verifies files against discovered documentation
- `spec-validator` reports planning gaps (non-blocking feedback)

## 2026-01-03

### Added

- Feature organization by sequential ID (`001-user-auth/`, `002-add-2fa/`)
- Optional branch association for automatic feature detection
- `/init` command (renamed from `/spec`) with `--link` flag for branch association
- `/validate` command (renamed from `/review`) with three-level validation
- `/archive` command for documentation generation
- `/specs` command to list all features by status
- `spec-validator` agent with artifact, consistency, and code validation
- `spec-archiver` agent for documentation generation
- Shared research in `docs/research/` for cross-feature reuse
- Feature documentation output to `docs/features/` with changelog
- Frontmatter metadata in spec.md (id, feature, status, branch, created)

### Changed

- Renamed `/spec` to `/init`
- Renamed `/review` to `/validate`
- Renamed `code-reviewer` agent to `spec-validator`
- Artifacts now in `.artifacts/{ID}-{feature}/` instead of `.artifacts/{branch}/`
- Research output to `docs/research/{topic}.md` (shared, committed)
- `/implement` auto-marks as `review` when all tasks complete
- `/validate` auto-marks as `done` if all checks pass
- All commands support optional `[ID]` argument
- Updated all commands with `/spec-driven:` prefix

### Removed

- Branch-based artifact organization
- Feature-specific research.md (now shared in docs/research/)
- Templates folder (formats defined in agents/commands)

## 2025-12-19

### Added

- Context Flow system for consistent context passing between phases
- Critical Files section in plan.md (Reference, Modify, Create)
- Artifacts section in tasks.md with references to all spec artifacts
- Acceptance Criteria validation in /implement and /review
- Architecture compliance validation in /review
- Reference file loading for implement-agent (patterns to follow)

### Changed

- code-architect now receives and outputs consolidated Critical Files
- implement-agent receives spec.md, research.md, and reference file contents
- code-reviewer validates against acceptance criteria and architectural decisions
- task-generator includes file refs only for complex tasks

## 2025-12-15

### Added

- Web-researcher agent for external research when specs mention external technologies
- Serena MCP integration for semantic code analysis

### Changed

- Standardize plugin commands to pure markdown format
- Disable Serena web UI auto-open
- Add color attribute to agent frontmatter

## 2025-12-05

### Added

- Initial release
- `/spec` command for creating feature specifications
- `/clarify` command for resolving ambiguities
- `/plan` command for generating technical plans
- `/tasks` command for task decomposition
- `/implement` command for executing tasks
- `/review` command for code review
- Agents: code-explorer, code-architect, code-reviewer, implement-agent, task-generator
