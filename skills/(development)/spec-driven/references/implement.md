# Implement Tasks

Implement, verify, and complete tasks. Verification happens continuously -- after each task or range, never deferred to the end.

> **LOAD FIRST:** [status-workflow.md](status-workflow.md) - Required for correct status management

## When to Use

When implementing tasks from a feature's tasks.md, or when scope is Medium and design/tasks were skipped.

Start with a clean context window. Load artifacts from disk (spec.md, design.md,
tasks.md), not from a previous phase's conversation context. See SKILL.md Phase
Transitions.

## Arguments

- `[T001]` - Single task
- `[T001-T005]` - Range
- `[S001]` - All tasks under story S001
- `[--all]` - All pending
- Empty - Next pending task

## Workflow

### Step 1: Resolve Feature

1. If feature ID provided -> use `.artifacts/features/{ID}-{name}/`
2. If no feature ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

If a story ID argument was given (`[S001]`):
- Read tasks.md, find the `### S001 ...` section
- Collect all tasks under that section header
- Treat them as the task range for this run

### Step 2: Load Context

Read `spec.md` (acceptance criteria).
If `.agents/knowledge.md` exists, read it for project-level decisions and gotchas.

Check which artifacts exist and adapt:

| Artifacts Found | Mode |
|-----------------|------|
| spec + design + tasks | **Full mode**: follow tasks.md |
| spec + design (no tasks) | **Inline mode**: list steps from design, then implement |
| spec only (Medium scope) | **Quick scan mode**: lightweight exploration, then implement |

### Step 3: Quick Scan (when design was skipped)

When operating in **Quick scan mode** (Medium scope, no design.md):

1. **Check research cache**: Look for `.artifacts/research/{topic}.md` relevant to this feature. If exists and valid, use it. Don't conduct deep research for Medium scope.

2. **Load project conventions**:
   - If `.agents/codebase/` exists: READ `conventions.md` (project abstractions,
     custom hooks, styling tokens -- these tell you what to use instead of
     framework primitives). READ relevant sections of `architecture.md`
     (component map, data flows)
   - If `.agents/codebase/` does not exist: scan 5-8 representative files.
     Prioritize shared component directories (find barrel exports / index files),
     custom hooks directories, style/theme files (variables, tokens), then files
     similar to what needs to be built

3. **Identify required abstractions**: Before writing any code, list:
   - Which shared components exist that should be used (not raw elements)
   - Which custom hooks handle the patterns needed (data fetching, state, etc.)
   - Which variables/tokens to use for styling (not hardcoded values)

4. **Complexity check**: If the quick scan reveals the change is more complex than expected (architectural decisions needed, unknown tech, many dependencies), stop and suggest running `design` first.

### Step 4: Safety Valve (inline step listing)

List atomic steps before starting implementation, even when tasks.md exists:

```
Execution steps:
1. {step}
2. {step}
3. {step}
...
```

**If >5 steps or complex dependencies detected:**
- Halt execution
- Inform user: "This is more complex than expected. Recommend creating formal tasks."
- Suggest running `tasks` (which requires `design` first if that was also skipped)
- Exit

**If <=5 steps:** Proceed with execution.

### Step 5: Validate Dependencies

For each task to implement (when tasks.md exists):
- Check [P] (parallel) - proceed
- Check [B:Txxx] - verify Txxx is done

**Sub-agent dispatch:** Spawn all `[P]` tasks as independent subagents in a
single turn — do not dispatch one at a time. Each subagent receives: spec.md +
design.md + its task(s) + coding-principles.md. Subagents write code to disk.
The main agent coordinates, tracks progress, and runs verify after each
subagent completes. The execution plan diagram in tasks.md serves as the
dispatch map — parallel branches map directly to independent subagents.

### Step 6: Update Status

If status is `ready` or `draft` (Medium scope may skip ready):
- Set `status: in-progress`

### Step 7: Implement Tasks

For each task, follow the 3-phase cycle:

#### Before (Preparation)

- Load [coding-principles.md](coding-principles.md)
- If project has test infrastructure: load [test-driven.md](test-driven.md)
- Read the relevant reference files from design.md or quick scan (patterns to follow)
- Check the conventions table (naming, imports, error handling)
- State the pre-implementation declaration before writing any code:

```
Assumptions: {what am I assuming about existing code -- verify each}
Files: {exhaustive list of files to create/modify -- only these}
Success criteria: {which ACs and Done when this task satisfies}
```

Do not proceed without stating all three explicitly.

- Verify the declaration against the checklist:

**Pre-Implementation Checklist:**

| Check | Question |
|-------|----------|
| Assumptions | Are all assumptions verified against actual code, not memory? |
| Files | Do listed files match design.md component locations? |
| Success criteria | Does it map directly to the task's Done when and AC-xxx? |
| Risk | Could this change break existing functionality? |

Any failed check: resolve before writing code.

#### During (Implementation)

- When TDD is active: write failing test first, then implement, then refactor
- Follow design.md architecture precisely (if design exists)
- Match patterns from reference files exactly
- Use project's error handling approach
- Follow naming conventions documented
- Apply research findings if applicable
- Follow Knowledge Verification Chain for any technical decisions
- **Scope guardrail:** if something outside the task definition is noticed (bug, improvement,
  tech debt), queue it to `.agents/knowledge.md ## Codebase Feedback` -- do not act on it inline.
  The heuristic: "Is this in my task definition?" If no, queue and move on.

#### After (Quality Gates + Verify)

Quality gates and verification run after EVERY task or range -- never deferred.

**Quality gates:**

```bash
# Use --fix flags when available
{lint command} --fix
{typecheck command}
{test command}
```

Fix errors before proceeding to verify.

**Verify:**

Run [verify.md](verify.md) to check implementation against design, project
patterns, and visual references (if provided). Verify handles:
- Design adherence (code matches spec/design)
- Pattern adherence (code follows project conventions)
- Visual adherence (layout matches references, optional)

If verify finds issues, fix them before moving to the next task. See
verify.md for the full workflow including loop escape.

### Step 8: Update Progress

If tasks.md exists:
1. Verify the "Done when" criteria for the task are met
2. Mark completed tasks:
```markdown
- [x] T001 [P] {description}
  - **Done when:** {verifiable outcome} -- VERIFIED
```
3. Update task counters in tasks.md header.

### Step 9: Check Completion

If all tasks done (or all inline steps done for Medium scope):
- Run final verification (see [Final Verification](#final-verification))
- Set `status: to-review`
- Do NOT set `status: done` -- audit owns that transition

### Step 10: Queue Discoveries

Load [knowledge.md](knowledge.md) for format.

Append discoveries from implementation to `.agents/knowledge.md`:

- **Runtime constraints, API quirks, workarounds** -> `## Gotchas`
- **New patterns, conventions, integration details, workflows, or tech debt observed in code** -> `## Codebase Feedback` with target tag (`conventions`, `architecture`, `testing`, `integrations`, `workflows`, `concerns`)

Never write to `.agents/codebase/*.md` -- those are owned by project-index.

If `.agents/knowledge.md` doesn't exist, create it with the three empty section headers (`## Decisions`, `## Gotchas`, `## Codebase Feedback`).

After appending, if `## Codebase Feedback` has rows, count by target and prompt the user:

> N discoveries queued in knowledge.md (X conventions, Y architecture, Z testing, W integrations). Run `/project-index integrate feedback` now? (y/n)

Do not auto-invoke project-index -- the user controls integration timing.

### Step 11: Approval Gate

When all tasks are done and Final Verification passes, present a summary and wait for approval:

```
Implementation ready: `.artifacts/features/{ID}-{name}/`
Tasks: {X} done | ACs: {Y}/{Z} verified
Remaining: {count or "none"}
Suggested commit: {message}

Approve to proceed to audit, or describe what to fix.
```

- If issues remain: fix before presenting gate.
- If changes requested: address and re-present gate.
- If approved: run `audit` (mandatory before `done`). For user-facing features, also consider `validate`.

Do not suggest `audit` until approved.

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

When all tasks are complete, run a final pass before setting `status: to-review`:

- [ ] All acceptance criteria (AC-xxx) are covered by tasks
- [ ] All ACs marked `[x]` in spec.md match the per-task verify results
- [ ] Quality gates pass on the full feature (not just per-task)
- [ ] No TODO/FIXME comments left from this feature
- [ ] Edge cases from spec.md are handled
- [ ] Verify passed (design + pattern adherence)

Goals and Success Criteria are NOT checked here -- they are audit.md's job.
Do not mark their `[ ]` from this reference.

Audit is mandatory before `done`. UAT is on-demand.

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

**DO:**
- Complete one task at a time before starting the next
- Load coding-principles.md before writing any code
- Verify after each task or range -- never batch all verification to the end
- Follow Knowledge Verification Chain -- never fabricate patterns or APIs

**DON'T:**
- Refactor beyond what the task requires
- Batch all verification to the end
- Skip loading coding-principles.md before implementation

## Error Handling

- Tasks not found: Check scope -- Medium may not have tasks.md (use inline mode)
- Dependency blocked: List prerequisites
- Quality gate failed: Fix before marking done
- Scope misjudged: Safety valve catches >5 steps, redirect to tasks/design
