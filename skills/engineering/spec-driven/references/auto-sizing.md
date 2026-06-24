# Auto-Sizing

Determine pipeline depth from the nature of the change, not its surface
area. Loaded by specify.md Step 1.

## When to Use

Before starting any feature — complexity determines the *depth* of each
phase, not whether it runs. Above Small, every phase runs; apply only the
depth the scope needs.

## Sizing Criterion

Sizing answers one question: **how many load-bearing decisions does this
change require, and are any of them novel to the codebase?**

File count, task count, and component count are consequences of that
answer — not inputs to it. A rename touching 40 files is mechanical
(Small/Medium). Introducing role-based auth touching 3 files is Large.
Counting files first inverts cause and effect.

## Complexity Table

| Scope | Nature of change | Specify | Design | Tasks | Implement |
|-------|------------------|---------|--------|-------|-----------|
| **Small** | Mechanical. Zero decisions. Outcome obvious from the description (typo, config swap, named bug + line, rename with no behavior change, dep bump with no API change). | **Quick mode** -- skip pipeline entirely | - | - | - |
| **Medium** | Canonical pattern already present in the codebase. The only decision is "reapply pattern X here." No new abstractions. | Spec (brief) | Light design | Light -- flat steps | Implement + verify per task |
| **Large** | ≥1 load-bearing decision new to the codebase. A peer reviewer reading the feature description alone could not predict the approach. | Full spec + requirement IDs | Full design + Plan dispatch | Full breakdown + dependencies | Implement + verify per task |
| **Complex** | Ambiguity in the problem itself. Solution space is open — needs exploration before design can converge. | Full spec + [discuss.md](discuss.md) | Research + full design | Breakdown + parallel design | Implement + verify per task |

## Depth Scaling

Above Small, Design and Tasks always run; depth scales with scope.

**Medium design — light.** Captures Scope, Decisions (with Source and Scope),
Patterns & Reuse, Subsystem Presence claims, Component Design, and Requirements
Traceability. Runs inline (no Plan dispatch). Omits full member enumeration,
Reused Component / Utility Contracts, Cross-Task Value Trace, and the Dependency
Inversion check.

**Large/Complex design — full.** Adds full member enumeration, contracts,
Cross-Task Value Trace, dependency inversion, and Plan-subagent dispatch.

**Medium tasks — light.** A flat task list (Done-when + Satisfaction sketch),
Quality Gates, and Requirements Coverage. Runs inline. Omits the execution-plan
diagram and Plan dispatch.

**Large/Complex tasks — full.** Adds the dependency graph and execution plan.

## The Reviewer Test

For any candidate Medium vs Large, ask:

> A peer reviewer reads only the feature description. Can they predict
> the files touched and the approach taken?

- **Yes** → Medium. Pattern is canonical; design and tasks run light.
- **No** → Large. Design and tasks run full.

Examples:

- Rename `UserService` → `AccountService` across 40 files → **Medium**. Mechanical reapplication, file count is incidental.
- Dark-mode toggle (persisted preference + system default + theme variables) → **Medium**. Canonical pattern, reviewer predicts it.
- Add "remember me" checkbox to existing login → **Medium**. Pattern known, scope bounded.
- Add role-based access control to an app with no prior auth model → **Large**. Novel decision: where does role live (JWT vs DB lookup), how does the enforcement layer work. Reviewer cannot reconstruct from description.
- Offline-first sync with conflict resolution, no prior CRDT experience → **Complex**. Problem itself is ambiguous (LWW vs CRDT vs event sourcing), new domain.

Multi-component is not multi-decision: a multi-component change with no novel
decision is Medium (light design), not Large. Use full depth only when a
decision is novel to the codebase.

## Rules

- **Specify and Implement are always required** -- you always need to know WHAT and DO it
- **Design depth scales** -- Medium runs a light design, Large/Complex the full design with Plan dispatch (see Depth Scaling). Never skipped above Small.
- **Tasks depth scales** -- Medium runs a flat step list, Large/Complex the full breakdown with dependency graph. Never skipped above Small.
- **Discuss is triggered within Specify** only when the agent detects ambiguous gray areas that need user input
- **Verify runs after every task/range** -- checks design adherence, pattern adherence, code correctness (tooling-aware deep analysis), and visual adherence (optional); also marks AC `[x]` in spec.md on pass
- **Audit runs before done** -- validates Goals and Success Criteria against evidence, marks their `[x]`, and transitions `to-review` -> `done`; mandatory for every `.artifacts/specs/` feature (Medium/Large/Complex)
- **Validate (UAT) is on-demand** -- user requests it when they want to manually test, any scope; may revert any `[x]` if user reproves
- **Quick mode** is the express lane -- mechanical changes with zero decisions (no audit needed)
- **Verification is continuous** -- quality gates and acceptance criteria run after each task or range, never deferred to the end

## Safety Valve

If the light Medium design surfaces a load-bearing decision novel to the
codebase — branching dependencies, multiple viable approaches, or unknowns
that need real research — STOP and escalate Medium → Large: run the full
design (with Plan dispatch) and the full tasks breakdown. The sizing
underestimated the change; correct it at design time, before writing code —
never paper over it during implement.
