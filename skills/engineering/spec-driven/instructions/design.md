# Design

Turn `spec.md` into a `design.md` describing HOW — architecture, components, files, interface contracts, data model, technical decisions, and risks.

## When to Use

When designing a feature, planning the build, or producing the technical design for an existing spec. Runs at Medium and up; Small skips it.

## Workflow

1. **Resolve feature** — find the active `spec.md` and read `.artifacts/specs/{slug}/STATE.md` first. If `Phase` points to `specify`, stop and report that phase. Design reads a spec at `status: ready`; one still at `draft` has not closed its own phase, so route back to [specify.md](specify.md) rather than designing against it. When creating or editing `design.md`, set its status to `draft` before writing.
2. **Load context** — read the active feature's `STATE.md`, `spec.md`, the root `CONTEXT.md`, confirmed lessons (`lessons.py list --status confirmed` — never the lessons file, which also holds untrusted candidates), `discuss.md` (if present), and `AGENTS.md` / `CLAUDE.md`. The spec is the source of truth for WHAT + WHY; design never reopens its resolved ambiguities. An open `OQ-N` is a pendency for design to inspect, not a mechanism tag or a new requirement. Design owns HOW and derives it from the codebase — any HOW an upstream input implied (a named pattern, an "obvious" placement) is a claim to verify here, never authority to inherit. Reopening a HOW is not reopening the WHAT: a mechanism the spec fixed — a data structure, a schema contract, where a value lives — stays rebuttable even when recorded as the user's choice, because specify had no codebase evidence to settle it. Refuted by the codebase, it goes back to the user as a correction, not forward as a pendency. Design may expose component dependencies in `Depends on`; the task graph and its derived waves are owned by `tasks.md`. Spec content crosses only as `AC-N.M` references in traceability, never as restated prose — the template's MUST-NOT names the rest. See [memory.md](../references/memory.md).
3. **Land pending questions** — sweep the spec's `## Open Questions` for `OQ-N` rows. Resolve each question with codebase evidence or the user's answer when required. If neither provides an answer, keep the `OQ-N` open and record the consequence in `Risks & Concerns`; design may continue without inventing a default.
   - **Premise before mechanism** — a mechanism is verified only after the premise it serves clears rung 2 of the ladder ([simplicity.md](../references/simplicity.md)): does this codebase already carry the same class of data, and how? A check answers *does this work?*, never *should this exist?* — a green observation on a wrong premise armors the error instead of exposing it, and every layer built on top then arrives as a necessary consequence.
   - **Evidence for an `OQ-N`** — take the cheapest observation that answers the question, verified against the environment now, climbing only when the rung below cannot answer: a cached finding in `.artifacts/research/` that already answers this exact claim and still holds under the basis it recorded ([research-cache.md](../references/research-cache.md) decides when an entry is void) → static evidence (types, signatures, config, the installed dependency's schema) → an existing test or CI log that already exercises the mechanism → a one-liner (REPL, `--dry-run`, a single command) → a throwaway spike as the last rung. The cache is the bottom rung because a read is cheaper than any observation — a claim a previous design already settled is never re-spiked.
   - **The spike ceiling** — one claim, one disposable file, no scaffolding, at most two executions, three terminal states; never "iterate until it works", which is what keeps a spike from growing into a build. The first disproof ends it. A spike that would need environment or infra setup to run ends there too: that setup cost is itself the finding — record it as a precondition in Risks & Concerns instead of building the setup. An inconclusive run is the third terminal state, not an invitation to try harder: a spike is never rewritten to make itself conclusive, so mark the claim `UNVERIFIED` in Decisions or record it as a precondition in Risks & Concerns. A failure inside the spike's own code — a wrong import, a typo — earns one correction, and a second failure abandons it under the inconclusive rule.
   - **The observation outlives the file** — the spike's code is thrown away, and when the claim could recur beyond this feature the observation is cached ([research-cache.md](../references/research-cache.md)), so the next design reads it at the bottom rung instead of spiking again. The same discipline applies to any mechanism the design itself introduces that this codebase or environment has never exercised.
   - **User-owned `OQ-N`** — batch questions that only the user can answer before writing the design. If the user does not answer, keep the row `open` and record the accepted uncertainty in Risks & Concerns; never replace it with an invented default.
   - **The lines that are not design's** — an `OQ-N` that codebase evidence cannot settle remains in the spec, with its risk recorded here. The spec's `## Divergences` table records its current differences from the seed; leave it unchanged because specify owns that comparison.
4. **Exploration** — dispatch a light subagent with only the relevant area as input; it returns a short structured summary of patterns, files to touch, and risks. The main agent judges it and fills the template.
   - **Challenge the plan, never confirm it** — do not stop at the first pattern that matches the input's own words.
   - **Enumerate before choosing** — a placement or trigger with ≥2 viable entry points is listed at the relevant layer first, tracing **runtime provenance, not just structure**: how does neighboring data of the same kind already arrive here on a real run?
   - **Return the derivations** — when the plan places logic into existing code, the summary also carries what that code already computes near where the logic lands, so the main agent reuses an existing derivation instead of recomputing it.
   - **A fork the codebase does not settle** — a load-bearing HOW fork with ≥2 viable entry points and no forced answer (runtime provenance doesn't decide it) is surfaced as a question before writing, same discipline as discuss and scoped strictly to HOW; when in doubt whether a fork is load-bearing, ask. A fork the codebase does decide stays an agent call, recorded in Decisions with its `Rejected` cell. One that can only be settled by reopening the spec's WHAT is not decided here — set `STATE.md` to `Phase: specify` and `Next: specify`.
   - **Citations** — `file:line` only on load-bearing claims (decisions, risks, reuse), and only when handy. A load-bearing decision that turns on a volatile external fact — version-specific behavior, a deprecation, an API changed across versions — carries the official doc's deep-link with anchor in its `Source` cell instead, cited from official documentation, never Stack Overflow, a blog, or training data; a stable framework pattern the agent knows reliably is not cited, since that only restates known ground.
5. **Research** — only when the knowledge chain (cached findings in `.artifacts/research/` → codebase → project docs → a docs MCP when available, e.g. Context7 → web) is exhausted without an answer. Before consulting the docs MCP or web, pin the dependency's version from the manifest and fetch docs for that installed version, not the latest — the version decides which pattern is correct. Inline by default; a subagent only for a large or independent topic. Cache to `.artifacts/research/{topic}.md` — the same file serves a documentary finding and a spike's observation alike, since both answer the same shape of question and both are read from the same rung. [research-cache.md](../references/research-cache.md) carries the entry's template and the rule that voids a stale one. Knowing the syntax is not knowing the environment accepts it — the spike discipline in step 3 applies regardless of whether research ran. When the chain is exhausted and a volatile external fact still cannot be backed by an authoritative source, mark the decision or risk `UNVERIFIED` rather than presenting it as settled — the honest record that it rests on unconfirmed knowledge, carried to the audit gate.
6. **Ladder** — load [simplicity.md](../references/simplicity.md) and run every component the design is about to introduce down its rungs, stopping each at the first rung that satisfies the ACs. This is a step, not a lens applied in passing: a component that never met the ladder was never chosen, only reached. Among viable entry points, take the simplest that satisfies the ACs; where the ladder and a fork from Exploration disagree, the ladder decides which entry point survives — never a fork step 4 routed to the user. The rungs rank by machinery added, not capability delivered, so on a tool or dependency fork the ladder supplies the lean the question carries, never the answer.
7. **Approaches** — Complex only: present 2-3 approaches with trade-offs, recommend one, confirm with the user before detailing.
8. **Write `design.md`** — fill the template below from resolved inputs. Represent each frontend, backend, or integration component as an explicit compact block. Give every component a unique name and record the applicable fields: area or layer, responsibility, location or files, interfaces, relationships, `Depends on`, and `Reuses`. Keep design-wide relationships and data flow in `Architecture Overview`; the component blocks define what will be built. Keep an interface in its component block when it belongs clearly to that component. Put an interface that crosses components in a separate `Interfaces` section. Add `Endpoints` only when the feature exposes or changes an HTTP surface, and use one compact block per endpoint. Record decisions, traceability, and risks. Record each resolved decision in the Decisions table, never the deliberation that produced it.
9. **Self-check** — run `python3 ${CLAUDE_SKILL_DIR}/scripts/lint_artifact.py design .artifacts/specs/{slug}` and fix every line it reports, then read for what it cannot: boundaries hold (nothing from spec leaked in, nothing from tasks leaked in — see [discriminator.md](../references/discriminator.md)); any decision conflicting with `CONTEXT.md` is conformed or explicitly superseded, never ignored; no component the ACs do not require survives — an interface with one implementation, a factory for one product, a wrapper that only delegates, an unused layer: each is a cut, not a link to follow; no new component re-implements what the codebase already carries a few files over, and a derivation exploration surfaced as reusable is recorded in the `Reuses` field rather than left for the build to recompute; no chain of necessity survives — when each new piece is required only because of the piece before it, the root decision is wrong, not the last link; every `OQ-N` is either answered by evidence or linked to a risk, and no open question is silently treated as settled; every placement, trigger, tool, or dependency decision fills its `Rejected` cell — an empty cell on a ≥2-entry-point choice means the exploration is unfinished, not the design; every Decisions row's `Source` names what closed it — the evidence that forced it, or `user` when the question was asked; each interface names the operation, parameters, return type, and any error that is a feature decision; and each endpoint names the method, route, input, output, and responses or status codes that are feature decisions. A Decisions row with neither `Rejected` nor `Source` is a fork closed silently. A mechanism the design introduces that no evidence settled is marked `UNVERIFIED`, never asserted bare. Keep `status: draft` while editing and set `status: ready` after this self-check and the peer check pass.
10. **Peer check** — Medium and up: the agent that wrote the design cannot clear it, so dispatch a Sonnet subagent with no conversation history, handed `design.md`, `spec.md`, the root `CONTEXT.md`, the convention sources, and the template's MUST-NOT list verbatim — never the deliberation that produced the design or a claim that it holds, since a delivered conclusion anchors the reader toward agreement. It reads the design against its own contract: the template's MUST-NOT, a component the ACs do not require, a chain of necessity, a `Rejected` or `Source` cell left empty on a fork with ≥2 entry points, and a mechanism no evidence in the payload supports. It never reads the codebase — a claim the payload cannot support is a finding, not a prompt to go looking for it. It returns one line per finding — where it is, the contract it breaks, what would satisfy it — and nothing else: no summary of the artifact, no verdict, no edit to the file. Fix each inline, then re-check what changed.
11. **Approval gate** — present the architecture in 1-2 sentences, main components, non-obvious decisions, 1-2 risks with mitigation, then ask *"Move to tasks?"*
12. **Update the active feature's `STATE.md ## Progress`** — phase and next step. See [memory.md](../references/memory.md).

A project-level decision (a convention future features must follow) is appended to `CONTEXT.md ## Decisions`; a local decision stays in `design.md`.

## Template: `design.md`

ALWAYS use this exact template structure. Conditional sections appear only when their trigger is met.

```markdown
---
name: {slug}
spec: .artifacts/specs/{slug}/spec.md
status: draft
---

# Design: {Feature}

## Scope
{In-scope / out-of-scope — only what affects the design.}

## Architecture Overview
{Brief description + optional mermaid.}

## Components

### [Component Name]
- **Area:** [frontend, backend, or integration layer]
- **Responsibility:** [what this component does]
- **Location:** `[path or files for the component]`
- **Relationships:** [how this component connects to adjacent components, or `none`]
- **Interfaces:** <!-- conditional: only for interfaces that belong clearly to this component -->
  - `[name]([parameters]): [ReturnType]` — [error the caller must handle, when it is a feature decision.]
- **Depends on:** [components or services this component needs, or `none`]
- **Reuses:** [existing code this component builds upon, or `none`]

## Interfaces          <!-- conditional: only for interfaces that cross components -->

### [Interface Name]
- **Operation:** `[name]([parameters]): [ReturnType]`
- **Errors:** [errors the caller must handle when they are feature decisions, or `none`]
- **Between:** [components or services that share this contract]

## Data Model            <!-- conditional: only if the feature involves data -->
{Entities and relations; no exhaustive member enumeration.}

## Endpoints           <!-- conditional: only when the feature exposes or changes an HTTP surface -->

### [VERB] [route]
- **Input:** [path, query, headers, or body relevant to the contract, or `none`]
- **Output:** [response contract]
- **Responses:** [status codes and errors that carry a feature decision]

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

## Design Gaps Discovered During Implementation  <!-- conditional: only when implement records a design gap; written there, not here -->
| Gap | Correction |
|-----|------------|
```

A placement, trigger, tool, or dependency with ≥2 viable entry points is a Decisions row, not a silent mechanical pick: record the choice and name the ruled-out alternative in its `Rejected` cell, even when one looks obvious. A `Rejected` cell is empty only when the decision genuinely had one viable home.

An interface is an internal contract between components or services. Keep it inside a component block when it belongs clearly to that component; put a cross-component contract in the separate `Interfaces` section. An endpoint is a public HTTP contract and stays in the separate `Endpoints` section. Do not add an endpoint-to-component link.

Component names are exact references for `Builds`. Keep each name unique, do not use a comma, and do not use the reserved name `none`.

The `Reuses` field records reuse at any altitude the codebase already carries the value: an imported module or helper, and equally a derivation the code already computes near where the new logic lands, cited by `file:line`. A new local that recomputes such a derivation is not reuse — name the existing one in the field so the build reuses it rather than authoring a second copy.

A `Mitigation` that accepts a cost names the constraint that forces it — an API exposing no hook, a platform limit, a contract that cannot change. An `AC-N.M` is not a constraint: it states what must be true, not what cannot be otherwise, so it never explains why a cost is unavoidable. Cite the mechanism, or the cost was never actually weighed.

MUST NOT contain: acceptance criteria restated (traceability references `AC-N.M`, never copies it), observable-behavior clauses (`When Y, then Z` — that is spec), function bodies, tests, step sequences, or commit order (those are tasks). Say *where* and *what responsibility*, never *how the function is written internally*. This bars authoring a body, not reading one: exploration reads existing code, and pointing the `Reuses` cell at a derivation that code already computes (by `file:line`) records reuse, not a body. Subsystem presence is a declared assumption (`assumes X via file:line`), not a proof of wiring.
