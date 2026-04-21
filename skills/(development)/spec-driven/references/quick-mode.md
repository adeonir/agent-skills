# Quick Mode

Express lane for small changes. Minimal ceremony, minimal artifacts.

## When to Use

- Bug fixes, config changes, small tweaks
- ≤3 files affected
- Scope describable in one sentence
- No architectural decisions needed
- No ambiguity in requirements

## Workflow

### Step 1: Ensure Structure

Check if `.artifacts/quick/` exists. If not:

```bash
mkdir -p .artifacts/quick
```

### Step 2: Generate Task ID

Scan `.artifacts/quick/` for highest numbered directory:

```bash
ls .artifacts/quick/ | sort -V | tail -1
```

Next ID = highest + 1 (padded: 001, 002...)

Generate slug from description:
- "Fix login redirect" -> `fix-login-redirect`

Create directory:

```bash
mkdir -p .artifacts/quick/{NNN}-{slug}
```

### Step 3: Detect Quality Gates

Read `package.json` (or equivalent for the stack):
- Lint script
- Typecheck script
- Test script

Record the actual commands for this project -- they go into the task file and
run in Step 6. If a gate doesn't exist, write `n/a` instead of inventing one.

### Step 4: Create Task File

**LOAD ORDER:** Load this template before reading any existing quick task in `.artifacts/quick/`. Existing tasks may be stale -- template wins on structure.

**USE TEMPLATE:** `templates/quick-task.md`

Create `.artifacts/quick/{NNN}-{slug}/task.md` with:
- Description of what needs to change
- Files to modify (if known)
- Expected outcome
- Quality Gates filled with commands detected in Step 3
- Current git branch (or `main`) in frontmatter

### Step 5: Load Patterns

Even small changes must follow project patterns.

- If `.agents/codebase/conventions.md` exists: read it. Pay attention to
  Project Abstractions and Custom Hooks -- use these instead of primitives
- If not: follow patterns already present in the files being modified

### Step 6: Implement

Follow [coding-principles.md](coding-principles.md) during implementation.

1. Read relevant files
2. Make the change -- match the patterns loaded in Step 5

### Step 7: Run Quality Gates

Run the gates recorded in the task file, in order, using `--fix` flags when
available:

```bash
{lint command} --fix
{typecheck command}
{test command}
```

Fix errors before proceeding. If the same gate fails 3 times, stop and ask
the user how to proceed -- never loop indefinitely.

Skip gates marked `n/a` in the task file.

### Step 8: Verify

Quick verification checklist:
- [ ] Change works as described
- [ ] No regressions in affected files
- [ ] Quality gates pass

### Step 9: Queue Discoveries (lightweight)

If you found a pattern, convention, or gotcha worth persisting, append to `.agents/knowledge.md`:

- **Gotchas** -> `## Gotchas`
- **Codebase discoveries** -> `## Codebase Feedback` with target tag (`conventions`, `architecture`, `testing`, `integrations`, `workflows`, `concerns`)

Load [knowledge.md](knowledge.md) for format.

Never write to `.agents/codebase/*.md` -- those are owned by project-index.

No prompt to integrate -- the next design or implement flow will surface queued items.

### Step 10: Update Task File

Set `status: done` in `task.md` frontmatter.

### Step 11: Generate Summary

**USE TEMPLATE:** `templates/quick-summary.md`

Create `.artifacts/quick/{NNN}-{slug}/summary.md` with:
- What was changed and why
- Files modified
- Patterns discovered (if any)
- Side effects or follow-up needed

### Step 12: Suggest Commit

Suggest a commit message following git-helpers conventions:
- Conventional commit type: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `style`, `perf`
- Format: `type: concise description in imperative mood`
- Imperative mood: "add", "fix", "implement" (not "added", "fixes")
- First line under 72 characters
- No scope, no file names, no versions, no attribution
- Body only for complex changes: 1-5 bullet points starting with lowercase
- Preview message and ask for confirmation before committing

## Scope Escalation

If during implementation the change turns out to be bigger than expected:

| Signal | Action |
|--------|--------|
| >3 files need changes | Stop. Suggest `specify` with Medium scope. |
| Architectural decision needed | Stop. Suggest `specify` with Large scope. |
| Requirements unclear | Stop. Suggest `specify` to clarify first. |
| Dependencies on other features | Stop. Suggest `specify` to map dependencies. |

When escalating, the quick task file serves as input for the specify phase.

## Guidelines

**DO:**
- Keep it simple -- quick mode exists to avoid ceremony for trivial changes
- Run quality gates even for small changes
- Escalate to specify when in doubt about scope
- Treat quick task artifacts as disposable after implementation

**DON'T:**
- Skip quality gates for small changes
- Force quick mode when scope is uncertain
- Over-document trivial changes

## Error Handling

- No .artifacts/: Create it
- Scope too large: Escalate to specify
- Quality gate fails: Fix before marking done
