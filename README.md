# Agent Skills

A personal collection of skills for AI coding agents. Each skill packages instructions, references, and workflows that extend agent capabilities beyond their defaults.

## What are Skills?

Skills are packaged instructions that teach AI agents new workflows and specialized knowledge. Think of them as plugins -- a `SKILL.md` file with YAML frontmatter tells the agent when to activate, and markdown content tells it what to do. Supporting files (references, templates, scripts) are loaded on demand to keep context usage minimal.

Skills follow the [Agent Skills](https://agentskills.io) open standard, which originated in Claude Code and has been adopted across all major AI coding agents.

## Installation

Install any skill with a single command using the [Skills CLI](https://skills.sh):

```bash
npx skills add adeonir/agent-skills
```

## Skills

| Skill | Category | Description |
|-------|----------|-------------|
| **[design-builder](skills/(design)/design-builder)** | Design | Greenfield design pipeline for any digital product: extract, structure, preview, tune, sync, handoff |
| **[debug-tools](skills/(development)/debug-tools)** | Development | Iterative debugging: investigate, fix, verify loop with pattern comparison and escalation. Confidence scoring |
| **[project-index](skills/(development)/project-index)** | Development | Generate project context and deep codebase documentation with code snippets. Creates `.agents/` with depth over brevity |
| **[spec-driven](skills/(development)/spec-driven)** | Development | Specification-driven development: Specify, Design, Tasks, Implement. Auto-sized by complexity, full traceability |
| **[system-design](skills/(development)/system-design)** | Development | Guided system design from problem to architecture: discovery, requirements, trade-offs, components, brief |
| **[brainstorming](skills/(product)/brainstorming)** | Product | Structured idea exploration: discover context, diverge with techniques, converge on direction. Feeds docs-writer, spec-driven, design-builder |
| **[docs-writer](skills/(product)/docs-writer)** | Product | Structured document generation: PRD, Brief, Design Doc, TDD, RFC, ADR. Guided discovery per type |
| **[epic-tracker](skills/(product)/epic-tracker)** | Product | Delivery lifecycle management: plan epics, track stories and bugs, group releases. Feeds spec-driven |
| **[product-naming](skills/(product)/product-naming)** | Product | Research and validate product names with domain/social availability checks and quality scoring |
| **[git-helpers](skills/(tooling)/git-helpers)** | Tooling | Conventional commits, confidence-scored code review, PR summaries, pull request creation, and branch lifecycle |
| **[session-notes](skills/(tooling)/session-notes)** | Tooling | Obsidian note creation for projects, companies, challenges, brags, daily logs, sessions, and conversations |
| **[wrap-up](skills/(tooling)/wrap-up)** | Tooling | End-of-session context persistence across auto-memory, Basic Memory, and Obsidian |

## How They Connect

```mermaid
flowchart TD
    BR[brainstorming] -->|direction| PN[product-naming]
    BR -->|direction| DW[docs-writer]
    BR -->|direction| DB[design-builder]
    BR -.->|direction| SD[spec-driven]
    PN -->|name| DW
    PN -->|name| DB
    DW -->|requirements| ET[epic-tracker]
    DW -->|requirements| DB
    DW -->|requirements| SD
    ET -->|handoff| SD
    PI[project-index] -->|codebase docs| SD
    DB -->|approved design| SD
    SD -->|commits & PRs| GH[git-helpers]
    SD -->|discoveries| PI
    SYS[system-design] -->|brief| DW
    SYS -->|architecture| SD
    BR -.->|direction| SYS
```

Dashed arrow: optional shortcut for small, well-scoped work.
**debug-tools**, **session-notes**, and **wrap-up** are independent — available at any point, not tied to the pipeline.

## Typical Greenfield Flow

```
1. brainstorming     --> explore ideas, choose direction
2. product-naming    --> research and validate name
3. docs-writer       --> generate requirements (PRD, Brief)
4. epic-tracker      --> plan epics, track stories and bugs
5. design-builder    --> extract, structure, preview, approve
6. spec-driven       --> specify, design, tasks, implement
7. git-helpers       --> commit, review, PR, finish
```

**Always available:**

```
project-index   --> scan codebase and generate context (brownfield or re-index)
debug-tools     --> investigate and fix issues
session-notes   --> document work in Obsidian
wrap-up         --> persist session context across memory systems
```

## Output Structure

Skills write artifacts to `.artifacts/` and reference context to `.agents/`:

```
.agents/
├── codebase/       # project-index: deep codebase analysis
└── project.md      # project-index: project context

.artifacts/
├── brainstorm/     # brainstorming: ideation artifacts
├── design/         # design-builder: copy.yaml, design.json, variants/
├── docs/           # docs-writer + system-design + product-naming: PRD, ADR, TDD, RFC, system-brief.md
├── epics/          # epic-tracker: epics, stories, bugs, releases
├── features/       # spec-driven: feature specs, designs, tasks
├── quick/          # spec-driven: quick mode tasks
└── research/       # spec-driven: research cache
```

This directory is gitignored by default but can be committed for team collaboration.

## License

MIT
