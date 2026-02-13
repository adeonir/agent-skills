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
| **[spec-driven](skills/(development)/spec-driven)** | Development | Specification-driven development: Initialize, Plan, Tasks, Implement+Validate. Full traceability |
| **[git-helpers](skills/(tooling)/git-helpers)** | Tooling | Conventional commits, confidence-scored code review, PR descriptions, and push-to-PR workflow |
| **[docs-writer](skills/(product)/docs-writer)** | Product | Structured document generation: PRD, Brief, Issue, Task, User Story, RFC, ADR, TDD. Guided discovery per type |
| **[debug-tools](skills/(development)/debug-tools)** | Development | 5-phase debugging: investigate, inject logs, propose fix, verify, cleanup. With confidence scoring |
| **[design-builder](skills/(design)/design-builder)** | Design | Design-to-code pipeline: extract copy from URLs, design tokens from images, build React components |

## Installation

Install any skill with a single command using the [Skills CLI](https://skills.sh):

```bash
npx skills add adeonir/agent-skills
```

## License

MIT
