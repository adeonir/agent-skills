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

### Step 3: Create Task File

**USE TEMPLATE:** `templates/quick-task.md`

Create `.artifacts/quick/{NNN}-{slug}/task.md` with:
- Description of what needs to change
- Files to modify (if known)
- Expected outcome

### Step 4: Load Patterns

Even small changes must follow project patterns.

- If `.agents/codebase/conventions.md` exists: read it. Pay attention to
  Project Abstractions and Custom Hooks -- use these instead of primitives
- If not: follow patterns already present in the files being modified

### Step 5: Execute

Follow [coding-principles.md](coding-principles.md) during implementation.

1. Read relevant files
2. Make the change -- match the patterns loaded in Step 4
3. Run quality gates (lint, typecheck, tests if available)
4. Fix any issues

### Step 6: Verify

Quick verification checklist:
- [ ] Change works as described
- [ ] No regressions in affected files
- [ ] Quality gates pass

### Step 7: Persist Discoveries

If `.agents/codebase/` exists and you found a pattern not yet documented
(new shared component, new hook, new convention), update the relevant file.
Merge new findings, never overwrite existing content.

### Step 8: Update Task File

Mark task as done in `task.md`. Add:
- Files modified
- Brief summary of what was done

### Step 9: Suggest Commit

Suggest a commit message following git-helpers conventions:
- Conventional commit type: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `style`, `perf`
- Format: `type: concise description in imperative mood`
- Imperative mood: "add", "fix", "implement" (not "added", "fixes")
- First line under 72 characters
- No scope, no file names, no versions, no attribution
- Body only for complex changes: 1-5 bullet points starting with lowercase
- Preview message and ask for confirmation before committing

### Step 10: Update State

If `.artifacts/state.md` exists and the fix reveals a pattern (recurring bug, tech debt area), note it under Lessons or Deferred.

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
