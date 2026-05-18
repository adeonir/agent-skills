# Refresh Codebase Index

Incrementally patch `.agents/codebase/*.md` from recent git changes, dispatching only the sub-agents whose domain was touched.

## When to Use

- `.agents/codebase/` already exists (baseline created by `initialize`)
- User says "refresh codebase", "sync codebase", "patch index", "update codebase index"
- Branch has progressed past the last sync point and docs may have drifted
- Cheaper alternative to re-running the full fan-out when only part of the tree changed

Not for first-time setup (use `initialize.md`) or for merging manual discoveries (use `integrate-feedback.md`).

## Workflow

### Step 1: Verify Preconditions

- `.agents/codebase/` exists. If missing, exit with "Run initialize first to create the baseline."
- Working tree clean OR user confirms diffing against uncommitted changes. If dirty and not confirmed, ask once before proceeding.
- `git` available and the project is a git repository. If not, exit with "Refresh requires git; use `map codebase` for a full re-run."

### Step 2: Resolve Sync Range

Read `.agents/.sync` (single-line file with the last sync commit SHA).

| State | Action |
|-------|--------|
| File exists, SHA reachable | Diff range = `<sha>..HEAD` |
| File exists, SHA unreachable | Warn, ask user: fall back to `map codebase` or pick a base ref manually |
| File missing | Detect the main branch (`git symbolic-ref refs/remotes/origin/HEAD` → fallback `main`, `master`, `develop` in order), then default to merge-base with it; confirm with user before using |

Compute changed files:

```bash
git diff --name-status <range>
```

Capture additions (`A`), modifications (`M`), deletions (`D`), and renames (`R`). Renames count as a touch on both old and new paths.

### Step 3: Apply Fallback Thresholds

If ANY of the following is true, abort the incremental path and dispatch the full fan-out from SKILL.md instead:

| Threshold | Reason |
|-----------|--------|
| More than 50 files changed | Empirical breakpoint where path-mapping fidelity drops — beyond ~50 unrelated touches, the routing table starts marking nearly every sub-agent, so the savings versus full fan-out disappear |
| More than 20% of tracked source files changed | Catches sweeping refactors that stay under the absolute count (small repos) — proportionally large change sets behave like full re-derivations regardless of file count |
| Entry point file changed (`index.*`, `main.*`, `cmd/**/main.go`, `src/app/**/layout.*`) | Architecture re-derivation needed; entry points anchor the whole structure map and one change ripples to every downstream doc |
| Project manifest replaced or major version bump (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod` semver-major change) | Conventions, integrations, checklist all shift simultaneously; routing each separately is more work than rerunning the whole set |
| Vertical slicing signal flipped (slice dirs added/removed wholesale) | The `features.md` gate must re-evaluate, and that detection lives in initialize, not refresh |

Report the fallback reason to the user before dispatching the full fan-out.

### Step 4: Route Paths to Sub-Agents

For each changed path, mark the sub-agents whose domain it touches. A single path may mark multiple sub-agents.

| Path pattern | Sub-agents to refresh |
|--------------|------------------------|
| Project manifests (`package.json`, `Cargo.toml`, `pyproject.toml`, `go.mod`, `Gemfile`, `pom.xml`, `composer.json`) | conventions, checklist, integrations |
| Lockfiles (`package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, `Cargo.lock`, `poetry.lock`) | (skip — derived) |
| Linter/formatter config (`.eslintrc*`, `.prettierrc*`, `biome.json`, `ruff.toml`, `.editorconfig`) | conventions |
| TS/JS config (`tsconfig*.json`, `vite.config.*`, `next.config.*`, `webpack.config.*`) | conventions, architecture |
| Test files (`**/*.test.*`, `**/*.spec.*`, `__tests__/**`, `tests/**`) | testing |
| Test config (`vitest.config.*`, `jest.config.*`, `playwright.config.*`, `pytest.ini`) | testing, checklist |
| API clients, HTTP wrappers, SDK adapters (`**/api/**`, `**/clients/**`, `**/integrations/**`) | integrations |
| DB models, migrations, schema (`**/models/**`, `**/migrations/**`, `**/schema.*`, `**/prisma/**`, `**/drizzle/**`) | integrations, architecture |
| Env templates (`.env.example`, `.env.template`) | integrations |
| Slice dirs when vertical slicing detected (`features/**`, `modules/**`, `apps/**`, `domains/**`) | features, workflows |
| Route handlers, controllers (`**/routes/**`, `**/controllers/**`, `**/handlers/**`, `**/app/**/route.*`, `**/pages/api/**`) | workflows, architecture |
| Other source under recognized roots (`src/**`, `lib/**`, `pkg/**`, `internal/**`) | architecture, conventions |
| Build scripts, CI (`.github/**`, `Makefile`, `Justfile`, `scripts/**`, `.husky/**`, `lefthook.yml`) | checklist, workflows |
| Docs-only (`README.md`, `docs/**`, `*.md` outside `.agents/`) | (skip) |
| `.agents/**`, `.artifacts/**` | (skip — agent artifacts, never feed back into the index) |

If a changed path matches no rule, log it under "unmatched" in the final report so the user can extend the mapping.

### Step 5: Dispatch Subset Fan-Out

Dispatch the marked sub-agents as **independent Agent calls in the same turn** (parallel), using the same protocol as SKILL.md fan-out. Each sub-agent reads only its domain inputs and merges into its target file under `.agents/codebase/` per `merge-policy.md`.

Pass the diff range and the list of changed paths scoped to that sub-agent's domain in the prompt — sub-agents should focus on the delta, not re-derive the whole file from scratch when an existing version is on disk.

If the marked set is empty, exit with "No codebase docs affected by changes in <range>." Update `.sync` anyway (Step 7).

### Step 6: Re-Run Review

Always run `review.md` after the subset fan-out. Review synthesizes across files and may surface inconsistencies introduced by the patch even when only one sub-agent ran.

### Step 7: Update Sync Marker

Capture `HEAD` SHA with `git rev-parse HEAD`, then write it to `.agents/.sync` using the Write tool (single line). Prefer Write over Bash redirects (`>`, `>>`) — many harnesses gate redirects against project files and route them through the file-creation tool instead.

On first write, also add `.agents/.sync` to `.git/info/exclude` if not already present — the marker is local machine state, not project history:

```bash
grep -qxF '.agents/.sync' .git/info/exclude 2>/dev/null || echo '.agents/.sync' >> .git/info/exclude
```

(Appending to `.git/info/exclude` is a non-project git infrastructure write and is treated separately from project-file creation.)

### Step 8: Report

Show:

- Sync range: `<sha>..HEAD` (N commits, M files changed)
- Refreshed: list of sub-agents that ran
- Skipped (no domain match): K files
- Unmatched paths: list (if any, for mapping gaps)
- Fallback triggered: yes/no (with reason if yes)
- New sync marker: `<new-sha>`

## Guidelines

- Treat the path map as a routing heuristic, not a contract — when in doubt, mark the sub-agent
- Run `review` even on tiny patches; cross-file drift is exactly what review catches
- Never skip the sync marker update, even when no sub-agent ran — empty diffs still advance the baseline
- Keep `.agents/.sync` local; it's machine state, not project history

## Anti-Pattern: Stale Sync Marker

A sync marker that points at a commit no longer reachable (rebased, force-pushed) silently corrupts subsequent refreshes. Always validate the SHA with `git cat-file -e <sha>^{commit}` before computing the diff range; on failure, ask the user for a new base ref instead of silently falling back to `HEAD~1`.

## Anti-Pattern: Cross-Cutting Refactor Slip

Symbol renames or import path rewrites can touch dozens of files without changing any architectural fact. The path map will mark every affected sub-agent, but the actual content shift may be zero. Trust the thresholds in Step 3 to escalate to full fan-out when the change set is broad; do not hand-tune the subset to "just rerun architecture" — the threshold catches what the heuristic cannot.

## Error Handling

- `.agents/codebase/` missing: "Run initialize first."
- Not a git repository: "Refresh requires git; use `map codebase`."
- `.agents/.sync` points at unreachable SHA: warn, ask for fallback base ref or full re-run
- Empty diff in range: skip dispatch, still update sync marker, report "Already in sync."
- Sub-agent failure: report which sub-agent failed, leave its target file untouched, do not advance sync marker
