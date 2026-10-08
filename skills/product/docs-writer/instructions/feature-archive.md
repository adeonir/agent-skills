# Feature Archive

Move feature folders out of `.artifacts/features/` into dated cold storage, with no change to the documents inside.

## When to Use

Only when the user explicitly asks to archive a feature. Never archive automatically and never suggest it. A feature folder may be archived in any document status; archiving changes the folder location only.

## Workflow

```text
list folders → select → resolve date → move → report
```

1. **Select features.** List every folder under `.artifacts/features/`. If none exists, report that there is nothing to archive and stop. Show the list on every run, even when the request names a feature, as a multi-select question with one option per `<feature-slug>` and the H1 title of its `PRD.md`, `RFC.md`, or `audit.md`, in that order, as the description. When the list exceeds the options one question holds, split it across as many questions as needed, and across further calls when the questions exceed what one call holds. Where the host has no multi-select question, print the list as `- [ ] <feature-slug>` lines and take the user's answer. Archive only the features the user selects; when the user selects none, stop.
2. **Resolve the date.** For each selected `<feature-slug>`, take the earliest `created:` from the frontmatter of its `PRD.md` and `RFC.md`. When neither file exists, take the date from the `Date:` line of `audit.md`. When no date is found, ask the user for it.
3. **Move.** Move each `.artifacts/features/<feature-slug>/` whole, with every file in it, to `.artifacts/archive/features/<created>-<feature-slug>/`. Keep every document unchanged, including its status.
4. **Report.** Report only the archive paths the moves created. Make no claim about the documents; the move does not check them.

Never read `.artifacts/archive/features/` when writing a new feature document — archived features are cold storage, not discovery input.
