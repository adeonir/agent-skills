---
name: spec-driven
---

# Changelog

All notable changes to this skill will be documented in this file.

## 2026-04-17

### Changed

- Entities table in design template reduced to index columns (Entity, Purpose) with explicit sub-blocks for member enumeration, removing the tension between table structure and Step 9's file:line requirement
- design.md Step 7 codebase-feedback report is now mandatory -- always surface the count (including zero) so the `/project-index integrate feedback` handoff is never silently skipped
- specify.md MUST NOT list expanded to cover code identifiers (`mode: 'create'`, `reason: 'validation_error'`, `discountType === 'fixed'`), component/hook/function names, and named libraries; the rule now applies explicitly to every spec section
- spec-writing.md Baseline guidance tightened to forbid component/hook/function names alongside file paths
- spec template Notes and Baseline placeholders rewritten to steer the model toward behavioral context only

### Added

- DON'T rules in design.md forbidding `### Gotcha` subsections in Considerations (route to Decisions or `.agents/knowledge.md`) and forbidding prose/bullet substitution for the Entities table
- Behavior vs Symbol section in spec-writing.md with leak/rewrite pairs (mode, reason, discountType, TanStack, ClientFormDrawer) so the model can calibrate against real anti-patterns
- Notes section guidance in spec-writing.md so the free-form section no longer becomes a HOW dumping ground
- Pre-write checklist in specify.md Step 13 gating spec finalization on Content Separation compliance across every section

## 2026-04-16

### Added

- Artifact Structure Authority section in SKILL.md establishing `templates/` as canonical source of truth
- LOAD ORDER notes in creation references to prevent pattern-matching on stale artifacts
- Member Enumeration phase in codebase-exploration requiring exhaustive member listing with file:line
- Touched Types section in exploration template for structured member and absence-claim capture
- Exploration Depth Gate in design blocking Data Model until member enumeration is complete
- Currently Exposed Fields subsection in design template with self-auditing Gap column
- Granularity rule for Requirements Traceability (N-field ACs expand to N rows)
- Data Model closing checklist gating AC-field coverage, source anchors, and absence-claim anchors
- DO/DON'T rules against sampling touched types and unanchored absence claims
- `references/knowledge.md` canonical format spec for `.agents/knowledge.md`
- `## Codebase Feedback` queue section in knowledge.md for project-index handoff with target-tagged metadata
- Integration prompt after design Step 7 and implement Step 10 when feedback is queued

### Changed

- Data Model step requires enumerated members cited to file:line (not loose "attributes"/"shapes")
- Requirements Traceability bullet reflects per-field granularity
- design.md Step 7, implement.md Step 10, and quick-mode.md Step 7 queue discoveries in knowledge.md instead of writing `.agents/codebase/*.md` directly
- knowledge.md format tightened to `## Decisions` + `## Gotchas` + `## Codebase Feedback`
- Guidelines reflect one-writer rule: spec-driven writes knowledge.md, project-index writes codebase/*.md

### Removed

- `## Architecture` and `## Patterns` sections from knowledge.md format
- Direct writes from spec-driven to `.agents/codebase/conventions.md|architecture.md|testing.md`

## 2026-04-03

### Added

- Phase Transitions section with context window discipline and session dump pattern
- Sub-agent dispatch guidance for research and implementation phases
- PRD-as-input triggers for better discoverability of `@file.md` entry point
- Project knowledge artifact `.agents/knowledge.md` for cross-feature decisions and gotchas
- Clean window notes in design, implement, and research references

### Changed

- Design reference renumbered steps after adding knowledge loading step
- Project structure diagram updated to include knowledge.md

## 2026-03-30

### Changed

- Research reference adds depth levels: conceptual vs integration
- Integration depth requires researching exact interfaces, flags, env vars per stage, and runtime constraints
- Research process gains Step 3: determine depth per topic
- Research template adds optional Integration Constraints section

## 2026-03-29

### Added

- Baseline capture reference for hypothesis-free documentation of existing modules
- Baseline template for `.agents/baselines/{name}.md` output
- New triggers: "capture baseline", "document module", "document existing code"
- Specify Step 8 checks `.agents/baselines/` before running baseline-discovery

### Changed

- baseline-discovery.md notes baseline-capture for hypothesis-free use
- baseline-discovery.md checks existing baselines before rediscovering
- Cross-references updated with baseline-capture pipeline position
- Project structure updated with `.agents/baselines/` directory

## 2026-03-25

### Added

- Deep-verify reference for code correctness analysis (24 categories, tooling-aware)
- Verify Step 5: Code Correctness loads deep-verify.md between pattern and visual checks
- Verify phase: check implementation against design, project patterns, and visual references
- New triggers: "verify", "verify implementation"

### Changed

- Validate rewritten to UAT only, on-demand, any scope (was UAT + artifact validation, Complex only)
- Implement now references verify.md after quality gates
- Verify runs after every task/range regardless of scope
- Updated workflow diagram to show verify as explicit phase

## 2026-03-23

### Changed

- Rename Plan phase to Design (plan.md -> design.md) for better semantic clarity
- Rename Execute phase to Implement (execute.md -> implement.md) for precision
- Remove context budget (fixed token targets), keep qualitative loading rules only
- Quick mode now generates summary.md post-execution record
- Spec-driven retrofeeds .agents/codebase/ during design and implement phases
- Restructure spec.md: add Goals and Out of Scope sections, move ACs inline per story with Why Px justification
- Remove separate Functional Requirements and Acceptance Criteria sections from spec template
- Traceability now flows through AC-xxx IDs (inline per story) instead of FR-xxx + AC-xxx
- Condensate design.md template: merge Critical Files + Codebase Patterns into Patterns & Reuse, merge Architecture Decision + Decisions
- Add concerns check step in design workflow (loads .agents/codebase/concerns.md)
- Add Component Design "Action" column (new/modify) replacing separate Critical Files lists
- Add execution plan ASCII diagram to tasks.md template
- Add "Done when" checklist per task for explicit verification criteria

### Added

- Quick summary template (templates/quick-summary.md)

### Removed

- state.md template, state-management.md reference, and all state.md mentions
- Fixed token budget numbers (~15k base, <40k target, 160k+ reserve)

## 2026-03-21

### Added

- Test-driven development reference (red-green-refactor, behavior vs implementation)
- Pattern loading in quick-mode (Step 4: Load Patterns from conventions.md)
- Persist discoveries step in quick-mode and execute
- "Test first" principle in coding-principles when project has tests

### Changed

- Quick Scan rewritten: loads conventions.md + architecture.md when available, scans 5-8 files otherwise
- Quick-mode commit rules aligned with git-helpers conventions
- Coding-principles references conventions.md as source of truth for patterns

## 2026-03-12

### Changed

- Remove allowed-tools and External Content Trust Boundary from SKILL.md

## 2026-03-10

### Added

- External Content Trust Boundary section in SKILL.md for web research sanitization

### Changed

- Break frontmatter description into multi-line YAML to avoid obfuscation alerts
- Rename Implement phase to Execute (implement.md -> execute.md)
- Fold Validate phase into Execute as continuous per-task verification
- Reduce pipeline from 5 phases to 4 (Specify, Plan, Tasks, Execute)
- Verification now runs after each task or range, never deferred to the end
- Validate reference repositioned as sub-reference for interactive UAT within Execute
- Add project context check in Specify (suggests project-index for brownfield without .agents/)
- Update README, status-workflow, and all cross-references for new phase names

## 2026-03-09

### Added

- Adaptive phases with auto-sizing by complexity (Small/Medium/Large/Complex)
- Quick mode for small changes (≤3 files): express lane with minimal artifacts in .artifacts/quick/
- Discuss phase for resolving gray areas and ambiguities, generates decisions.md
- Knowledge Verification Chain: strict 5-step order for research and technical decisions (Codebase -> Project docs -> Context7 -> Web -> Flag uncertain)
- State management with .artifacts/state.md for persistent decisions, blockers, lessons, and deferred ideas
- Safety valve in implement: lists inline steps first, redirects to tasks if >5 steps detected
- Quick scan mode in implement: lightweight codebase exploration when plan is skipped (Medium scope)
- Interactive UAT in validate for Complex scope with user-facing features
- Scope field in spec.md frontmatter (medium/large/complex)
- New references: specify.md, discuss.md, quick-mode.md, state-management.md
- New templates: state.md, decisions.md, quick-task.md

### Changed

- Rename initialize phase to specify (initialize.md -> specify.md)
- Plan, Tasks, and Validate phases are now optional (auto-sized by scope)
- Simplify status workflow from 6 to 4 values (draft, ready, in-progress, done)
- Implement absorbs lightweight codebase scan and research cache check when plan is skipped
- Plan loads decisions.md for resolved gray areas
- All references updated with When to Skip sections and Knowledge Verification Chain references

### Removed

- Archive phase and all related files (references/archive.md, templates/archive.md)
- docs/features/ consolidation (no archive, no consolidated docs)
- Status values: to-review, archived
- references/initialize.md (replaced by specify.md)

## 2026-03-04

### Added

- Support for visual references (screenshots, mockups, wireframes) in feature specs
- New `designs/` folder within feature directory for storing images
- Automatic detection and saving of images attached to feature requests
- Visual References section in spec.md template for linking images
- Plan phase considers visual references in component design decisions

## 2026-03-03

### Changed

- Extract project-init and codebase-mapping to new project-index skill
- Consume `.agents/` instead of `.artifacts/project/` and `.artifacts/codebase/`
- Plan phase updates `.agents/codebase/` conditionally (only if it exists)
- Simplify archive (remove CHANGELOG.md update step)

### Removed

- project-init.md, codebase-mapping.md, roadmap.md references
- project.md, ROADMAP.md, CHANGELOG.md templates
- ROADMAP and CHANGELOG management (no longer in scope)

## 2026-03-02

### Added

- Brownfield auto-detection in project-init (auto-triggers codebase mapping for existing codebases)
- Persist Codebase Discoveries step in plan phase (feeds exploration findings back to project-level docs)
- Codebase feedback loop note in codebase-exploration reference

### Changed

- Replace feature-scoped exploration delegation with inline deep analysis workflow in codebase-mapping
- Codebase mapping now has 4 phases: Project Discovery, Deep Code Analysis, Testing & Integrations, Convention Extraction
- Enrich codebase mapping templates: ARCHITECTURE.md with entry points, layers, and data flow; CONVENTIONS.md with exploration-style table; TESTING.md with infrastructure table and reference tests

## 2026-02-27

### Changed

- Merge task-decomposition.md into tasks.md (single file with workflow + guidelines)
- Extract inline templates from codebase-exploration.md and research.md to templates/
- Add exploration.md and research.md to templates table in SKILL.md
- Fix CHANGELOG template to use date-only headers (was using version numbers)
- Enhance description with adjacent trigger contexts for better skill matching
- Standardize reference section naming: Process to Workflow, Rules to Guidelines
- Standardize reference closing sections: add Guidelines to operational files before Error Handling
- Add When to Use section to all reference files
- Add Templates section to SKILL.md with links to 7 templates
- Convert SKILL.md Guidelines to DO/DON'T format

## 2026-02-26

### Changed

- Replace inline Q&A with structured feature discovery (2 topics: Problem & Context, Scope & Success) with adaptive deepening and critical posture
- Redefine P1/P2/P3 as implementation order (core, increment, polish) instead of product-level must/should/could
- Doc extraction now transforms requirements instead of copying (filter to feature scope, make measurable, derive edge cases)
- P1 stories require Independent Test (vertical slice, demo-able end-to-end)

### Added

- Edge Cases section in spec template (boundary conditions, error scenarios)
- Success Criteria section in spec template (measurable outcomes)
- Quality gate before spec drafting (sufficiency criteria, synthesis confirmation)
- Edge cases and success criteria validation checks
- Writing guidelines for edge cases and success criteria in spec-writing reference

## 2026-02-25

### Changed

- Task grouping now uses commit boundaries instead of component-based grouping
- Align commit suggestions in implement reference with git-helpers conventions
- Update doc-extraction reference for simplified output filenames
- Standardize frontmatter metadata across templates

## 2026-02-20

### Changed

- Output directory migrated from `.specs/` to `.artifacts/specs/`
- Research cache location updated to `.artifacts/specs/research/`
- All references and templates updated with new paths

## 2026-02-11

### Added

- Templates for all artifacts (PROJECT, ROADMAP, CHANGELOG, spec, plan, tasks, archive)
- `status-workflow.md` reference with exact status values

### Changed

- References simplified by extracting output schemas into templates

### Removed

- Session state management (STATE.md template and session-state.md reference)
- State generation steps from project initialization

## 2026-02-08

### Added

- Migrate from plugin format to unified skills format
- `project-init.md` reference for project initialization workflow
- `roadmap.md` reference for feature planning and milestones
- `codebase-mapping.md` reference for comprehensive codebase analysis
- `baseline-discovery.md` reference for brownfield baseline analysis
- `doc-extraction.md` reference for PRD/document extraction
- `research.md` reference for research caching with MCP support
- Enforce content separation between spec/plan/tasks
- Consistent feature lookup by ID or branch in all references
- `coding-principles.md` with behavioral principles loaded before implementation
- WHEN/THEN/SHALL acceptance criteria format in spec-writing reference
- P1/P2/P3 priority levels on user stories
- Data model definition (entities, relationships, API contracts) in plan reference
- Mermaid diagram recommendations in Data Flow and Relationships sections
- Pre-implementation checklist (assumptions, files, success criteria, risk) in implement reference
- Edge case verification (error states, boundaries, concurrency, permissions) in validate reference
- Inline Q&A for ambiguity resolution during initialization (3-5 questions, max 2 rounds)
- Open Questions section replacing [NEEDS CLARIFICATION] markers in spec template

### Changed

- Expand `plan.md` with Requirements Traceability, Test Strategy, Codebase Patterns
- Expand `codebase-exploration.md` with 4-phase process and output template
- Expand `validate.md` with Pattern Compliance and gap categories
- Expand `implement.md` with 3-phase per-task process (Before/During/After)
- Task size guidelines (Small/Medium/Large) added to tasks reference
- Archive changelog entries now use dates only (no feature IDs)
- Research cache location changed to `.artifacts/research/`
- Simplify `validate.md` from 4 separate modes to single adaptive validation
- Unify validate output format with categorized checks table
- Resolve ambiguities inline during init instead of separate clarify phase
- Add Data Model Definition step before component design in plan reference
- Load `coding-principles.md` in Before (Preparation) step of implement reference
- Replace "Check MCP Memory Bank" with "Load Existing Context" in project-init reference
- Move conflicting requirements to "Open Questions" instead of markers in doc-extraction reference

### Removed

- `clarify.md` reference (clarifications happen inline during initialization)
- Clarify phase from workflow, triggers table, cross-references, and examples
- [NEEDS CLARIFICATION] markers (replaced with inline Q&A and Open Questions section)
- MCP Strategy sections from plan, implement, codebase-exploration, and research references
- MCP tool name references (Serena/Context7) from all references (tool-agnostic)

## 2026-02-04

### Added

- `codebase-exploration` skill for standardized codebase analysis patterns
- `output-templates` skill for pre-defined plan.md and tasks.md templates
- `validation-checklists` skill for structured checklists by validation mode
- `research-cache` skill for caching strategies with TTL and automatic invalidation
- Optional MCP support with `serena` for semantic code analysis and symbol navigation
- Automatic MCP detection in `/spec-plan` command with fallback to native tools

### Changed

- Reduce `spec-explorer` steps from 30 to 25 with directive prompts and explicit file content reading
- Reduce `spec-architect` steps from 30 to 20, remove redundancies
- Reduce `spec-tasker` steps from 15 to 10, streamline process
- Reduce `spec-implementer` steps from 50 to 35, optimize quality gates
- Reduce `spec-validator` steps from 25 to 15, add automatic mode detection
- Add YAML metadata for cache management in `spec-researcher`
- Reduce `/spec-plan` from 2-3 parallel explorers to 1 comprehensive explorer
- Add automatic stage detection and filtered git diff in `/spec-validate`
- Enhance context passing in `/spec-implement`

### Fixed

- Status workflow consistency across all commands

## 2026-02-03

### Added

- `spec-writing` skill for specification writing guidelines
- `task-decomposition` skill for task breakdown and dependency mapping
- `/spec-branch` command for creating feature branch from spec
- `/spec-status` command for detailed status with task progress and next steps
- Agent `temperature` (0.1-0.2) for deterministic output
- Agent `steps` limit (10-50 depending on agent) to control cost
- Granular `permission.bash` restrictions where applicable
- `permission.webfetch: allow` for researcher agent
- `agent: build` to `/spec-init`, `/spec-implement`, `/spec-archive`
- `agent: plan` to `/spec-clarify`, `/spec-plan`, `/spec-tasks`, `/spec-specs`, `/spec-status`
- `subtask: true` to `/spec-validate` for isolated context

### Changed

- Installation now includes `skills/` directory
- Update README with skills documentation and new commands
- Commands renamed with prefix: `spec-init.md`, `spec-plan.md`, `spec-tasks.md`, etc.
- Agents renamed with prefix: `spec-researcher.md`, `spec-explorer.md`, `spec-architect.md`, etc.
- Invocation now uses `/spec-init` and `@spec-architect` instead of `/spec/init` and `@spec/architect`
- Update all internal references in commands and agents
- Simplify installation: files copy directly to `.opencode/commands/` and `.opencode/agents/` without subdirectories

## 2026-01-31

### Added

- Test Infrastructure Discovery step in `explorer` agent (framework detection, test directories, shared utilities, fixtures, helpers, mocks)
- Test Strategy section in `architect` plan output (Existing Infrastructure, Reference Tests, New Tests tables)

### Changed

- Task grouping is now a flat list with adjacency-based grouping (blank lines between groups, no section headers)
- Related tasks (types, implementation, tests) are always adjacent with component-specific deps next to the code that uses them
- `/plan` command no longer runs inline validation, suggests `/spec-driven:validate` as optional step
- `architect` process now analyzes test patterns from explorer output

### Removed

- Inline plan validation step from `/plan` command (use `/spec-driven:validate` instead)
- Category-based task sections (Foundation, Implementation, Documentation)
- Generic "Testing: {strategy}" field from architect Considerations

## 2026-01-25

### Changed

- `/init` now enforces strict content separation between spec.md and plan.md (spec=WHAT, plan=HOW, tasks=WHEN)
- Brownfield baseline now describes behavior only, no file paths or code
- Task grouping by component for atomic commits (types, implementation, tests grouped together)
- Quality gates run after each task, not as separate final tasks
- Remove assumption that all projects have tests

### Fixed

- spec.md was including implementation details (file paths, code, technology choices)
- Tasks were being separated from related work (e.g., component far from its tests)

## 2026-01-18

### Added

- Quality Gates in tasks.md output (detects lint/typecheck scripts from package.json)
- Implementer runs quality gates after each task, tries `--fix` flag first
- Project Conventions Discovery step in `explorer` agent (wrapper libraries, patterns, conventions with reference files)
- "Project conventions" as mandatory output item in explorer analysis

### Changed

- `/tasks` command now reads package.json to detect quality gate commands
- Rule 4 in explorer now emphasizes explicit documentation of conventions

## 2026-01-12

### Added

- Brownfield support in `/init` command (auto-detects greenfield vs brownfield, generates Baseline section, new `type` field in frontmatter)
- Multi-mode validation in `/validate` command (Spec, Plan, Tasks, Full modes with auto-detection)
- `plan-validator` agent to validate plan.md against project documentation
- Plan validation step in `/plan` command (Step 8) with auto-correction loop (max 3 iterations)

### Changed

- Consolidate `plan-validator` and `spec-validator` into unified `validator` agent
- Rename agents for consistency (web-researcher, code-explorer, code-architect, task-generator, implement-agent, spec-archiver)
- Reduce agent count from 8 to 7
- `/validate` can now run at any workflow phase (not just after /implement)
- `/plan` command now has 10 steps (was 9)

### Removed

- `plan-validator` agent (merged into `validator`)
- `spec-validator` agent (merged into `validator`)

### Fixed

- `/init` now systematically reads all files in referenced @path
- `/init` extracts rules, constraints, and examples from documentation
- `code-architect` re-reads referenced docs before implementation decisions
- `code-architect` marks undocumented decisions as `[NOT DOCUMENTED - needs verification]`

## 2026-01-07

### Changed

- Rename status values for consistency (`planning` to `ready`, `review` to `to-review`)
- Status lifecycle: `draft` -> `ready` -> `in-progress` -> `to-review` -> `done` -> `archived`
- `/archive` now generates centralized changelog at `docs/CHANGELOG.md`
- Feature docs (`docs/features/*.md`) no longer include changelog section
- Changelog uses Keep a Changelog format (Added/Changed/Removed/Fixed/Deprecated/Security)

### Fixed

- Status update timing in `/plan` command: now sets `ready` only after plan is generated

## 2026-01-05

### Added

- Requirements Traceability in `code-architect` agent (mapping step, mandatory table in plan.md)
- Requirements Coverage in `task-generator` agent (extract step, verify step, mandatory table in tasks.md)
- `/tasks` command now passes spec.md to task-generator agent

### Changed

- Rename task categories (Setup & Dependencies to Foundation, Core Implementation to Implementation, Testing & Validation to Validation, Polish & Documentation to Documentation)
- `code-architect` must map every FR-xxx to components
- `task-generator` must ensure every FR-xxx has at least one task

## 2026-01-03

### Added

- Documentation Discovery phase in `code-explorer` agent (READMEs, architecture docs, diagrams, specs, CLAUDE.md)
- Documentation Review phase in `code-architect` agent (extracts implicit requirements, verifies plan completeness)
- Documentation Context section in plan.md template
- Planning Completeness validation in `spec-validator` agent (detects unplanned files, reports planning gaps)
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

- `code-explorer` now includes documentation findings in output
- `code-architect` verifies files against discovered documentation
- `spec-validator` reports planning gaps (non-blocking feedback)
- Rename `/spec` to `/init` and `/review` to `/validate`
- Rename `code-reviewer` agent to `spec-validator`
- Artifacts now in `.artifacts/{ID}-{feature}/` instead of `.artifacts/{branch}/`
- Research output to `docs/research/{topic}.md` (shared, committed)
- `/implement` auto-marks as `review` when all tasks complete
- `/validate` auto-marks as `done` if all checks pass
- All commands support optional `[ID]` argument
- Update all commands with `/spec-driven:` prefix

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

- `code-architect` now receives and outputs consolidated Critical Files
- `implement-agent` receives spec.md, research.md, and reference file contents
- `code-reviewer` validates against acceptance criteria and architectural decisions
- `task-generator` includes file refs only for complex tasks

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
