# CLAUDE.md

Authoring conventions for skills in this repository.

This file is **repo-level guidance for skill authors**. It is never installed
alongside skills and never reaches the consumer. Each skill ships standalone
via `skills.sh`.

## Rules

Verifiable conventions live as path-scoped rules in `.claude/rules/`, loaded
automatically when editing skill files. Each is an Incorrect/Correct rule
managed with the rule-creator skill. This file keeps the structural and
narrative guidance that is not a discrete rule.

| Rule file | Scope | Covers |
|-----------|-------|--------|
| `markdown-conventions` | global | code fences carry a language, forward slashes, English-only |
| `naming-conventions` | global | file and directory casing, slash command equals name |
| `skill-isolation` | `skills/**` | no cross-skill refs, own-artifact isolation, inline subagents |
| `skill-frontmatter` | `SKILL.md` | description voice, inline triggers, name tokens, no `when_to_use` |
| `skillmd-structure` | `SKILL.md` | required top, forbidden sections, body length |
| `skill-references` | `skills/**` | one level deep, required header, no fan-forward |
| `skill-templates` | `skills/**` | inline 1:1, no `templates/` folder, marked strict or flexible |
| `scope-boundary` | `skills/**` | strip upstream scope from output, MUST-NOT in templates |
| `skill-scripts-mcp` | `skills/**` | `${CLAUDE_SKILL_DIR}`, qualified MCP names, no voodoo constants, scripts handle own errors |
| `skill-timeless` | `skills/**` | no dates or version pins, consistent terminology |
| `skill-security` | `skills/**` | no secrets, no piped download-execute, trust boundary, safe shell |

## Commands

No build, no tests, no linter. Validation is manual: read files, verify
structure, check cross-references within a skill.

After editing a skill, the self-checks worth running over its directory
(`skills/<category>/<skill>/`):

```bash
grep -rn '^```$' .              # bare fences are closings; every opening must carry a language
grep -rn '\.md)' .             # spot-check that every relative link target still exists
grep -rln '<sibling-skill>' .  # isolation: a skill never names a sibling (expect empty)
```

Also confirm the `description` stays within the 1,536-char listing cap.

## Overview

Repository of skills for AI coding agents. Markdown-first.

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
| engineering | Debugging, specs, system design, code review, git tooling |
| product | Brainstorming, design, documentation, domain modeling, epic tracking |
| personal | Session notes, vault sync, end-of-session wrap-up |

## Canonical Workflow

Skills compose via artifacts on disk (`.artifacts/`), not via cross-references
inside skill files. The repo `README.md` owns the pipeline diagram and the skill
index — this file does not duplicate them.

## Skill File Layout

Default — flat `references/` for the on-demand bundle:

```
skill-name/
├── SKILL.md           # entrypoint (required)
├── README.md          # user-facing doc (required)
├── references/        # on-demand details (optional)
│   └── *.md
├── scripts/           # executables loaded on demand (optional)
└── assets/            # static data files for scripts (optional)
```

Split — `instructions/` + `references/` when files genuinely mix intent
(≥2 procedural workflows AND ≥2 lookup-style references). The signal
is intent mix, not file count.

```
skill-name/
├── SKILL.md           # entrypoint (required)
├── README.md          # user-facing doc (required)
├── instructions/      # invokable workflow files (e.g. one per trigger)
│   └── *.md
├── references/        # lookup tables, principles, enums, rules
│   └── *.md
├── scripts/           # executables loaded on demand (optional)
└── assets/            # static data files for scripts (optional)
```

Classification rule:

- **Instruction** — procedural workflow the user (or another instruction)
  invokes to do a job. Has a `## Workflow` with numbered steps. The
  agent acts on it.
- **Reference** — lookup material the workflows compose (style axes,
  validation rules, technical principles, naming taxonomies). The agent
  reads it for context but does not "run" it.

Stay flat when in doubt. Splitting too early adds path overhead without
information gain. Split when the directory has both invokable files and
files that exist purely to be composed by others.

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

#### Extended Fields

The Claude Code harness accepts additional frontmatter fields beyond
`name` and `description`. Use them only when the skill needs the behavior
— every extra field is a maintenance surface and a divergence from the
open Agent Skills standard.

| Field | When to use |
|-------|-------------|
| `allowed-tools` | When the skill always runs the same deterministic tool set (e.g. `git`, `gh`, specific MCPs). Pre-approves them to skip per-use prompts. Space-separated string or YAML list. Example: `Bash(git:*) Bash(gh:*) Read Write Task`. |
| `argument-hint` | When the skill accepts `/skill <args>`. Shown during autocomplete. |
| `context: fork` + `agent` | When the skill is a self-contained task that should run in an isolated subagent context with no parent history. `agent` picks the subagent type (e.g. `Explore`). Rare — most skills run inline. |
| `paths` | Glob patterns that auto-activate the skill on matching files. Comma-separated string or YAML list. |
| `disable-model-invocation` | `true` blocks automatic loading. Use for irreversible workflows (`/deploy`, `/send-slack`) where the human must control timing. |
| `user-invocable` | `false` hides from the `/` menu. For background knowledge the user should not invoke directly. |
| `model` / `effort` | Override the active model or effort for the skill turn. Rare — defaults inherit the session. |
| `hooks` | Skill-scoped lifecycle hooks. Rare. |

Use the same folded-block `>-` style for any multi-line field.

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

### Workflow Notation

Use `→` arrows. No box-drawing, no pipes. Lines under 70 chars.

```
phase-1 → phase-2 → phase-3 → output
  ^_________________________|  (note about loop)
```

### Voice / Tone

Imperative neutral by default. Authorial opinionated voice (italics, bold for
emphasis) is permitted in any section when it adds clarity. No table of
contents — SKILL.md is short enough to dispense with it.

## References and Instructions

Layout: `references/` subfolder for lookup material, optional
`instructions/` subfolder for procedural workflows when the split
criteria in [Skill File Layout](#skill-file-layout) apply. Same
internal structure, same kebab-case filenames, same rules apply to both
buckets — the only difference is intent (workflows act, references
inform). The rest of this section uses "reference" to mean a file in
either bucket.

Required internal structure:

```markdown
# Title

One-line description.

## When to Use

[conditions that trigger this reference]

## [free sections from here]
```

After the required header, sections are free (`Workflow`, `Discovery`,
`Phases`, `Guidelines`, `Error Handling` — all optional).

Cross-links between sibling references **within the same skill** are
permitted when they explain dependencies, hand-offs, or shared logic
(e.g. "see [validate.md](validate.md) for the gate flow"). SKILL.md
remains the primary routing hub — refs should not re-route operations
SKILL.md already owns — but an inline sibling link inside prose is the
natural way to surface a prereq or follow-up without duplicating
content.

XML tags (`<example>`, `<instructions>`, `<input>`) are permitted in
references when content is ingested as input by the model. Default to
markdown; use tags only when structure justifies them.

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

State whether Claude should run a script or read it: "Run `analyze.py` to
extract fields" vs "See `analyze.py` for the extraction algorithm".

Skills using MCP must detect availability before invoking the tool, document a
fallback when the MCP is unavailable, and mark each dependency hard-required or
optional.

## Authoring Discipline

These conventions apply at the moment of writing skills; they affect the output,
not the runtime — consumer Claude never sees CLAUDE.md. The rigid, verifiable
ones are enforced by rules in `.claude/rules/`; what remains here is guidance
that is not a discrete rule.

### Token Budget Awareness

Document what each reference loads and what should never load
simultaneously. Orthogonal references (e.g., one per business domain) must
be explicit about their scope so Claude reads only what's needed.

### Dynamic Context Injection

Workflow files (SKILL.md, instructions, references) may embed
`` !`<command>` `` placeholders. The harness runs the command before
the file is sent to the model and substitutes the output inline. Claude
receives data, not the command. Substitution runs once over the
original file; injected output is not re-scanned for further
placeholders.

Use this at the top of workflows whose first step is gathering state
(git status, gh queries, file existence) to remove the "run command,
then act on output" round-trip:

```markdown
## Current state

!`git status --short`
!`git diff --staged`
!`git log --oneline -10 --no-merges`
```

Rules:
- Inline form only. No nested or recursive substitution.
- Commands must be safe and read-only (`git`, `gh`, `ls`, `cat`, `awk`
  on local files). Never inject mutating commands (`rm`, `git push`,
  `gh pr merge`).
- Steps that consume the output reference the section by name ("the
  staged diff above"), not re-run the command.
- Substitutions available inside any skill file: `${CLAUDE_SKILL_DIR}`,
  `${CLAUDE_PROJECT_DIR}`, `${CLAUDE_SESSION_ID}`, `${CLAUDE_EFFORT}`,
  `$ARGUMENTS`, `$0`/`$1`/... or `$ARGUMENTS[N]`.
- The user can disable injection globally via the
  `disableSkillShellExecution` setting. Skills must still be readable
  and useful when that happens — treat injection as a fast path, not a
  required dependency.

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

## Output Artifacts

Skills split outputs between committed strategic docs (`docs/`) and a
gitignored agent workspace (`.artifacts/`).

`docs/` — committed, human-readable, audience-first; `.artifacts/` — gitignored
agent workspace. The owning skill is in the comment; each skill documents its own
outputs in its README.

```
docs/
├── product/   # brainstorming, docs-writer
├── tech/      # docs-writer
├── adr/       # docs-writer
└── design/    # design-brief, blueprint, copywriting

.artifacts/
├── knowledge.md, codebase/, features/, quick/, research/   # spec-driven
├── epics/     # epic-tracker
└── design/    # design-brief; design/variants/ # craft-ui
```

`.artifacts/` is excluded locally via `.git/info/exclude` on first write —
it stays out of `git status` without touching `.gitignore`. Commit specific
files only when explicitly requested.

## Terminology Disambiguation

`TDD` in this repo always means Test-Driven Development (red-green-refactor
discipline), referenced by `spec-driven` during implementation. The
docs-writer skill no longer ships a "Technical Design Document" artifact
type — that role is now covered by the project-wide Design Doc.

`register` / `surface` are shared design vocabulary across `craft-ui`,
`design-brief`, `copywriting`, and `blueprint`: **register** = posture (`brand`
vs `product`, two values), **surface** = granular type named by context. Each
skill carries its own `brand.md` + `product.md`; the terms must not diverge.

## New Skill Checklist

Before finalizing a new skill, verify the items the path-scoped rules in
`.claude/rules/` do not enforce — the rules cover the rest automatically when
you edit a skill file:

- [ ] Folder at `skills/<category>/skill-name/`
- [ ] Frontmatter minimal (`name` + `description` [+ `argument-hint`]); extended fields only when needed
- [ ] `description` ≤ 1,536 chars (skill listing cap)
- [ ] `allowed-tools` declared when the skill always runs the same deterministic tool set (e.g. `git`, `gh`)
- [ ] Dynamic context injection (`` !`<cmd>` ``) limited to read-only commands
- [ ] `README.md` present with mermaid + Usage
- [ ] Skill listed in repo `README.md` table
- [ ] No links to untrusted or non-official domains

`skills.sh` runs the published security audit (Gen Agent Trust Hub, Socket,
Snyk) on every skill. The `skill-security` rule already covers secrets, piped
download-execute, trust boundaries, and safe shell — the domain-trust check
above is the one audit item that lives outside the rules.

## Reference Exemplars

When in doubt about a pattern, study `brainstorming` (simple — inline templates,
prose Anti-Patterns), `spec-driven` (complex — many templates, sub-agent fan-out,
the refactor at scale), or `review-lens` (two peer modes sharing one rubric, model
tiering).

## Skill Installation

Source of truth is `skills/`. Never edit `~/.agents/skills/` or
`~/.claude/skills/` — those are install targets (symlinks). See repo
`README.md` for `skills.sh` usage.
