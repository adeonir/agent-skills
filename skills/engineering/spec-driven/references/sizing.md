# Sizing

The four scopes, what each phase produces at each scope, and the safety valve that raises a level when the scope breaks.

## When to Use

During specify, once discovery is done, to set `scope`. Also read whenever any later phase (design, tasks, implement) suspects the scope was mis-sized and needs to re-evaluate.

## The measurement

One measurement, taken after discovery, plus a quick trivial triage at the start that catches the obvious Small. The criterion is how many load-bearing decisions the change requires, and whether any is new to the codebase — file count is a consequence, not an input. Default adversarial: when in doubt, size up.

## The four scopes

| Scope | Nature of change | spec.md | design.md | tasks.md | implement | validate | audit |
|-------|------------------|---------|-----------|----------|-----------|----------|-------|
| **Small** | Mechanical, zero load-bearing decisions | one-liner (no `spec.md`) | skip | skip | inline | skip | skip (inline verify) |
| **Medium** | Canonical pattern reapplied | full; ambiguity logged where it cannot be closed | full, no approaches / heavy research | full | subagent | optional, `user-facing` only | optional subagent |
| **Large** | ≥1 load-bearing decision new to the codebase | full; ambiguity closed | full + research when needed | full | subagent | optional, `user-facing` only | optional subagent |
| **Complex** | Ambiguity in the problem itself | full + `discuss.md` | full + approaches + research | full | subagent | optional, `user-facing` only | optional subagent |

Small does not produce a spec and does not run the pipeline: one-liner → branch → inline implement → inline verify.

`spec.md` and `design.md` are each read by a subagent that did not write them before their approval gate. The check does not scale with scope — an artifact either survives a reader who did not author it or it does not. `tasks.md` is not peer-checked: it sequences decisions already settled upstream, and every claim it makes is re-read against running code — by the safety valve when a task turns out to carry a decision, and by the audit's discrimination sensor when a gate would pass with the logic removed.

A peer reads no wider than the phase that wrote the artifact. Where the phase derives its work from artifacts alone, so does its peer, and a claim those artifacts cannot support is a finding rather than a prompt to go searching; where the phase's contract traces claims to the codebase, its peer reaches there too. The reach follows each phase's contract, never one uniform rule across the two.

## Safety valve

If, at any phase, the scope breaks — a new load-bearing decision appears, inline steps run past ~5, dependencies turn out more complex than planned, or the work needs approaches or heavy research — **stop and re-evaluate the sizing**. Raise one level; never push through in implement.

- **Small → Medium** — the one-liner becomes a `spec.md`; the full pipeline applies. Specify's triage catches it up front; a Small that breaks only once inline implement starts is caught there and routed back to specify.
- **Medium → Large** — the spec closes its ambiguity instead of logging it; the design gains research where the knowledge chain runs out.
- **Large → Complex** — add `discuss.md` and design approaches.

The valve is the one guard against a scope quietly growing until it overruns an under-planned phase.
