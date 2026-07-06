# Archive

Move a done feature out of the active `specs/` tree into dated cold storage — housekeeping only, no lifecycle effect.

## When to Use

Only when the user explicitly asks to archive a feature, and only for a spec at `status: done`. Optional and manual — never automatic, never suggested. A done feature that no one archives simply stays in `.artifacts/specs/`; its state is already settled (`status: done` set and `STATE.md` cleared when it reached done), so archiving changes nothing but the folder.

## Workflow

1. **Resolve feature** — the `.artifacts/specs/{slug}/` to archive; confirm `spec.md` is at `status: done` — anything earlier is still in flight and stays. Read `created:` from `spec.md` frontmatter; that date prefixes the archive name.
2. **Move** `.artifacts/specs/{slug}/` to `.artifacts/archive/{created}-{slug}/`.
3. **Keep** `spec.md` at `status: done`.

The agent never reads `.artifacts/archive/` when creating a new spec — archived features are cold storage, not discovery input.
