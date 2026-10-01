# Official CLI

Command contracts and result handling for the official DESIGN.md tool.

## When to Use

Load for validate, export, diff, or when the installed command behavior is unclear.

## Invocation

Use the registry-resolved package without installing it into the project:

```bash
npx -y @google/design.md@latest <command>
```

On PowerShell, use the dot-free executable alias:

```powershell
npx -y -p @google/design.md designmd <command>
```

If the project already provides the CLI, use its project command instead of adding a dependency.

## Result Rules

- Parse JSON output for lint and diff.
- Lint exit status reflects errors, not warnings. Read `summary.errors` and `summary.warnings`.
- Zero errors with warnings is `passed with warnings`, never `clean`.
- Diff may exit non-zero to signal a regression; parse its JSON before treating the run as failed.
- Export success does not prove the source linted clean; validate first.
- If `npx` cannot run, report the operation as unaudited instead of substituting another linter.
