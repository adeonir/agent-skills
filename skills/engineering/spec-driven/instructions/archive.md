# Archive

Move a merged feature out of the active `specs/` tree into dated cold storage.

## When to Use

Only when the user explicitly asks to archive a feature, and only after its PR has merged. Optional and manual — the skill never observes the merge event, so it never runs this automatically and never suggests it. A done feature that no one archives simply stays in `.artifacts/specs/`.

## Workflow

1. **Resolve feature** — the active `.artifacts/specs/{slug}/`. Read `created:` from `spec.md` frontmatter; that date prefixes the archive name.
2. **Move** `.artifacts/specs/{slug}/` to `.artifacts/archive/{created}-{slug}/`. The date lands here, at archive time — the active folder never carried it, so same-day features never share a redundant prefix while in flight.
3. **Clear** `.artifacts/STATE.md ## Progress` — the feature is no longer active.
4. **Keep** `spec.md` at `status: done`.

The agent never reads `.artifacts/archive/` when creating a new spec — archived features are cold storage, not discovery input.
