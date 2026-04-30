# Context Audit Report Template

Use this exact structure when presenting audit results. The headline is
estimated tokens saved per turn -- score is secondary. Lead with savings.

## Template

```markdown
# Context Audit

**Estimated savings: ~{{N}} tokens/turn** if you apply the Top 3 below.
**Score: {{N}}/100** -- {{CLEAN | NEEDS WORK | BLOATED | CRITICAL}}

## /context snapshot
{{Paste key numbers from /context output. If not provided, write
"Not provided -- file-only audit, savings estimates carry ~ prefix."}}

## What's working
- {{Positive finding 1}}
- {{Positive finding 2}}
- {{Positive finding 3}}

## Issues found

### [{{CRITICAL | WARNING | INFO}}] {{Category}}
**Location:** {{file path or scope}}
**Problem:** {{What is wrong, in plain language}}
**Estimated cost:** ~{{N}} tokens/turn
**Fix:** {{One-line actionable instruction}}

{{Repeat per issue, ordered CRITICAL then WARNING then INFO.}}

## Rules to cut
| File | Line | Rule | Filter | Why |
|------|------|------|--------|-----|
| {{path}} | {{N}} | {{exact text}} | {{Default | Vague | Bandaid | Redundancy | Contradiction}} | {{one-line reason}} |

## Conflicts
{{Cross-file contradictions. Empty section: write "None found".}}

## Top 3 fixes (ranked by savings divided by effort)

1. **{{Action}}** -- saves ~{{N}} tokens/turn, {{trivial | small | medium | large}} effort
   {{One-paragraph how-to}}
2. **{{Action}}** -- saves ~{{N}} tokens/turn, {{effort}}
   {{How-to}}
3. **{{Action}}** -- saves ~{{N}} tokens/turn, {{effort}}
   {{How-to}}

## Want me to apply any of these?
I can:
- Show a diff for settings.json with the missing keys added
- Show a diff for permissions.deny rules
- Show a cleaned-up CLAUDE.md with the flagged rules removed
- Suggest a progressive-disclosure split for long files

I'll always show the diff first -- never auto-apply.
```

## Worked example

Filled-in audit from a hypothetical Node project:

```markdown
# Context Audit

**Estimated savings: ~38,000 tokens/turn** if you apply the Top 3 below.
**Score: 64/100** -- BLOATED

## /context snapshot
Total: 92,400 tokens before first message
- MCP servers: 51,200 (4 servers)
- CLAUDE.md: 8,300
- Skills: 4,800
- System: 28,100

## What's working
- env.BASH_MAX_OUTPUT_LENGTH set to 150,000
- Project CLAUDE.md uses @imports for testing.md and deploy.md
- 0 agents over 150 lines

## Issues found

### [CRITICAL] MCP servers with CLI alternatives
**Location:** ~/.claude/settings.json
**Problem:** 3 of 4 connected MCPs (playwright, github, filesystem) have CLI
equivalents. ~45,000 tokens loaded every turn.
**Estimated cost:** ~30,000 tokens/turn
**Fix:** Disconnect playwright, github, filesystem. Use `npx playwright`,
`gh`, native Read/Write/Edit instead.

### [WARNING] CLAUDE.md flagged rules
**Location:** ./CLAUDE.md (8 rules flagged)
**Problem:** 3 default-behavior rules, 2 vague, 1 bandaid, 2 redundant.
**Estimated cost:** ~5,000 tokens/turn
**Fix:** See "Rules to cut" below.

### [WARNING] Missing BASH_MAX_OUTPUT_LENGTH
**Location:** ~/.claude/settings.json
**Problem:** Bash output truncates at default ~30k chars; each truncation forces a retry.
**Estimated cost:** ~3,000 tokens/turn
**Fix:** Add `"env": { "BASH_MAX_OUTPUT_LENGTH": "150000" }`.

## Rules to cut
| File | Line | Rule | Filter | Why |
|------|------|------|--------|-----|
| ./CLAUDE.md | 12 | "Write clean, readable code." | Default | Default behavior. |
| ./CLAUDE.md | 23 | "Be concise but thorough." | Vague | Self-contradictory; rewrite. |
| ./CLAUDE.md | 31 | "Don't break the auth flow like in #1247." | Bandaid | Specific to one PR. |

## Conflicts
None found.

## Top 3 fixes (ranked by savings divided by effort)

1. **Disconnect MCPs with CLI alternatives** -- saves ~30,000 tokens/turn, small effort
   Run `/mcp` and disconnect playwright, github, filesystem. Use the CLIs through Bash when needed.

2. **Cut 8 flagged rules from project CLAUDE.md** -- saves ~5,000 tokens/turn, trivial effort
   Open ./CLAUDE.md and remove flagged lines. Brings the file from 47 to 39 lines.

3. **Add BASH_MAX_OUTPUT_LENGTH to settings** -- saves ~3,000 tokens/turn, trivial effort
   Add `"env": { "BASH_MAX_OUTPUT_LENGTH": "150000" }` to ~/.claude/settings.json.
```
