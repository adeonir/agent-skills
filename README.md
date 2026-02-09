# Agent Skills

A personal collection of skills for AI coding agents. Each skill packages instructions, references, and workflows that extend agent capabilities beyond their defaults.

## What are Skills?

Skills are packaged instructions that teach AI agents new workflows and specialized knowledge. Think of them as plugins -- a `SKILL.md` file with YAML frontmatter tells the agent when to activate, and markdown content tells it what to do. Supporting files (references, templates, scripts) are loaded on demand to keep context usage minimal.

```
skill-name/
  SKILL.md              # Entry point: frontmatter + instructions
  references/           # On-demand detailed documentation
  CHANGELOG.md
  README.md
```

Skills follow the [Agent Skills](https://agentskills.io) open standard, which originated in Claude Code and has been adopted across all major AI coding agents.

## Skills

| Skill | Category | Description |
|-------|----------|-------------|
| **[git-helpers](skills/(tooling)/git-helpers)** | Tooling | Conventional commits, confidence-scored code review, PR descriptions, and push-to-PR workflow |
| **[debug-tools](skills/(development)/debug-tools)** | Development | 5-phase debugging: investigate, inject logs, propose fix, verify, cleanup. With confidence scoring |
| **[spec-driven](skills/(development)/spec-driven)** | Development | Specification-driven development: Initialize, Plan, Tasks, Implement+Validate. Full traceability |
| **[design-builder](skills/(design)/design-builder)** | Design | Design-to-code pipeline: extract copy from URLs, design tokens from images, build React components |
| **[prd-writer](skills/(product)/prd-writer)** | Product | PRD generation through structured discovery interview, scoping, and technical drafting |

## Supported Agents

The `SKILL.md` format is an [open standard](https://agentskills.io) supported natively by most AI coding agents. Here are some of them:

| Agent | Project Skills | Personal Skills |
|-------|---------------|-----------------|
| **[Claude Code](https://code.claude.com/docs/en/skills)** | `.claude/skills/<name>/` | `~/.claude/skills/<name>/` |
| **[Cursor](https://cursor.com/changelog/2-4)** | `.cursor/skills/<name>/` | -- |
| **[GitHub Copilot](https://code.visualstudio.com/docs/copilot/customization/agent-skills)** | `.github/skills/<name>/` | `~/.copilot/skills/<name>/` |
| **[Windsurf](https://docs.windsurf.com/windsurf/cascade/skills)** | `.windsurf/skills/<name>/` | `~/.codeium/windsurf/skills/<name>/` |
| **[Gemini CLI](https://geminicli.com/docs/cli/skills/)** | `.gemini/skills/<name>/` | `~/.gemini/skills/<name>/` |
| **[Kimi Code](https://moonshotai.github.io/kimi-cli/en/customization/skills.html)** | `.kimi/skills/<name>/` | `~/.kimi/skills/<name>/` |
| **[OpenCode](https://opencode.ai/docs/skills/)** | `.opencode/skills/<name>/` | `~/.config/opencode/skills/<name>/` |

Other agents like Cline, Roo Code, Aider, Amazon Q, and Augment also support skills. Check your agent's documentation for the exact paths.

## Installation

Copy or symlink a skill into your agent's skills directory. Replace the paths below with the correct ones for your agent (see table above).

```bash
# Symlink (recommended -- stays in sync)
ln -s /path/to/agents-skills/skills/(tooling)/git-helpers ~/.claude/skills/git-helpers

# Or copy
cp -r /path/to/agents-skills/skills/(tooling)/git-helpers ~/.claude/skills/git-helpers
```

For project-local installation, use the project skills path instead:

```bash
# Example: install spec-driven into a project for Claude Code
ln -s /path/to/agents-skills/skills/(development)/spec-driven .claude/skills/spec-driven
```

## License

MIT
