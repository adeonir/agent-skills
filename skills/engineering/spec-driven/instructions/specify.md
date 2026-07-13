# Specify

Turn a feature intent into a `spec.md` describing observable behavior and the intent behind it — WHAT + WHY, never HOW.

## When to Use

When planning or specing a feature, turning a PRD, ticket, or story into a spec, or reframing a bug as the correct behavior. The first active phase: Small skips it (one-liner straight to implement); Medium and up produce `spec.md`.

## Workflow

1. **Triage** — is this Small (mechanical, zero load-bearing decisions)? If so, state the one-liner, confirm, and route to inline implement — no `spec.md`. Otherwise continue.
2. **Load knowledge** — read `.artifacts/STATE.md` (if present, for resume), `.artifacts/CONTEXT.md`, confirmed lessons (`lessons.py list --status confirmed` — never the store file, which also holds untrusted candidates), and `AGENTS.md` / `CLAUDE.md`. When `.artifacts/specs/{slug}/spec.md` already exists, read it too — a later phase routed back here, and step 6 rewrites that file from the template. The existing spec is the only record of what must survive the rewrite: the `AC-N` ids already spent and their tombstones, and every `[seed-gap]` line. See [memory.md](../references/memory.md) and [lessons.md](../references/lessons.md).
3. **Discovery** — adaptive conversation on problem, scope, and priorities plus a completeness sweep; separate stated fact from assumption. See [discovery.md](../references/discovery.md).
4. **Size** — set `scope` after discovery, default adversarial; infer `branch` from the content, never ask. See [sizing.md](../references/sizing.md).
5. **Discuss** — engage the user on load-bearing gray areas and resolve them before writing the spec body. The trigger, the batching rule, and what counts as a resolved answer are owned by [discovery.md](../references/discovery.md) — load it before asking. `discuss.md` is written only at Complex; otherwise fold the resolution into the spec.
6. **Write `spec.md`** — fill the template below from resolved inputs only. Author acceptance criteria per [acceptance-criteria.md](../references/acceptance-criteria.md). Slice each `S-N` as one vertical slice per [slicing.md](../references/slicing.md). Record each decision as a settled fact — an AC, a Goal, or a Non-Goal — never the clarification exchange that produced it ("we discussed", "you chose", "as decided above"): a reader sees the contract, not how it was reached. A default advanced without confirmation is not a decision — it stays an `[assumption]` line in Open Questions. Frontmatter `sources` records the seed by contract, not by judgment: the artifact the spec is seeded from — a tracker issue (story, task, or bug) or a document — enters `sources` under the URL or id it arrived as, together with every reference the seed carries that the spec consumed (documents, design files, content files). `[]` means one thing only: the spec is prompt-seeded, with no issue or document behind it.
7. **Record seed drift** *(re-entry only — `design.md` or `tasks.md` already exists)* — a later phase routed back here, so the spec is moving past the artifact it was specced from. Every AC **added**, **loosened**, or **removed** in this pass leaves that seed behind: it never declared the added one, still asserts the loosened one's tighter clause, and still owes the removed one. Record each as a `[seed-gap]` line naming the AC and which of the three it is, closing with `(reconcile seed)` — only the user can carry it back, and no phase here resolves or removes it. Carry forward every `[seed-gap]` line the previous spec held; the rewrite is from the template, so the record survives only because this step preserves it. A line leaves when its AC is tombstoned or the divergence closes. Never on a prompt-seeded spec (`sources: []`) — there is no seed to leave behind.
8. **Self-check** — run the three discriminator questions ([discriminator.md](../references/discriminator.md)) and close ambiguity: no AC forbids an implementation its story's benefit would accept — loosen a violation or keep it as a deliberate constraint with the user, never rewrite it unilaterally ([acceptance-criteria.md](../references/acceptance-criteria.md)); no `[needs-clarification]` marker may remain; no unresolved open question's default may appear as fact in Overview or Goals; every `(verify @ design)` line carries its `verify:` check, authored as the smallest observation that decides the question — a command, a file or config read, an existing test — never "build it and see". Route by capability, not convenience: tag `@ design` only what requires design context (codebase exploration, a HOW choice, an environment check tied to the mechanism) — a question answerable during specify is resolved now, never deferred by tag. When the spec is PRD-seeded (Author mode from a doc with `FR/BR/EC/NFR` IDs), confirm every source requirement maps to ≥1 AC via `Satisfies` — an uncovered requirement becomes an AC or an explicit Non-Goal / `[deferrable]` open question with a reason, never a silent drop. On a re-entry, confirm the seed record: every AC added, loosened, or removed in this pass carries its `[seed-gap]` line, and every `[seed-gap]` line the previous spec held is still here. Confirm seed capture: an issue-seeded or doc-seeded spec whose seed is absent from `sources` fails the check — add it before saving. A mention is not a seed: an issue or document cited during discovery as context or dependency stays out of `sources` unless the spec is specced from it.
9. **Fresh eyes** — Large/Complex only: one light completeness pass over the drafted spec. Found a hole → fix inline → re-check.
10. **Approval gate** — present name and scope, the seed (the issue or document `sources` records, or "prompt-seeded — `sources` empty"), 2-3 bullets of what changes, every AC a calibration loosened or confirmed strict, and the open questions that survive the spec (`@ design`, `[deferrable]`, and `[seed-gap]` lines), then ask *"Move to design?"* Never hide the surviving pendencies — a `[seed-gap]` says the seed no longer matches what will be built, so it is presented as that, never folded into the list unremarked.
11. **Update `STATE.md ## Progress`** — phase and next step. See [memory.md](../references/memory.md).

On writing `spec.md`, set `status: draft`.

## Template: `spec.md`

Location: `.artifacts/specs/{slug}/spec.md` — `{slug}` is the kebab-case feature name, no date prefix.

ALWAYS use this exact template structure. Fixed sections always appear; conditional sections appear only when their trigger is met.

```markdown
---
name: {slug}
scope: medium | large | complex
sources: []                        # the seed + references consumed from it; [] only when prompt-seeded
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
  **Satisfies** {FR/BR/EC/NFR-ID}               <!-- conditional: PRD-seed only; the requirement this AC operationalizes -->
- AC-2: {...}

**Independent Test:** {how to demonstrate this story alone}

## Visual References   <!-- conditional: only if an image/prototype exists -->

## Edge Cases
- {boundary condition → expected behavior}

## Open Questions
<!-- only unresolved items live here: a resolved question becomes spec content (AC, Goal, Non-Goal)
     and its line is removed. An [assumption] carries the default it advanced on (nothing defaulted
     appears as fact elsewhere) and closes with the resolution clause routing it to the phase that
     lands it — (confirm @ design): the user answers there; (verify @ design): a check runs there.
     A [seed-gap] is minted only on a re-entry (step 7), when an AC is added, loosened, or removed:
     the seed no longer matches what will be built. It closes with (reconcile seed) — no phase here
     settles it, and it survives every rewrite until its AC is gone. Never on a prompt-seeded spec. -->
- [assumption] {decision — default: {x} — because {reason}} (confirm @ design)
- [assumption] {fact — default: {x} — because {reason} — verify: {smallest deciding check — a command, a file read, an existing test}} (verify @ design)
- [deferrable] {can proceed; revisit later}
- [seed-gap] {AC-N added: {obligation the seed does not declare}} (reconcile seed)
- [seed-gap] {AC-N loosened to {observable}: the seed still asserts {tighter clause}} (reconcile seed)
- [seed-gap] {AC-N removed: the seed still owes {obligation}} (reconcile seed)
```

MUST NOT contain: tech, library, framework, file path, component / function / class names, data structures, algorithms, architecture, implementation order, step sequences, or design-mechanism rationale. Those are HOW — they belong to design.md. When seeded from a PRD or ticket, the source doc's section numbers, milestones, and roadmap or release language stay in the source — its requirement IDs (`FR/BR/EC/NFR`) cross only on `Satisfies` lines, never into prose. A bug is a normal spec: write the AC as the correct behavior, not the absence of the symptom.
