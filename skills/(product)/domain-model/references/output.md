# Output

Produce the domain artifact and hand off to the next skill.

## When to Use

Load after all BR-xxx rules are assigned and the quality gate passes.

> Before writing artifacts, ensure `.artifacts` is excluded locally:
> `grep -qxF '.artifacts' .git/info/exclude 2>/dev/null || echo '.artifacts' >> .git/info/exclude`

## Artifact

Save to `.artifacts/docs/domain.md`. Create the directory if it does
not exist.

**USE TEMPLATE:** `../templates/domain.md`

## Update Mode

When running in update mode (triggered by domain gaps from spec-driven):

1. Read `.agents/knowledge.md` `## Domain Gaps` section
2. For each gap entry, update the relevant entity or rule in the artifact
3. Append each processed gap to `## Processed Gaps` in `domain.md`
4. Clear processed rows from `knowledge.md ## Domain Gaps`

This follows the same pattern as project-index consuming
`## Codebase Feedback`. The queue lives in `knowledge.md`; the artifact
holds the historical record.

Note: `knowledge.md ## Domain Gaps` section does not exist yet — it will
be added in a follow-up upgrade. Document the integration point here so
update mode has a clear target when that section lands.

## Handoff

After saving, ask directly:

> "Domain model saved to `.artifacts/docs/domain.md`. What's next?
> - **system-design** — bounded contexts inform service boundaries
> - **spec-driven** — entities and rules become implementation contracts
> - **epic-tracker** — entity lifecycle states can scope story definition
> - **Nothing for now** — model is enough"

## Quality Gate

Before presenting the artifact:

- [ ] All sections complete (no empty sections)
- [ ] Every entity has at least one invariant
- [ ] Every BR-xxx appears in exactly one lifecycle assignment
- [ ] Bounded context map is present
- [ ] No implementation concepts (table names, column types, ORM models)

## Error Handling

- `.artifacts/docs/` does not exist: create it before saving
- User wants to add an entity after output: return to `entities.md`,
  propagate through `relationships.md` and `rules.md` before regenerating
- Update mode — `## Domain Gaps` not found in knowledge.md: note the
  section does not exist yet; ask user to describe the gap directly
