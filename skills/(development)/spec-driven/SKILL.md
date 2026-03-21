---
name: spec-driven
description: >-
  Specification-driven development that auto-sizes depth by complexity.
  Creates structured feature specs with traceability to requirements. Use when
  planning features, breaking work into tasks, implementing with verification,
  or tracking decisions across sessions. Triggers on "create feature", "specify
  feature", "plan", "tasks", "execute", "implement", "validate", "quick fix",
  "quick task", "discuss feature", "break this into tasks", "plan this
  feature", "record decision", "show state".
---

# Spec-Driven Development

Structured development workflow with adaptive depth. Right ceremony for the right scope.

## Workflow

```
specify --> plan* --> tasks* --> execute
  ^___________________________|  (verify after each task)
```

Adaptive pipeline: Specify and Execute always run; Plan and Tasks auto-skip when scope is small enough. Verification is continuous throughout Execute.

## Context Loading Strategy

**Base load (~15k tokens):**
- `.agents/project.md` (context, if exists)
- `.artifacts/state.md` (persistent memory)
- Current feature spec.md

**On-demand:**
- `.agents/codebase/*.md` (brownfield)
- decisions.md (designing or executing from user decisions)
- plan.md (executing)
- tasks.md (executing)
- research/*.md (new technologies)

**Never simultaneous:**
- Multiple feature specs
- Multiple codebase docs

**Target:** <40k tokens total context
**Reserve:** 160k+ tokens for work, reasoning, outputs

## Triggers

### Feature-Level (auto-sized)

| Trigger Pattern | Reference |
|-----------------|-----------|
| Create new feature, specify feature | [specify.md](references/specify.md) |
| Modify feature, improve feature | [specify.md](references/specify.md) (brownfield) |
| Discuss feature, capture context, how should this work | [discuss.md](references/discuss.md) |
| Create technical plan | [plan.md](references/plan.md) |
| Research technology, cache research | [research.md](references/research.md) |
| Create tasks | [tasks.md](references/tasks.md) |
| Execute task, implement task | [execute.md](references/execute.md) |
| Validate, UAT, verify work | [validate.md](references/validate.md) (within Execute) |
| Quick fix, quick task, small change, bug fix | [quick-mode.md](references/quick-mode.md) |
| List features, show status | [status-specs.md](references/status-specs.md) |

### Project-Level

| Trigger Pattern | Reference |
|-----------------|-----------|
| Record decision, log blocker, add deferred idea | [state-management.md](references/state-management.md) |

### Guidelines

| Trigger Pattern | Reference |
|-----------------|-----------|
| How to write specs | [spec-writing.md](references/spec-writing.md) |
| How to decompose tasks | [tasks.md](references/tasks.md) |
| Codebase exploration | [codebase-exploration.md](references/codebase-exploration.md) |
| Research patterns | [research.md](references/research.md) |
| Baseline discovery | [baseline-discovery.md](references/baseline-discovery.md) |
| Extract from PRD/docs | [doc-extraction.md](references/doc-extraction.md) |
| Coding principles | [coding-principles.md](references/coding-principles.md) |
| Status workflow, when to update status | [status-workflow.md](references/status-workflow.md) |

## Cross-References

```
specify.md -------> discuss.md (when gray areas detected)
specify.md -------> quick-mode.md (when Small scope)
specify.md -------> plan.md (when Large/Complex, spec complete)
specify.md -------> execute.md (when Medium, skip plan/tasks)
plan.md ----------> tasks.md (when Large/Complex)
plan.md ----------> research.md (if new tech)
tasks.md ---------> execute.md
execute.md -------> coding-principles.md (loaded before coding)
execute.md -------> validate.md (interactive UAT, Complex scope)
execute.md -------> tasks.md (safety valve: >5 inline steps)
```

## Auto-Sizing

**Complexity determines depth, not a fixed pipeline.** Before starting any feature, assess its scope and apply only what's needed:

| Scope | What | Specify | Plan | Tasks | Execute |
|-------|------|---------|------|-------|---------|
| **Small** | ≤3 files, one sentence | **Quick mode** -- skip pipeline entirely | - | - | - |
| **Medium** | Clear feature, <10 tasks | Spec (brief) | Skip -- explore inline | Skip -- steps implicit | Implement + verify per step |
| **Large** | Multi-component feature | Full spec + requirement IDs | Full plan | Full breakdown + dependencies | Implement + verify per task |
| **Complex** | Ambiguity, new domain | Full spec + [discuss gray areas](references/discuss.md) | Research + full plan | Breakdown + parallel plan | Implement + verify per task + [interactive UAT](references/validate.md) |

**Rules:**

- **Specify and Execute are always required** -- you always need to know WHAT and DO it
- **Plan is skipped** when the change is straightforward (no architectural decisions, no new patterns)
- **Tasks is skipped** when there are ≤3 obvious steps (they become implicit in Execute)
- **Discuss is triggered within Specify** only when the agent detects ambiguous gray areas that need user input
- **Interactive UAT is triggered within Execute** only for Complex scope with user-facing features
- **Quick mode** is the express lane -- for bug fixes, config changes, and small tweaks
- **Verification is continuous** -- quality gates and acceptance criteria run after each task or range, never deferred to the end

**Safety valve:** Even when Tasks is skipped, Execute ALWAYS starts by listing atomic steps inline (see [execute.md](references/execute.md)). If that listing reveals >5 steps or complex dependencies, STOP and create a formal `tasks.md` -- the Tasks phase was wrongly skipped.

## Project Structure

```
.artifacts/
├── state.md              # Decisions, blockers, lessons, deferred ideas (persistent)
├── features/
│   └── {ID}-{name}/
│       ├── spec.md       # WHAT: Requirements (always created)
│       ├── decisions.md    # WHY: Decisions on gray areas (only when discuss triggered)
│       ├── plan.md       # HOW: Architecture (only for Large/Complex)
│       ├── tasks.md      # WHEN: Tasks (only for Large/Complex)
│       └── designs/      # Visual references (optional)
├── quick/                # Quick mode tasks
│   └── NNN-{slug}/
│       └── task.md
└── research/             # Research cache (reusable across features)
    └── {topic}.md
```

**Project context** (generated by project-index skill):
```
.agents/
├── project.md            # Project context
└── codebase/             # Codebase analysis
```

> Note: `.agents/` is generated by the `project-index` skill. If it exists, spec-driven uses and updates it. If not, Specify suggests running project-index for better context (especially for brownfield projects). All feature artifacts stay within `.artifacts/`.

## Templates

| Context | Template |
|---------|----------|
| Feature spec | [spec.md](templates/spec.md) |
| Discuss context | [decisions.md](templates/decisions.md) |
| Technical plan | [plan.md](templates/plan.md) |
| Task breakdown | [tasks.md](templates/tasks.md) |
| Project state | [state.md](templates/state.md) |
| Quick task | [quick-task.md](templates/quick-task.md) |
| Codebase exploration | [exploration.md](templates/exploration.md) |
| Research cache | [research.md](templates/research.md) |

## Knowledge Verification Chain

When researching, designing, or making any technical decision, follow this chain in strict order. Never skip steps.

```
Step 1: Codebase   -> check existing code, conventions, and patterns already in use
Step 2: Project docs -> README, docs/, inline comments, .agents/codebase/
Step 3: Context7 MCP -> resolve library ID, then query for current API/patterns
Step 4: Web search   -> official docs, reputable sources, community patterns
Step 5: Flag uncertain -> "I'm not certain about X -- here's my reasoning, but verify"
```

**Rules:**

- Never skip to Step 5 if Steps 1-4 are available
- Step 5 is ALWAYS flagged as uncertain -- never presented as fact
- **NEVER assume or fabricate.** If you cannot find an answer, say "I don't know" or "I couldn't find documentation for this". Inventing APIs, patterns, or behaviors causes cascading failures across plan -> tasks -> implementation. Uncertainty is always preferable to fabrication.

## Guidelines

**DO:**
- Separate content by purpose: spec=WHAT, plan=HOW, tasks=WHEN
- Follow status flow: draft -> ready -> in-progress -> done
- Use sequential Feature IDs (001, 002)
- Reuse research cache across features (.artifacts/research/)
- Consume `.agents/` for project context and codebase info (optional -- use if exists)
- Update `.agents/codebase/` with new discoveries during plan phase (if it exists)
- Update `.artifacts/state.md` with decisions and blockers as they arise
- Auto-size depth based on complexity -- skip phases that add no value
- Verify continuously during Execute -- after each task or range, not as a separate phase

**DON'T:**
- Reuse Feature IDs from previous features
- Mix spec, plan, and task content in a single file
- Skip status transitions (e.g., jumping from draft to done)
- Create feature-specific research files outside .artifacts/research/
- Generate `.agents/` content (that's project-index's responsibility)
- Force full pipeline on small/medium changes -- respect auto-sizing
- Assume or fabricate when information is unavailable -- follow Knowledge Verification Chain
- Defer all verification to the end -- verify per task/range during Execute

## Error Handling

- No .artifacts/: Create it (features/ and research/ are created on demand)
- Spec not found: List available features
- Open questions blocking architecture: Resolve before planning (trigger discuss)
- Plan not found: Suggest plan before tasks (or skip if Medium scope)
- Tasks not found: Suggest tasks before execute (or skip if Medium scope)
- Scope misjudged: Safety valve catches it -- redirect to appropriate phase
