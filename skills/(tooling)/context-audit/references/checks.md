# Audit Checks by Category

What each scanner in `scripts/audit.py` inspects, what its output means,
and what judgment to apply on top.

## When to Use

- Loaded only when troubleshooting an unexpected scanner result
- Not loaded by default in the audit workflow -- the script JSON plus
  filters.md is sufficient for normal runs
- Reach for this file when the script output looks wrong or surprising

## Workflow

Look up the category, read what the scanner does, compare with what you
see in the output JSON, decide if the discrepancy is a real issue or a
scanner gap.

### MCP servers

**Source:** `mcpServers` key in `~/.claude/settings.json` and project settings.

**Output fields:** `count`, `with_cli_alternative`, `servers[]` with
name, scope, and matched CLI alternative.

**Apply:**
- Cross-reference each server name against `assets/cli_alternatives.json`
- Pull actual MCP token overhead from `/context` output when available
- Use the PDF heuristic: daily use keeps the MCP, weekly or less means switch to CLI

### Slash commands

**Source:** `.claude/commands/*.md` (project) and `~/.claude/commands/*.md` (user).

**Output fields:** path, line count, body line count, name, `flagged_rules[]`.

**Apply:**
- Run filters.md against each command body
- Flag commands the user describes as "I forgot I had this"
- Commands over 100 lines often hide pasted prompts that should be skills

### Hooks

**Source:** `hooks` key in settings.json plus `.claude/hooks/` scripts.

**Output fields:** `hook_events[]` listing lifecycle events with hooks.

**Apply:**
- Hook commands that emit large outputs cost tokens every turn they fire
- Flag hooks that print logs or status to stdout -- that output enters context
- Suggest redirecting verbose output to files

### Agents

**Source:** `.claude/agents/*.md` (project) and `~/.claude/agents/*.md` (user).

**Output fields:** path, line count, name, `flagged_rules[]`.

**Apply:**
- Agent definitions load into the parent context just to be available
- Flag agents over 150 lines as compression candidates
- Apply filters.md to agent prompts the same way as CLAUDE.md

### Skills

**Source:** `.claude/skills/*/SKILL.md` (project and user scopes).

**Output fields:** name, path, total_lines, body_lines, description_words,
has_references_dir, has_scripts_dir.

**Apply:**
- Skills over 200 lines without `references/` are flagged for progressive disclosure
- Skills over 500 lines are critical
- A `description` over 80 words may hurt triggering accuracy

### CLAUDE.md files

**Source:** project root, `.claude/CLAUDE.md`, `~/.claude/CLAUDE.md`,
plus files referenced via `@path/to/file.md` (resolved recursively).

**Output fields:** path, raw_lines, resolved_lines, `flagged_rules[]`.

**Apply:**
- Apply filters.md to every rule
- Files over 200 lines (resolved): recommend progressive disclosure
- Files over 500 lines (resolved) are critical
- Compare project CLAUDE.md against `~/.claude/CLAUDE.md` for redundancy

### Settings

**Source:** `~/.claude/settings.json` and project settings.

**Output fields per scope:** present, autocompact_override, autocompact_ok,
bash_max_output_length, bash_max_ok, deny_count, status_line, hook_events.

**Apply:**

| Key | Flag if | Recommended |
|-----|---------|-------------|
| `autocompact_percentage_override` | Missing or > 80 | 75 |
| `env.BASH_MAX_OUTPUT_LENGTH` | Missing or < 100,000 | 150,000 |
| `permissions.deny` | Missing | See below |

User-scope settings cascade to every project. Flagging them is higher
priority than project-scope misses.

### File permissions

**Source:** `permissions.deny` array in settings.json.

**Output fields:** `missing_deny_patterns[]` based on `assets/bloat_patterns.json`
plus detected project markers.

**Apply:**
- Cross-check against `.gitignore` -- ignored directories are strong deny candidates
- Only suggest patterns for directories that actually exist
- Do not over-deny: a pattern with no target dir is noise

## Guidelines

**DO:**
- Read the scanner output before re-scanning files manually
- Cross-reference scanner findings with /context when /context is available
- Add cross-file judgment the scanner cannot do: contradictions, redundancy across scopes
- Distinguish quality fixes (autocompact threshold) from token-savings fixes (MCP disconnect) in the report

**DON'T:**
- Re-implement the scanner inline (contrasts: read scanner output first)
- Trust file estimates over /context numbers (contrasts: cross-reference with /context)
- Skip cross-file checks because the scanner did not flag them (contrasts: add cross-file judgment)
- Conflate quality fixes with token savings (contrasts: distinguish in the report)

## Error Handling

- Scanner output missing a category: file likely missing or unreadable, note in report and skip
- Scanner reports a finding the user disagrees with: ask why, treat as feedback for next pre-filter pass
- /context numbers contradict scanner estimates: trust /context, mark estimate as superseded
