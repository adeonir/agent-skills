---
name: spec-driven
description: >-
  Specification-driven feature development with auto-sized depth.
  Produces spec.md, design.md, and tasks.md artifacts with requirements
  traceability, plus verify and audit phases tied to acceptance
  criteria. Use when planning a feature, breaking a change into tasks
  or stories, implementing a named story or task, verifying
  implementation against acceptance criteria, auditing goals before
  closing, or turning a PRD into engineering artifacts. Triggers: "plan
  this feature", "spec this feature", "turn this PRD into a spec",
  "break this into tasks/stories", "create technical design",
  "implement story S-1", "implement task T-1", "verify
  implementation", "check acceptance criteria", "audit feature",
  "audit this spec", "validate goals", "UAT", "manual testing",
  "discuss this feature", "show feature status", "quick fix", "quick
  task", "quick mode", "small change", and known one-line fixes where
  the user names file and line. Not for diagnosing unknown bugs,
  authoring standalone PRD/RFC/ADR/TDD documents, PR/commit mechanics,
  or PM backlog tracking.
---

# Spec-Driven Development

Structured development workflow with adaptive depth.

## Workflow

```
specify --> design* --> tasks* --> implement --> verify --> audit --> done
  ^______________________________________|  (verify after each task)
```

Adaptive: Specify and Implement always run. Design and Tasks auto-skip
when scope is small enough. Verify runs after every task or range.

## Triggers

### Feature-level (auto-sized)

- **New feature** ("create new feature", "specify feature", "from PRD",
  "modify feature") → [specify.md](references/specify.md)
- **Discuss / capture context** ("discuss feature", "how should this
  work") → [discuss.md](references/discuss.md)
- **Technical design** ("create technical design", "plan feature") →
  [design.md](references/design.md)
- **Research technology** ("research", "cache research") →
  [research.md](references/research.md)
- **Tasks** ("create tasks") → [tasks.md](references/tasks.md)
- **Implement** ("implement task", "execute task", "implement story
  S-1", "implement task T-1") → [implement.md](references/implement.md)
- **Verify** ("verify implementation", "check adherence", "verify
  code") → [verify.md](references/verify.md)
- **Audit** ("audit feature", "validate goals", "audit goals and
  success criteria") → [audit.md](references/audit.md)
- **UAT / manual testing** ("validate", "UAT", "manual testing", "test
  manually") → [validate.md](references/validate.md)
- **Quick mode** ("quick fix", "quick task", "small change", "bug
  fix") → [quick-mode.md](references/quick-mode.md)
- **Status overview** ("list features", "show status") →
  [status-specs.md](references/status-specs.md)

### Methodological refs (loaded by other refs)

- **Sub-agent dispatch protocol** →
  [phases.md](references/phases.md)
- **Codebase exploration** →
  [codebase-exploration.md](references/codebase-exploration.md)
- **Coding principles** →
  [coding-principles.md](references/coding-principles.md)
- **Status workflow** ("when to update status") →
  [status-workflow.md](references/status-workflow.md)
- **Knowledge / Codebase Feedback format** →
  [knowledge.md](references/knowledge.md)
- **Auto-sizing scope assessment** →
  [auto-sizing.md](references/auto-sizing.md) (loaded by `specify.md` Step 1)
- **Discovery topics** →
  [discovery.md](references/discovery.md) (loaded by `specify.md` Step 7)
- **Code-correctness analysis** →
  [code-correctness.md](references/code-correctness.md) (loaded by
  `verify.md` Step 5)

## Knowledge Verification Chain

For all technical decisions, follow in order:

1. Codebase
2. Project docs
3. Context7 MCP
4. Web search
5. Flag or ask

Never skip to step 5 if steps 1-4 are available. **Never assume or
fabricate** — follow the chain or say "I don't know."

## Artifact Structure Authority

Every artifact's structure is canonical in the matching reference (each
ref carries its template inline, 1:1). Load the relevant reference
before reading any existing artifact in `.artifacts/` — existing files
are context, not structural reference. When structure diverges from the
template, template wins. Do not propagate legacy structure.

## Guidelines

- Separate content by purpose: spec = WHAT, design = HOW, tasks = WHEN
- Follow status flow: `draft → ready → in-progress → to-review → done`
- Use sequential Feature IDs (`001`, `002`); never reuse
- Reuse research cache across features (`.artifacts/research/`)
- Auto-size depth based on complexity — skip phases that add no value
- Run verify after each task or range — never deferred to the end

## Anti-Pattern: Forced Full Pipeline

Forcing every change through specify → design → tasks → implement on
small or medium scopes is process tax. Auto-sizing exists for a reason:
small fixes go through `quick-mode.md`, medium scopes skip design and
tasks, large/complex scopes get the full pipeline. Respect the sizing
decision.

## Anti-Pattern: Deferred Verification

Implementing all tasks first and verifying at the end loses traceability
between implementation and acceptance criteria. Verify after every task
or range — `verify.md` is part of the loop, not a final phase. Failed
verification reverts checked AC and reopens the relevant tasks.

## Anti-Pattern: Knowledge Skipping

Jumping to "I'll guess based on dependency name" or "let me web-search
that" without exhausting steps 1-4 of the Knowledge Verification Chain
produces fabricated patterns that don't match the codebase. Read the
codebase first, then project docs, then Context7 MCP, then web. Only
flag or ask after the chain is exhausted.
