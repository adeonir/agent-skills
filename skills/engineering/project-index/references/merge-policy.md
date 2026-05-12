# Merge Policy

Rules every fan-out ref follows when re-run finds an existing `.agents/codebase/*.md`. Read this when refreshing any doc or when the user asks why something survived (or did not survive) a re-scan.

## When to Use

- Re-running `initialize`, `summary`, or any single-doc refresh
- Author wants to understand which sections are owned by the agent versus the human
- Resolving conflicts between current source state and existing doc content

## Principles

1. **Source is authoritative**: code state on disk wins over any sentence in the doc that contradicts it.
2. **Human prose survives**: free-form sentences and bullet text added by a human are preserved when the surrounding section still has structural reason to exist.
3. **Auto-generated tables refresh**: structured data (tables, file lists, route maps) is regenerated from current source.
4. **Stale references flagged, not deleted silently**: a file path no longer present is marked stale before removal.
5. **Frontmatter is mechanical**: `updated`, `sources` refresh every run; `created`, `name`, `status` preserved unless explicitly changed.

## Per-Section Behavior

| Section type | Behavior on re-run |
|--------------|--------------------|
| Tables (entry points, routes, services, env vars) | **Replaced** from current source |
| Code snippets with `Source: <path>` | **Replaced** when source file still exists; **flagged stale** when source deleted |
| Mermaid diagrams | **Replaced** from current source |
| Prose paragraphs (without `Source:` link) | **Preserved** if section structurally still applies |
| `Notable`, `Inconsistencies`, `Coverage Gaps`, `Concerns` | **Preserved**, agent may append new findings |
| Sections whose subject no longer exists | **Removed**, listed in re-run report |

## Frontmatter Handling

| Field | Re-run behavior |
|-------|-----------------|
| `name` | Preserved |
| `created` | Preserved |
| `updated` | Set to current date |
| `status` | Preserved unless agent detects the doc no longer applies (see below) |
| `sources` | **Replaced** with the actual list of files read this run, never appended blindly |

`status` transitions:

- `active` → `deprecated`: when the underlying scope no longer exists (e.g., `features.md` after a project flattens to layer-oriented). Doc kept for one cycle, then removed.
- `active` → `active`: default.

## Conflict Resolution

When a re-run produces a fact that contradicts an existing line:

1. Trust current source state.
2. Overwrite the contradicted line.
3. If the contradicted line was clearly human-written prose (no `Source:` marker, narrative tone), surface the diff in the run report and ask the user before overwriting.

## Stale File Flag

When a path is referenced in the doc but no longer present on disk:

```markdown
- `path/to/old.ts` (stale — file no longer exists)
```

On the next re-run, lines marked stale that remain stale for two consecutive runs are removed.

## Removed Files Cleanup

Files deleted from source are removed from the doc on the second re-run, not the first. This buffer protects against transient deletions during refactors.

## Re-Run Report

After any re-run that modifies docs, surface:

- Files added to `sources`
- Sections replaced
- Sections preserved as-is
- Stale flags introduced
- Stale flags removed

Keep the report short (one paragraph per doc).

## Guidelines

- Never overwrite human prose without surfacing it for review
- Tables and code snippets are owned by the agent — refresh freely
- `sources` is the source of truth for what the run actually read — populate it accurately even when no other changes happen
- Flag stale before deleting; keep the buffer cycle
