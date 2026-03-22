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
- Development commands
- Validation checklist
- Key workflows
- Concerns and tech debt (when detected)

## Workflow

### Step 1: Check Existing

If `.agents/codebase/` exists:
- Check age of files
- Ask if refresh needed
- If refresh: update existing docs (merge, never overwrite)

### Step 2: Explore Codebase

Perform a **deep analysis** of the entire codebase. This is NOT feature-specific -- the goal is to understand the project as a whole.

**Critical rule**: Don't just list or find files -- READ them and extract concrete patterns. Every convention documented must have evidence from actual code.

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

10. **Extract Commands**

    From package.json scripts, Makefile, justfile, or equivalent, document:
    - Setup/install commands
    - Development server commands
    - Test commands (all variants: unit, watch, coverage, ci)
    - Lint/format commands
    - Build/deploy commands
    - Code generation commands (if any)
    - Access points (local URLs, dev tools)

11. **Define Validation Checklist**

    Based on the project's tooling, define the verification steps to run after completing a task:
    - Type checking command
    - Lint command
    - Test command (for changed files)
    - Format command
    - Code generation (if applicable)
    - Pre-commit hooks (if configured)

12. **Identify Key Workflows**

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

13. **Flag Concerns (optional)**

    During analysis, note any issues that could affect development:
    - Outdated or vulnerable dependencies
    - Inconsistent patterns across the codebase
    - Missing test coverage in critical areas
    - Hard-coded values that should be configurable
    - Security concerns (exposed secrets, missing auth checks)

    Only create concerns.md if real issues are detected. Don't force it.

### Step 3: Generate

Generate documents in `.agents/codebase/` using the templates:

| Document | Template | Content |
|----------|----------|---------|
| Stack | [templates/stack.md](../templates/stack.md) | Framework, dependencies, dev tools |
| Architecture | [templates/architecture.md](../templates/architecture.md) | Structure, patterns, layers, data flows with code examples |
| Conventions | [templates/conventions.md](../templates/conventions.md) | Every observed pattern with code snippets and file references |
| Testing | [templates/testing.md](../templates/testing.md) | Patterns with example test structure from actual tests |
| Integrations | [templates/integrations.md](../templates/integrations.md) | All external touchpoints with config details |
| Commands | [templates/commands.md](../templates/commands.md) | All available commands with descriptions |
| Checklist | [templates/checklist.md](../templates/checklist.md) | Validation steps after tasks |
| Workflows | [templates/workflows.md](../templates/workflows.md) | Core flows with step-by-step detail and file references |
| Concerns | [templates/concerns.md](../templates/concerns.md) | Tech debt, risks, inconsistencies (optional) |

**Depth over brevity.** These docs are loaded on-demand, not always in context.
Include code snippets and file references as evidence for every pattern.
Avoid redundancy across files, but do not sacrifice depth for token savings.

### Step 4: Update AGENTS.md

Load [root-agents.md](root-agents.md) and generate/update `AGENTS.md` at the project root.

### Step 5: Self-Assessment

After generating all docs, review them for consistency and completeness:

- **Consistency**: Do service names, paths, and patterns match across files?
- **Completeness**: Are there areas the scan could not cover deeply? Flag them
- **Gaps**: What would an agent still need to know that is not documented?

Save findings to `.agents/codebase/review-notes.md` using the template.

### Step 6: Save

Create `.agents/codebase/` with generated docs.

### Step 7: Report

Inform user:
- Mapped {count} areas (8 standard + review notes + concerns if created)
- Updated AGENTS.md
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

## Error Handling

- No codebase: Inform this is for existing projects
- Empty project: Treat as greenfield, skip summary
