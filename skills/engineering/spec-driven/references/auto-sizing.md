# Auto-Sizing

Determine pipeline depth from the nature of the change, not its surface
area. Loaded by specify.md Step 1.

## When to Use

Before starting any feature — complexity determines which phases run, not a
fixed pipeline. Apply only the ceremony the scope needs.

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
| **Medium** | Canonical pattern already present in the codebase. The only decision is "reapply pattern X here." No new abstractions. | Spec (brief) | Skip -- explore inline | Skip -- steps implicit | Implement + verify per step |
| **Large** | ≥1 load-bearing decision new to the codebase. A peer reviewer reading the feature description alone could not predict the approach. | Full spec + requirement IDs | Full design | Full breakdown + dependencies | Implement + verify per task |
| **Complex** | Ambiguity in the problem itself. Solution space is open — needs exploration before design can converge. | Full spec + [discuss.md](discuss.md) | Research + full design | Breakdown + parallel design | Implement + verify per task |

## The Reviewer Test

For any candidate Medium vs Large, ask:

> A peer reviewer reads only the feature description. Can they predict
> the files touched and the approach taken?

- **Yes** → Medium. Pattern is canonical, reapplication is mechanical.
- **No** → Large. The gap between description and approach is exactly
  what design.md exists to capture.

Examples:

- Rename `UserService` → `AccountService` across 40 files → **Medium**. Mechanical reapplication, file count is incidental.
- Dark-mode toggle (localStorage + system pref + CSS vars) → **Medium**. Canonical pattern, reviewer predicts it.
- Add "remember me" checkbox to existing login → **Medium**. Pattern known, scope bounded.
- Add role-based access control to an app with no prior auth model → **Large**. Novel decision: where does role live (JWT vs DB lookup), how does the enforcement layer work. Reviewer cannot reconstruct from description.
- Offline-first sync with conflict resolution, no prior CRDT experience → **Complex**. Problem itself is ambiguous (LWW vs CRDT vs event sourcing), new domain.

If you find yourself reaching for design.md because the feature is
"multi-component," pause: multi-component is not the same as multi-decision.
Design.md exists to capture decisions a peer reviewer could not reconstruct
from the spec — if there are no such decisions, design.md is ceremony.

## Rules

- **Specify and Implement are always required** -- you always need to know WHAT and DO it
- **Design is skipped** when no load-bearing decision is new to the codebase (reviewer test passes)
- **Tasks is skipped** when execution is a single canonical pattern with no branching dependencies (steps become implicit in Implement)
- **Discuss is triggered within Specify** only when the agent detects ambiguous gray areas that need user input
- **Verify runs after every task/range** -- checks design adherence, pattern adherence, code correctness (tooling-aware deep analysis), and visual adherence (optional); also marks AC `[x]` in spec.md on pass
- **Audit runs before done** -- validates Goals and Success Criteria against evidence, marks their `[x]`, and transitions `to-review` -> `done`; mandatory for every `.artifacts/features/` feature (Medium/Large/Complex)
- **Validate (UAT) is on-demand** -- user requests it when they want to manually test, any scope; may revert any `[x]` if user reproves
- **Quick mode** is the express lane -- mechanical changes with zero decisions (no audit needed)
- **Verification is continuous** -- quality gates and acceptance criteria run after each task or range, never deferred to the end

## Safety Valve

Even when Tasks is skipped, Implement ALWAYS starts by listing atomic steps
inline (see [implement.md](implement.md)). If that listing surfaces
hidden decisions — branching dependencies, multiple viable approaches per
step, or unknowns that require research — STOP and create a formal
`tasks.md`. The sizing missed a load-bearing decision; correct it before
writing code.
