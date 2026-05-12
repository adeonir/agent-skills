# CLAUDE.md

Authoring conventions for skills in this repository.

This file is **repo-level guidance for skill authors**. It is never installed
alongside skills and never reaches the consumer. Each skill ships standalone
via `skills.sh`.

## Overview

Repository of skills for AI coding agents. Markdown-first, no build system, no
tests, no linter. Validation is manual: read files, verify structure, check
cross-references within a skill.

Skills follow the [Agent Skills](https://agentskills.io) open standard.

## Repository Structure

```
agent-skills/
├── CLAUDE.md                # this file
├── README.md                # repo-level skill index
├── .artifacts/              # gitignored local artifacts
└── skills/
    ├── engineering/
    │   └── skill-name/
    ├── product/
    │   └── skill-name/
    └── personal/
        └── skill-name/
```

Skills directories use flat lowercase kebab-case names. Skill folders also
use kebab-case.

| Directory | Usage |
|-----------|-------|
| engineering | Debugging, specs, system design, codebase indexing, git tooling |
| product | Brainstorming, design, documentation, domain modeling, epic tracking |
| personal | Session notes, vault sync, auto-memory wrap-up |

## Canonical Workflow

Skills compose via artifacts on disk (`.artifacts/`, `.agents/`), not via
cross-references inside skill files. The workflow is documented here at the
repo level only:

```
brainstorming + project-index (parallel discovery)
    --> docs-writer (product requirements + technical docs)
    --> design-builder (visual identity + screens)
    --> epic-tracker (epics --> stories)
    --> spec-driven (per story: spec + design + tasks)
    --> git-helpers (atomic commits per task)
    --> wrap-up (persist context to BM + Obsidian)
```

Skills themselves stay isolated. SKILL.md files do not reference other skills
by name and do not document this pipeline.

## Skill File Layout

```
skill-name/
├── SKILL.md           # entrypoint (required)
├── README.md          # user-facing doc (required)
├── references/        # on-demand details (optional)
│   └── *.md
├── scripts/           # executables loaded on demand (optional)
└── assets/            # static data files for scripts (optional)
```

There is no `templates/` directory. Templates live inline in the reference
that uses them, 1:1 ref:template.

There is no `CHANGELOG.md` per skill. Git history is the source.

## SKILL.md

### Frontmatter

```yaml
---
name: skill-name
description: >-
  <Capability sentence>. Use when [contexts/keywords] or user
  [actions/says "X"].
argument-hint: [optional-arg]    # only when skill accepts /skill <args>
---
```

Rules:
- `name`: kebab-case, ≤64 chars, lowercase + digits + hyphens. Forbidden:
  `anthropic`, `claude`.
- `description`: ≤1024 chars, third person or noun phrase. Never first or
  second person ("I help...", "You can use...").
- Folded block `>-` with 2-space indentation. Lines under 80 chars to avoid
  obfuscation alerts during security audits.
- Triggers go inline in the description, not in a separate field.

No other frontmatter fields.

### Triggers

Use `Use when [contexts/keywords] or user [actions/says "X"]`. Mix:
- Action verbs ("committing", "reviewing changes")
- Topical keywords ("Excel files", "spreadsheets")
- Literal user phrases in quotes ("commit this", "open PR")
- Negative routing inline when ambiguous ("not for: brainstorming exploration")

Phrases must be ≥ 2 words. Never bare single words — they collide between
skills.

### Section Order

Required at the top:
1. `# Title` (H1)
2. Triggers or Quick start

After that, sections are free, named by domain. No canonical order.

Permitted sections:
- `## Philosophy` — when the skill has strong conceptual framing
- `## Anti-Pattern: <name>` — trap + prose explanation
- `## Workflow` / `## Phases` / `## <domain>` — domain-specific
- `## Guidelines` — short DO list (4-6 non-obvious items)

Forbidden sections:
- `## Cross-References` — skills are isolated
- `## Compact Instructions` — skills are stateless
- `## Output` — output spec lives in the reference that produces it
- `## Error Handling` — errors handled inline in the workflow
- `**Recommended effort:**` line — not used

### Body Length

Prefer ≤100 lines. Acceptable up to 150. Beyond that, split into references.

### Workflow Notation

ASCII with `-->` arrows. No box-drawing, no pipes. Lines under 70 chars.

```
phase-1 --> phase-2 --> phase-3 --> output
  ^_________________________|  (note about loop)
```

### Voice / Tone

Imperative neutral by default. Authorial opinionated voice (italics, bold for
emphasis) is permitted in any section when it adds clarity. No table of
contents — SKILL.md is short enough to dispense with it.

## References

Layout: `references/` subfolder, kebab-case filenames.

Required internal structure:

```markdown
# Title

One-line description.

## When to Use

[conditions that trigger this reference]

## [free sections from here]
```

After the required header, sections are free (`Workflow`, `Discovery`,
`Phases`, `Guidelines`, `Error Handling`, `Next Steps` — all optional).

References are one level deep. Link them directly from SKILL.md, never from
another reference. Nested references cause partial reads (`head -100`) and
miss content.

XML tags (`<example>`, `<instructions>`, `<input>`) are permitted in
references when content is ingested as input by the model. Default to
markdown; use tags only when structure justifies them.

## Templates

Templates are inline in the reference that uses them. One template per
reference (1:1). No reuse between references. No `templates/` folder.

Every template explicitly marks expected behavior:

- **Strict** — `ALWAYS use this exact template structure:`
- **Flexible** — `Here is a sensible default format, but use your best judgment:`

## Guidelines

Short DO list (4-6 non-obvious items). Skip DOs that are common sense.

When a real trap exists, document it as `## Anti-Pattern: <name>` with prose
explaining the failure mode and the correct alternative. Do not pair every
DON'T with a DO; if the proscription has no positive counterpart, the
Anti-Pattern section carries it alone.

## README per Skill

Required structure:

```markdown
# Skill Name

One-line tagline.

## What It Does

```mermaid
flowchart TD    # or LR — see direction rule below
...
```

| Phase | Output |
|-------|--------|
| ... | ... |

## Usage

Natural-language examples of how the user invokes the skill.

## Output (if applicable)

Where artifacts land.

## Requirements (if applicable)

External tools or MCPs.

## FAQ (if applicable)
```

Mermaid direction:
- `flowchart TD` for branching, loops, decision trees
- `flowchart LR` for linear sequential pipelines

There is no per-skill `Installation` or `Integration` section. Installation
is handled by `skills.sh`. Skills are isolated and do not document
integration with other skills.

## Discovery

Three discovery types are recognized at the authoring level. Skills do not
label them — apply the right pattern silently.

- **Type A — Product discovery.** Understand the problem, user, and
  direction before any execution. Iterative, question-driven, no disk state.
  Lives in `references/discovery.md` of skills like brainstorming,
  docs-writer, spec-driven.

- **Type B — Context discovery.** Determine execution state — which
  artifacts exist, which project is active, what the codebase looks like.
  Deterministic, reads disk and context. Lives at the **start of the
  reference that needs it**, never in SKILL.md.

- **Type C — Technical discovery.** Understand the solution space —
  requirements, trade-offs, architecture. Structured by topics, adaptive
  depth. Lives in `references/discovery.md` of design and engineering
  skills. Same location as Type A, technical focus.

## Skill Split Criteria

Create a new skill when triggers describe a job disconnected from existing
skills, or when the existing skill solves a different problem from the new
one. Otherwise, add a reference to the existing skill.

## Code and Scripts

`scripts/` and `assets/` directories are optional. Use them only when the
skill genuinely needs deterministic operations or static data.

### MCP Tools

Reference MCP tools by qualified name in SKILL.md and references:
`ServerName:tool_name` (e.g., `BigQuery:bigquery_schema`,
`GitHub:create_issue`). Without the prefix, Claude may fail when multiple
servers expose tools with the same name.

Skills using MCP must:
- Detect availability before invoking the tool
- Document fallback when MCP is unavailable
- Mark each MCP dependency as hard-required or optional

### Authoring Rules

- **Solve, don't punt.** Scripts handle errors with explicit fallbacks
  (try/except, default values). Don't return raw exceptions for Claude to
  resolve.
- **No voodoo constants.** Justify every numeric constant with a comment.
  If you don't know the right value, Claude won't either.
- **Execute vs read intent.** State whether Claude should run a script or
  read it as reference: "Run `analyze.py` to extract fields" vs "See
  `analyze.py` for the extraction algorithm".

## Authoring Discipline

These rules apply to the moment of writing skills. They affect the output,
not the runtime — consumer Claude never sees CLAUDE.md.

### Time-Sensitive Content (rigid)

Skills must be timeless. No absolute dates, no mutable version pins, no
ephemeral product state, no "soon we will" language. When legacy content
must coexist with current content, use:

```markdown
## Current method

Use the v2 endpoint: `api.example.com/v2/messages`

## Old patterns

<details>
<summary>Legacy v1 API (deprecated)</summary>

Historical context here.

</details>
```

### Consistent Terminology (rigid, with enforcement)

Choose one term per concept and keep it across SKILL.md, references, and
templates within a single skill. Mixing "field" / "box" / "element" or
"extract" / "pull" / "get" / "retrieve" makes Claude work harder.

### Output Language (rigid)

All files in the repository — SKILL.md, references, templates, README,
CLAUDE.md — are written in English. Conversation in chat may be in any
language; output files are always English.

### File Paths (rigid)

Always use forward slashes (`scripts/helper.py`, not `scripts\helper.py`).
Forward slashes work cross-platform; Windows-style paths break on Unix.

### Code Blocks (rigid)

Every fenced code block declares its language: ` ```bash `, ` ```python `,
` ```yaml `, ` ```markdown `, etc. No untagged fences.

### Token Budget Awareness

Document what each reference loads and what should never load
simultaneously. Orthogonal references (e.g., one per business domain) must
be explicit about their scope so Claude reads only what's needed.

### Recommended Patterns

- **Checklist copiável** — Multi-step workflows and decision points may
  include `- [ ]` checklists Claude marks as it progresses. Useful, not
  required.
- **Validation loop** — When a skill produces verifiable output, document
  a validator → fix → repeat loop (script or reference doc as validator).
- **Conditional workflow** — When a skill has 2+ paths, branch explicitly:
  "Creating? → workflow A. Editing? → workflow B."
- **Examples pattern** — When output style matters (commits, PR copy, code
  review notes), embed concrete I/O pairs in the reference. Pairs beat
  abstract descriptions.
- **Positive examples over proscriptions.** Show the desired form rather
  than listing what to avoid.
- **Tool-stack neutrality.** Describe behavior, not specific tools. When a
  concrete library helps, mention it as an example, not a hard requirement.

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Fixed files | UPPERCASE.md | `SKILL.md`, `README.md`, `CLAUDE.md` |
| Skill directories | kebab-case in `<category>/` | `spec-driven`, `git-helpers` |
| Category directories | lowercase, kebab-case | `engineering`, `product`, `personal` |
| Reference files | kebab-case `.md` | `quick-mode.md`, `discovery.md` |
| Sub-directories | lowercase | `references/`, `scripts/`, `assets/` |

Slash command name always equals the skill `name` (Claude Code default). No
aliases.

## Output Artifacts

Skills write outputs to `.artifacts/` organized by domain:

```
.artifacts/
├── features/      # spec-driven: specs, designs, tasks
├── quick/         # spec-driven: quick mode tasks
├── research/      # spec-driven: research cache
├── epics/         # epic-tracker: epics, stories, bugs, releases
├── docs/          # docs-writer: PRD, Brief, Design Doc, TDD
├── design/        # design-builder: copy, preview variants, generated assets
├── brainstorm/    # brainstorming: direction artifacts
└── changelog.md   # consolidated repo changelog (local-only narrative)
```

`.artifacts/` is excluded locally via `.git/info/exclude` on first write —
it stays out of `git status` without touching `.gitignore`. Commit specific
files only when explicitly requested.

`.agents/` is a separate directory for reference context consumed across
skills:

```
.agents/
├── project.md          # project-index: project context
├── codebase/           # project-index: deep codebase analysis
├── baselines/          # spec-driven: area behavioral baselines
├── knowledge.md        # spec-driven: decisions, gotchas, feedback queue
└── design/             # design-builder: DESIGN.md (visual identity)
```

Ownership: `project-index` writes `project.md` and `codebase/*.md`;
`spec-driven` writes `knowledge.md` and `baselines/*.md`;
`design-builder` writes `design/DESIGN.md`.

## Auto-Memory

The `wrap-up` skill is the only skill that interacts with auto-memory. No
other skill reads from or writes to memory.

## Subagent Fan-Out

Skills never delegate to subagents automatically. The user can request
fan-out explicitly in their prompt; the skill itself executes inline.

## Terminology Disambiguation

`TDD` has two meanings depending on the skill:
- **`docs-writer`** — Technical Design Document (artifact type)
- **`spec-driven`** — implements red-green-refactor tests, but does not
  follow strict Test-Driven Development discipline

## Security Audit

`skills.sh` audits every published skill (Gen Agent Trust Hub, Socket,
Snyk). Run this self-check after any skill change:

- No plaintext passwords or API keys (use `$ENV_VAR` or `{placeholder}`)
- No `curl | sh` or piped download-and-execute patterns
- No links to untrusted or non-official domains
- External content ingestion has a trust boundary in the relevant
  reference file
- Shell commands limited to non-destructive operations (`mkdir`, `ls`,
  `grep`)
- No instructions that could exfiltrate local data to external services

## New Skill Checklist

Before finalizing a new skill, verify:

- [ ] Folder at `skills/<category>/skill-name/`
- [ ] `SKILL.md` ≤100-150 lines, with required top (H1 + Triggers/Quick start)
- [ ] Frontmatter minimal (`name` + `description` [+ `argument-hint`])
- [ ] Description in third person or noun phrase, with inline triggers
- [ ] Triggers ≥ 2 words, no bare single word
- [ ] References in `references/` with H1 + description + `## When to Use`
- [ ] Templates inline in their reference, marked strict or flexible
- [ ] No cross-references to other skills
- [ ] No time-sensitive content
- [ ] Consistent terminology across SKILL.md, references, templates
- [ ] All file paths use forward slashes
- [ ] All code blocks have a language tag
- [ ] `README.md` present with mermaid + Usage
- [ ] Skill listed in repo `README.md` table
- [ ] Security audit checklist passes

## Reference Exemplars

When in doubt about how a pattern is applied, study these two skills:

- **`brainstorming`** (simple) — argument-hint exception, template
  inline 1:1 strict, three Anti-Patterns in prose, three refs covering
  distinct phases.
- **`spec-driven`** (complex) — eight templates inline 1:1, sub-agent
  fan-out + Plan dispatch, Knowledge Verification Chain, Artifact
  Structure Authority. Demonstrates the refactor at scale.

## Skill Installation

Source of truth is `skills/`. Never edit `~/.agents/skills/` or
`~/.claude/skills/` — those are install targets (symlinks). See repo
`README.md` for `skills.sh` usage.
