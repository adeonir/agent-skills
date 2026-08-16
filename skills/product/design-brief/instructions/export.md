# Export

Export validated DESIGN.md tokens through the official CLI.

## When to Use

Use when the user asks for Tailwind or DTCG output from the root `DESIGN.md`.

## Formats

Allow only:

- `json-tailwind`
- `css-tailwind`
- `tailwind`, the alias for `json-tailwind`
- `dtcg`

## Workflow

1. Load [validate.md](validate.md). Stop on `failed` or `not audited`; allow `clean` and `passed with warnings`, preserving every warning in the report.
2. Resolve the format from the request. Ask when it is missing.
3. Run the official CLI without a separate conversion layer:

```bash
npx -y @google/design.md@latest export DESIGN.md --format <format>
```

4. Return stdout when the user requested output only. If the user expects a file and did not name its path, confirm the destination before writing. Never invent a committed export path.
5. Report the format, destination or stdout, and the validation state.

## Error Handling

- Unsupported format: list the four supported values and stop.
- CLI emitter error: report stderr and do not create a partial file.
- Unreadable input: route to validate.
