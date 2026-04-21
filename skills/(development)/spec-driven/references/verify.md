# Verify Implementation

Check implementation against the spec design, project patterns, code correctness,
and visual references. Runs after every task or range -- never deferred to the end.

> **LOADS:** [deep-verify.md](deep-verify.md) -- code correctness analysis (Step 5)

## When to Use

- After completing a task or range of tasks (any scope)
- When the user explicitly requests verification
- After quality gates pass in implement.md -- verify is the deeper check

## When to Skip

- Quick mode (small fixes, config changes)

## Workflow

### Step 1: Resolve Feature

1. If ID provided -> use `.artifacts/features/{ID}-{name}/`
2. If no ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

### Step 2: Load Sources of Truth

Gather the references to verify against:

| Source | Location | Purpose |
|--------|----------|---------|
| Spec | `.artifacts/features/{ID}-{name}/spec.md` | Acceptance criteria, user stories, edge cases |
| Design | `.artifacts/features/{ID}-{name}/design.md` | Architecture, data model, file list, patterns |
| Project patterns | `.agents/codebase/` | Conventions, naming, error handling, data fetching |
| Visual references | `.artifacts/features/{ID}-{name}/designs/` or MCP | Layout, UI behavior (optional) |

Skip sources that don't exist. Design and project patterns are the primary
sources. Visual references only when provided or explicitly requested.

### Step 3: Design Adherence

Compare implementation against design.md (if exists) or spec.md:

- **Planned vs implemented**: functions, endpoints, components, routes described
  in design -- do they exist in code?
- **Behavior**: does the implementation match the described behavior, data flow,
  and state management?
- **Data model**: do entities, relationships, and API contracts match the design?
- **File structure**: are files created/modified as listed in the design?

Report findings as:

| Finding | Severity | Description |
|---------|----------|-------------|
| Missing endpoint | high | `POST /api/auth/login` in design but not implemented |
| Behavior mismatch | medium | Token refresh uses polling instead of designed event-based approach |

### Step 4: Pattern Adherence

Compare implementation against project conventions in `.agents/codebase/`
(if exists) or against patterns observed during quick scan:

- **Naming**: files, components, functions, variables follow project conventions
- **File structure**: new files placed in correct directories per project patterns
- **Error handling**: uses project's error handling approach (not ad-hoc)
- **Data fetching**: uses project's data fetching patterns (hooks, server actions, etc.)
- **Imports**: follows barrel exports, path aliases, import ordering
- **Styling**: uses design tokens, CSS variables, not hardcoded values

Report findings with the same severity table.

### Step 5: Code Correctness

Load [deep-verify.md](deep-verify.md) for semantic code analysis.

Deep-verify checks for logic errors, semantic issues, and correctness
problems that linters and type checkers cannot detect. It auto-detects
project tooling and skips categories already covered.

Skip this step when the task only changed configuration, documentation,
or static assets.

Findings merge into the outcome table in Step 7.

### Step 6: Visual Adherence (optional)

Only runs when visual references exist or user explicitly requests.

Sources of visual references:
- Screenshots or mockups in `.artifacts/features/{ID}-{name}/designs/`
- Figma via MCP (if available in session)
- Pencil via MCP (if available in session)
- Any reference the user provides during Specify phase

Compare:
- Layout structure matches reference
- Component hierarchy matches reference
- Responsive behavior matches reference (if specified)
- Spacing, alignment, visual hierarchy are consistent

### Step 7: Determine Outcome

**If all checks pass:**
- Report "Verification passed" with summary
- Mark covered ACs as `[x]` in spec.md (see [Step 8](#step-8-sync-ac-checkboxes))
- Continue to next task or mark done

**If issues found:**
- List findings with severity
- If a previously-marked AC is now failing, revert its `[x]` to `[ ]` in spec.md
- Fix issues immediately (verify --> fix --> verify loop)
- Re-run only the failed checks after fix

### Step 8: Sync AC Checkboxes

After verification passes for a task, update spec.md acceptance criteria.

**Which ACs to mark:**

1. If `tasks.md` exists: read `## Requirements Coverage` table -- mark every
   AC whose task list is fully verified (all listed tasks passed verify)
2. If no `tasks.md` (Medium scope): map by user story containing the code
   changed -- mark ACs inside that P1/P2/P3 story

**How to mark:**

Edit `spec.md` in place: flip `- [ ]` to `- [x]` and change the status tag
from `` `in-tasks` `` to `` `verified` `` on the matching AC line.
Never reorder, rename, or drop ACs. Preserve the `AC-xxx:` identifier.

**Revert rule:**

If a later verify run reopens a finding on an already-marked AC, flip it back
to `- [ ]` and revert the status tag to `` `in-tasks` ``. The checkbox and
status always reflect current verification state, not historical pass.

**Never touch Goals or Success Criteria here** -- those are audit.md's job.

### Step 9: Loop Escape

Track fix attempts per finding. If the same finding fails N times (default: 3):
- Stop the loop
- Report the stuck finding with context
- Ask the user for input: "I've attempted to fix this 3 times without
  success. Here's what I've tried and what's still failing. How should
  I proceed?"

Never loop indefinitely.

## Guidelines

**DO:**
- Run after every task or range, regardless of scope
- Check design adherence first, then patterns, then code correctness, then visual
- Fix issues before moving to the next task
- Report findings with severity (high/medium/low)
- Skip visual check when no references exist
- Sync AC checkboxes in spec.md after every pass (and revert on regression)

**DON'T:**
- Defer verification to the end of all tasks
- Report code style issues that linters already catch
- Loop indefinitely on the same finding
- Assume visual references exist -- check first
- Run visual verification without explicit references
- Run deep-verify on config-only or docs-only changes
- Mark Goals or Success Criteria checkboxes -- audit.md owns those

## Error Handling

- No design.md: verify against spec.md acceptance criteria only
- No .agents/codebase/: skip pattern adherence or use quick scan baseline
- No visual references: skip visual adherence entirely
- All sources missing: inform user, suggest running design or project-index first
