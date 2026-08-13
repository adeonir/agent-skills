# Archive

Move a feature out of the active `specs/` tree into dated cold storage — housekeeping only, no lifecycle effect.

## When to Use

Only when the user explicitly asks to archive a feature. Optional and manual — never automatic or suggested. The feature may be in any artifact state. Archiving changes the folder only; it does not change artifact states or the feature's `STATE.md`.

## Workflow

1. **Resolve feature** — the `.artifacts/specs/<slug>/` to archive. Read `created:` from `spec.md` frontmatter; that date prefixes the archive name.
2. **Move** `.artifacts/specs/<slug>/` to `.artifacts/archive/<created>-<slug>/`.
3. **Keep** every artifact, including `STATE.md`, unchanged.

The agent never reads `.artifacts/archive/` when creating a new spec — archived features are cold storage, not discovery input.
