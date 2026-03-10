# Execute Tasks

Implement, verify, and complete tasks. Verification happens continuously -- after each task or range, never deferred to the end.

> **LOAD FIRST:** [status-workflow.md](status-workflow.md) - Required for correct status management

## When to Use

When executing tasks from a feature's tasks.md, or when scope is Medium and plan/tasks were skipped.

## Arguments

- `[T001]` - Single task
- `[T001-T005]` - Range
- `[--all]` - All pending
- Empty - Next pending task

## Workflow

### Step 1: Resolve Feature

1. If ID provided -> use `.artifacts/features/{ID}-{name}/`
2. If no ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

### Step 2: Load Context

Read `spec.md` (acceptance criteria).

Check which artifacts exist and adapt:

| Artifacts Found | Mode |
|-----------------|------|
| spec + plan + tasks | **Full mode**: follow tasks.md |
| spec + plan (no tasks) | **Inline mode**: list steps from plan, then execute |
| spec only (Medium scope) | **Quick scan mode**: lightweight exploration, then execute |

### Step 3: Quick Scan (when plan was skipped)

When operating in **Quick scan mode** (Medium scope, no plan.md):

1. **Check research cache**: Look for `.artifacts/research/{topic}.md` relevant to this feature. If exists and valid, use it. Don't conduct deep research for Medium scope.

2. **Quick pattern scan**: Find 2-3 files similar to what needs to be built. Extract:
   - Naming conventions
   - Import patterns
   - Error handling approach
   - Test patterns (if applicable)

3. **Check .agents/codebase/**: If exists, scan for relevant conventions. Don't update it (that's plan's job).

4. **Complexity check**: If the quick scan reveals the change is more complex than expected (architectural decisions needed, unknown tech, many dependencies), STOP and suggest running `plan` first.

### Step 4: Safety Valve (inline step listing)

**ALWAYS** list atomic steps before starting implementation, even when tasks.md exists:

```
Execution steps:
1. {step}
2. {step}
3. {step}
...
```

**If >5 steps or complex dependencies detected:**
- STOP execution
- Inform user: "This is more complex than expected. Recommend creating formal tasks."
- Suggest running `tasks` (which requires `plan` first if that was also skipped)
- Exit

**If <=5 steps:** Proceed with execution.

### Step 5: Validate Dependencies

For each task to execute (when tasks.md exists):
- Check [P] (parallel) - proceed
- Check [B:Txxx] - verify Txxx is done

### Step 6: Update Status

If status is `ready` or `draft` (Medium scope may skip ready):
- Set `status: in-progress`

### Step 7: Execute Tasks

For each task, follow the 3-phase cycle:

#### Before (Preparation)

- Load [coding-principles.md](coding-principles.md)
- Read the relevant reference files from plan.md or quick scan (patterns to follow)
- Check the conventions table (naming, imports, error handling)
- Run pre-implementation checklist:

**Pre-Implementation Checklist:**

| Check | Question |
|-------|----------|
| Assumptions | What am I assuming about the existing code? Verify. |
| Files | Which files will I touch? Are they listed in the plan? |
| Success criteria | What acceptance criteria does this task satisfy? |
| Risk | Could this change break existing functionality? |

- Understand the scope: what files to create/modify
- Note specific patterns to match

#### During (Implementation)

- Follow plan.md architecture precisely (if plan exists)
- Match patterns from reference files exactly
- Use project's error handling approach
- Follow naming conventions documented
- Apply research findings if applicable
- Follow Knowledge Verification Chain for any technical decisions

#### After (Verification)

Verification runs after EVERY task or range of tasks -- never deferred to the end.

**Quality gates:**

```bash
# Use --fix flags when available
{lint command} --fix
{typecheck command}
{test command}
```

Fix errors before marking the task complete.

**Acceptance criteria check:**

- Validate against AC from spec.md that this task satisfies
- Verify follows project patterns (naming, imports, error handling)
- Check edge cases relevant to this task (see [Edge Case Verification](#edge-case-verification))

**If issues found:**
- Fix immediately before moving to the next task
- If the fix requires changes beyond the current task scope, note it and inform the user

### Step 8: Update Progress

If tasks.md exists, mark completed tasks:
```markdown
- [x] T001 [P] {description}
```

Update task counters in tasks.md header.

### Step 9: Check Completion

If all tasks done (or all inline steps done for Medium scope):
- Run final verification (see [Final Verification](#final-verification))
- Set `status: done`

### Step 10: Update State

If `.artifacts/state.md` exists and lessons were learned during execution, record them.

### Step 11: Report

Show:
- Tasks completed
- Files modified
- Quality gate results
- Verification summary (per-task results)
- Remaining tasks (if any)
- Suggested commit message
- For **Complex** scope with user-facing features: suggest running interactive UAT (see [validate.md](validate.md))

## Edge Case Verification

When verifying code after each task, check for relevant edge cases:

| Category | What to Verify |
|----------|---------------|
| Error states | Error paths return meaningful messages, no silent failures |
| Boundaries | Empty arrays, zero values, max lengths, off-by-one |
| Concurrency | Race conditions in async operations, state mutations |
| Permissions | Authorization checks on protected operations |
| Network | Timeout handling, retry logic, offline behavior |
| Invalid input | Null/undefined, wrong types, malformed data |

Not every category applies to every task. Check only what's relevant to the code just written.

## Final Verification

When all tasks are complete, run a final pass before marking `done`:

- [ ] All acceptance criteria (AC-xxx) from spec.md are satisfied
- [ ] All functional requirements (FR-xxx) are covered
- [ ] Quality gates pass on the full feature (not just per-task)
- [ ] No TODO/FIXME comments left from this feature
- [ ] Edge cases from spec.md are handled

For **Complex** scope with user-facing features, suggest interactive UAT:
- "Feature is implemented and verified. Want to run interactive UAT to walk through user scenarios?"
- If yes, follow [validate.md](validate.md) for the UAT workflow

## Interactive UAT (Complex scope)

For Complex scope features with user-facing behavior, interactive UAT can be triggered after all tasks pass verification. See [validate.md](validate.md) for the full UAT workflow. This is suggested, not automatic -- the user decides.

## Commit Suggestion

After completing a task or range, suggest a commit message based on what was actually changed.

**Follow git-helpers conventions:**

- Use conventional commit types: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `style`, `perf`, `ci`, `build`
- Format: `type: concise description in imperative mood`
- Imperative mood: "add", "fix", "implement" (not "added", "fixes")
- First line under 72 characters
- Focus on WHAT changed from the user's perspective
- No scope, no file names, no versions, no attribution, no future references
- Optional body: 1-5 bullet points explaining HOW (no file paths)

```
type: what changed from the user's perspective

- Optional: how it was implemented 1
- Optional: how it was implemented 2
```

Suggest atomic, logical commits at natural checkpoints (task group boundaries).

## Guidelines

- Complete one task at a time before starting the next
- Load coding-principles.md before writing any code
- Don't refactor beyond what the task requires
- Verify after each task or range -- never batch all verification to the end
- Follow Knowledge Verification Chain -- never fabricate patterns or APIs

## Error Handling

- Tasks not found: Check scope -- Medium may not have tasks.md (use inline mode)
- Dependency blocked: List prerequisites
- Quality gate failed: Fix before marking done
- Scope misjudged: Safety valve catches >5 steps, redirect to tasks/plan
