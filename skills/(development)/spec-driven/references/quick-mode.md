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

### Step 4: Execute

Follow [coding-principles.md](coding-principles.md) during implementation.

1. Read relevant files
2. Make the change
3. Run quality gates (lint, typecheck, tests if available)
4. Fix any issues

### Step 5: Verify

Quick verification checklist:
- [ ] Change works as described
- [ ] No regressions in affected files
- [ ] Quality gates pass

### Step 6: Update Task File

Mark task as done in `task.md`. Add:
- Files modified
- Brief summary of what was done

### Step 7: Suggest Commit

Suggest a commit message following git-helpers conventions:
- Conventional commit type (`fix`, `chore`, `refactor`, etc.)
- Concise description in imperative mood
- First line under 72 characters

### Step 8: Update State

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

- Keep it simple -- quick mode exists to avoid ceremony for trivial changes
- Don't skip quality gates even for small changes
- If in doubt about scope, escalate rather than force quick mode
- Quick task artifacts are disposable -- user can delete after implementation

## Error Handling

- No .artifacts/: Create it
- Scope too large: Escalate to specify
- Quality gate fails: Fix before marking done
