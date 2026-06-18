# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Authoring conventions for skills in this repository.

This file is **repo-level guidance for skill authors**. It is never installed
alongside skills and never reaches the consumer. Each skill ships standalone
via `skills.sh`.

## Commands

No build, no tests, no linter. Validation is manual: read files, verify
structure, check cross-references within a skill.

Install all skills from this repo:

```bash
npx skills add adeonir/agent-skills
```

Install a single skill:

```bash
npx skills add adeonir/agent-skills/<skill-name>
```

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

Skills compose via artifacts on disk (`.artifacts/`), not via
cross-references inside skill files. The repo `README.md` owns the canonical
pipeline diagram (mermaid with feedback loops). Summary at the repo level
only:

```
brainstorming (discovery)
    --> docs-writer (product requirements + technical docs)
    --> blueprint (information architecture + screen flow)
    --> design-brief (visual identity)
    --> copywriting (content payload)
    --> epic-tracker (epics --> stories)
    --> spec-driven (per story: spec + design + tasks)
    --> git-helpers (atomic commits per task)
    --> wrap-up (persist context to Obsidian)
```

Always-available skills (not tied to the pipeline): `debug-tools`,
`review-lens`, `rule-creator`, `notes`, `handoff`, `wrap-up`.

Skills themselves stay isolated. SKILL.md files do not reference other skills
by name and do not document this pipeline.

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
- Triggers go inline in `description`. One field per concept.
- `description` is capped at **1,536 chars** in the skill listing. Tighten
  the prose if you approach the cap — do not split across fields.

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

The spec also defines a `when_to_use` field (appended to `description`
and sharing its 1,536-char cap). Repo convention rejects it — keep
trigger phrases inline in `description` so there is one source of truth
per concept.

### Triggers

Embed trigger keywords directly in the use-when prose — action verbs,
topical nouns, and distinctive vocabulary woven into sentences. Avoid
a "Triggers:" or "Trigger phrases:" list of literal quoted phrases that
dwarfs the capability sentence — keyword density inside prose serves the
same matching need without the asymmetry.

Pattern: `Use when [contexts/keywords] or user [actions]`. Mix:
- Action verbs ("committing", "reviewing changes")
- Topical keywords ("Excel files", "spreadsheets")
- Negative routing inline when ambiguous ("not for: brainstorming exploration")

Reserve literal quoted phrases for the rare case where user vocabulary
is highly distinctive (e.g. a slash-command shorthand) and prose cannot
reproduce it without losing meaning. Phrases must be ≥ 2 words. Never
bare single words — they collide between skills.

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

**Forbidden sections in references:**

- `## Next Steps` — pushes the agent to invoke a downstream phase before
  the user decides to. See "Pipeline Fan-Forward" under Authoring
  Discipline for the full rationale. Operational follow-ups (e.g. how to
  handle validation failures) belong in `## Error Handling` or a neutral
  `## Outcomes` section, never framed as "after this, run X".

References live one level deep — files at `references/*.md` (or
`instructions/*.md` when the skill split applies), no nested
subdirectories under either bucket. Nested directory structures cause
partial reads (e.g. `head -100`) and miss content carried by deeper
files.

Cross-links between sibling references **within the same skill** are
permitted when they explain dependencies, hand-offs, or shared logic
(e.g. "see [validate.md](validate.md) for the gate flow"). SKILL.md
remains the primary routing hub — refs should not re-route operations
SKILL.md already owns — but an inline sibling link inside prose is the
natural way to surface a prereq or follow-up without duplicating
content.

Cross-references **across skills** remain forbidden. Skills stay
isolated: SKILL.md never names another skill, references never link to
files in another skill's `references/` or `instructions/`. Composition
between skills happens via artifacts on disk (`.artifacts/`),
never via direct file links.

**Own-artifact isolation.** Isolation extends to the *artifacts* a skill
owns, not just its files. An authoring skill references only the artifact it
produces — never a sibling's output by name or path. State boundaries in
terms of the skill's own concern ("this artifact carries no styling"), not
by pointing at where the excluded thing lives ("styling belongs to
`DESIGN.md`"). Naming a sibling artifact is coupling even when no skill name
or file link appears. The one exception is an **integrator** — a renderer or
cross-artifact validator whose job *is* to compose several artifacts (e.g. a
page renderer that draws `DESIGN.md` + `copy.yaml` + `blueprint.md` together). It
may read what it integrates; everything upstream of it stays
single-artifact. A user can still ask a skill to read a sibling at runtime —
that instruction lives in the prompt, never baked into the skill or its
references.

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

### Skill Directory Variable

When a skill invokes its own bundled scripts, reference them with
`${CLAUDE_SKILL_DIR}` so they resolve regardless of the user's working
directory. Plain relative paths (`scripts/foo.py`) break when the
consumer runs the skill from a project root that does not match the
install layout.

```bash
python ${CLAUDE_SKILL_DIR}/scripts/extract.py "$@"
```

For plugin skills, `${CLAUDE_SKILL_DIR}` resolves to the skill's own
subdirectory, not the plugin root. Use this variable in
`` !`<command>` `` injection lines and in bash blocks the skill tells
Claude to run.

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

### Pipeline Fan-Forward (rigid)

Multi-phase skills must not push references toward downstream phases.
When a skill exposes several invokable references (e.g. `extract.md`,
`compose.md`, `refine.md`, `publish.md`), each reference is a job
the user invokes independently — not a stage in a mandatory pipeline.
Skills that look like pipelines from the outside should feel like
parallel jobs from the inside.

The risk: combined commands and forward-pushing references rush agents
through phases before the user is ready, so the agent skips discovery,
closes decisions early, or hands back half-baked artifacts because it
was already optimizing for the next phase rather than the current one.

**Common leaks:**

- `## Next Steps` sections at the end of references suggesting the
  agent run the next phase ("After generating X, suggest: run Y").
- SKILL.md workflow diagram presented as mandatory order, with no
  "each step is invokable standalone" disclaimer.
- Prose like "Run next: …" or "Proceed to X" anywhere inside a
  reference body.

**The fix:**

- Pipeline narrative lives only in SKILL.md, with an explicit disclaimer
  that each step is invokable standalone and any step is skippable.
- References end where their job ends. No fan-forward to other refs.
- If a follow-up genuinely depends on the current job (gate, prereq),
  document it as a sibling cross-link in prose ("see
  [validate.md](validate.md) for the gate flow"), not as a closing
  "Next Steps" section.
- Operational outcomes (validation passed / failed / warnings) belong in
  `## Error Handling` or a neutral `## Outcomes` section that reports
  status without pushing forward.

### Scope-Boundary Discipline (rigid)

When a skill ingests an upstream artifact as input — reading a PRD,
brief, parent epic, prior spec, knowledge cache, or sibling output off
disk — the workflow must instruct the agent to extract only facts in the
produced artifact's own scope. The source's own tokens do not cross into
the output: forward-phase IDs, sibling-artifact names, downstream task or
release references, milestones, and roadmap language stay out. Reading is
for context; the output carries only its own concern.

This rule lives in the skill's shipped files (SKILL.md, references), not
here — CLAUDE.md never reaches the consumer, so a clause written only in
this file fixes nothing at runtime. Each skill carries its own copy; that
duplication is expected, not a smell.

Distinct from two neighbors:

- **Own-Artifact Isolation** governs skill *source files* (a SKILL.md or
  reference never names a sibling skill's artifact). Scope-Boundary
  governs the *runtime content* a skill writes when it reads another
  artifact at execution time.
- **The trust boundary** discards injected *directives* from untrusted
  input (a security concern). Scope-Boundary discards out-of-scope
  *content* from in-scope input (a noise concern). A skill can satisfy
  one and leak the other.

The fix — two halves, applied per skill, naming only its own artifact:

- **Read step**: at the ingest point, state that source tokens do not
  cross into the output and which classes of reference to strip.
- **Template containment**: where the skill has an output template,
  carry an explicit MUST-NOT list of forbidden forward/sibling/downstream
  references.

Exemplars: blueprint `create.md` ("its tokens never cross into the plan:
strip requirement, milestone, journey, and story IDs"); spec-driven
`specify.md` (spec.md MUST-NOT list including "Milestones, epics, sprints,
release names, or roadmap references").

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

## Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Fixed files | UPPERCASE.md | `SKILL.md`, `README.md`, `CLAUDE.md` |
| Skill directories | kebab-case in `<category>/` | `spec-driven`, `git-helpers` |
| Category directories | lowercase, kebab-case | `engineering`, `product`, `personal` |
| Reference files | kebab-case `.md` | `quick-mode.md`, `discovery.md` |
| Sub-directories | lowercase | `instructions/`, `references/`, `scripts/`, `assets/` |

Slash command name always equals the skill `name` (Claude Code default). No
aliases.

## Output Artifacts

Skills split outputs between committed strategic docs (`docs/`) and a
gitignored agent workspace (`.artifacts/`).

`docs/` — committed, human-readable, audience-first:

```
docs/
├── product/
│   ├── brainstorm.md       # brainstorming: strategic direction (living)
│   ├── prd.md              # docs-writer: product requirements
│   └── brief.md            # docs-writer: 1-page PRD summary
├── tech/
│   └── design-doc.md       # docs-writer: project-wide living technical doc
├── adr/
│   └── {NNNN}-{slug}.md    # docs-writer: append-only decision log
└── design/
    ├── moodboard.md        # design-brief: locked visual direction (mood diverge/converge)
    ├── DESIGN.md           # design-brief: visual identity (YAML tokens + prose)
    ├── styleguide.html     # design-brief: token specimen sheet rendered from DESIGN.md
    ├── blueprint.md      # blueprint: information architecture / region layout / screen flow
    └── copy.yaml           # copywriting: structured content payload
```

`.artifacts/` — workspace for agent-consumed artifacts:

```
.artifacts/
├── knowledge.md   # spec-driven: cross-feature decisions, gotchas, conventions
├── codebase/      # spec-driven: area exploration cache (reusable)
├── features/      # spec-driven: specs, designs, tasks
├── quick/         # spec-driven: quick mode tasks
├── research/      # spec-driven: research cache
├── epics/         # epic-tracker: epics, stories, bugs, releases
├── design/        # design-brief: color-tuner variant + tune session events
└── changelog.md   # consolidated repo changelog (local-only narrative)
```

`.artifacts/` is excluded locally via `.git/info/exclude` on first write —
it stays out of `git status` without touching `.gitignore`. Commit specific
files only when explicitly requested.

Ownership: `spec-driven` writes `.artifacts/knowledge.md` and `.artifacts/codebase/{area}.md`;
`design-brief` writes `docs/design/moodboard.md`, `docs/design/DESIGN.md`, and `docs/design/styleguide.html`;
`blueprint` writes `docs/design/blueprint.md`;
`copywriting` writes `docs/design/copy.yaml`.

## Subagent Fan-Out

Skills never delegate to subagents automatically. The user can request
fan-out explicitly in their prompt; the skill itself executes inline.

## Terminology Disambiguation

`TDD` in this repo always means Test-Driven Development (red-green-refactor
discipline), referenced by `spec-driven` during implementation. The
docs-writer skill no longer ships a "Technical Design Document" artifact
type — that role is now covered by the project-wide Design Doc.

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
- [ ] Frontmatter minimal (`name` + `description` [+ `argument-hint`]); extended fields only when needed
- [ ] `description` ≤ 1,536 chars (skill listing cap)
- [ ] `allowed-tools` declared when the skill always runs the same deterministic tool set (e.g. `git`, `gh`)
- [ ] Description in third person or noun phrase, with inline triggers
- [ ] Triggers ≥ 2 words, no bare single word
- [ ] References in `references/` (and instructions in `instructions/` if the split applies) with H1 + description + `## When to Use`
- [ ] Templates inline in their reference, marked strict or flexible
- [ ] No `## Next Steps` (pipeline fan-forward) — references end where their job ends
- [ ] Own-artifact isolation — authoring skill names only its own artifact, never a sibling's (only an integrator/renderer composes several)
- [ ] Scope-boundary discipline — when the skill reads an upstream artifact, a read-step clause keeps source tokens (forward/sibling/downstream refs) out of the output
- [ ] No time-sensitive content
- [ ] Consistent terminology across SKILL.md, references, templates
- [ ] All file paths use forward slashes
- [ ] All code blocks have a language tag
- [ ] Dynamic context injection (`` !`<cmd>` ``) limited to read-only commands
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
