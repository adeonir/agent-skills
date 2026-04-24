# Quick Mode

Express lane for small changes. Minimal ceremony, minimal artifacts.

## When to Use

- Bug fixes, config changes, small tweaks
- ≤3 files affected (count source files of user-written code only — exclude
  lock files, `.artifacts/`, `.agents/`, and auto-formatted files with no
  semantic change)
- Scope describable in one sentence
- No architectural decisions needed
- No ambiguity in requirements

## Workflow

If the user pauses mid-execution and resumes later, re-read `task.md` before
the next edit — branch, status, or scope may have drifted.

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
run in Step 7. If a gate doesn't exist, write `n/a` instead of inventing one.

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

### Design is inline, not a phase

Before Step 6, treat `task.md` as a hypothesis, not a contract. The author may
have assumed one approach without weighing alternatives.

Enumerate silently the 2-4 viable approaches. If only one exists, proceed. If
multiple exist with materially different trade-offs (lock contention, deploy
parity, library surface, reversibility, coupling to internal layouts), surface
them to the user as a short trade-off table before writing code. Let the user
pick — do not present a recommendation dressed as analysis.

This is a precondition to Step 6, not a numbered step. Skipping it and
implementing task-as-written is executing a command, not collaborating on a
design.

Trigger signals (enumerate):
- Task touches infrastructure (DB access, build tooling, CI, deploy)
- Task creates reusable tooling (seeds, fixtures, dev routes, mock servers)
- Task integrates a new dependency or runtime
- Task description names a filesystem path, internal API, or binary format

Skip signals (proceed without enumeration):
- Bug fix with file and line named
- Config value swap
- Rename or text-level refactor with no behavioral change
- Dependency version bump with no API change

### Step 6: Implement

Follow [coding-principles.md](coding-principles.md) during implementation.

1. Read relevant files
2. Make the change -- match the patterns loaded in Step 5

### Step 7: Run Quality Gates and Verify

Run in order. Static gates first; static failures short-circuit — do not execute
the change until static gates pass. A typecheck or lint failure means the
runtime behavior is moot; running the script or hitting the endpoint just burns
cycles before you have to come back and fix the static issue anyway.

```
1. {lint command} --fix       (static)
2. {typecheck command}        (static)
3. {test command}             (static, if any)
4. Execute the change end-to-end — run the script, open the UI, hit the endpoint
5. Inspect result against task.md "Expected Outcome"
```

Skip gates marked `n/a` in the task file. Fix errors before proceeding. If the
same gate fails 3 times, stop and ask the user how to proceed -- never loop
indefinitely.

### Step 8: Save Discoveries (default: save)

Append non-obvious findings to `.agents/knowledge.md` without asking. Real
gotchas, verified patterns, and environmental quirks all qualify.

SKIP only when:
- Already in knowledge.md (check first)
- Restatement of project conventions already documented elsewhere
- Change was purely mechanical (formatting, rename, dep bump with no behavior shift)

Targets:
- **Gotchas** -> `## Gotchas`
- **Codebase discoveries** -> `## Codebase Feedback` with target tag (`conventions`, `architecture`, `testing`, `integrations`, `workflows`, `concerns`)

Format per [knowledge.md](knowledge.md). Never write to `.agents/codebase/*.md` --
those are owned by project-index. No prompt to integrate -- the next design or
implement flow will surface queued items.

### Step 9: Update Task File

Set in `task.md` frontmatter:
- `status: done`
- `completed: {YYYY-MM-DD}`
- `patterns_discovered`: list of new patterns surfaced (or empty)
- `follow_up`: side effects, related issues, improvements noticed but not addressed (or empty)

### Step 10: Suggest Commit

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
- Treat `task.md` as a hypothesis; surface alternatives before implementing infra/tooling tasks
- Run static gates before executing the change
- Save discoveries by default; skip only when criteria above apply
- Escalate to specify when in doubt about scope
- Treat quick task artifacts as disposable after implementation

**DON'T:**
- Skip quality gates for small changes (contrasts: run static gates before executing)
- Implement task-as-written without enumerating alternatives when trigger signals fire (contrasts: treat task.md as hypothesis)
- Ask permission to record gotchas (contrasts: save by default)
- Force quick mode when scope is uncertain (contrasts: escalate when in doubt)

## Error Handling

- No .artifacts/: Create it
- Scope too large: Escalate to specify
- Static gate fails: Fix before running the change end-to-end
- Same gate fails 3 times: Stop and ask the user
- task.md modified mid-session: Re-read before the next edit
