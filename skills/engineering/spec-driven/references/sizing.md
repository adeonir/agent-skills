# Sizing

The four scopes, what each phase produces at each scope, and the safety valve that raises a level when the scope breaks.

## When to Use

During specify, once discovery is done, to set `scope`. Also read whenever any later phase (design, tasks, implement) suspects the scope was mis-sized and needs to re-evaluate.

## The measurement

One measurement, taken after discovery, plus a quick trivial triage at the start that catches the obvious Small. The criterion is how many load-bearing decisions the change requires, and whether any is new to the codebase — file count is a consequence, not an input. Default adversarial: when in doubt, size up.

## The four scopes

| Scope | Nature of change | spec.md | design.md | tasks.md | implement | audit |
|-------|------------------|---------|-----------|----------|-----------|-------|
| **Small** | Mechanical, zero load-bearing decisions | one-liner (no `spec.md`) | skip | skip | inline | skip (inline verify) |
| **Medium** | Canonical pattern reapplied | full | full, no approaches / heavy research | full | subagent | subagent |
| **Large** | ≥1 load-bearing decision new to the codebase | full | full + research when needed | full | subagent | subagent |
| **Complex** | Ambiguity in the problem itself | full + `discuss.md` | full + approaches + research | full | subagent | subagent |

Small does not produce a spec and does not run the pipeline: one-liner → branch → inline implement → inline verify.

Every scope that produces an artifact peer-checks it: `spec.md`, `design.md`, and `tasks.md` are each read by a subagent that did not write them before their approval gate. The check does not scale with scope — an artifact either survives a reader who did not author it or it does not.

## Safety valve

If, at any phase, the scope breaks — a new load-bearing decision appears, inline steps run past ~5, dependencies turn out more complex than planned, or the work needs approaches or heavy research — **stop and re-evaluate the sizing**. Raise one level; never push through in implement.

- **Small → Medium** — the one-liner becomes a `spec.md`; the full pipeline applies. Specify's triage catches it up front; a Small that breaks only once inline implement starts is caught there and routed back to specify.
- **Medium → Large** — more depth to the design, with research where the knowledge chain runs out.
- **Large → Complex** — add `discuss.md` and design approaches.

The valve is the one guard against a scope quietly growing until it overruns an under-planned phase.
