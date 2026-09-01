# AGENTS.md

Authoring conventions for skills in this repository.

This file is **repo-level guidance for skill authors**. It is never installed alongside skills and never reaches the consumer. Each skill ships standalone via `skills.sh`.

## Rules

Verifiable conventions live as rules in `.agents/rules/`, loaded automatically when editing skill files. Each rule is managed with the rule-creator skill and uses examples only when they clarify the constraint. This file keeps the structural and narrative guidance that is not a discrete rule.

| Rule file | Scope | Covers |
|-----------|-------|--------|
| `.agents/rules/content-style` | global | English-only files, direct prose, placeholder syntax, authoring style |
| `.agents/rules/markdown-conventions` | global | code fences carry a language, forward slashes, English-only |
| `.agents/rules/naming-conventions` | global | file and directory casing, slash command equals name |
| `.agents/rules/skill-md-structure` | `SKILL.md` | no constraint in a routing SKILL.md, instructions as the only routing target, required top, forbidden sections, routing over bulk reads, body length |
| `.agents/rules/skill-timeless` | `skills/**` | no dates or version pins, consistent terminology |
| `.agents/rules/skill-references` | `skills/**` | one instruction per job, shared constraint loaded as a step, one level deep, required header, no fan-forward |
| `.agents/rules/skill-voice` | `skills/**` | no authoring-chat rationale, declarative not narrated |
| `.agents/rules/scope-boundary` | `skills/**` | strip upstream scope from output, MUST-NOT in templates |
| `.agents/rules/skill-isolation` | `skills/**` | no cross-skill refs, own-artifact isolation, inline subagents |
| `.agents/rules/skill-templates` | `skills/**` | inline 1:1, no `templates/` folder, marked strict or flexible |
| `.agents/rules/skill-security` | `skills/**` | no secrets, no piped download-execute, trust boundary, safe shell |
| `.agents/rules/inbound-posture` | `skills/**` | upstream artifact enters as a claim, not authority; read step states the rebuttal |
| `.agents/rules/skill-scripts-mcp` | `skills/**` | bundled script paths, qualified MCP names, no voodoo constants, scripts handle own errors |
| `.agents/rules/skill-frontmatter` | `SKILL.md` | description voice, inline triggers, name tokens, no `when_to_use`, no angle brackets, negative scope, argument-hint grammar |

## Commands

No build, no tests, no linter. Validation is manual: read files, verify structure, check cross-references within a skill.

After editing a skill, the self-checks worth running over its directory (`skills/<category>/<skill>/`):

```bash
grep -n '(references/' SKILL.md                     # the entrypoint routes instructions only (expect empty when instructions/ exists)
grep -n '^## \(Anti-Pattern\|Guidelines\)' SKILL.md # constraints in a routing entrypoint (expect empty when instructions/ exists)
grep -n '^## When to Use' instructions/*.md         # an instruction carries none (expect empty)
for f in instructions/*.md; do b=$(basename "$f"); grep -q "instructions/$b" SKILL.md || echo "orphan: $f"; done
for f in references/*.md; do b=$(basename "$f"); grep -rq "$b" instructions/ references/ --exclude="$b" || echo "never loaded: $f"; done
grep -rho '](\.\./references/[a-z-]*\.md)' instructions/ | sed 's|](\.\./references/||;s|)||' | sort -u \
  | while read t; do [ -f "references/$t" ] || echo "missing: $t"; done
grep -rn '^```$' .              # bare fences are closings; every opening must carry a language
grep -rln '<sibling-skill>' .  # isolation: a skill never names a sibling (expect empty)
```

Also confirm the `description` stays within the 1,024-char listing cap.

## Overview

Repository of skills for AI coding agents. Markdown-first.

Skills follow the [Agent Skills](https://agentskills.io) open standard.

## Repository Structure

```text
agent-skills/
├── AGENTS.md                # this file
├── CLAUDE.md                # points to AGENTS.md
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

Skills directories use flat lowercase kebab-case names. Skill folders also use kebab-case.

| Directory | Usage |
|-----------|-------|
| engineering | Debugging, specs, system design, code review, git tooling |
| product | Brainstorming, design, documentation, domain modeling, epic tracking |
| personal | Session notes, vault sync, end-of-session wrap-up |

## Canonical Workflow

Skills compose via artifacts on disk (`.artifacts/`), not via cross-references inside skill files. The repo `README.md` owns the pipeline diagram and the skill index — this file does not duplicate them.

## Skill File Layout

Count the jobs the skill does. A job runs end to end and produces its own outcome; a mode that changes only what the procedure returns, an entry state that changes only where it starts, and a phase inside it are all part of one job.

One job — no `instructions/`. The SKILL.md is the procedure and loads what it needs as a step:

```text
skill-name/
├── SKILL.md           # entrypoint and procedure (required)
├── README.md          # user-facing doc (required)
├── references/        # what a step loads (optional)
│   └── *.md
├── scripts/           # executables loaded on demand (optional)
└── assets/            # static files for scripts or render output (optional)
```

Several jobs — one instruction per job, and the SKILL.md routes to them:

```text
skill-name/
├── SKILL.md           # entrypoint, routing only (required)
├── README.md          # user-facing doc (required)
├── instructions/      # one file per job, the routing targets
│   └── *.md
├── references/        # what a step loads (optional)
│   └── *.md
├── scripts/           # executables loaded on demand (optional)
└── assets/            # static files for scripts or render output (optional)
```

Classification rule:

- **Instruction** — a procedure the SKILL.md routes to, executed end to end. Several triggers may route to the same one when they share a procedure.
- **Reference** — what a procedure loads from inside a step: lookup material, a shared constraint, a contract. It carries no trigger and is never a routing target.

A file reachable both ways — routed from the top and loaded by a procedure — is doing two jobs and needs splitting.

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

The Claude Code harness accepts additional frontmatter fields beyond `name` and `description`. Use them only when the skill needs the behavior — every extra field is a maintenance surface and a divergence from the open Agent Skills standard.

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

A routing SKILL.md stops there, plus the flow diagram. Everything that changes what an instruction produces belongs to that instruction or to a reference it loads.

A one-job SKILL.md is the procedure, so it carries the procedure's own sections. After the required top, they are free and named by domain, in no canonical order:

- `## Philosophy` — when the skill has strong conceptual framing
- `## Anti-Pattern: <name>` — an observed trap + the correct alternative
- `## Workflow` / `## Phases` / `## <domain>` — domain-specific
- `## Guidelines` — short DO list (4-6 non-obvious items)

The same sections are available to an instruction, whatever the skill's shape.

### Workflow Notation

Use `→` arrows. Box-drawing is welcome where it sharpens structure — branches and convergence read best with `├ └ ┐ ┴ ┼ ┘ │`. Keep simple flows linear and lines under 70 chars.

```text
phase-1 → phase-2 → phase-3 → output
  ^_________________________|  (loop back)

a → b → c
    ├→ d ┐
    └→ e ┴→ f
```

### Voice / Tone

Imperative neutral by default. Authorial opinionated voice (italics, bold for emphasis) is permitted in any section when it adds clarity. No table of contents — SKILL.md is short enough to dispense with it.

## References and Instructions

Both buckets share the kebab-case filenames and every rule in `.agents/rules/`. They differ in who puts the file in context: the SKILL.md routes an instruction, a step loads a reference.

A reference opens with its title, a one-line description, and `## When to Use` — what loading it buys:

```markdown
# Title

One-line description.

## When to Use

[what loading this file settles]

## [free sections from here]
```

An instruction opens with its title, a one-line description, and the step that loads what it needs before the job starts. It carries no `## When to Use`: the SKILL.md already named the condition that routed to it.

After the required header, sections are free (`Workflow`, `Discovery`, `Phases`, `Guidelines`, `Error Handling` — all optional).

A constraint two instructions need lives in one reference, and each instruction loads it as a step at the point of use. A prose mention is not the mechanism — an agent working through an instruction applies what a step tells it to load, and reads a bare cross-link as background it may skip. The threshold is size: a constraint that fits in one sentence stays inline in each instruction, and one that needs a block earns the reference.

Sibling cross-links **within the same skill** stay available for a genuine dependency or hand-off. They never re-route an operation the SKILL.md already owns, and a reference never links forward into an instruction.

XML tags (`<example>`, `<instructions>`, `<input>`) are permitted in references when content is ingested as input by the model. Default to markdown; use tags only when structure justifies them.

## Guidelines

Short DO list (4-6 non-obvious items). Skip DOs that are common sense.

When a real trap exists, document it as `## Anti-Pattern: <name>` with prose explaining the failure mode and the correct alternative. Do not pair every DON'T with a DO; if the proscription has no positive counterpart, the Anti-Pattern section carries it alone.

A trap is found, not derived. It names something an agent did — in a run, in a shipped artifact, in a failure the user hit — and it earns a section because the constraint alone did not stop it. A trap written to guard a rule the same edit introduced is that rule in costume: the constraint already states itself, the section only says it louder, and the prose reads as evidence the failure happens. Where nothing was observed, the constraint ships alone.

## README per Skill

Required structure:

````markdown
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
````

Mermaid direction:
- `flowchart TD` for branching, loops, decision trees
- `flowchart LR` for linear sequential pipelines

There is no per-skill `Installation` or `Integration` section. Installation is handled by `skills.sh`. Skills are isolated and do not document integration with other skills.

## Discovery

Three discovery types are recognized at the authoring level. Skills do not label them — apply the right pattern silently.

- **Type A — Product discovery.** Understand the problem, user, and direction before any execution. Iterative, question-driven, no disk state. Lives in `references/discovery.md` of skills like brainstorm, docs-writer, spec-driven.

- **Type B — Context discovery.** Determine execution state — which artifacts exist, which project is active, what the codebase looks like. Deterministic, reads disk and context. Lives at the **start of the reference that needs it**, never in SKILL.md.

- **Type C — Technical discovery.** Understand the solution space — requirements, trade-offs, architecture. Structured by topics, adaptive depth. Lives in `references/discovery.md` of design and engineering skills. Same location as Type A, technical focus.

## Skill Split Criteria

Create a new skill when triggers describe a job disconnected from existing skills, or when the existing skill solves a different problem from the new one. Otherwise, add a reference to the existing skill.

## Code and Scripts

`scripts/` and `assets/` directories are optional. Use them only when the skill genuinely needs deterministic operations or static assets — data files for a script, or a file the render inlines into its output (e.g. a stylesheet).

State whether Claude should run a script or read it: "Run `analyze.py` to extract fields" vs "See `analyze.py` for the extraction algorithm".

A script's language follows the job, not the skill: pure computation and text validators are Python stdlib (`slop_scan.py`, `validate_copy.py`, `check-contrast.py`); live web preview and render servers are bun/TS (`render-server.ts`, `preview-server.ts`). Match an existing sibling's conventions when adding one — a skill that ships both runtimes declares each in `allowed-tools` (`Bash(bun:*) Bash(python3:*)`).

Skills using MCP must detect availability before invoking the tool, document a fallback when the MCP is unavailable, and mark each dependency hard-required or optional.

## Authoring Discipline

These conventions apply at the moment of writing skills; they affect the output, not the runtime — consumer Claude never sees AGENTS.md. The rigid, verifiable ones are enforced by rules in `.agents/rules/`; what remains here is guidance that is not a discrete rule.

### Instruct, Don't Teach

Write the least that does the job, and stop there. A skill file directs the agent — it does not explain the domain, justify the design, or narrate how the mechanism was arrived at. The test is what the agent *does* with the sentence: a rationale that changes its behavior is a constraint and stays; one that only makes a human nod is weight paid on every load. State the constraint and move on: "MCP is the only channel" carries everything the agent needs; the sentence explaining that there is no CLI to fall back to carries nothing it can act on.

The test cuts both ways, so a why is not stripped on sight. A constraint often wears one, and there it is load-bearing: the read step saying an upstream artifact enters as a claim to check, not authority to inherit, is what tells the agent to rebut — cut it and the step reads as "go read the file". Where prose earns more room than a clause, it says so structurally: `## Philosophy` and `## Anti-Pattern` exist for the trap that needs explaining. Neither section suspends the test — a heading permits prose, it never justifies it.

The same discipline applies to mechanism. The trap is building a detector for an event that announces itself. Before adding a test, a comparison, or a state to track, ask what the agent already knows at that moment: an artifact it just wrote, a phase it just re-entered, an input the user just handed it. A mechanism that infers what is already given is scaffolding, and scaffolding attracts more scaffolding — each round of review finds real defects in it, and fixing them makes it larger, never smaller.

Competence the model already has is not the skill's to supply. A skill carries preference and constraint — how this project wants a thing done, and what it must not be — never the craft underneath it. A component entry needs its intent, its knob, and what it is wrong for; the DOM sketch and the CSS block are the model's job and cost a load every time they ship.

### Walk the Consumption Path

Judge a structure by the path the consuming agent takes through it. Before shipping, trace one real request end to end: what it reads, in what order, what it writes, and where it would fall back on habit because nothing told it otherwise. Then write the output that request would produce — a vocabulary with no value for the real case, a field shaped for a different product, a step whose input arrives two steps late surface only there. Reading for contradictions and walking a request find disjoint defects; run both, and switch when a pass starts finding what the previous pass introduced.

### Audit on Merit, Not Authorship

Judge the current state on its merits: fix a genuine defect regardless of which commit introduced it, and drop a non-finding regardless of how it got there. Scope may defer a fix — say so as scope, not as authorship. An audit driven down a checklist only grows the file, so judge each finding as you would judge a proposal: is the content already required somewhere, is the cost paid on every load against a rare failure, does it contradict a register the skill already chose.

### Dynamic Context Injection

`SKILL.md` may embed `` !`<command>` `` placeholders. The harness runs the command before the file reaches the model and substitutes the output inline, so Claude receives data rather than the command. Substitution runs once over the original file; injected output is not re-scanned for further placeholders.

Use this at the top of a `SKILL.md` whose first step is gathering state (git status, gh queries, file existence) to remove the "run command, then act on output" round-trip:

```markdown
## Current state

!`git status --short`
!`git diff --staged`
!`git log --oneline -10 --no-merges`
```

**References and instructions are never substituted.** The harness loads `SKILL.md` itself; every other skill file reaches the model through a read, and the placeholder arrives literal. A reference that opens on state carries a plain command block instead:

````markdown
## Current state

Run these before composing:

```bash
git status --short
git log --oneline -10 --no-merges
```
````

Rules:
- `SKILL.md` only. A placeholder in a reference or instruction is dead text.
- Inline form only. No nested or recursive substitution.
- Commands must be safe and read-only (`git`, `gh`, `ls`, `cat`, `awk` on local files). Never inject mutating commands (`rm`, `git push`, `gh pr merge`).
- Steps that consume the output reference the section by name ("the staged diff above"), not re-run the command.
- Substitutions available inside any skill file: `$ARGUMENTS`, `$0`/`$1`/... or `$ARGUMENTS[N]`. Never write a `${CLAUDE_*}` variable in a skill file.
- The user can disable injection globally via the `disableSkillShellExecution` setting. No workflow depends on it — treat injection as a fast path, and give every step that needs state a command it can run.

### Recommended Patterns

- **Checklist copiável** — Multi-step workflows and decision points may include `- [ ]` checklists Claude marks as it progresses. Useful, not required.
- **Validation loop** — When a skill produces verifiable output, document a validator → fix → repeat loop (script or reference doc as validator).
- **Conditional workflow** — When a skill has 2+ paths, branch explicitly: "Creating? → workflow A. Editing? → workflow B."
- **Examples pattern** — Where the output has a form the agent must match (commit subject, PR body, review note), embed concrete I/O pairs. Pairs beat abstract descriptions for form; they narrow the model everywhere else.
- **Expressive interface over usage example** — For a script flag, a template field, or a tool the skill drives, spend the effort on parameters that carry their own meaning (an enum of allowed states, a named field) rather than on an example of a call. The example fixes one path; the parameter leaves the space open.
- **Positive examples over proscriptions.** Show the desired form rather than listing what to avoid.
- **Tool-stack neutrality.** Describe behavior, not specific tools. When a concrete library helps, mention it as an example, not a hard requirement.

## Output Artifacts

Skills split outputs between committed strategic docs (`docs/`) and a gitignored agent workspace (`.artifacts/`).

`docs/` — committed, human-readable, audience-first; `.artifacts/` — gitignored agent workspace. The owning skill is in the comment; each skill documents its own outputs in its README.

```text
docs/
├── product/   # brainstorm, docs-writer
├── tech/      # docs-writer
├── adr/       # docs-writer
└── design/    # design-brief, copywriting, craft-ui

PROJECT.md                 # spec-driven: committed project memory
.artifacts/
├── specs/, archive/, LESSONS.md, research/   # spec-driven
└── design/    # design-brief; design/structure.yaml + design/VARIANTS.md + design/wireframes/ + design/mockups/ # craft-ui
```

`epic-tracker` writes no artifacts — its output lives in the tracker.

`wrap-up` is the only skill that mutates another skill's artifact: it reads `.artifacts/HANDOFF.md` (owned by `handoff`) to enrich the session notes it writes to Obsidian, then clears it — only after persisting, and within the empty-file-equals-cleared contract `handoff` defines. Reading a sibling's artifact is ordinary composition (`craft-ui`'s mockup phase integrates the arrangement, tokens, and content); a mutating integrator is the exception, and `wrap-up` is its single instance — no other skill may write to or clear a sibling's artifact.

`.artifacts/` is excluded locally via `.git/info/exclude` on first write — it stays out of `git status` without touching `.gitignore`. Commit specific files only when explicitly requested.

## Terminology Disambiguation

The docs-writer skill no longer ships a "Technical Design Document" artifact type — that role is now covered by the project-wide Design Doc.

`register` / `surface` are shared design vocabulary across `craft-ui`, `design-brief`, and `copywriting`: **register** = posture (`brand` vs `product`, two values), **surface** = granular type named by context. Each skill carries its own `brand.md` + `product.md`; the terms must not diverge. `docs-writer` originates `register` upstream: its `PRODUCT.md` sets the product's posture (`brand` vs `product`), which the design skills read from that artifact — the definition must not diverge from theirs.

## New Skill Checklist

Before finalizing a new skill, verify the items the path-scoped rules in `.agents/rules/` do not enforce — the rules cover the rest automatically when you edit a skill file:

- [ ] Folder at `skills/<category>/skill-name/`
- [ ] Jobs counted: one job stays flat with the procedure in the `SKILL.md`; several get one instruction each
- [ ] Frontmatter minimal (`name` + `description` [+ `argument-hint`]); extended fields only when needed
- [ ] `description` ≤ 1,024 chars (skill listing cap)
- [ ] `allowed-tools` declared when the skill always runs the same deterministic tool set (e.g. `git`, `gh`)
- [ ] Dynamic context injection (`` !`<cmd>` ``) confined to `SKILL.md` and limited to read-only commands
- [ ] `README.md` present with mermaid + Usage
- [ ] Skill listed in repo `README.md` table
- [ ] No links to untrusted or non-official domains

`skills.sh` runs the published security audit (Gen Agent Trust Hub, Socket, Snyk) on every skill. The `skill-security` rule already covers secrets, piped download-execute, trust boundaries, and safe shell — the domain-trust check above is the one audit item that lives outside the rules.

## Reference Exemplars

When in doubt about a pattern, study `brainstorm` (one job, the procedure in the SKILL.md, a reference per phase), `review-lens` (one job, two modes sharing one rubric reference, model tiering), `git-helpers` (three jobs, one instruction each, one shared reference loaded by all three), or `spec-driven` (seven jobs, many templates, sub-agent fan-out, the refactor at scale).

## Skill Installation

Source of truth is `skills/`. Never edit `~/.agents/skills/` or `~/.claude/skills/` — those are install targets. See repo `README.md` for `skills.sh` usage.
