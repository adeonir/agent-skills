# AGENTS.md

Authoring conventions for skills in this repository.

This file is **repo-level guidance for skill authors**. It is never installed alongside skills and never reaches the consumer. Each skill ships via `skills.sh`.

The canonical form of a skill — its files, `SKILL.md`, the reference layer, scripts, and assets — is defined in [`knowledge/skill-architecture-patterns.md`](knowledge/skill-architecture-patterns.md). Read it before writing or reshaping a skill.

## Rules

Verifiable conventions live as rules in `.agents/rules/`, loaded automatically when editing skill files. Each rule is managed with the rule-creator skill and uses examples only when they clarify the constraint.

These are authoring rules: path-scoped to the skill files they govern and applied while a skill is written. In a repository that installs `rule-creator`, the same `.agents/rules/` path holds runtime rules for the agent, which are unconditional. Keep the two contexts apart.

| Rule file | Scope | Covers |
|-----------|-------|--------|
| `.agents/rules/skill-markdown` | `SKILL.md` | router carries routing only, index every procedure, entry point format, standard frontmatter fields, description boundary |
| `.agents/rules/skill-references` | `skills/**/*.md` | one routing level, material loaded at its step, reference header, procedure scope, scripts and tool calls, assets |
| `.agents/rules/skill-writing` | `skills/**/*.md` | English and imperative, a reason that changes behavior, one default, no dates |
| `.agents/rules/skill-safety` | `skills/**/*.md` | no secrets, no piped download-execute, trust boundary, read-only injected commands |

## Repository

Repository of skills for AI coding agents. Markdown-first, following the [Agent Skills](https://agentskills.io) open standard.

```text
agent-skills/
├── AGENTS.md                # this file
├── CLAUDE.md                # points to AGENTS.md
├── README.md                # repo-level skill index
├── knowledge/               # the skill pattern
├── .artifacts/              # gitignored local artifacts
└── skills/
    ├── engineering/
    │   └── skill-name/
    ├── product/
    │   └── skill-name/
    └── productivity/
        └── skill-name/
```

| Directory | Usage |
|-----------|-------|
| engineering | Debugging, specs, system design, code review, git tooling |
| product | Brainstorming, design, documentation, domain modeling, epic tracking |
| productivity | Session notes, vault sync, end-of-session wrap-up, plan interviews |

## Canonical Workflow

Skills compose via artifacts on disk (`.artifacts/`), and a skill file may name or load another skill. The repo `README.md` owns the pipeline diagram and the skill index — this file does not duplicate them.

## Authoring Discipline

### Instruct, Don't Teach

Write the least that does the job, and stop there. A skill file directs the agent — it does not explain the domain or narrate how the mechanism was arrived at. State the constraint and move on: "MCP is the only channel" carries everything the agent needs; the sentence explaining that there is no CLI to fall back to carries nothing it can act on.

Competence the model already has is not the skill's to supply. A skill carries preference and constraint — how this project wants a thing done, and what it must not be — never the craft underneath it. A component entry needs its intent, its knob, and what it is wrong for; the DOM sketch and the CSS block are the model's job and cost a load every time they ship.

### Walk the Consumption Path

Judge a structure by the path the consuming agent takes through it. Before shipping, trace one real request end to end: what it reads, in what order, what it writes, and where it would fall back on habit because nothing told it otherwise. Then write the output that request would produce — a vocabulary with no value for the real case, a field shaped for a different product, a step whose input arrives two steps late surface only there. Reading for contradictions and walking a request find disjoint defects; run both, and switch when a pass starts finding what the previous pass introduced.

### One Term Per Concept

Choose one term per concept and keep it across `SKILL.md` and references within a skill. Mixing synonyms ("field" / "box" / "element", or "extract" / "pull" / "get") forces the model to re-map them and weakens matching.

### Discovery

Three discovery types are recognized at the authoring level. Skills do not label them — apply the right pattern silently.

- **Type A — Product discovery.** The problem, user, and direction, before any execution: iterative, question-driven, no disk state.
- **Type B — Context discovery.** The execution state — which artifacts exist, which project is active, what the codebase looks like. Deterministic.
- **Type C — Technical discovery.** The solution space — requirements, trade-offs, architecture. Structured by topics, adaptive depth.

Types A and C live in `references/discovery.md`; Type B lives at the start of the reference that needs it, never in `SKILL.md`.

### Guidelines and Anti-Patterns

A `## Guidelines` section is a short DO list of 4-6 non-obvious items; skip the common sense. A real trap becomes `## Anti-Pattern: <name>`, with prose on the failure and the correct alternative — and a proscription with no positive counterpart stands alone there.

A trap is found, not derived. It names something an agent did — in a run, in a shipped artifact, in a failure the user hit — and it earns a section because the constraint alone did not stop it. A trap written to guard a rule the same edit introduced is that rule in costume: the constraint already states itself, the section only says it louder. Where nothing was observed, the constraint ships alone.

### Dynamic Context Injection

`SKILL.md` may embed `` !`<command>` `` placeholders. The harness runs the command before the file reaches the model and substitutes the output inline, so Claude receives data rather than the command. Substitution runs once over the original file; injected output is not re-scanned for further placeholders.

Use this at the top of a `SKILL.md` whose first step is gathering state (git status, file existence) to remove the "run command, then act on output" round-trip:

```markdown
## Current state

!`git status --short`
!`git diff --staged`
!`git log --oneline -10 --no-merges`
```

**References are never substituted.** The harness loads `SKILL.md` itself; every other skill file reaches the model through a read, and the placeholder arrives literal. A reference that opens on state carries a plain command block instead.

Rules:
- `SKILL.md` only. A placeholder in a reference is dead text.
- Inline form only. No nested or recursive substitution.
- Steps that consume the output reference the section by name ("the staged diff above"), not re-run the command.
- Substitutions available inside any skill file: `$ARGUMENTS`, `$0`/`$1`/... or `$ARGUMENTS[N]`. Never write a `${CLAUDE_*}` variable in a skill file.
- The user can disable injection globally via the `disableSkillShellExecution` setting. No workflow depends on it — treat injection as a fast path, and give every step that needs state a command it can run.

### Scripts and Assets

`scripts/` and `assets/` are optional. Use them when the skill genuinely needs deterministic operations or static assets — data files for a script, or a file the render inlines into its output (e.g. a stylesheet).

A script's language follows the job, not the skill: pure computation and text validators are Python stdlib (`slop_scan.py`, `validate_copy.py`, `check-contrast.py`); live web preview and render servers are bun/TS (`render-server.ts`, `preview-server.ts`). Match an existing sibling's conventions when adding one — a skill that ships both runtimes declares each in `allowed-tools` (`Bash(bun:*) Bash(python3:*)`).

Skills using MCP must detect availability before invoking the tool, document a fallback when the MCP is unavailable, and mark each dependency hard-required or optional.

## Output Artifacts

Skills write to `docs/` (committed, human-readable, audience-first) or `.artifacts/` (gitignored agent workspace). The owning skill is named in the comment, and each skill documents its own outputs in its references; the tree lives in the repo `README.md`.

`epic-tracker` writes no artifacts — its output lives in the tracker.

`wrap-up` is the only skill that mutates another skill's artifact: it reads `.artifacts/HANDOFF.md` (owned by `handoff`) to enrich the session notes it writes to Obsidian, then removes the blocks it read — only after every note write succeeds, and never a block another session wrote. Reading a sibling's artifact is ordinary composition (`craft-ui`'s mockup phase integrates the arrangement, tokens, and content); a mutating integrator is the exception, and `wrap-up` is its single instance — no other skill may write to or clear a sibling's artifact.

`.artifacts/` is excluded locally via `.git/info/exclude` on first write — it stays out of `git status` without touching `.gitignore`. Commit specific files only when explicitly requested.

## Terminology Disambiguation

`register` / `surface` are shared design vocabulary across `craft-ui`, `design-md-builder`, and `copywriting`: **register** = posture (`brand` vs `product`, two values), **surface** = granular type named by context. Each skill carries its own `brand.md` + `product.md`; the terms must not diverge. `docs-writer` originates `register` upstream: its `PRODUCT.md` sets the product's posture (`brand` vs `product`), which the design skills read from that artifact — the definition must not diverge from theirs.

## New Skill Checklist

Before finalizing a new skill, verify the items the path-scoped rules in `.agents/rules/` do not enforce:

- [ ] Folder at `skills/<category>/skill-name/`
- [ ] Jobs counted: one job stays flat with the procedure in the `SKILL.md`; several get one reference each
- [ ] `agents/openai.yaml` present with `interface.display_name` and `interface.short_description`
- [ ] Skill listed in repo `README.md` table
- [ ] No links to untrusted or non-official domains

`skills.sh` runs the published security audit (Gen Agent Trust Hub, Socket, Snyk) on every skill. The `skill-safety` rule already covers secrets, piped download-execute, and trust boundaries — the domain-trust check above is the one audit item that lives outside the rules.

## Skill Source and Installation

Edit skill sources under `agent-skills/skills/<category>/<skill-name>/`. Load an invoked skill only from the path supplied by the runtime; never search or load it from `agent-skills/`. Never edit `~/.agents/skills/` or `~/.claude/skills/` — those are install targets. See repo `README.md` for `skills.sh` usage.
