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

#### Phase 2: Deep Code Analysis

4. **Read Representative Source Files**

   Select and READ source files that represent different areas of the codebase. The number depends on project size and diversity:

   | Project Size | Suggested Files | Coverage Goal |
   |--------------|-----------------|---------------|
   | Small (< 30 files) | 5-8 files | At least one from each directory |
   | Medium (30-100 files) | 8-12 files | Multiple layers and modules |
   | Large (> 100 files) | 12-20 files | Each major module, different patterns |

   **Selection strategy**: Pick files from different directories AND different architectural layers:
   - Entry points (API routes, CLI commands, main files)
   - Business logic (services, use cases, domain models)
   - Data access (repositories, API clients, database models)
   - Utilities (helpers, constants, shared types)
   - UI components (if applicable)

   **Stop when**: You're seeing repeated patterns and no new conventions.

   For each file, extract:
   - Naming conventions (functions, classes, variables, files)
   - Import/export patterns and module organization
   - Error handling approach (try/catch, Result types, error boundaries)
   - Type definitions style (interfaces vs types, inline vs shared)
   - Code organization within files (ordering, grouping)

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
   - What the project uses (with evidence from multiple files)
   - What to avoid (anti-patterns observed or implied)
   - Edge cases or inconsistencies found

   Cover at minimum: naming, imports, error handling, types, state management, async patterns, logging.

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

### Step 3: Generate

Generate 8 documents in `.agents/codebase/` using the templates:

| Document | Template | Content |
|----------|----------|---------|
| Stack | [templates/stack.md](../templates/stack.md) | Framework, dependencies, dev tools |
| Architecture | [templates/architecture.md](../templates/architecture.md) | Structure, patterns, layers, data flow |
| Conventions | [templates/conventions.md](../templates/conventions.md) | Naming, error handling, imports, types |
| Testing | [templates/testing.md](../templates/testing.md) | Infrastructure, patterns, reference tests |
| Integrations | [templates/integrations.md](../templates/integrations.md) | External services and their purpose |
| Commands | [templates/commands.md](../templates/commands.md) | Setup, dev, test, build commands |
| Checklist | [templates/checklist.md](../templates/checklist.md) | Validation steps after tasks |
| Workflows | [templates/workflows.md](../templates/workflows.md) | User and development workflows |

### Step 4: Generate AGENTS.md

Generate or update `AGENTS.md` at the project root. The file should reference the contents of `.agents/` and provide a concise summary of the project for any AI agent.

Content should include:
- Project summary (from project.md)
- Key conventions (from conventions.md)
- Important commands (from commands.md)
- Checklist (from checklist.md)
- References to `.agents/` files for deeper context

If `AGENTS.md` already exists: merge new content, preserve any manual additions.

### Step 5: Save

Create `.agents/codebase/` with generated docs.

### Step 6: Report

Inform user:
- Mapped 8 areas
- Updated AGENTS.md
- Next: Create feature with baseline context

## Guidelines

### File Reading Strategy
- **Quality over quantity**: Better to read 10 diverse files than 30 similar ones
- **Cover all layers**: Ensure every architectural layer is represented
- **Look for inconsistencies**: Note when the same pattern is implemented differently
- **Stop when saturated**: When new files don't reveal new patterns, you've read enough

### Update Mode
When `.agents/codebase/` already exists:
- Read existing docs first
- Merge new findings with existing content
- Never remove existing content unless it's clearly outdated
- Add new sections/rows to existing tables
- Update version numbers and dependency changes

### General
- Don't overwrite existing codebase/ mapping without user confirmation
- Focus on architecture-relevant patterns, not implementation details
- Keep mapping files concise and scannable
- Document conventions as observed, not as prescribed

## Error Handling

- No codebase: Inform this is for existing projects
- Empty project: Treat as greenfield, skip summary
