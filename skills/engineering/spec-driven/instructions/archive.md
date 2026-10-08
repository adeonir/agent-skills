# Archive

Move a feature out of the active `specs/` tree into dated cold storage — housekeeping only, no lifecycle effect.

## When to Use

Only when the user explicitly asks to archive a feature. Optional and manual — never automatic or suggested. The feature may be in any artifact state. Archiving changes the folder only; it does not change artifact states or the feature's `STATE.md`.

## Workflow

1. **Select features.** List every folder under `.artifacts/specs/`. If none exists, report that there is nothing to archive and stop. Show the list on every run, even when the request names a feature, as a multi-select question with one option per `<slug>` and the `# Feature:` title of its `spec.md` as the description. When the list exceeds the options one question holds, split it across as many questions as needed, and across further calls when the questions exceed what one call holds. Where the host has no multi-select question, print the list as `- [ ] <slug>` lines and take the user's answer. Archive only the features the user selects; when the user selects none, stop.
2. **Resolve each feature.** For each selected `<slug>`, read `created:` from the `spec.md` frontmatter; that date prefixes the archive name.
3. **Move.** Move each `.artifacts/specs/<slug>/` to `.artifacts/archive/specs/<created>-<slug>/`.
4. **Keep.** Keep every artifact, including `STATE.md`, unchanged.
5. **Report.** Report only the archive paths the moves created. Make no claim about the artifacts or `STATE.md`; the move does not check them.

The agent never reads `.artifacts/archive/specs/` when creating a new spec — archived features are cold storage, not discovery input.
