# Diff

Compare two DESIGN.md files through the official CLI.

## Load first

Read [discovery.md](../references/discovery.md) before starting — it settles the available context, the field, the brownfield intent, and the surfaces and register this operation must respect. Load [cli.md](../references/cli.md) for the command surface.

## Workflow

1. Resolve the before and after file paths from the request. Ask only for a missing path.
2. Validate both files with [validate.md](validate.md). Stop when either result is `failed` or `not audited`; allow warnings and carry them into the report.
3. Run:

```bash
npx -y @google/design.md@latest diff --format json <before> <after>
```

4. Parse the report and present:
   - Tokens added, removed, and modified by official group.
   - Finding counts before and after.
   - Error or warning regressions.
   - The CLI regression flag.
5. Keep the operation read-only. Do not implement a separate diff algorithm or patch either file.

## Error Handling

- Missing or unreadable file: name the path and stop.
- CLI regression exit: parse and report the JSON; a regression exit is a finding, not a command failure.
- Malformed report: return stderr and mark the comparison incomplete.
