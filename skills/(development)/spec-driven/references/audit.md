# Audit Feature

Validate Goals and Success Criteria against evidence, mark the corresponding
checkboxes in spec.md, and transition status from `to-review` to `done`.

> **LOAD FIRST:** [status-workflow.md](status-workflow.md) -- required for correct status management

## When to Use

- Feature reached `status: to-review` after implement completed
- User explicitly requests `audit` or `validate goals`
- Before closing a feature -- `done` requires audit

## When to Skip

- Feature is still `in-progress` -- finish implement first
- Feature is already `done` -- re-audit only if requested

## Workflow

### Step 1: Resolve Feature

1. If ID provided -> use `.artifacts/features/{ID}-{name}/`
2. If no ID -> match current git branch to `branch:` in spec.md frontmatter
3. If no match -> list available features and ask user

### Step 2: Pre-Audit Check

Read spec.md frontmatter. If `status` is not `to-review`:

| Current Status | Action |
|----------------|--------|
| `draft`, `ready` | Stop. Inform user implement has not started. |
| `in-progress` | Stop. Inform user to finish implement (which sets `to-review`). |
| `done` | Ask user if they want to re-audit. If yes, proceed. |

### Step 3: Load Audit Targets

Read spec.md and extract every `- [ ]` item under:

- `## Goals`
- `## Success Criteria`

Record each target with its exact line text. These are the only items this
reference may mark -- never touch ACs (verify.md owns those).

### Step 4: Gather Evidence

For each target, collect evidence that it is met. Evidence sources, in order
of preference:

| Evidence Type | Source | When to Use |
|---------------|--------|-------------|
| Automated test | Test files matching the behavior | Goals tied to behavior |
| Metric measurement | Benchmark, profiler, instrumentation output | Success Criteria with numbers ("under 2 minutes", "zero errors") |
| Code inspection | Relevant files from design.md | Goals tied to presence of a capability |
| Manual observation | UAT session notes or user-supplied evidence | Subjective user-facing behavior |

If `.artifacts/features/{ID}-{name}/validate.md` or UAT notes exist, consult
them -- validate may have already confirmed some targets.

### Step 5: Classify Each Target

For each target, mark one of:

- **Met** -- evidence clearly supports the claim
- **Unmet** -- evidence missing or contradicts the claim
- **Unmeasurable** -- target is phrased in a way that cannot be verified (e.g., vague wording)

Report a table:

| Target | Classification | Evidence |
|--------|----------------|----------|
| G1: Users complete onboarding in under 2 minutes | Met | Benchmark: median 87s across 20 runs (see perf report) |
| SC1: Zero errors in payment flow | Unmet | 2 errors observed in integration test run |
| G2: Improve conversion | Unmeasurable | No metric defined -- needs spec update before re-audit |

### Step 6: Update spec.md

For every target classified **Met**:

- Edit spec.md in place, flipping `- [ ]` to `- [x]` on the matching line
- Preserve exact wording and identifier
- Never reorder, rename, or drop items

For **Unmet** targets: leave `- [ ]` unchanged.

For **Unmeasurable** targets: leave `- [ ]` unchanged and report -- the spec
needs a rewrite, not an audit pass.

### Step 7: Determine Outcome

**If every Goal and Success Criterion is Met:**

- Set `status: done` in spec.md frontmatter
- Report "Audit passed. Feature closed."
- Suggest commit for the audit updates (if any checkboxes flipped)

**If any target is Unmet or Unmeasurable:**

- Keep `status: to-review`
- Report the failing targets with evidence gaps
- Suggest next action per category:
  - Unmet -> fix implementation or update tests, then re-run audit
  - Unmeasurable -> update spec.md (via specify) with a verifiable rewrite

### Step 8: Structural Delta Check

Independent of audit outcome. Inform the user when `.agents/codebase/*.md` may
be stale so they can decide whether to refresh it. Never prompt, never block
the status transition.

Run against the feature branch:

```bash
git diff --name-status $(git merge-base main HEAD)..HEAD
```

Flag as structural delta if any of the following is true:

- Any `A` (added), `D` (deleted), `R` (renamed), or `C` (copied) entry outside `.artifacts/`
- `package.json` `dependencies` or `devDependencies` sections changed
- `.env.example` changed
- New directory under `src/app/api/` or equivalent route root (framework-specific)

If any flag fires, append exactly one line to the audit report:

> Structural changes detected -- consider running `/project-index re-index` to refresh `.agents/codebase/*.md`.

If no flag fires, emit no output for this step.

### Step 9: Relationship to Validate

Audit is evidence-based and automated. Validate ([validate.md](validate.md))
is user-observation based and interactive. They do not block each other:

- Audit can run before or after validate
- Audit transitions status to `done`; validate does not
- Validate may revert any `[x]` (AC, Goal, Success Criterion) if the user
  reproves a scenario -- audit must be re-run after such a revert

## Guidelines

**DO:**
- Require evidence for every `[x]` mark -- never flip based on plausibility
- Prefer automated evidence (tests, metrics) over manual observation
- Leave Unmeasurable targets unchecked and flag the spec for rewrite
- Keep audit deterministic -- same evidence yields same classification
- Consult UAT notes if validate ran before audit
- Suggest `/project-index re-index` when structural deltas exist -- inform only, never prompt

**DON'T:**
- Touch AC checkboxes or status tags -- those belong to verify.md
- Set `status: done` if any Goal or Success Criterion is Unmet or Unmeasurable
- Rewrite Goals or Success Criteria during audit -- route to specify instead
- Assume Met because the code exists -- check the observable outcome

## Error Handling

- Status is not `to-review`: follow Step 2 table
- No Goals or Success Criteria in spec.md: inform user spec is incomplete, suggest specify
- All targets Unmeasurable: stop, tell user the spec needs rewritten Goals/Success Criteria with verifiable wording
- Evidence source unavailable (no tests, no metrics): report gap, suggest adding the missing evidence before re-audit
- Conflicting evidence between automated and manual sources: report both, ask user to adjudicate
