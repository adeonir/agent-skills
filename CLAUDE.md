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

## Category Directories

| Directory | Usage |
|-----------|-------|
| (design) | Design, UI, brand skills |
| (development) | Development, debugging, specs skills |
| (product) | Product, documentation, naming skills |
| (tooling) | Git, CI, workflow tooling skills |

## Skill File Conventions

### SKILL.md Frontmatter

```yaml
---
name: skill-name
description: >-
  Short sentence of what it does. Use when: usage contexts.
  Triggers on "phrase 1", "phrase 2", "phrase 3".
---
```

Only `name` and `description` -- no other fields.

Description structure: `[What it does]. Use when [scenarios]. Triggers on "[trigger1]", "[trigger2]"`.

Formatting rules:
- `name`: kebab-case, matches the directory name
- `description`: folded block `>-` string, max 1024 characters (skills.sh spec limit)
  - Structure: what it does + when to use + specific triggers
  - Avoid internal mechanics (phases, loops, stages) -- focus on what and when
  - Include varied trigger phrases to improve matching
  - Use `>-` with 2-space indentation
  - Keep lines under 80 characters -- long single-line descriptions trigger obfuscation alerts in security audits

### SKILL.md Section Order

All skills follow this exact order:

```
1. # Title                  (H1, descriptive skill name)
2. **Recommended effort:**  (optional single line; skills with heavy phases)
3. ## Workflow              (flow diagram)
4. ## Context Loading       (reference loading strategy)
5. ## Triggers              (trigger -> reference table)
6. ## Cross-References      (ASCII dependency diagram)
7. ## Guidelines            (DO/DON'T)
8. ## Output                (output format and location, if applicable)
9. ## Error Handling        (edge case list)
10. ## Compact Instructions (optional; long-running skills only)
```

### Recommended Effort

Optional single line placed immediately after the H1 title, before Workflow.
Use only for skills with cognitively heavy phases (audit, design, discovery,
review). Omit on light skills (quick fixes, naming, single-step tooling).

Format: one bold line with the effort level and a short rationale.

```markdown
**Recommended effort:** xhigh for design/audit phases; medium for quick mode.
```

Guidance by level:
- `medium`: cost- or latency-sensitive work with tight scope
- `high`: balance of intelligence and cost; concurrent sessions
- `xhigh`: default for intelligence-sensitive work (API design, migrations,
  multi-file reviews)
- `max`: reserve for evals and ceiling tests; diminishing returns

### Compact Instructions

Optional section for long-running skills where context pressure is realistic.
Tells Claude Code what to preserve when autocompact fires.

```markdown
## Compact Instructions

Preserve:
- Current phase, phase artifacts paths, open decisions
- User's acceptance criteria and constraints

Drop:
- Raw tool outputs, intermediate grep results, scratch reasoning
```

Skills that persist state to disk across phases (e.g., `spec-driven` via
`.artifacts/.session-dump.md`) do not need this section -- the artifact
already survives `/clear` and is a stronger guarantee than compact hints.

### Workflow

Simple `-->` arrows. Optional loop on second line with `^` and `|___|`.
No pipes or box-drawing. Keep lines under 70 chars.

```
phase-1 --> phase-2 --> phase-3 --> output
  ^_________________________|  (note about the loop)
```

One sentence explaining the flow right below.

### Context Loading Strategy

Documents which references to load and when. Specify:
- What to load per trigger
- Automatic dependencies (ref A loads ref B)
- What should never be loaded together

```markdown
Load only the reference matching the current trigger. Never load multiple
references simultaneously unless explicitly noted.
```

### Triggers

Table mapping natural language phrases to references:

```markdown
| Trigger Pattern | Reference |
|-----------------|-----------|
| Commit changes, create commit | [commit.md](references/commit.md) |
| Review code, check changes | [code-review.md](references/code-review.md) |
```

Followed by `Notes:` for auxiliary references (not direct triggers):

```markdown
Notes:

- `auxiliary.md` is not a direct trigger. It is loaded by `main.md` as part of its process.
```

### Cross-References

ASCII diagram showing dependencies between internal references and with other skills:

```markdown
reference-a.md ----> reference-b.md (a loads b)
reference-a.md <---> reference-c.md (bidirectional)
skill-name --------> other-skill (output feeds into)
```

### Guidelines

Always DO/DON'T format. Never prose. 3-8 items per list. Concrete rules, not aspirational.

Voice rule: every `DON'T` must be a contrast of a concrete `DO` in the same
list. A `DON'T` without a matching `DO` is proscription without direction --
move it to a positive instruction elsewhere or drop it. Positive examples
("write it like this") steer behavior better than standalone proscriptions.

```markdown
**DO:**
- Validate output before saving
- Ask the user for missing context
- Match the project's existing conventions

**DON'T:**
- Skip validation to save a step (contrasts: validate before saving)
- Invent context the user did not provide (contrasts: ask for missing context)
- Introduce patterns foreign to the project (contrasts: match conventions)
```

### Error Handling

List of conditions and actions:

```markdown
- No context provided: ask user for details
- Ambiguous trigger: ask which workflow to use
- Output directory missing: create it
- Conflicting results: present options to user
```

### Reference Files (references/*.md)

Each file is loaded on demand by SKILL.md. Internal structure:

```
1. # Descriptive Title
2. Introductory sentence (one line)
3. ## When to Use
   - Conditions that trigger this reference
4. ## Workflow (or ## Discovery, ## Phases)
   - Numbered or bulleted steps
   - Subsections with ### for complex phases
5. ## Guidelines (optional)
   - DO/DON'T format
6. ## Error Handling (optional)
   - Edge cases specific to this phase
7. ## Next Steps (optional)
   - What to do after completing this phase
```

- Every reference has `When to Use`; include `Guidelines` and `Error Handling` when relevant
- Template usage: `**USE TEMPLATE:** \`templates/file.md\``
- Loading other references: `Load [file.md](file.md)` or `**LOAD:** [file.md](file.md)`

Dependencies between references -- indicate at the top of the file:

```markdown
> **LOAD FIRST:** [dependency.md](dependency.md) -- description of why
```

This dependency must also be documented in the SKILL.md Cross-References section.

Internal links always relative to the references directory:

```markdown
[evaluation.md](evaluation.md)
[../templates/report.md](../templates/report.md)
```

### Template Files (templates/*.md)

Optional. Exist when the skill generates artifacts with a fixed structure.

When to create:
- The skill generates files as output (documents, reports, configs)
- The output has a repeatable structure across executions
- No template needed: skills that operate inline (debug-tools, git-helpers)

Use `{{mustache}}` for dynamic values:

```yaml
---
name: {{project-name}}
source: {{url or description}}
created: {{YYYY-MM-DD}}
---

# {{Title}}

## Section

{{description of what goes here}}
```

For fill-in instructions (not value placeholders), use `{single braces}`:

```markdown
{For each item, one line:}
{Brief recommendation if one clearly dominates.}
```

Templates named after the output type they generate:

| Template | Output |
|----------|--------|
| `report.md` | Naming report |
| `prd.md` | Product Requirements Document |
| `copy.yaml` | Copy extraction |

### CHANGELOG.md

Frontmatter:

```yaml
---
name: skill-name
---
```

Format:

```markdown
# Changelog

All notable changes to this skill will be documented in this file.

## YYYY-MM-DD

### Added

- Description of added feature

### Changed

- Description of change

### Fixed

- Description of fix

### Removed

- Description of removal
```

Rules:
- Date headers: `## YYYY-MM-DD` -- never versions
- Subsections: `### Added`, `### Changed`, `### Fixed`, `### Removed`
- Each item is one sentence (no paragraphs)
- Most recent first (descending chronological order)
- Reference filenames when relevant

### README.md

User-facing documentation. Sections in order:

```
1. # Title
2. Descriptive sentence (one line)
3. ## Installation
   - npx skills add adeonir/agent-skills --skill {name}
4. ## What It Does
   - Mermaid diagram (flowchart LR or TD)
   - Table with phases/outputs
5. ## Usage
   - Code block with natural language usage examples
6. ## Output (if applicable)
   - Output format or directory
7. ## Requirements (if applicable)
   - Dependencies and external tools
8. ## Integration (if applicable)
   - Table of connections with other skills
```

Mermaid diagrams always `flowchart LR` or `flowchart TD` (never `graph`).
Decisions with `{}`, actions with `[]`, arrows with labels via `-->|label|`.

## New Skill Checklist

Before finalizing a new skill, verify:

- [ ] Directory at `skills/(category)/skill-name/`
- [ ] `SKILL.md` with complete frontmatter and all sections in correct order
- [ ] `README.md` with Installation, mermaid diagram, and usage examples
- [ ] `CHANGELOG.md` with creation date entry
- [ ] `references/` with one file per phase/workflow
- [ ] Each reference has a "When to Use" section
- [ ] Cross-references documented in SKILL.md
- [ ] Guidelines in DO/DON'T format; every DON'T contrasts a concrete DO
- [ ] `templates/` if the skill generates artifacts with fixed structure
- [ ] Skill added to the root README.md table (sorted by category)
- [ ] `Recommended effort:` line added if skill has heavy phases
- [ ] `Compact Instructions` section added if skill is long-running and does not persist state to disk
- [ ] Entrypoint skills state a first-turn brief (intent, constraints, acceptance, files)
- [ ] Skills that fan out across items instruct the model to spawn subagents explicitly

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
- XML tags (`<example>`, `<instructions>`, `<input>`) are permitted inside
  `references/*.md` and `templates/*.md` when the file is ingested as input by
  the model. Do not use XML tags in `SKILL.md` -- it stays human-readable markdown

## Prompt Conventions

Rules for how skills should instruct the model at runtime (distinct from
authoring style, which is Writing Style above).

- **First-turn brief**: entrypoint skills (those the user invokes directly) must
  accept intent, constraints, acceptance criteria, and target files in the first
  turn. Avoid multi-turn clarification loops -- they add reasoning overhead and
  degrade coherence over long sessions
- **Explicit fan-out**: skills that rely on parallel exploration must instruct
  the model to spawn multiple subagents in the same turn. Opus 4.7 is
  conservative about spawning subagents by default, so "fan out across N files"
  must be stated, not assumed
- **Positive examples over proscriptions**: when steering output shape, show an
  example of the desired form rather than listing what to avoid
- **No tool-stack coupling**: instructions describe behavior (what to do), not
  specific tools or commands. Keep skills portable across harnesses

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
├── features/       # spec-driven: specs, designs, tasks
├── quick/          # spec-driven: quick mode tasks
├── research/       # spec-driven: research cache
├── epics/          # epic-tracker: epics, stories, bugs, releases
├── docs/           # docs-writer: PRD, ADR, RFC, etc.
│                   # product-naming: naming research and validation reports
├── design/         # design-builder: copy, design tokens, variants
└── brainstorm/     # brainstorming: direction artifacts
```

`.agents/` is a separate directory for reference context, consumed by other skills:

```
.agents/
├── project.md      # project-index: project context
├── codebase/       # project-index: deep codebase analysis
├── baselines/      # spec-driven: area behavioral baselines
└── knowledge.md    # spec-driven: decisions, gotchas, Codebase Feedback queue
```

Ownership is strict: project-index is the sole writer to `project.md` and `codebase/*.md`; spec-driven is the sole writer to `knowledge.md` and `baselines/*.md`. Codebase discoveries from spec-driven (design, implement, quick-mode) land in `knowledge.md`'s `## Codebase Feedback` section and are merged into `codebase/*.md` on demand via `/project-index integrate feedback`.

`codebase/*.md` captures only observable current state -- no milestones, feature numbers, `(planned)` or `(TBD)` markers, and no stubs for services/routes/deps not present in the codebase. Inventory and structural facts (installed packages, new routes, new modules, new directories, new env vars) are not queued in `knowledge.md` -- they are re-derived by `/project-index re-index`, which audit suggests (never prompts) when structural deltas exist on the feature branch.

Root instruction files: project-index owns `AGENTS.md` and generates/updates it only when the project already uses it or the user opts in. `CLAUDE.md` is user-authored territory -- project-index never edits or overwrites it.

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
This installs the skill files to using symlinks in `~/.agents/skills/{name}/`.

**NEVER edit files in `~/.agents/skills/` directly.** That is the installation target.
The source of truth is this repository (`skills/` directory). Edit here, then reinstall.
