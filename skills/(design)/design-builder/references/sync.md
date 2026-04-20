# Sync

Propagate changes from derivative artifacts back to the source of truth
(`design.json` + `structure.md`).

## When to Use

- User iterated in `design.pen` (Pencil MCP) and wants to persist changes in tokens and structure
- Implementation (usually under `spec-driven`) adjusted tokens or structural decisions during build
- Agent notices that a derivative diverged from source artifacts and suggests reconciling

Source artifacts are greenfield-first outputs of this skill. Sync is the
operation that keeps them current as derivatives evolve.

## Source of Truth

`design.json` and `structure.md` are authoritative. Everything else is a
derivative:

- `design.pen` — iteration surface. Optional. Present only when the user
  adopted Pencil MCP during structure or preview
- implementation code (components, Tailwind config, tokens files, routing) —
  consumes the source and may adjust during build

Derivatives drift. Sync reconciles them back to source without flipping the
ownership.

## Prerequisites

- `design.json` in `.artifacts/design/`
- `structure.md` in `.artifacts/design/`
- At least one derivative to read from (design.pen or implementation code)

If no derivative exists, there is nothing to sync.

## Workflow

### Step 1: Detect Derivatives

Check what exists:

- `.artifacts/design/design.pen` (Pencil file, optional)
- Implementation code in the project under sync (component files, Tailwind
  config, tokens file, global CSS, routing config)

Report findings. Exit early if nothing was found.

### Step 2: Ask User What to Sync

Present options based on what was detected:

- Sync from `design.pen` only
- Sync from implementation only
- Sync from both, resolving conflicts per field

### Step 3: Read Derivative State

**From `design.pen`:**

Use Pencil MCP `batch_get` to read the file. Extract:

- Updated colors, typography, spacing, shadow, radius values
- Component style changes (button, card, input, badge)
- Structural adjustments (section order, new or removed sections,
  hero composition changes)

**From implementation:**

Read relevant files — ask user to confirm paths if ambiguous:

- Tailwind config (`tailwind.config.{js,ts,mjs}`)
- Design tokens file (`tokens.json`, `tokens.css`, `theme.ts`)
- Global CSS with custom properties (`globals.css`, `app.css`)
- Component variant definitions (shadcn, cva, stitches, styled-components themes)
- Router or navigation config (screen names, order, grouping)

Extract the current state of tokens and structural decisions.

### Step 4: Diff Against Source

Compare derivative state with `design.json` + `structure.md`. Group findings:

- Token diffs (value changes, additions, removals)
- Component style diffs (per component and state)
- Structural diffs (section order, missing or extra sections, layout changes)

Present the diff as a report. Do not write anything yet.

### Step 5: Resolve Conflicts

When syncing from both derivatives and they disagree, for each field:

- Show value from `design.pen`
- Show value from implementation
- Ask which wins (design.pen, implementation, or a custom value)

Record the resolution. Never pick silently.

### Step 6: Apply Changes

Update `design.json` and `structure.md` with the resolved state. Preserve
everything the derivatives did not touch — only rewrite changed fields.

Save. Confirm what changed.

### Step 7: Suggest Downstream Actions

- If a preview was approved before sync, suggest regenerating it so the visual
  reference matches updated tokens
- If implementation is in progress, note that the updated tokens will show up
  in the next build
- If a handoff was produced earlier, suggest regenerating it if the consumer
  has not started

## Guidelines

**DO:**
- Treat `design.json` and `structure.md` as authoritative — nothing else overrides silently
- Let the user trigger sync explicitly — suggest when a diff is detected, never start automatically
- Ask the user per-conflict when derivatives disagree
- Offer each available derivative as an explicit source option, even when only one has changed
- Report what changed after sync so the user can decide if downstream artifacts need regeneration
- Only rewrite fields that actually changed — preserve everything else

**DON'T:**
- Auto-run sync based on file timestamps (contrasts: let the user trigger sync explicitly)
- Merge derivatives without asking on conflicts (contrasts: ask per-conflict)
- Rewrite whole files when only a few fields changed (contrasts: preserve unchanged fields)
- Sync from one derivative and silently discard the other (contrasts: offer each available derivative as an explicit source option)

## Error Handling

- No `design.json`: nothing to sync to. Suggest running extract design first
- No `structure.md`: partial sync is possible (tokens only). Suggest running structure after
- No derivatives detected: report "nothing to sync" and exit
- `design.pen` format unexpected: ask the user to describe the changes textually
- Implementation scattered across many files: scope to the ones the user points at

## Next Steps

After sync, suggest:

- "Run preview to regenerate the visual with updated tokens"
- "Run handoff if you need to repackage for the implementer"
