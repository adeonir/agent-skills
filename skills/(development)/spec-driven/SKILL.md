---
name: spec-driven
description: >-
  Specification-driven development that auto-sizes depth by complexity.
  Creates structured feature specs with traceability to requirements. Use when
  planning features, breaking work into tasks, implementing with verification,
  auditing goals before closing, tracking decisions across sessions, or
  extracting specs from PRDs.
when_to_use: >-
  Triggers on "create feature", "specify feature", "plan", "design feature",
  "tasks", "implement", "verify", "verify implementation", "validate", "UAT",
  "audit", "audit feature", "validate goals", "quick fix", "quick task",
  "discuss feature", "break this into tasks", "plan this feature",
  "show status", "from PRD", "extract from document", "use this PRD",
  "here's the PRD".
effort: xhigh
---

# Spec-Driven Development

**Recommended effort:** xhigh for design, implement, and audit phases; medium
for quick mode and status checks.

Structured development workflow with adaptive depth. Right ceremony for the
right scope. Use ultrathink for design and audit phases.

## Workflow

```
specify --> design* --> tasks* --> implement --> verify --> audit --> done
  ^______________________________________|  (verify after each task)
```

Adaptive pipeline: Specify and Implement always run; Design and Tasks auto-skip when scope is small enough. Verify runs after every task/range and marks AC checkboxes. Implement finishes at `to-review`; Audit validates Goals and Success Criteria, then transitions to `done`. Validate (UAT) is on-demand and can reprove any `[x]`.

## Context Loading Strategy

**Base load:**
- `.agents/project.md` (context, if exists)
- Current feature spec.md

**On-demand:**
- `.agents/codebase/*.md` (brownfield)
- `.agents/knowledge.md` (cross-feature decisions and gotchas)
- decisions.md (designing or implementing from user decisions)
- design.md (implementing)
- tasks.md (implementing)
- research/*.md (new technologies)

**Never simultaneous:**
- Multiple feature specs
- Multiple codebase docs

## Artifact Structure Authority

Templates in `templates/` are the canonical source of truth for every artifact's structure. Existing artifacts in `.artifacts/` may be stale, predate skill updates, or have been authored before current conventions -- they are context, NEVER structural reference.

**Load order when creating any artifact:**

1. Load the relevant template from `templates/` first
2. Only then read existing artifacts (`spec.md`, `design.md`, `tasks.md`, etc.) for domain context, prior decisions, or cross-feature continuity

If an existing artifact's structure diverges from the template, follow the template. Do not propagate legacy structure.

## Triggers

### Feature-Level (auto-sized)

| Trigger Pattern | Reference |
|-----------------|-----------|
| Create new feature, specify feature | [specify.md](references/specify.md) |
| From PRD, extract from document, use this PRD | [specify.md](references/specify.md) (via @file.md) |
| Modify feature, improve feature | [specify.md](references/specify.md) (brownfield) |
| Discuss feature, capture context, how should this work | [discuss.md](references/discuss.md) |
| Create technical design, plan feature | [design.md](references/design.md) |
| Research technology, cache research | [research.md](references/research.md) |
| Create tasks | [tasks.md](references/tasks.md) |
| Implement task, execute task | [implement.md](references/implement.md) |
| Verify implementation, check adherence, verify code | [verify.md](references/verify.md) |
| Audit feature, validate goals, audit goals and success criteria | [audit.md](references/audit.md) |
| Validate, UAT, manual testing, test manually | [validate.md](references/validate.md) |
| Quick fix, quick task, small change, bug fix | [quick-mode.md](references/quick-mode.md) |
| List features, show status | [status-specs.md](references/status-specs.md) |

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
| Knowledge format, Codebase Feedback format | [knowledge.md](references/knowledge.md) |

Notes:

- `deep-verify.md` is not a direct trigger. It is loaded by `verify.md`
  during Step 5 (Code Correctness).
- `baseline-discovery.md` is not a direct trigger. It is loaded by
  `specify.md` Step 8 for brownfield features.

## Cross-References

```
specify.md --------> discuss.md (when gray areas detected)
specify.md --------> quick-mode.md (when Small scope)
specify.md --------> design.md (when Large/Complex, spec complete)
specify.md --------> implement.md (when Medium, skip design/tasks)
design.md ---------> tasks.md (when Large/Complex)
design.md ---------> research.md (if new tech)
tasks.md ----------> implement.md
implement.md ------> coding-principles.md (loaded before coding)
implement.md ------> verify.md (after every task/range)
verify.md --------> deep-verify.md (code correctness analysis)
verify.md --------> spec.md (marks AC [x] on pass, reverts on regression)
implement.md ------> audit.md (after to-review, validates Goals/Success)
audit.md ---------> spec.md (marks Goals/Success [x], transitions done)
implement.md ------> validate.md (on-demand UAT, any scope)
validate.md ------> audit.md (re-run required after UAT reproves any [x])
implement.md ------> tasks.md (safety valve: >5 inline steps)
specify.md --------> baseline-discovery.md (brownfield features)
design.md ---------> project-index (prompts integrate feedback after Step 7)
implement.md ------> project-index (prompts integrate feedback after Step 10)
```

## Auto-Sizing

**Complexity determines depth, not a fixed pipeline.** Before starting any feature, assess its scope and apply only what's needed:

| Scope | What | Specify | Design | Tasks | Implement |
|-------|------|---------|--------|-------|-----------|
| **Small** | ≤3 files, one sentence | **Quick mode** -- skip pipeline entirely | - | - | - |
| **Medium** | Clear feature, <10 tasks | Spec (brief) | Skip -- explore inline | Skip -- steps implicit | Implement + verify per step |
| **Large** | Multi-component feature | Full spec + requirement IDs | Full design | Full breakdown + dependencies | Implement + verify per task |
| **Complex** | Ambiguity, new domain | Full spec + [discuss gray areas](references/discuss.md) | Research + full design | Breakdown + parallel design | Implement + verify per task |

**Rules:**

- **Specify and Implement are always required** -- you always need to know WHAT and DO it
- **Design is skipped** when the change is straightforward (no architectural decisions, no new patterns)
- **Tasks is skipped** when there are ≤3 obvious steps (they become implicit in Implement)
- **Discuss is triggered within Specify** only when the agent detects ambiguous gray areas that need user input
- **Verify runs after every task/range** -- checks design adherence, pattern adherence, code correctness (tooling-aware deep analysis), and visual adherence (optional); also marks AC `[x]` in spec.md on pass
- **Audit runs before done** -- validates Goals and Success Criteria against evidence, marks their `[x]`, and transitions `to-review` -> `done`; mandatory for every `.artifacts/features/` feature (Medium/Large/Complex)
- **Validate (UAT) is on-demand** -- user requests it when they want to manually test, any scope; may revert any `[x]` if user reproves
- **Quick mode** is the express lane -- for bug fixes, config changes, and small tweaks (no audit needed)
- **Verification is continuous** -- quality gates and acceptance criteria run after each task or range, never deferred to the end

**Safety valve:** Even when Tasks is skipped, Implement ALWAYS starts by listing atomic steps inline (see [implement.md](references/implement.md)). If that listing reveals >5 steps or complex dependencies, STOP and create a formal `tasks.md` -- the Tasks phase was wrongly skipped.

## Project Structure

```
.artifacts/
├── features/
│   └── {ID}-{name}/
│       ├── spec.md       # WHAT: Requirements (always created)
│       ├── decisions.md  # WHY: Decisions on gray areas (only when discuss triggered)
│       ├── design.md     # HOW: Architecture (only for Large/Complex)
│       ├── tasks.md      # WHEN: Tasks (only for Large/Complex)
│       └── designs/      # Visual references (optional)
├── quick/                # Quick mode tasks
│   └── NNN-{slug}/
│       ├── task.md
│       └── summary.md    # Post-execution summary
└── research/             # Research cache (reusable across features)
    └── {topic}.md
```

**Project context:**
```
.agents/
├── project.md            # Project context (project-index)
├── codebase/             # Codebase analysis (project-index)
└── knowledge.md          # Cross-feature decisions and gotchas (spec-driven)
```

> Note: `.agents/codebase/` is generated by the `project-index` skill. `.agents/knowledge.md` is owned by spec-driven -- it accumulates cross-feature decisions, gotchas, and queues codebase discoveries in a `## Codebase Feedback` section for project-index to integrate. project-index reads knowledge.md for context and consumes the Codebase Feedback queue on demand (`/project-index integrate feedback`), but never rewrites Decisions or Gotchas. spec-driven is the sole writer to knowledge.md; project-index is the sole writer to `.agents/codebase/*.md` and `.agents/project.md`. If `.agents/` doesn't exist, Specify suggests running project-index for better context (especially for brownfield projects). All feature artifacts stay within `.artifacts/`.

## Templates

| Context | Template |
|---------|----------|
| Feature spec | [spec.md](templates/spec.md) |
| Discuss context | [decisions.md](templates/decisions.md) |
| Technical design | [design.md](templates/design.md) |
| Task breakdown | [tasks.md](templates/tasks.md) |
| Quick task | [quick-task.md](templates/quick-task.md) |
| Quick summary | [quick-summary.md](templates/quick-summary.md) |
| Codebase exploration | [exploration.md](templates/exploration.md) |
| Research cache | [research.md](templates/research.md) |

## Knowledge Verification Chain

When researching, designing, or making any technical decision, follow this chain in strict order. Never skip steps.

```
Step 1: Codebase      -> check existing code, conventions, and patterns already in use
Step 2: Project docs  -> README, docs/, inline comments, .agents/codebase/
Step 3: Context7 MCP  -> resolve library ID, then query for current API/patterns
Step 4: Web search    -> official docs, reputable sources, community patterns
Step 5: Flag or ask   -> state partial reasoning tagged "verify", or ask user for direction
```

**Rules:**

- Never skip to Step 5 if Steps 1-4 are available
- Step 5 output is never presented as fact -- either flagged as uncertain or framed as a direction question to the user
- **NEVER assume or fabricate.** If the chain does not resolve an answer, say "I don't know" and ask the user for direction. Inventing APIs, patterns, or behaviors causes cascading failures across design -> tasks -> implementation. Uncertainty is always preferable to fabrication.

## Guidelines

**DO:**
- Separate content by purpose: spec=WHAT (goals, stories, ACs), design=HOW, tasks=WHEN
- Follow status flow: draft -> ready -> in-progress -> to-review -> done
- Use sequential Feature IDs (001, 002)
- Reuse research cache across features (.artifacts/research/)
- Consume `.agents/` for project context and codebase info (optional -- use if exists)
- Queue codebase discoveries to `.agents/knowledge.md` `## Codebase Feedback` section -- project-index integrates them into `codebase/*.md` on demand
- Record cross-feature decisions and gotchas in `.agents/knowledge.md` during design and implement
- Auto-size depth based on complexity -- skip phases that add no value
- Run verify after each task or range -- design adherence, pattern adherence, visual (if references exist)

**DON'T:**
- Reuse Feature IDs from previous features
- Mix spec, design, and task content in a single file
- Skip status transitions (e.g., jumping from draft to done)
- Create feature-specific research files outside .artifacts/research/
- Generate `.agents/` content from scratch (that's project-index's responsibility)
- Force full pipeline on small/medium changes -- respect auto-sizing
- Assume or fabricate when information is unavailable -- follow Knowledge Verification Chain
- Defer verification to the end -- verify runs per task/range, not as a final batch
- Loop indefinitely on verify findings -- escape after 3 failed fix attempts

## Phase Transitions

Each phase (specify, design, research, tasks, implement) should run in a clean
context window. A polluted window (used for research and then for implementation)
grows large and increases hallucination risk.

**Between phases:**

```
finish phase -> append to session dump -> clean window -> start next phase
                                                           ...
                                                         (more phases)
                                                           ...
                                         end of session -> wrap-up (reads dump)
```

1. Complete the current phase and write its artifacts to disk
2. Append session context to `.artifacts/.session-dump.md` -- a near-complete
   dump of what happened (decisions, discoveries, blockers, open items, phase
   completed, next phase). Each phase appends, building a cumulative record
3. Clear the context window
4. Start the next phase in a clean window, loading only the artifacts it needs

The session dump is ephemeral -- wrap-up reads it at end of session to compose
notes, then the file is disposable. It is not a project artifact.

**Sub-agent dispatch:**

Research and implementation phases can be delegated to sub-agents for better
context isolation and parallelism. The artifacts on disk are the handoff
mechanism -- sub-agents don't need to return findings through the context.

- Research sub-agent: reads codebase + external sources, writes to
  `.artifacts/research/{topic}.md`
- Implementation sub-agents: receive spec + design + task(s), write code to
  disk. Main agent coordinates and runs verify
- Parallel tasks (`[P]` marker) map directly to independent sub-agents

## Error Handling

- No .artifacts/: Create it (features/ and research/ are created on demand)
- Spec not found: List available features
- Open questions blocking architecture: Resolve before planning (trigger discuss)
- Design not found: Suggest design before tasks (or skip if Medium scope)
- Tasks not found: Suggest tasks before implement (or skip if Medium scope)
- Scope misjudged: Safety valve catches it -- redirect to appropriate phase
