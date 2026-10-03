# Spec-Driven Development

Spec-driven feature development. Light by default; weight only where the change pays for it.

## What It Does

Builds features in phases. A mechanical fix is a one-liner; anything larger runs a full pipeline where each artifact closes on its own self-check plus a linter, and the delivery answers to a final independent audit that reads the diff and the tests against the contract.

```mermaid
flowchart TD
    A[Specify<br/>triage, then self-check + linter] --> B{Load-bearing decision?}
    B -->|none| S[Inline implement<br/>own branch, no spec]
    B -->|one or more| D[Design<br/>self-check + linter]
    D --> T[Tasks<br/>linted + self-checked]
    T --> I[Implement<br/>verify per task]
    I --> V{Validate?}
    V -->|user-facing and selected| VA[Validate / UAT]
    V -->|skip| AD{Audit?}
    VA --> AD
    AD -->|selected| AU[Audit<br/>independent subagent]
```

| Phase | Output |
|-------|--------|
| **Specify** | `spec.md` — WHAT + WHY |
| **Design** | `design.md` — HOW: architecture, components, decisions |
| **Tasks** | `tasks.md` — WHEN: atomic steps, tests, gates, coverage |
| **Implement** | code + commits + updated `tasks.md` (verify per task) |
| **Validate / UAT** | `validate.md` — per-criterion browser verdicts, accessibility, and responsiveness on a user-facing feature |
| **Audit** | `audit.md` — Goals, ACs, discrimination sensor, spec-defect findings |
| **Archive** | feature moved to `.artifacts/archive/specs/<created>-<slug>/` (optional and manual, any state) |

### Triage

| Change | Pipeline |
|--------|----------|
| Mechanical, zero load-bearing decisions | one-liner → branch → inline implement |
| Everything else | Specify → Design → Tasks → Implement → [Validate] → [Audit] |

Depth inside the phases follows what the change needs — how far discovery probes, whether design has to research. The agent judges that depth as the work runs; nothing fixes it in advance.

## Usage

```text
# Specify a feature (greenfield or brownfield)
plan a feature for user authentication
from PRD @docs/payment-prd.md
modify the existing auth flow to add 2FA

# Move through the pipeline
design this feature
create tasks
implement T-1 to T-4
implement S-1
implement W-1
implement W-1..W-3 in parallel
implement everything

# Close it out
audit feature
run UAT                 # user-facing only

```

## Output

```text
PROJECT.md                         # committed codebase knowledge
.artifacts/
├── specs/
│   └── <slug>/                    # one folder per feature
│       ├── spec.md                # WHAT + WHY
│       ├── STATE.md               # feature state and report routing
│       ├── design.md              # HOW
│       ├── tasks.md               # WHEN
│       ├── audit.md               # independent audit report
│       ├── validate.md            # optional user-facing validation report
│       └── evidences/             # UAT screenshots (user-facing only)
├── research/
│   └── <topic>.md                 # research cache (reusable)
└── archive/
    └── specs/
        └── <created>-<slug>/      # closed specs; date from `created:`, added at archive; never read during discovery
```

## Requirements

- An existing project directory.
- `python3` (standard library only) for `scripts/lint_artifact.py` and `scripts/select_tasks.py`.
- Optional: a browser-automation MCP (e.g. Playwright) for Validate/UAT screenshots — falls back to user-guided capture when absent.
- Optional: a docs MCP (e.g. Context7) for design research — the knowledge chain falls through to web search when absent.

## FAQ

**Q: What does spec-driven persist across features?**

A: `PROJECT.md` at the project root accumulates cross-feature stakes, conventions, decisions, and gotchas. `archive/` is never foraged.

**Q: When does a change skip the pipeline?**

A: When it is mechanical, with zero load-bearing decisions. It runs as a one-liner straight to inline implement on its own branch, with no `spec.md` and no audit. If it turns out to carry a real decision, it routes back to specify and the full pipeline applies.

**Q: What is the difference between self-check, verify, audit, and validate?**

A: Self-check closes each artifact before its approval gate: the phase reads its own output for what no script can settle, then runs the linter over the text that reading produced, and an error keeps the artifact at `draft`. No artifact gets a second subagent over the same text — that reads the same rules twice and buys a second pass rather than a second view. Verify is mental and internal to implement — it runs after each task and never appears as a user phase. Validate is an optional user-facing check: it exercises every acceptance criterion a running application can settle, checks accessibility and responsiveness on the screens it visits, and writes `validate.md`. Audit is an optional independent check: a fresh subagent (author ≠ auditor) verifies Goals and ACs against the diff and tests, and writes `audit.md`. A criterion no reading of code or test can settle takes the verdict `validate.md` recorded for it, and fails the run where that report carries none. When both phases run, validate runs first. A failed report sets the feature's `STATE.md` routing field, and `Phase` names who reads it: `tasks` turns verified findings into correction tasks that `implement` executes, and `specify` takes back what needs the contract itself corrected.

**Q: How are tasks ordered and dispatched?**

A: `Depends on` is the only ordering source. An edge exists where the dependent task cannot leave the tree green without the other, and where two tasks write the same file — those never run in parallel. `Sequence` derives graph waves and lists every task once. Implement accepts task, slice, and wave selectors; sequential mode is the default and uses the current worktree. Parallel mode is optional and creates one worktree per dispatch unit, not per task. A wave can always run sequentially without a worktree.

**Q: What happens after implementation and optional checks?**

A: Pull request and merge happen outside this skill. The optional archive command is manual and accepts a feature in any state; it moves the feature from `.artifacts/specs/<slug>/` to `.artifacts/archive/specs/<created>-<slug>/` (the date comes from the spec's `created:`, added only at archive). The agent never reads `archive/specs/` when creating a new spec.
