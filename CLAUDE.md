# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Repository of skills for AI coding agents. Mostly markdown, with optional `scripts/` and `assets/` per skill. No build system, no tests, no linter.
Validation is manual: read files, verify structure, check cross-references.

Skills follow the [Agent Skills](https://agentskills.io) open standard.

## Canonical Skill Flow

Product-first workflow from discovery to implementation:

```
brainstorming + project-index (parallel, discovery)
    --> docs-writer (PRD or Brief)
    --> domain-model (entities, invariants, bounded contexts)
    --> system-design + design-builder (parallel)
    --> epic-tracker (epics --> stories)
    --> spec-driven (per story: spec + design + tasks)
    --> git-helpers (atomic commits per task)
    --> wrap-up (persist context to BM + Obsidian)
```

- `brainstorming` and `project-index` run in parallel — both are discovery
- `domain-model` translates PRD business rules and journeys into domain
  entities, invariants, and bounded contexts
- `system-design` defines technical architecture (APIs, data models,
  boundaries); bounded contexts from `domain-model` inform service design
- `design-builder` defines visual design (tokens, layout, components)
- `system-design` and `design-builder` are independent — run in parallel
  after `domain-model`; both inform `epic-tracker` scope
- `epic-tracker` needs both outputs to scope stories correctly
- `spec-driven` consumes `domain-model` entities and rules as contracts
- `spec-driven` runs per story, not per epic — correct granularity
  for atomic tasks
- `spec-driven` signals domain gaps back to `domain-model` via
  `knowledge.md`; `domain-model` update mode reads and clears the queue
- `wrap-up` is mandatory at end of any heavy session

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
        ├── guides/     # Standalone guides for users (optional)
        ├── scripts/    # Executable helpers loaded on demand (optional)
        └── assets/     # Static data files consumed by scripts (optional)
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
when_to_use: >-
  Trigger phrases or example requests that activate this skill.
---
```

Frontmatter fields:

| Field | Notes |
|-------|-------|
| `name` | kebab-case, max 64 chars. Defaults to directory name. |
| `description` | Recommended. What it does + when to use it. Combined with `when_to_use`, truncated at 1,536 chars in skill listing. |
| `when_to_use` | Optional. Extra trigger context appended to `description`. Counts toward 1,536-char cap. |
| `argument-hint` | Optional. Autocomplete hint for expected args, e.g. `[issue-number]`. |
| `disable-model-invocation` | Optional. `true` = user-only invoke. Default: `false`. |
| `user-invocable` | Optional. `false` = hidden from `/` menu. Default: `true`. |
| `allowed-tools` | Optional. Tools pre-approved while skill active. Space-separated or YAML list. Supports scoping: `Bash(git *)` allows only git commands; `Bash(gh pr *)` allows only `gh pr` subcommands. |
| `model` | Optional. Model override when skill is active. |
| `effort` | Optional. Effort level when skill is active; overrides session level. Default: inherits from session. Options: `low`, `medium`, `high`, `xhigh`, `max`. |
| `context` | Optional. `inline` (default) or `fork` (run in subagent). |
| `agent` | Optional. Subagent type when `context: fork`. Built-ins: `Explore`, `Plan`, `general-purpose`. Custom: any agent in `.claude/agents/`. Default: `general-purpose`. |

Description structure: `[What it does]. Use when [scenarios].`
`when_to_use` structure: trigger phrases, example requests, invocation patterns.

Formatting rules:
- `description` and `when_to_use`: folded block `>-` with 2-space indentation
  - Avoid internal mechanics (phases, loops, stages) -- focus on what and when
  - Include varied trigger phrases to improve matching
  - Keep lines under 80 characters -- long single-line descriptions trigger
    obfuscation alerts in security audits

### SKILL.md Runtime Variables

**`$ARGUMENTS`** — replaced with whatever the user typed after `/skill-name <args>`.
Use for skills that accept a target, message, or topic at invocation time.

**`!`command``** — shell command executed before Claude sees the skill content;
output is injected in place. Use to inject live context (diff, PR data, file list).
Security: keep commands read-only (`gh`, `git log`, `cat`). Never pipe to a shell
or write to disk from this interpolation.

### SKILL.md Section Order

All skills follow this exact order:

```
1. # Title                  (H1, descriptive skill name)
2. **Recommended effort:**  (optional single line; skills with heavy phases)
3. ## Workflow              (flow diagram)
4. ## Triggers              (trigger -> reference table)
5. ## Cross-References      (ASCII dependency diagram)
6. ## Guidelines            (DO/DON'T)
7. ## Output                (output format and location, if applicable)
8. ## Error Handling        (edge case list)
9. ## Compact Instructions  (optional; long-running skills only)
```

Extra sections are allowed but must respect this order. Methodological sections
(e.g., Knowledge Verification Chain, Artifact Structure Authority) go between
`## Cross-References` and `## Guidelines`. Context loading belongs in the refs
that execute it — never as a SKILL.md section.

### Recommended Effort

Optional single line placed immediately after the H1 title, before Workflow.
Use only for skills with cognitively heavy phases (audit, design, discovery,
review). Omit on light skills.

Format: one bold line with the effort level and a short rationale.

```markdown
**Recommended effort:** xhigh for design/audit phases; medium for quick mode.
```

Levels: `low` · `medium` · `high` · `xhigh` (default for heavy reasoning) · `max` (complex design phases only; use sparingly).

### Compact Instructions

Optional section for long-running skills where context pressure is realistic.
List what to preserve (current phase, artifact paths, open decisions) and what
to drop (raw tool outputs, scratch reasoning) when autocompact fires.

Skills that persist state to disk across phases do not need this section --
the artifact already survives `/clear` and is a stronger guarantee.

### Workflow

Simple `-->` arrows. Optional loop on second line with `^` and `|___|`.
No pipes or box-drawing. Keep lines under 70 chars.

```
phase-1 --> phase-2 --> phase-3 --> output
  ^_________________________|  (note about the loop)
```

One sentence explaining the flow right below.

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

### Discovery Types

Three fundamentally different discovery patterns exist. Placing them in the
wrong location causes bloated SKILL.md and inconsistent behavior.

**Type A — Product discovery**
Understand the problem, user, and direction before any execution. Iterative,
question-driven, no disk state. Output is direction, not artifact.
Lives in `references/discovery.md`. Loaded as the first step before triggers.
Skills: `brainstorming`, `docs-writer`, `system-design`, `spec-driven`.

**Type B — Context discovery**
Determine execution state — which artifacts exist, which project is active,
what the codebase looks like. Deterministic, reads disk and context. Output
is a routing decision.
Lives at the **start of the reference that needs it**. Never in SKILL.md.
When a skill has `discovery.md` used as pre-load, document it in Triggers
Notes (same pattern as `wrap-up` / `mapping.md`).

**Type C — Technical discovery**
Understand the solution space — requirements, trade-offs, architecture.
Exclusive to design/engineering skills. Structured by topics, adaptive depth.
Lives in `references/discovery.md` (same location as Type A, technical focus).
Skills: `system-design`, `spec-driven`.

Reference models for the correct patterns: `git-helpers`, `wrap-up`, `project-index`.

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

Optional. Create when the skill generates artifacts with a repeatable structure.
Not needed for inline skills (debug-tools, git-helpers).

Use `{{mustache}}` for dynamic values, `{single braces}` for fill-in instructions.
Name templates after the output type they generate (`report.md`, `prd.md`, `copy.yaml`).

### CHANGELOG.md

Frontmatter: `name: skill-name`.

Structure:
- `# Changelog`
- Intro line: `All notable changes to this skill will be documented in this file.`
- `## YYYY-MM-DD` per dated entry, most recent first (never versions)
- `### Added` / `### Changed` / `### Fixed` / `### Removed` subsections
- Each item is one sentence (no paragraphs)
- Reference filenames when relevant, but never lead the sentence with a filename -- start with the concept or change

### README.md

User-facing documentation. Required sections in order:

| Section | Content |
|---------|---------|
| `# Title` + tagline | One descriptive sentence |
| `## Installation` | `npx skills add adeonir/agent-skills --skill {name}` |
| `## What It Does` | Mermaid diagram + phases table |
| `## Usage` | Natural language usage examples |
| `## Output` | Output format or directory (if applicable) |
| `## Requirements` | Dependencies and external tools (if applicable) |
| `## Integration` | Connections with other skills (if applicable) |

Mermaid: `flowchart LR` or `flowchart TD` (never `graph`). Decisions `{}`, actions `[]`, labels via `-->|label|`.

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
- [ ] `Compact Instructions` section added if skill has heavy phases where autocompact could fire before the next disk write (even if the skill persists state to disk — the guarantee only holds after the write happens)
- [ ] Entrypoint skills state a first-turn brief (intent, constraints, acceptance, files)
- [ ] Skills that fan out across items instruct the model to spawn subagents explicitly
- [ ] SKILL.md is a pure dispatcher (≤ ~150 lines): only triggers, cross-refs, short guidelines — no operational logic inline
- [ ] No inline logic in SKILL.md that applies only to a subset of triggers (move it to that trigger's ref)
- [ ] Discovery type identified and placed correctly: Type A/C in `references/discovery.md`, Type B at the start of the ref that needs it

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
- **`ultrathink`**: include the word `ultrathink` anywhere in skill content to
  enable extended thinking for that skill. Use for intelligence-sensitive phases
  (audit, design, API review, multi-file analysis). Omit on light or
  latency-sensitive skills
- **Context pressure and autocompact guards**: heavy phases need two layers:
  (1) automatic mid-phase checkpoint to disk before the heaviest steps;
  (2) `Compact Instructions` as fallback if autocompact fires before the checkpoint.
  End-of-phase dumps remain opt-in. Pattern: checkpoint → opt-in dump → Compact Instructions.

## Commit Conventions

- Conventional commits: `type: description in imperative mood`
- Types: `feat`, `fix`, `refactor`, `chore`, `docs`, `test`, `style`, `perf`
- First line under 72 characters
- No scope, no emojis, no attribution (no Co-Authored-By)
- Never push without explicit confirmation

## Output Artifacts

Skills write to `.artifacts` organized by domain:

```
.artifacts/
├── features/           # spec-driven: specs, designs, tasks
├── quick/              # spec-driven: quick mode tasks
├── research/           # spec-driven: research cache
├── epics/              # epic-tracker: epics, stories, bugs, releases
├── docs/               # docs-writer: PRD, Brief, Design Doc, TDD
├── design/             # design-builder: copy, design tokens, variants
├── brainstorm/         # brainstorming: direction artifacts
└── .session-dump.md    # spec-driven: ephemeral cross-phase memory
```

`.artifacts` is excluded locally via `.git/info/exclude` on first write — it stays out of `git status` without touching the project's `.gitignore`. Commit specific files only when the user explicitly requests it.

`.artifacts/.session-dump.md` is ephemeral — written during heavy phases to survive `/clear` and autocompact, read by wrap-up at session end, then disposable. It is not a project artifact and should never be committed.

`.agents/` is a separate directory for reference context, consumed by other skills:

```
.agents/
├── project.md      # project-index: project context
├── codebase/       # project-index: deep codebase analysis
├── baselines/      # spec-driven: area behavioral baselines
└── knowledge.md    # spec-driven: decisions, gotchas, Codebase Feedback queue
```

Ownership: project-index writes `project.md` and `codebase/*.md`; spec-driven writes `knowledge.md` and `baselines/*.md`. Spec-driven discoveries land in `knowledge.md`'s `## Codebase Feedback` and merge into `codebase/*.md` via `/project-index integrate feedback`.

## Terminology

TDD has two meanings in this project depending on context:
- docs-writer: Technical Design Document (`references/tdd.md`)
- spec-driven: Test-Driven Development (`references/test-driven.md`)

## Security Audits

skills.sh audits every published skill (Gen Agent Trust Hub, Socket, Snyk). Run this self-check after any skill change:

- No plaintext passwords or API keys (use `$ENV_VAR` or `{placeholder}`)
- No `curl | sh` or piped download-and-execute patterns
- No links to untrusted or non-official domains
- External content ingestion has trust boundary in the relevant reference file
- Shell commands limited to non-destructive operations (mkdir, ls, grep)
- No instructions that could exfiltrate local data to external services

## Skill Installation

Source of truth is `skills/`. Never edit `~/.agents/skills/` or `~/.claude/skills/` -- those are install targets (symlinks). See README for `npx skills add` usage.
