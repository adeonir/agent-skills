# Design

Turn `spec.md` into a `design.md` describing HOW — architecture, components, files, interface contracts, data model, technical decisions, and risks.

## When to Use

When designing a feature, planning the build, or producing the technical design for an existing spec. Runs at Medium and up; Small skips it.

## Workflow

1. **Resolve feature** — find the active `spec.md` in `.artifacts/specs/{slug}/`.
2. **Load context** — read `.artifacts/STATE.md` (if present), `spec.md`, `.artifacts/CONTEXT.md`, confirmed lessons, `discuss.md` (if present), and `AGENTS.md` / `CLAUDE.md`. The spec is the source of truth for WHAT + WHY; design never reopens its resolved ambiguities — but a tagged `@ design` line in the spec's Open Questions is not a resolved ambiguity: it is a pendency the spec delegated here, and landing it is design's first job (step 3). Design owns HOW and derives it from the codebase — any HOW an upstream input implied (a named pattern, an "obvious" placement) is a claim to verify here, never authority to inherit. See [memory.md](../references/memory.md).
3. **Land pending questions** — sweep the spec's `## Open Questions` for `@ design` clauses. Every `(verify @ design)` line is verified against the environment now — run its `verify:` check as a cheap throwaway spike; the same spike discipline applies to any mechanism the design itself introduces that this codebase or environment has never exercised. Every `(confirm @ design)` line joins the questions batched for the user before writing. A failed verification never becomes a task: record it as a precondition in Risks & Concerns, or route back to specify when it breaks the WHAT. No `@ design` line may remain unresolved when the template is filled — each resolution lands as a Decisions row or a Risks entry.
4. **Exploration** — dispatch a light subagent with only the relevant area as input; it returns a short structured summary of patterns, files to touch, and risks. Exploration challenges the plan; it does not confirm it — never stop at the first pattern that matches the input's own words. When a placement or trigger has ≥2 viable entry points, **enumerate them at the relevant layer** before choosing, and **trace runtime provenance, not just structure** — how does neighboring data of the same kind already arrive here on a real run? The main agent judges and fills the template. When a load-bearing HOW fork has ≥2 viable entry points and the codebase gives no forced answer (runtime provenance doesn't decide it), surface it as a question before writing — same discipline as discuss, scoped strictly to HOW; when in doubt whether a fork is load-bearing, ask. A fork the codebase does decide stays an agent call, recorded in Decisions with its `Rejected` cell. A fork that can only be settled by reopening the spec's WHAT is not decided here — surface it and route back to specify. `file:line` citations only on load-bearing claims (decisions, risks, reuse), and only when handy.
5. **Research** — only when the knowledge chain (codebase → project docs → Context7 MCP → web) is exhausted without an answer. Inline by default; a subagent only for a large or independent topic. Cache to `.artifacts/research/{topic}.md`. Knowing the syntax is not knowing the environment accepts it — the spike discipline in step 3 applies regardless of whether research ran.
6. **Approaches** — Complex only: present 2-3 approaches with trade-offs, recommend one, confirm with the user before detailing.
7. **Write `design.md`** — fill the template below from resolved inputs: components with reuse, decisions, traceability, risks. Record each resolved decision in the Decisions table, never the deliberation that produced it.
8. **Self-check** — boundaries hold (nothing from spec leaked in, nothing from tasks leaked in — see [discriminator.md](../references/discriminator.md)); any decision conflicting with `CONTEXT.md` is conformed or explicitly superseded, never ignored; no `@ design` open question in the spec remains unresolved; every placement or trigger decision fills its `Rejected` cell — an empty cell on a ≥2-entry-point choice means the exploration is unfinished, not the design.
9. **Approval gate** — present the architecture in 1-2 sentences, main components, non-obvious decisions, 1-2 risks with mitigation, then ask *"Move to tasks?"*
10. **Update `STATE.md ## Progress`** — phase and next step. See [memory.md](../references/memory.md).

Read `CONTEXT.md` before any design decision. A project-level decision (a convention future features must follow) is appended to `CONTEXT.md ## Decisions`; a local decision stays in `design.md`.

## Template: `design.md`

ALWAYS use this exact template structure. Conditional sections appear only when their trigger is met.

```markdown
---
name: {slug}
spec: .artifacts/specs/{slug}/spec.md
---

# Design: {Feature}

**Spec**: `.artifacts/specs/{slug}/spec.md`

## Scope
{In-scope / out-of-scope — only what affects the design.}

## Architecture Overview
{Brief description + optional mermaid.}

## Components
| Component | File | Responsibility | Depends on | Reuses |
|-----------|------|----------------|------------|--------|

## Data Model            <!-- conditional: only if the feature involves data -->
{Entities and relations; no exhaustive member enumeration.}

## Decisions
| Decision | Choice | Rejected | Source | Rationale |
|----------|--------|----------|--------|-----------|

## Error Handling
| Scenario | Handling | User Impact |
|----------|----------|-------------|

## Risks & Concerns
| Concern | Location | Impact | Mitigation |
|---------|----------|--------|------------|

## Requirements Traceability
| AC | Component | File |
|----|-----------|------|

## Research Summary        <!-- conditional: only if research ran -->
{Summary of the .artifacts/research/{topic}.md caches.}

## Visual Design Considerations  <!-- conditional: only if visual references exist -->
{Notes on images/prototypes.}
```

A placement or trigger with ≥2 viable entry points is a Decisions row, not a silent mechanical pick: record the choice and name the ruled-out alternative in its `Rejected` cell, even when one looks obvious. A `Rejected` cell is empty only when the decision genuinely had one viable home.

MUST NOT contain: acceptance criteria restated (traceability references `AC-N`, never copies it), observable-behavior clauses (`When Y, then Z` — that is spec), function bodies, tests, step sequences, or commit order (those are tasks). Say *where* and *what responsibility*, never *how the function is written internally*. Subsystem presence is a declared assumption (`assumes X via file:line`), not a proof of wiring.
