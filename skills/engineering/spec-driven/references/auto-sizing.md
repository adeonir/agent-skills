# Auto-Sizing

Determine pipeline depth from feature complexity. Loaded by specify.md Step 1.

## When to Use

Before starting any feature — complexity determines which phases run, not a
fixed pipeline. Apply only the ceremony the scope needs.

## Complexity Table

| Scope | What | Specify | Design | Tasks | Implement |
|-------|------|---------|--------|-------|-----------|
| **Small** | ≤5 files, one sentence, no user-facing feature | **Quick mode** -- skip pipeline entirely | - | - | - |
| **Medium** | Canonical pattern, ≤10 tasks, no novel architectural decisions | Spec (brief) | Skip -- explore inline | Skip -- steps implicit | Implement + verify per step |
| **Large** | Novel architectural decisions, or >10 tasks, or pattern new to this codebase | Full spec + requirement IDs | Full design | Full breakdown + dependencies | Implement + verify per task |
| **Complex** | Ambiguity in problem itself, or new domain to the user | Full spec + [discuss.md](discuss.md) | Research + full design | Breakdown + parallel design | Implement + verify per task |

## Medium vs Large — Resolving the Gray Zone

Multi-file is not Large. Touching 4-6 files does not upgrade a canonical
pattern to Large -- the count of files is incidental. The question is whether
the feature requires an architectural decision the reader of the spec could
not have predicted from the feature description alone.

- Dark-mode toggle (localStorage + system preference + CSS vars) -- **Medium**. Canonical pattern, no novel decision. Files touched is incidental.
- Add "remember me" checkbox to existing login -- **Medium**. Pattern known, scope bounded.
- Add role-based access control to an app without any prior auth model -- **Large**. Novel decision: where does role live (JWT vs DB lookup), how does enforcement layer work.
- Build offline-first sync with conflict resolution, no prior CRDT experience -- **Complex**. Ambiguity in the problem itself (LWW vs CRDT vs event sourcing), new domain.

If you find yourself reaching for design.md because the feature is
"multi-component," pause: if every file you will touch is an obvious
consequence of the feature description, you are in Medium territory.
Design.md exists to capture decisions a peer reviewer could not reconstruct
from the spec -- if there are no such decisions, design.md is ceremony.

## Rules

- **Specify and Implement are always required** -- you always need to know WHAT and DO it
- **Design is skipped** when the change is straightforward (no architectural decisions, no new patterns)
- **Tasks is skipped** when there are ≤3 obvious steps (they become implicit in Implement)
- **Discuss is triggered within Specify** only when the agent detects ambiguous gray areas that need user input
- **Verify runs after every task/range** -- checks design adherence, pattern adherence, code correctness (tooling-aware deep analysis), and visual adherence (optional); also marks AC `[x]` in spec.md on pass
- **Audit runs before done** -- validates Goals and Success Criteria against evidence, marks their `[x]`, and transitions `to-review` -> `done`; mandatory for every `.artifacts/features/` feature (Medium/Large/Complex)
- **Validate (UAT) is on-demand** -- user requests it when they want to manually test, any scope; may revert any `[x]` if user reproves
- **Quick mode** is the express lane -- for bug fixes, config changes, and small tweaks (no audit needed)
- **Verification is continuous** -- quality gates and acceptance criteria run after each task or range, never deferred to the end

## Safety Valve

Even when Tasks is skipped, Implement ALWAYS starts by listing atomic steps
inline (see [implement.md](implement.md)). If that listing reveals >5 steps
or complex dependencies, STOP and create a formal `tasks.md` -- the Tasks
phase was wrongly skipped.
