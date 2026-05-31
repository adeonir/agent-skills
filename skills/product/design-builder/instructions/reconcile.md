# Reconcile

Patch `DESIGN.md` back from a drifted implementation. Brownfield-only: when the running code's tokens or component variants no longer match the authored design, this reference diffs the implementation against DESIGN.md and applies surgical patches. Content drift in `copy.yaml` is out of scope here — this reconciles `DESIGN.md` only.

## When to Use

- Implementation drifted from `docs/design/DESIGN.md` after handoff (color shifted to pass contrast, spacing tightened to fit a viewport, a new component variant added that was not anticipated)
- User says "sync design from implementation", "update DESIGN.md from code", "reconcile drift", or "refresh design tokens from this codebase" when DESIGN.md already exists
- Pre-handoff audit before treating DESIGN.md as authoritative for a new feature

Not for: authoring DESIGN.md from scratch or restyling it from a new external reference / vibe (use [design-brief.md](design-brief.md)).

## Prerequisites

- `docs/design/DESIGN.md` exists. If absent, this is not reconciliation — route to [design-brief.md](design-brief.md) to author the design first.
- Codebase path or live URL available as the implementation source.

## Workflow

> Before writing artifacts, ensure `.artifacts` is excluded locally: `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

### Step 1: Read Current Design

Parse the YAML frontmatter of `docs/design/DESIGN.md` as the authored state.

### Step 2: Extract Implementation State

Detect and read in this order (same detection chain as design-brief.md Step 2 Codebase source):

- Tailwind theme — `@theme` directive in CSS files (`globals.css`, `app.css`)
- Design token files (`tokens.json`, `design-tokens.json`, `theme.ts`, `theme.js`) — structured token definitions
- Global CSS with custom properties (`globals.css`, `app.css`, `tokens.css`) — CSS variables for colors, spacing, typography
- Component libraries (shadcn under `components/ui`, cva variants, styled-components themes) — component styles and states
- Font imports in layout or root files — active font families

If multiple sources overlap, ask the user which is authoritative.

### Step 3: Diff

Per frontmatter group (`colors`, `typography`, `rounded`, `spacing`, `components`, `elevation`, `duration`, `easing`, `breakpoints`), list tokens that changed, were added, or are missing in the implementation.

Emit one structured diff for DESIGN.md.

### Step 4: Confirm Before Write

Present the diff inline. User approves, rejects, or edits each patch row. No silent writes. If the user rejects every row, stop with `no patches applied`.

### Step 5: Patch DESIGN.md Surgically

Patch the YAML frontmatter first (authoritative), then patch the prose bullets in Sections 2, 3, 4, 5, 6, 7, 8 that cite the patched tokens, so prose mirrors the frontmatter.

Leave narrative sections (`## 1. Visual Theme & Atmosphere`, `## 10. Do's and Don'ts`, `## 11. Agent Prompt Guide`, `## 9. Responsive Behavior`) untouched. Flag them as potentially stale relative to the new tokens; recommend re-running [design-brief.md](design-brief.md) if narrative refresh is wanted.

### Step 6: Validate

Run [validate.md](validate.md) against the patched DESIGN.md as the gate. Do not declare done with `errors > 0`. Surface validation findings to the user; let them fix or accept trade-offs.

## Guidelines

**DO:**

- Treat the implementation as authoritative for drifted values only after the user confirms each patch row
- Patch YAML frontmatter before prose bullets so the two layers stay in sync
- Preserve narrative sections; flag staleness, do not rewrite
- Run validate as the gate after patching, same pattern as design-brief.md Step 5

**DON'T:**

- Patch silently (contrasts: confirm-before-write per row)
- Rewrite narrative sections (contrasts: only token-citing bullets follow the patched YAML)
- Run from scratch when DESIGN.md is missing (contrasts: this is reconciliation, not authoring — route to design-brief.md)
- Touch `docs/design/structure.md` (contrasts: structure is owned by its own reference)
- Import a new visual direction from the implementation (contrasts: implementation reflects accepted drift, not a fresh identity — use design-brief.md for that)

## Error Handling

- DESIGN.md missing: stop and route the user to [design-brief.md](design-brief.md) to author one
- Implementation source unreadable (codebase path missing, MCP down for design-tool fallback): ask user to re-supply or provide a live URL fallback
- Codebase partially defines tokens: report what is present, ask user how to treat missing groups (keep DESIGN.md value or mark as gap)
- Diff is empty across all groups: report `no drift detected` and stop
- User rejects every patch row: leave files untouched, report what was rejected so the user can revisit later
- Validation gate fails after patching: surface findings; user fixes via re-run, edits DESIGN.md manually, or accepts as trade-off
