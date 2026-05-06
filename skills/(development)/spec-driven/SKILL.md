---
name: spec-driven
description: >-
  Specification-driven feature development with auto-sized depth. Produces
  spec.md, design.md, and tasks.md artifacts with requirements traceability,
  plus verify and audit phases tied to acceptance criteria. Use when planning
  a feature, breaking a change into tasks or stories, implementing a named
  story or task, verifying implementation against acceptance criteria,
  auditing goals before closing, or turning a PRD into engineering artifacts.
  Not for diagnosing unknown bugs (use debug-tools), authoring standalone
  PRD/RFC/ADR/TDD documents (use docs-writer), PR/commit mechanics (use
  git-helpers), or PM backlog tracking (use epic-tracker).
when_to_use: >-
  Triggers on "plan this feature", "plan this out", "spec this feature",
  "turn this PRD into a spec", "break this into tasks", "break this into stories",
  "create technical design for this feature", "implement story S###",
  "implement task T###", "verify implementation", "check acceptance criteria",
  "audit feature", "audit this spec", "validate goals", "UAT", "manual testing",
  "discuss this feature", "show feature status", "quick fix", "quick task",
  "quick mode", "small change", and known one-line fixes where the user names
  file and line (for example, "fix the typo in components/Footer.tsx line 12",
  "one-line change in <file>:<line>"). Do NOT trigger on "why is X not working",
  "debug this", "trace issue", "create PRD/RFC/ADR/TDD", "code review this
  diff", "commit this", "create an issue", or tooling/setup tasks.
---

# Spec-Driven Development

**Recommended effort:** xhigh for design and audit phases; medium for
implement, quick mode, and status checks.

Structured development workflow with adaptive depth.

## Workflow

```
specify --> design* --> tasks* --> implement --> verify --> audit --> done
  ^______________________________________|  (verify after each task)
```

Adaptive: Specify and Implement always run; Design and Tasks auto-skip when
scope is small enough. Verify runs after every task/range.

## Triggers

### Feature-Level (auto-sized)

| Trigger Pattern                                                            | Reference                                          |
| -------------------------------------------------------------------------- | -------------------------------------------------- |
| Create new feature, specify feature                                        | [specify.md](references/specify.md)                |
| From PRD, extract from document, use this PRD                              | [specify.md](references/specify.md) (via @file.md) |
| Modify feature, improve feature                                            | [specify.md](references/specify.md) (brownfield)   |
| Discuss feature, capture context, how should this work                     | [discuss.md](references/discuss.md)                |
| Create technical design, plan feature                                      | [design.md](references/design.md)                  |
| Research technology, cache research                                        | [research.md](references/research.md)              |
| Create tasks                                                               | [tasks.md](references/tasks.md)                    |
| Implement task, execute task                                               | [implement.md](references/implement.md)            |
| Verify implementation, check adherence, verify code                        | [verify.md](references/verify.md)                  |
| Audit feature, validate goals, audit goals and success criteria            | [audit.md](references/audit.md)                    |
| Validate, UAT, manual testing, test manually                               | [validate.md](references/validate.md)              |
| Quick fix, quick task, quick mode, start quick mode, small change, bug fix | [quick-mode.md](references/quick-mode.md)          |
| List features, show status                                                 | [status-specs.md](references/status-specs.md)      |

### Guidelines

| Trigger Pattern                            | Reference                                                     |
| ------------------------------------------ | ------------------------------------------------------------- |
| Phase transitions, session dump protocol   | [phases.md](references/phases.md)                             |
| How to decompose tasks                     | [tasks.md](references/tasks.md)                               |
| Codebase exploration                       | [codebase-exploration.md](references/codebase-exploration.md) |
| Research patterns                          | [research.md](references/research.md)                         |
| Coding principles                          | [coding-principles.md](references/coding-principles.md)       |
| Status workflow, when to update status     | [status-workflow.md](references/status-workflow.md)           |
| Knowledge format, Codebase Feedback format | [knowledge.md](references/knowledge.md)                       |

Notes:

- `code-correctness.md` not a direct trigger; loaded by `verify.md` Step 5.
- `discovery.md` not a direct trigger; loaded by `specify.md` Step 7.
- `auto-sizing.md` not a direct trigger; loaded by `specify.md` Step 1.

## Cross-References

```
specify.md --------> discovery.md (feature discovery before drafting)
specify.md --------> auto-sizing.md (scope assessment)
specify.md --------> discuss.md (when gray areas detected)
specify.md --------> quick-mode.md (when Small scope)
specify.md --------> design.md (Large/Complex)
specify.md --------> implement.md (Medium, skip design/tasks)
design.md ---------> tasks.md (Large/Complex)
design.md ---------> research.md (if new tech)
tasks.md ----------> implement.md
implement.md ------> coding-principles.md (before coding)
implement.md ------> verify.md (after every task/range)
verify.md ---------> code-correctness.md (code correctness analysis)
verify.md ---------> spec.md (marks AC [x] on pass, reverts on regression)
implement.md ------> audit.md (after to-review)
audit.md ----------> spec.md (marks Goals/Success [x], transitions done)
implement.md ------> validate.md (on-demand UAT)
validate.md -------> audit.md (re-run after UAT reproves any [x])
implement.md ------> tasks.md (safety valve: >5 inline steps)
phases.md ---------> specify/design/tasks/implement (session dump + dispatch protocol)
design.md ---------> project-index (integrate feedback after Step 8)
implement.md ------> project-index (integrate feedback after Step 10)
domain-model -----> spec-driven      (entities+rules as impl contracts)
spec-driven ------> domain-model     (domain gaps trigger update mode)
```

## Artifact Structure Authority

`templates/` is canonical for every artifact's structure. Load the relevant
template before reading any existing artifact in `.artifacts/` -- existing
files are context, not structural reference. When structure diverges from the
template, template wins. Do not propagate legacy structure.

## Knowledge Verification Chain

For all technical decisions, follow in order: (1) Codebase → (2) Project
docs → (3) Context7 MCP → (4) Web search → (5) Flag or ask. Never skip to
Step 5 if Steps 1-4 are available. **NEVER assume or fabricate** -- follow
the chain or say "I don't know." Referenced by design.md and implement.md
as `../SKILL.md#knowledge-verification-chain`.

## Guidelines

**DO:**

- Separate content by purpose: spec=WHAT, design=HOW, tasks=WHEN
- Follow status flow: draft -> ready -> in-progress -> to-review -> done
- Use sequential Feature IDs (001, 002)
- Reuse research cache across features (.artifacts/research/)
- Consume `.agents/` for project context and codebase info (optional)
- Queue codebase discoveries to `.agents/knowledge.md` Codebase Feedback
- Auto-size depth based on complexity -- skip phases that add no value
- Run verify after each task or range -- never deferred to the end

**DON'T:**

- Reuse Feature IDs from previous features
- Mix spec, design, and task content in a single file
- Skip status transitions (e.g., jumping from draft to done)
- Force full pipeline on small/medium changes -- respect auto-sizing
- Assume or fabricate -- follow Knowledge Verification Chain
- Defer verification to the end -- verify runs per task/range

## Output

Artifacts in `.artifacts/` (excluded via `.git/info/exclude`):

```
.artifacts/features/{ID}-{name}/   spec.md, design.md, tasks.md, decisions.md
.artifacts/quick/NNN-{slug}/       task.md
.artifacts/research/{topic}.md     research cache (reusable across features)
```

Project context (`.agents/` -- not committed):

```
.agents/knowledge.md               cross-feature decisions (spec-driven)
```

Templates in `templates/` define every artifact's canonical structure.

## Error Handling

- No .artifacts/: Create it (subdirs created on demand)
- Spec not found: List available features
- Open questions blocking architecture: Resolve via discuss before planning
- Design not found: Suggest design before tasks (or skip if Medium scope)
- Tasks not found: Suggest tasks before implement (or skip if Medium scope)
- Scope misjudged: Safety valve in implement catches this

## Compact Instructions

Heavy phases write a mid-phase checkpoint to disk before autocompact fires
(design.md Step 9a). If autocompact fires before that checkpoint, preserve:

- Current phase and step number
- Feature ID and path (`.artifacts/features/{ID}-{name}/`)
- Open decisions not yet captured in any artifact
- AC check status (which `[x]` are marked and which are not)
- Session dump path if already written

Drop everything else -- spec.md, design.md, and tasks.md survive autocompact
on disk.
