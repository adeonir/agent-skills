# Validate

Validate the root `DESIGN.md` with the official CLI, semantic contrast checks, and document-surface rules.

## When to Use

Use when the user asks to validate, lint, check, or audit `DESIGN.md`; after design writes; after confirmed preview adjustments; and before export or diff.

## Output

Return one state:

- `clean` — zero CLI errors, zero CLI warnings, and no supplemental error.
- `passed with warnings` — zero CLI errors, one or more CLI or supplemental warnings, and no supplemental error.
- `failed` — one or more CLI or supplemental errors.
- `not audited` — the official CLI could not run.

Warnings prevent `clean` but do not block. Errors and `not audited` block design completion, preview, export, and diff.

## Workflow

1. Confirm that `DESIGN.md` exists at the project root.
2. Run the official CLI in parseable form:

```bash
npx -y @google/design.md@latest lint --format json DESIGN.md
```

3. Parse `findings` and `summary`. Never infer the result from the exit code because warnings do not make the command fail.
4. When validate is the gate inside an authoring workflow, fix structural errors and rerun until `errors: 0`. Stop when a correction changes the identity or needs a user decision. When validate is invoked as an audit, report findings without writing.
5. During an authoring gate, fix warnings when the correction is supported by the source and does not change a confirmed identity decision. Keep deliberate warnings visible. Use `omitted` only for a genuinely absent official group or section.
6. Run the semantic contrast checker:

```bash
python3 <this-skill>/scripts/check-contrast.py DESIGN.md --json
```

7. Require every `<base>` / `<base>-foreground` or `on-<base>` pair to reach 4.5:1. Require `muted-foreground` or `on-muted` against both `background` or `surface` and `card` or `muted` when those tokens exist. Treat an unparseable required pair as an error, never a skip.
8. Load [anti-patterns.md](../references/anti-patterns.md) and run only rules whose Surface is `DESIGN.md` or `both`.
9. Check prose-to-YAML parity:
   - Every token path cited in prose resolves.
   - Every component relationship described in prose agrees with frontmatter.
   - Colors remain flat CSS strings.
   - Every frontmatter key is one the artifact contract allows.
   - All present sections follow the canonical order in [design.md](design.md), reading an official alias as its canonical section.
10. Report initial and final CLI counts, supplemental findings, and the exact final state.

Here is a sensible default format, but use your best judgment:

```text
DESIGN.md validation

CLI: [initial errors/warnings] → [final errors/warnings]
Supplemental: [errors/warnings]
State: clean | passed with warnings | failed | not audited

Errors
- [path] [finding]

Warnings
- [path] [finding]
```

## Boundaries

- Keep standalone validation read-only. A validation gate may patch structural defects inside its parent authoring workflow, but never change the identity without confirmation.
- Do not repeat CLI rules as supplemental rules.
- Do not turn every anti-slop tell into a lint finding.
- Do not call a result with warnings `clean`.
- If Node, `npx`, registry access, or the package is unavailable, report `not audited`; never replace the official gate with the supplemental checks.
