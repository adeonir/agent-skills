# Specify

Turn a feature intent into a `spec.md` describing observable behavior and the intent behind it — WHAT + WHY, never HOW.

## When to Use

When planning or specing a feature, turning a PRD, ticket, or story into a spec, or reframing a bug as the correct behavior. The first active phase: Small skips it (one-liner straight to implement); Medium and up produce `spec.md`.

## Workflow

1. **Triage** — is this Small (mechanical, zero load-bearing decisions)? If so, state the one-liner, confirm, and route to inline implement — no `spec.md`. Otherwise continue.
2. **Load knowledge** — read `.artifacts/STATE.md` (if present, for resume), `.artifacts/CONTEXT.md`, confirmed lessons (`.artifacts/lessons.json`), and `AGENTS.md` / `CLAUDE.md`. See [memory.md](../references/memory.md) and [lessons.md](../references/lessons.md).
3. **Discovery** — adaptive conversation on problem, scope, and priorities plus a completeness sweep; separate stated fact from assumption. See [discovery.md](../references/discovery.md).
4. **Size** — set `scope` after discovery, default adversarial; infer `branch` from the content, never ask. See [sizing.md](../references/sizing.md).
5. **Discuss** — engage the user on load-bearing gray areas and resolve them before writing the spec body. The trigger, the batching rule, and what counts as a resolved answer are owned by [discovery.md](../references/discovery.md) — load it before asking. `discuss.md` is written only at Complex; otherwise fold the resolution into the spec.
6. **Write `spec.md`** — fill the template below from resolved inputs only. Author acceptance criteria per [acceptance-criteria.md](../references/acceptance-criteria.md). Each `S-N` is one vertical slice delivering one benefit, demonstrable on its own — a story carrying two distinct benefits is two stories. Record each decision as a settled fact — an AC, a Goal, or a Non-Goal — never the clarification exchange that produced it ("we discussed", "you chose", "as decided above"): a reader sees the contract, not how it was reached. A default advanced without confirmation is not a decision — it stays an `[assumption]` line in Open Questions.
7. **Self-check** — run the three discriminator questions ([discriminator.md](../references/discriminator.md)) and close ambiguity: no `[needs-clarification]` marker may remain; no unresolved open question's default may appear as fact in Overview or Goals; every `(verify @ design)` line carries its `verify:` check, authored as the smallest observation that decides the question — a command, a file or config read, an existing test — never "build it and see". Route by capability, not convenience: tag `@ design` only what requires design context (codebase exploration, a HOW choice, an environment check tied to the mechanism) — a question answerable during specify is resolved now, never deferred by tag. When the spec is PRD-seeded (Author mode from a doc with `FR/BR/EC/NFR` IDs), confirm every source requirement maps to ≥1 AC via `Satisfies` — an uncovered requirement becomes an AC or an explicit Non-Goal / `[deferrable]` open question with a reason, never a silent drop.
8. **Fresh eyes** — Large/Complex only: one light completeness pass over the drafted spec. Found a hole → fix inline → re-check.
9. **Approval gate** — present name and scope, 2-3 bullets of what changes, and the open questions that survive the spec (`@ design` and `[deferrable]` lines), then ask *"Move to design?"* Never hide the surviving pendencies.
10. **Update `STATE.md ## Progress`** — phase and next step. See [memory.md](../references/memory.md).

On writing `spec.md`, set `status: draft`.

## Template: `spec.md`

Location: `.artifacts/specs/{slug}/spec.md` — `{slug}` is the kebab-case feature name, no date prefix.

ALWAYS use this exact template structure. Fixed sections always appear; conditional sections appear only when their trigger is met.

```markdown
---
name: {slug}
scope: medium | large | complex
sources: []                        # durable pointers (PRD/ticket/story); [] if none
user-facing: true | false          # true → UAT required before done
status: draft
created: {YYYY-MM-DD}
branch: {slug}                     # inferred from content, not asked
---

# Feature: {Title}

## Overview
{2-3 sentences: problem + what changes + why (macro why).}

## Baseline            <!-- conditional: brownfield only, lean -->
{Only the current behavior relevant to the delta. The agent reads code for the rest.}

## Goals
- [ ] {measurable observable result, e.g. "Checkout completes in < 3s (p95)"}

## Non-Goals
- {thing X} — {why it is out}

## Glossary            <!-- conditional: only if a domain term appears -->
| Term | Definition |

## User Stories
### S-1: {Title} (P-1)
**As a** {role}, **I want** {capability}, **so that** {benefit}.

**Acceptance Criteria:**
- AC-1: {EARS-lite clause} (because {intent})   <!-- rationale inline OPTIONAL, non-obvious AC only -->
  **Satisfies:** {FR/BR/EC/NFR-ID}              <!-- conditional: PRD-seed only; the requirement this AC operationalizes -->
- AC-2: {...}

**Independent Test:** {how to demonstrate this story alone}

## Visual References   <!-- conditional: only if an image/prototype exists -->

## Edge Cases
- {boundary condition → expected behavior}

## Open Questions
<!-- only unresolved items live here: a resolved question becomes spec content (AC, Goal, Non-Goal)
     and its line is removed. An [assumption] carries the default it advanced on (nothing defaulted
     appears as fact elsewhere) and closes with the resolution clause routing it to the phase that
     lands it — (confirm @ design): the user answers there; (verify @ design): a check runs there. -->
- [assumption] {decision — default: {x} — because {reason}} (confirm @ design)
- [assumption] {fact — default: {x} — because {reason} — verify: {smallest deciding check — a command, a file read, an existing test}} (verify @ design)
- [deferrable] {can proceed; revisit later}
```

MUST NOT contain: tech, library, framework, file path, component / function / class names, data structures, algorithms, architecture, implementation order, step sequences, or design-mechanism rationale. Those are HOW — they belong to design.md. When seeded from a PRD or ticket, the source doc's section numbers, milestones, and roadmap or release language stay in the source — its requirement IDs (`FR/BR/EC/NFR`) cross only on `Satisfies` lines, never into prose. A bug is a normal spec: write the AC as the correct behavior, not the absence of the symptom.
