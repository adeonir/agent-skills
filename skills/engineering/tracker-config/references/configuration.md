# Tracker Configuration

Owned keys, instruction-block format, and the persistence interface.

## When to Use

Load when inspecting, configuring, or resolving the project's tracker.

## Owned keys

Use repository-local `git config` under `tracker.*` only. Do not store credentials. Persist a complete settings object with the unprefixed keys below; absent optional keys remove stale values from this namespace during reconfiguration.

| Key | Meaning |
|-----|---------|
| kind | Required: `linear` or `github` |
| team | Linear team ID; required for Linear |
| team-name | Linear team name; required for Linear; used in the instruction block |
| project | Linear project ID, required; GitHub Projects number, optional |
| project-name | Linear project name; required for Linear; used in the instruction block |
| repository | GitHub `owner/name`; required for GitHub |
| project-owner | GitHub project owner; required when project is set |
| channel | GitHub primary: `mcp` or `cli` |
| fallback | GitHub secondary: `mcp`, `cli`, or `none`; different from primary |

Linear settings contain kind, team, team-name, project, and project-name. Keep the stable team and project IDs in local settings for tracker operations; render only the names in the versioned instruction block. Resolve each name against its ID before persistence. GitHub settings contain no team; omit project-owner when project is absent. A one-operation override never changes saved settings. The repository and project owner make GitHub's destination explicit even when remotes or project ownership differ.

## Persistence commands

Run the bundled script from the repository root:

```bash
python3 <this-skill>/scripts/config.py show
python3 <this-skill>/scripts/config.py apply <settings.json>
```

`show` returns owned settings, validation errors, the instruction-file path, and block consistency. It makes no changes. `apply` validates first, writes only local owned keys, and updates the block. On failure it attempts to restore the prior owned settings and file, reports rollback errors, and exits unsuccessfully. Resolve an ambiguous instruction target before retrying.

## Instruction block

Maintain one `## Issue tracker` section in the instruction file the harness reads. Prefer a root CLAUDE.md, then .claude/CLAUDE.md; when it imports AGENTS.md, resolve that import relative to the importing file and use the imported path. Otherwise use that CLAUDE.md. Without either, use AGENTS.md. Preserve unrelated sections; reject duplicate blocks, extra or ambiguous section content, and targets outside the repository. Replace only a tracker heading with its single summary paragraph; resolve other content manually before retrying.

ALWAYS use this exact template structure:

```markdown
## Issue tracker

Tracker: [Linear team and project names, or GitHub repository and optional project owner/number]. Configuration: repository-local `tracker.*`; inspect with `git config --local --get-regexp '^tracker\.'`. Change with "configure tracker".
```

MUST NOT contain: credentials, another configuration namespace, issue-body content, delivery plans, or instructions to invoke another skill.

The local config is authoritative for this block. An operation reports a stale block; repair it through configuration without changing issue content.
