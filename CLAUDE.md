# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Pure-markdown repository of skills for AI coding agents. No build system, no tests, no linter.
Validation is manual: read files, verify structure, check cross-references.

Skills follow the [Agent Skills](https://agentskills.io) open standard.

## Repository Structure

```
skills/
├── (design)/           # Category directories use parenthesized names
├── (development)/
├── (product)/
└── (tooling)/
    └── skill-name/     # kebab-case directory
        ├── SKILL.md    # Entry point: YAML frontmatter + instructions
        ├── CHANGELOG.md
        ├── README.md
        ├── references/ # On-demand detailed docs (loaded by triggers)
        ├── templates/  # Output templates for artifacts (optional)
        └── guides/     # Standalone guides for users (optional)
```

## Skill File Conventions

For detailed structure, section order, and examples, see `.artifacts/docs/skill-structure.md`.

### SKILL.md Frontmatter

```yaml
---
name: skill-name                    # kebab-case, matches directory name
description: >-                     # Max 1024 chars (skills.sh spec limit)
  Multi-line with                   # Keep lines under 80 chars
  indentation for continuation.
  Triggers on "phrase 1", "phrase 2".
---
```

Only `name` and `description` -- no other fields.

Description structure: `[What it does]. Use when [scenarios]. Triggers on "[trigger1]", "[trigger2]"`.

Formatting rules:
- Use YAML folded block `>-` with 2-space indentation
- Keep each line under 80 characters -- long single-line descriptions trigger obfuscation alerts in security audits
- Max 1024 characters total (skills.sh spec limit)

### SKILL.md Sections

Every SKILL.md starts with an H1 title + one-liner subtitle and ends with Guidelines (DO/DON'T)
and Error Handling. Between those, include whichever sections the skill needs. Common sections:

- `## Workflow` -- ASCII art or text flow diagram
- `## Context Loading Strategy` -- what to load and when, token budgets
- `## Templates` -- table linking to template files (if templates/ exists)
- `## Triggers` -- tables mapping trigger patterns to reference files
- `## Cross-References` -- ASCII arrows showing reference dependencies
- `## Guidelines` -- split into **DO:** and **DON'T:** bullet lists
- `## Error Handling` -- bulleted `- Condition: action` pairs

### Reference Files (references/*.md)

- Every reference has `When to Use`; include `Guidelines` and `Error Handling` when relevant
- Template usage: `**USE TEMPLATE:** \`templates/file.md\``
- Loading other references: `Load [file.md](file.md)` or `**LOAD:** [file.md](file.md)`

### Template Files (templates/*.md)

Use `{{placeholder}}` syntax (Handlebars-like).

### CHANGELOG.md

- Frontmatter with `name` field only
- Date headers (`## YYYY-MM-DD`), not version numbers
- Keep a Changelog categories: Added, Changed, Removed, Fixed
- Reverse-chronological order

### README.md

Sections in order: Installation, What It Does, Usage, Output, Requirements, Integration, FAQ.
Installation always uses `npx skills add adeonir/agent-skills --skill {name}`.

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Skill directories | kebab-case | `spec-driven`, `git-helpers` |
| Category directories | Parenthesized lowercase | `(design)`, `(development)` |
| Reference/template files | kebab-case .md | `quick-mode.md`, `code-review.md` |
| Fixed files | UPPERCASE .md | `SKILL.md`, `CHANGELOG.md`, `README.md` |

## Writing Style

- Direct, imperative voice: "Create", "Load", "Check" (not "You should create")
- No emojis in prose or commit messages
- English throughout
- Simple `-->` arrows for workflows, no pipes or box-drawing, lines under 70 chars
- Tables for structured information (triggers, phases, comparisons)
- Guidelines always in DO/DON'T format
- Error handling always in `- Condition: action` format
- Cross-references use relative paths: `[file.md](references/file.md)`
- Token budget awareness: document what to load, what never to load simultaneously

## Commit Conventions

- Conventional commits: `type: description in imperative mood`
- Types: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `style`, `perf`
- First line under 72 characters
- No scope, no emojis, no attribution (no Co-Authored-By)
- Never push without explicit confirmation

## Output Artifacts

Skills write to `.artifacts/` organized by domain:

```
.artifacts/
├── state.md        # spec-driven: persistent decisions
├── features/       # spec-driven: specs, plans, tasks
├── quick/          # spec-driven: quick mode tasks
├── research/       # spec-driven: research cache
├── docs/           # docs-writer: PRD, ADR, RFC, etc.
│                   # product-naming: naming research and validation reports
├── design/         # design-builder: copy, design tokens, variants
└── brainstorm/     # brainstorming: direction artifacts
```

`.agents/` is a separate directory generated by `project-index`, consumed by other skills.

## Terminology

TDD has two meanings in this project depending on context:
- docs-writer: Technical Design Document (`references/tdd.md`)
- spec-driven: Test-Driven Development (`references/test-driven.md`)

## Documentation

When updating docs, maintain consistency with existing patterns. Do not add product names to titles, use informal chat context as formal documentation, or include conversational topics as architectural decisions.

## Security Audits

Run security self-assessment after any skill change or new skill creation. The skills.sh
platform audits every published skill with 3 providers:

### Gen Agent Trust Hub

| Category | What Triggers It |
|----------|-----------------|
| COMMAND_EXECUTION | Instructions to run shell commands (mkdir, git, npm) |
| REMOTE_CODE_EXECUTION | Downloads + execution of external scripts (curl \| sh) |
| PROMPT_INJECTION | Ingesting untrusted external content (web pages, APIs) without sanitization |
| DATA_EXFILTRATION | Sending local data to external services |
| EXTERNAL_DOWNLOADS | Downloading from unverified domains |

### Socket

| Check | What It Detects |
|-------|----------------|
| Malicious behavior | Injection, exfiltration, untrusted installs |
| Security concerns | Credential exposure, tool/trust exploitation |
| Code obfuscation | Hidden or obfuscated code |
| Suspicious patterns | Reconnaissance, excessive autonomy, resource abuse |

### Snyk

| Code | What It Flags |
|------|--------------|
| W007 | Plaintext credentials in instructions or examples |
| E005 | Suspicious or untrusted download URLs |
| W011 | Third-party content exposure (indirect prompt injection risk) |

### Self-Assessment Checklist

Before publishing, verify:

- No plaintext passwords or API keys in examples (use `$ENV_VAR` or `{placeholder}`)
- No `curl | sh` or piped download-and-execute patterns
- No links to untrusted or non-official domains
- External content ingestion has trust boundary in the relevant reference file
- Shell commands are limited to non-destructive operations (mkdir, ls, grep)
- No instructions that could exfiltrate local data to external services

## Skill Installation

Skills are installed globally via `npx skills add adeonir/agent-skills --skill {name}`.
This copies files to `~/.agents/skills/{name}/`.

**NEVER edit files in `~/.agents/skills/` directly.** That is the installation target.
The source of truth is this repository (`skills/` directory). Edit here, then reinstall.
