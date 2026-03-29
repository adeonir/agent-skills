# Baseline Capture

Document an existing module, subsystem, or area without a feature hypothesis.

## When to Use

- Inherit a module with no documentation
- Document existing code before deciding what to refactor
- Create a behavioral baseline before evolving a feature
- Onboard a new developer to a legacy subsystem
- NOT when you already have a feature description (use
  [specify.md](specify.md) + [baseline-discovery.md](baseline-discovery.md)
  instead)

## Workflow

### Step 1: Identify Target

Input options (accept any):
- Module name: "capture baseline for auth module"
- Directory path: "capture baseline for src/payments/"
- Area description: "capture baseline for the caching layer"
- Discovery mode: "help me find what to capture"

**If discovery mode:**
1. Check `.agents/project.md` and `.agents/codebase/*.md` (if exists)
2. List top-level source directories
3. Present areas with brief descriptions
4. User selects one

### Step 2: Load Available Context

| Context Found | Action |
|---------------|--------|
| `.agents/project.md` exists | Load for project overview |
| `.agents/codebase/*.md` exists | Load relevant module doc |
| Neither exists | Proceed with raw exploration (suggest project-index for better results) |

### Step 3: Scope the Area

Define boundaries before exploring:

1. Identify entry points (files, exports, routes, commands)
2. Identify boundaries (where this area ends and others begin)
3. Estimate breadth: how many files, how many concerns

Output: area name (kebab-case) for the output filename.

**If area spans >50 files:** suggest splitting into sub-areas.
**If area covers 1-2 files:** suggest documenting the parent module instead.

### Step 4: Explore Without Hypothesis

**Critical difference from baseline-discovery:** no feature keywords to
guide search. Explore systematically:

1. **Entry Points**: Find public API, routes, exports, CLI commands
2. **Data Flow**: Trace primary paths through the module
3. **Dependencies**: What this area depends on (internal + external)
4. **Dependents**: What depends on this area
5. **Configuration**: Environment variables, config files, feature flags
6. **Error Handling**: How failures are managed
7. **Testing**: Existing test coverage and patterns

### Step 5: Document Behavior

For each concern discovered, describe WHAT it does, not HOW:

- User-facing behavior and capabilities
- System-level behavior (background jobs, integrations, data
  transformations)
- Error states and edge cases observed in code
- Implicit contracts (what callers expect, what the module guarantees)

**Content rules (same as baseline-discovery):**

| Include | Exclude |
|---------|---------|
| What users/callers can do | File paths (except in Scope section) |
| Current capabilities | Function/class names |
| Behavioral contracts | Code snippets |
| Error states observed | Line numbers |
| Configuration surface | Implementation algorithms |

Exception: the Scope section MAY include directory paths to define
boundaries.

Mark uncertainty explicitly: "appears to..." when behavior is inferred,
not confirmed.

### Step 6: Identify Gaps, Risks, and Tech Debt

- **Gaps**: Missing functionality, incomplete features, TODO/FIXME markers
- **Risks**: Security concerns, single points of failure, missing
  validation
- **Tech Debt**: Inconsistent patterns, deprecated dependencies, dead
  code, missing tests

### Step 7: Generate Output

**USE TEMPLATE:** `templates/baseline.md`

Output to: `.agents/baselines/{name}.md`

1. Ensure `.agents/baselines/` exists (create if not)
2. Generate baseline document following the template
3. If `.agents/baselines/{name}.md` already exists, ask user: update or
   create new

### Step 8: Report

Inform user:
- Created: `.agents/baselines/{name}.md`
- Scope: {number of entry points, breadth}
- Key findings: {2-3 most notable items}
- Gaps found: {count}
- Risks found: {count}
- Next steps: suggest options (see Next Steps below)

## Guidelines

**DO:**
- Describe behavior, not implementation (same rules as baseline-discovery)
- Include the Scope section with directory boundaries
- Note uncertainty: "appears to..." when behavior is inferred
- Check for existing baseline before creating a new one
- Keep each baseline focused on one area (split if too broad)

**DON'T:**
- Include file paths outside the Scope section
- Include code snippets or function signatures
- Add goals, user stories, or acceptance criteria (this is NOT a spec)
- Overlap with project-index output (don't redocument architecture
  conventions)
- Use "should" statements -- only "does" statements

## Error Handling

- No `.agents/` directory: create `.agents/baselines/` directly
- Target not found: suggest discovery mode (Step 1)
- Area too broad (>50 files): suggest splitting into sub-areas
- Area too narrow (1-2 files): suggest documenting the parent module
- Existing baseline found: ask user whether to update or create adjacent

## Next Steps

After capturing a baseline, suggest:
1. **Form a hypothesis** -> run `specify` to create a feature spec
   (baseline will be consumed in Step 8)
2. **Capture adjacent area** -> run `baseline-capture` for related modules
3. **Deep index** -> run `project-index` if `.agents/` doesn't exist yet
