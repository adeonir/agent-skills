# Export

Export validated DESIGN.md tokens through the official CLI.

## Load first

Read [discovery.md](../references/discovery.md) before starting — it settles the available context, the field, the brownfield intent, and the surfaces and register this operation must respect. Load [cli.md](../references/cli.md) for the command surface.

## Formats

Allow only:

- `json-tailwind`
- `css-tailwind`
- `tailwind`, the alias for `json-tailwind`
- `dtcg`
- `css-vars`, accepts an optional `--prefix`

## Workflow

1. Load [validate.md](validate.md). Stop on `failed` or `not audited`; allow `clean` and `passed with warnings`, preserving every warning in the report.
2. Resolve the format from the request. Ask when it is missing. For `css-vars`, resolve a `--prefix` only when the user names one.
3. Run the official CLI without a separate conversion layer:

```bash
npx -y @google/design.md@latest export DESIGN.md --format <format>
```

For `css-vars` with a named prefix:

```bash
npx -y @google/design.md@latest export DESIGN.md --format css-vars --prefix <prefix>
```

4. Return stdout when the user requested output only. If the user expects a file and did not name its path, confirm the destination before writing. Never invent a committed export path.
5. Report the format, destination or stdout, and the validation state.

## Error Handling

- Unsupported format: list the five supported values and stop.
- CLI emitter error: report stderr and do not create a partial file.
- Unreadable input: route to validate.
