# Design

Turn `spec.md` into a `design.md` describing HOW — architecture, components, files, interface contracts, data model, technical decisions, and risks.

## When to Use

When designing a feature, planning the build, or producing the technical design for an existing spec. Runs at Medium and up; Small skips it.

## Workflow

1. **Resolve feature** — find the active `spec.md` in `.artifacts/specs/{slug}/`.
2. **Load context** — read `.artifacts/STATE.md` (if present), `spec.md`, `.artifacts/CONTEXT.md`, confirmed lessons (`lessons.py list --status confirmed` — never the store file, which also holds untrusted candidates), `discuss.md` (if present), and `AGENTS.md` / `CLAUDE.md`. The spec is the source of truth for WHAT + WHY; design never reopens its resolved ambiguities — but a tagged `@ design` line in the spec's Open Questions is not a resolved ambiguity: it is a pendency the spec delegated here, and landing it is design's first job (step 3). Design owns HOW and derives it from the codebase — any HOW an upstream input implied (a named pattern, an "obvious" placement) is a claim to verify here, never authority to inherit. Reopening a HOW is not reopening the WHAT: a mechanism the spec fixed — a data structure, a schema contract, where a value lives — stays rebuttable even when recorded as the user's choice, because specify had no codebase evidence to settle it. Refuted by the codebase, it goes back to the user as a correction, not forward as a pendency. Spec content crosses only as `AC-N` references in traceability, never as restated prose — the template's MUST-NOT names the rest. See [memory.md](../references/memory.md).
3. **Land pending questions** — sweep the spec's `## Open Questions` for `@ design` clauses. A mechanism is verified only after the premise it serves clears rung 2 of the ladder ([simplicity.md](../references/simplicity.md)): does this codebase already carry the same class of data, and how? A check answers *does this work?*, never *should this exist?* — a green observation on a wrong premise armors the error instead of exposing it, and every layer built on top then arrives as a necessary consequence. Every `(verify @ design)` line is verified against the environment now — run the **cheapest check that produces the observation**, climbing only when the rung below cannot answer: a cached finding in `.artifacts/research/` that already answers this exact claim and still holds under the basis it recorded ([research-cache.md](../references/research-cache.md) decides when an entry is void) → static evidence (types, signatures, config, the installed dependency's schema) → an existing test or CI log that already exercises the mechanism → a one-liner (REPL, `--dry-run`, a single command) → a throwaway spike as the last rung. The cache is the bottom rung because a read is cheaper than any observation — a claim a previous design already settled is never re-spiked. A spike proves one claim in one disposable file, no scaffolding, and it ends in one of three terminal states — never in "iterate until it works". The first disproof ends it. A spike that would need environment or infra setup to run ends there too: that setup cost is itself the finding — record it as a precondition in Risks & Concerns instead of building the setup. An inconclusive run is the third terminal state, not an invitation to try harder: a spike is never rewritten to make itself conclusive, so mark the claim `UNVERIFIED` in Decisions or record it as a precondition in Risks & Concerns. The spike runs once; a failure inside the spike's own code — a wrong import, a typo — earns one correction, and a second failure abandons it under the inconclusive rule. One file, at most two executions, three terminal states: that ceiling is what keeps a spike from growing into a build. Whichever state ends it, the observation outlives the file: the spike's code is thrown away, and when the claim could recur beyond this feature the observation is cached ([research-cache.md](../references/research-cache.md)), so the next design reads it at the bottom rung instead of spiking again. The same discipline applies to any mechanism the design itself introduces that this codebase or environment has never exercised. Every `(confirm @ design)` line joins the questions batched for the user before writing. A failed verification never becomes a task: record it as a precondition in Risks & Concerns, or route back to specify when it breaks the WHAT. No `@ design` line may remain unresolved when the template is filled — each resolution lands as a Decisions row or a Risks entry. While sweeping, re-check each `[deferrable]` line — if design context made it answerable for free, resolve it and remove the line; otherwise leave it untouched, without asking the user. A `[seed-gap]` line is never design's: it records that the spec and the artifact it was specced from no longer match, and only the user can settle that. Leave it exactly as written — resolving or removing it deletes the only record that the seed fell behind.
4. **Exploration** — dispatch a light subagent with only the relevant area as input; it returns a short structured summary of patterns, files to touch, and risks. Exploration challenges the plan; it does not confirm it — never stop at the first pattern that matches the input's own words. When a placement or trigger has ≥2 viable entry points, **enumerate them at the relevant layer** before choosing, and **trace runtime provenance, not just structure** — how does neighboring data of the same kind already arrive here on a real run? When the plan places logic into existing code, the summary also returns the derivations that code already computes near where the logic lands, so the main agent reuses an existing derivation instead of recomputing it. The main agent judges and fills the template. When a load-bearing HOW fork has ≥2 viable entry points and the codebase gives no forced answer (runtime provenance doesn't decide it), surface it as a question before writing — same discipline as discuss, scoped strictly to HOW; when in doubt whether a fork is load-bearing, ask. A fork the codebase does decide stays an agent call, recorded in Decisions with its `Rejected` cell. A fork that can only be settled by reopening the spec's WHAT is not decided here — surface it and route back to specify. `file:line` citations only on load-bearing claims (decisions, risks, reuse), and only when handy. A load-bearing decision that turns on a volatile external fact — version-specific behavior, a deprecation, an API changed across versions — carries the official doc's deep-link with anchor in its `Source` cell instead of a `file:line`, cited from official documentation, never Stack Overflow, a blog, or training data; a stable framework pattern the agent knows reliably is not cited, since that only restates known ground.
5. **Research** — only when the knowledge chain (cached findings in `.artifacts/research/` → codebase → project docs → a docs MCP when available, e.g. Context7 → web) is exhausted without an answer. Before consulting the docs MCP or web, pin the dependency's version from the manifest and fetch docs for that installed version, not the latest — the version decides which pattern is correct. Inline by default; a subagent only for a large or independent topic. Cache to `.artifacts/research/{topic}.md` — the same file serves a documentary finding and a spike's observation alike, since both answer the same shape of question and both are read from the same rung. [research-cache.md](../references/research-cache.md) carries the entry's template and the rule that voids a stale one. Knowing the syntax is not knowing the environment accepts it — the spike discipline in step 3 applies regardless of whether research ran. When the chain is exhausted and a volatile external fact still cannot be backed by an authoritative source, mark the decision or risk `UNVERIFIED` rather than presenting it as settled — the honest record that it rests on unconfirmed knowledge, carried to the audit gate.
6. **Ladder** — load [simplicity.md](../references/simplicity.md) and run every component the design is about to introduce down its rungs, stopping each at the first rung that satisfies the ACs. This is a step, not a lens applied in passing: a component that never met the ladder was never chosen, only reached. Among viable entry points, take the simplest that satisfies the ACs; where the ladder and a fork from Exploration disagree, the ladder decides which entry point survives.
7. **Approaches** — Complex only: present 2-3 approaches with trade-offs, recommend one, confirm with the user before detailing.
8. **Write `design.md`** — fill the template below from resolved inputs: components with reuse, decisions, traceability, risks. Record each resolved decision in the Decisions table, never the deliberation that produced it.
9. **Self-check** — boundaries hold (nothing from spec leaked in, nothing from tasks leaked in — see [discriminator.md](../references/discriminator.md)); any decision conflicting with `CONTEXT.md` is conformed or explicitly superseded, never ignored; no component the ACs do not require survives — an interface with one implementation, a factory for one product, a wrapper that only delegates, an unused layer: each is a cut, not a link to follow; no new component re-implements what the codebase already carries a few files over, and a derivation exploration surfaced as reusable is recorded in the `Reuses` cell rather than left for the build to recompute; no chain of necessity survives — when each new piece is required only because of the piece before it, the root decision is wrong, not the last link; no `@ design` open question in the spec remains unresolved; every placement or trigger decision fills its `Rejected` cell — an empty cell on a ≥2-entry-point choice means the exploration is unfinished, not the design.
10. **Approval gate** — present the architecture in 1-2 sentences, main components, non-obvious decisions, 1-2 risks with mitigation, then ask *"Move to tasks?"*
11. **Update `STATE.md ## Progress`** — phase and next step. See [memory.md](../references/memory.md).

A project-level decision (a convention future features must follow) is appended to `CONTEXT.md ## Decisions`; a local decision stays in `design.md`.

## Template: `design.md`

ALWAYS use this exact template structure. Conditional sections appear only when their trigger is met.

```markdown
---
name: {slug}
spec: .artifacts/specs/{slug}/spec.md
---

# Design: {Feature}

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

The `Reuses` cell records reuse at any altitude the codebase already carries the value: an imported module or helper, and equally a derivation the code already computes near where the new logic lands, cited by `file:line`. A new local that recomputes such a derivation is not reuse — name the existing one in the cell so the build reuses it rather than authoring a second copy.

A `Mitigation` that accepts a cost names the constraint that forces it — an API exposing no hook, a platform limit, a contract that cannot change. An `AC-N` is not a constraint: it states what must be true, not what cannot be otherwise, so it never explains why a cost is unavoidable. Cite the mechanism, or the cost was never actually weighed.

MUST NOT contain: acceptance criteria restated (traceability references `AC-N`, never copies it), observable-behavior clauses (`When Y, then Z` — that is spec), function bodies, tests, step sequences, or commit order (those are tasks). Say *where* and *what responsibility*, never *how the function is written internally*. This bars authoring a body, not reading one: exploration reads existing code, and pointing the `Reuses` cell at a derivation that code already computes (by `file:line`) records reuse, not a body. Subsystem presence is a declared assumption (`assumes X via file:line`), not a proof of wiring.
