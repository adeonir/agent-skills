# Summary

Analyze existing codebase and generate documentation for AI agents.

## When to Use

- Starting work on existing project
- Need general codebase understanding
- `.agents/codebase/` doesn't exist or needs refresh

## Scope

**Macro-level analysis** -- understanding the whole codebase:
- Technology stack
- Architecture patterns
- Project conventions
- Testing approach
- External integrations
- Validation checklist
- Key workflows
- Concerns and tech debt (when detected)

## Workflow

### Step 1: Check Existing

If `.agents/codebase/` exists:
- Update existing docs, merging new findings
- Never overwrite blindly

### Step 2: Explore Codebase

Perform a **deep analysis** of the entire codebase. This is NOT feature-specific -- the goal is to understand the project as a whole.

**Critical rule**: Don't just list or find files -- READ them and extract concrete patterns. Every convention documented must have evidence from actual code.

**Source boundary**: summary maps only the observable current state of source code, config, and tooling. Never read `.artifacts/` (docs-writer briefs, PRDs, design docs, epics, issues, roadmaps) or any planning document as a source of codebase facts. Milestones, epics, stories, `(planned)`, `(TBD)`, and feature IDs belong to planning artifacts -- they are not current state. If a module, route, or dependency is described in `.artifacts/` but absent from the filesystem right now, it does not exist and must not appear in `codebase/*.md`.

#### Phase 1: Project Discovery

1. **Read Project Metadata**

   Read package.json, tsconfig.json, pyproject.toml, go.mod, or equivalent. Extract:
   - Framework and runtime versions
   - All meaningful dependencies and their purpose
   - Scripts/commands available (build, test, lint, dev)
   - Configuration choices (module system, target, strict mode)

2. **Read Documentation**

   Read README.md, CLAUDE.md, CONTRIBUTING.md, or similar docs. Extract:
   - Project purpose and scope
   - Architecture decisions already documented
   - Coding standards and conventions
   - Setup and development workflow

3. **Map Directory Structure**

   Explore the full directory tree to understand the project, but only document the top-level directories and key subdirectories that define the architecture. Omit generated, vendored, or obvious directories.

   **Monorepos** (packages/, apps/, workspaces): Document the workspace structure and identify the primary package. Analyze shared packages first (shared types, config, utilities), then the main app. Don't try to deeply analyze every package -- focus on the ones most relevant to the project's core purpose.

#### Phase 2: Deep Code Analysis

4. **Read Representative Source Files**

   Select and READ source files that represent different areas of the codebase. The number depends on project size and diversity:

   | Project Size | Suggested Files | Coverage Goal |
   |--------------|-----------------|---------------|
   | Small (< 30 files) | 5-8 files | At least one from each directory |
   | Medium (30-100 files) | 8-12 files | Multiple layers and modules |
   | Large (> 100 files) | 12-20 files | Each major module, different patterns |

   **Reading priority** (start with what gives most context):
   1. Config and setup files (framework config, theme config, style tokens, env.example)
   2. Entry points (API routes, CLI commands, main files, layout files)
   3. Custom hooks (all hooks in hooks/ or similar directories)
   4. Business logic (services, use cases, domain models)
   5. Data access (repositories, API clients, database models)
   6. Styling (global styles, theme files, design tokens, CSS/SCSS variables)
   7. UI components (if applicable)
   8. Utilities (helpers, constants, shared types)

   **Always skip:**
   - Generated files (.d.ts, lockfiles, build output, source maps)
   - Vendored code (node_modules, vendor/, third_party/)
   - Data fixtures and seed files (large JSON/SQL dumps)
   - Migration files (schema history, not current patterns)
   - Minified or bundled files

   **Stop when**: You're seeing repeated patterns and no new conventions.

   For each file, extract:
   - Naming conventions (functions, classes, variables, files)
   - Import/export patterns and module organization
   - Error handling approach (try/catch, Result types, error boundaries)
   - Type definitions style (interfaces vs types, inline vs shared)
   - Code organization within files (ordering, grouping)
   - Styling patterns (custom properties, tokens, preprocessor usage, theme structure)
   - Shared components and utilities (what exists, how to import, when to use)

5. **Map Module Dependencies**

   For key modules/directories, identify:
   - What they import (dependencies)
   - What imports from them (dependents)
   - Circular dependency patterns if any
   - Shared utilities, constants, or types used across modules

6. **Trace Data Flows**

   Follow complete flows from entry to output. Quantity depends on project complexity:

   | Complexity | Flows to Trace |
   |------------|----------------|
   | Simple CRUD | 2-3 core flows |
   | Multi-domain | 3-5 flows covering different domains |
   | Complex/Event-driven | 5+ flows including edge cases |

   For each flow, trace:
   - Input: where data enters (API route, CLI arg, event handler, UI action)
   - Validation: how input is validated/parsed
   - Processing: business logic transformation
   - Persistence: how data is stored/retrieved
   - Output: how results are returned/rendered

   Document each step as a pattern, not with specific file references.

#### Phase 3: Testing & Integrations

7. **Analyze Testing Setup**

   READ actual test files (not just find them). Quantity guidelines:

   | Project Size | Test Files to Read |
   |--------------|-------------------|
   | Small | 2-3 tests |
   | Medium | 3-5 tests (unit, integration, e2e) |
   | Large | 5-8 tests across different types |

   Ensure diversity: unit tests, integration tests, and different test categories (happy path, edge cases, error handling).

   Extract:
   - Test framework and runner
   - Test file naming and location conventions
   - describe/it structure and nesting patterns
   - Mocking approach (what's mocked, how)
   - Fixture and helper patterns
   - Setup/teardown patterns

8. **Identify External Integrations**

   Search for and document all external touchpoints:
   - API calls (HTTP clients, SDK usage)
   - Database connections and ORM patterns
   - Third-party services (auth, payments, analytics)
   - Environment variables and configuration
   - File system operations

#### Phase 4: Convention Extraction

9. **Synthesize Patterns**

   Cross-reference findings from all files read. For each convention, provide:
   - What the project uses, with **code snippets** from actual source files as evidence
   - The **source file path** where the pattern was observed
   - What to avoid (anti-patterns observed or implied, not theoretical)
   - Inconsistencies: places where the same pattern is done differently

   The goal is to produce a reference that another agent can follow to write
   code that matches the project's existing patterns exactly. Generic
   descriptions like "uses camelCase" are not enough -- show the actual code.

   **Required categories** (document all that apply):

   | Category | What to look for |
   |----------|-----------------|
   | Naming | Functions, classes, variables, files, directories |
   | Imports | Order, grouping, aliases, barrel files |
   | Error handling | try/catch, Result types, error boundaries, error messages |
   | Types | Interfaces vs types, inline vs shared, strictness |
   | State management | Local state, global state, server state patterns |
   | Async patterns | Promises, async/await, error handling in async code |
   | Logging | Logger usage, log levels, structured logging |
   | Styling | CSS approach, preprocessor, custom properties, design tokens, theme structure |
   | Shared components | Reusable components library, how to import, when to use instead of raw HTML/framework primitives |
   | Custom hooks | All hooks the project defines, their signatures, return types, and usage examples |
   | Components | File structure, props patterns, composition patterns (if UI project) |

   **Critical**: Don't assume a framework or library based on dependency name alone.
   READ config files and actual usage to understand customizations. Projects often
   override or extend framework defaults -- document the project's actual values, not
   the framework's.

   **Project-specific abstractions are high priority.** When a project wraps framework
   primitives (custom components, variables, tokens, helpers, hooks), the agent needs to
   know they exist and use them instead of the underlying primitives. Scan for shared
   directories, component libraries, theme files, and utility modules. Document each
   abstraction with import paths and usage examples.

10. **Define Validation Checklist**

    Based on the project's tooling, define the verification steps to run after completing a task:
    - Type checking command
    - Lint command
    - Test command (for changed files)
    - Format command
    - Code generation (if applicable)
    - Pre-commit hooks (if configured)

11. **Identify Key Workflows**

    Document the main flows -- both user-facing and development:

    **User workflows**: The core user journeys through the application (e.g., authentication, main feature flow, data submission). For each:
    - Trigger: what starts the flow
    - Steps: sequence of actions
    - End state: what the user sees when done

    **Development workflows**: How developers work with the codebase (e.g., local dev with mocks, feature flag workflow, code generation workflow). For each:
    - When to use
    - Steps to follow
    - Key files involved

    Keep workflows concise -- describe patterns, not every edge case.

12. **Flag Concerns (optional)**

    During analysis, note any issues that could affect development:
    - Outdated or vulnerable dependencies
    - Inconsistent patterns across the codebase
    - Missing test coverage in critical areas
    - Hard-coded values that should be configurable
    - Security concerns (exposed secrets, missing auth checks)

    Populate the Concerns section in review.md only if real issues are detected. Omit the section otherwise.

### Step 3: Generate (sub-agent fan-out)

Dispatch one sub-agent per output doc in a single turn. Each sub-agent receives the Phase 1 baseline (project metadata, docs, directory structure already gathered by main) plus the matching template, reads only the files relevant to its domain, and writes its output file directly. Sub-agents do not return findings through the context -- the disk artifact is the handoff.

| Sub-agent | Template | Reads | Writes |
|-----------|----------|-------|--------|
| architecture | [templates/architecture.md](../templates/architecture.md) | Entry points, dir tree, layer boundaries | `.agents/codebase/architecture.md` |
| conventions | [templates/conventions.md](../templates/conventions.md) | Representative source files (Phase 2 reading priority) | `.agents/codebase/conventions.md` |
| testing | [templates/testing.md](../templates/testing.md) | Test files, test config | `.agents/codebase/testing.md` |
| integrations | [templates/integrations.md](../templates/integrations.md) | API clients, DB models, env files | `.agents/codebase/integrations.md` |
| checklist | [templates/checklist.md](../templates/checklist.md) | Scripts (package.json/Makefile), pre-commit config | `.agents/codebase/checklist.md` |
| workflows | [templates/workflows.md](../templates/workflows.md) | Entry points to traced data flows (Phase 2 step 6) | `.agents/codebase/workflows.md` |
Dispatch all sub-agents in the same turn -- they run independently.

**Depth over brevity.** These docs are loaded on-demand, not always in context.
Include code snippets and file references as evidence for every pattern.
Avoid redundancy across files, but do not sacrifice depth for token savings.

### Step 4: Self-Assessment (main agent)

After all sub-agents finish, the main agent reads the generated docs together and reviews them for consistency and completeness:

- **Consistency**: Do service names, paths, and patterns match across files?
- **Completeness**: Are there areas the scan could not cover deeply? Flag them
- **Gaps**: What would an agent still need to know that is not documented?

Save findings to `.agents/codebase/review.md` using the template. Cross-doc visibility cannot be split across sub-agents -- the main agent owns this synthesis.

### Step 5: Save

Create `.agents/codebase/` with generated docs.

### Step 6: Report

Inform user:
- Mapped {count} areas (6 standard + review)
- Gaps identified: {list areas lacking detail}
- Next: Create feature with baseline context

## Guidelines

**DO:**
- Read configuration and setup files before source code -- they reveal actual choices
- Prefer 10 diverse files over 30 similar ones
- Cover every architectural layer with representative files
- Read actual config and usage files before documenting conventions
- Note inconsistencies when the same pattern is implemented differently
- Stop reading when new files don't reveal new patterns
- Read existing docs first before analyzing when updating
- Merge new findings with existing content on updates
- Preserve discoveries added by spec-driven during planning (more specific context wins)
- Focus on architecture-relevant patterns, not implementation details
- Keep mapping files concise and scannable
- Document conventions as observed, not as prescribed

**DON'T:**
- Document conventions based on dependency names alone
- Overwrite existing codebase/ mapping without user confirmation
- Remove existing content unless it is clearly outdated
- Override feature-specific analysis (spec-driven) with general analysis (project-index)
- Include forward-looking content (`(planned)`, `(TBD)`, `(coming soon)`, milestone labels like `M5+`, feature numbers/IDs, phrases like "shipped through feature X") -- `codebase/*.md` captures only observable current state
- Include stubs for services, dependencies, routes, or modules that are not installed or present in the codebase right now -- if it does not exist today, it does not belong here
- Read `.artifacts/` (briefs, PRDs, design docs, epics, issues, roadmaps) as a source of codebase facts -- those are planning artifacts and describe intent, not current state

## Error Handling

- No codebase: Inform this is for existing projects
- Empty project: Treat as greenfield, skip summary

## Size Guidelines

These docs are loaded on-demand. Be thorough -- document patterns with real code examples and file references. Avoid redundancy across files, but do not sacrifice depth for brevity.

| Document        | Guideline                                                     |
| --------------- | ------------------------------------------------------------- |
| project.md      | Concise overview with full stack (~40 lines)                  |
| architecture.md | Structure, patterns, data flows with code examples            |
| conventions.md  | Every observed pattern with code snippets and file references |
| testing.md      | Patterns with example test structure from actual tests        |
| integrations.md | All external touchpoints with config details                  |
| checklist.md    | Concise validation steps (~15 lines)                          |
| workflows.md    | Core flows with step-by-step detail                           |
| review.md       | Consistency check, completeness gaps, concerns if found       |
