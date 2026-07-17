# Epic Derivation

Cluster a PRD into a set of capability-level epics — the method that turns requirements into candidate epics before they are evaluated and ordered.

## When to Use

Composed by `decompose` at level 1 (roadmap → epics), after the PRD is read and before ICE scoring. It produces the candidate set; it does not rank or order it (that is `ice-scoring.md` and the ordering step in `decompose`).

## What an Epic Is

An epic is a **deliverable capability that groups stories** — a coherent slice of product the delivery can plan, sequence, and demo. The boundary is where one capability ends and the next begins. Name epics as capabilities, never as UI widgets, endpoints, or technologies.

## The Seams

Read the PRD for the natural cut lines. Cluster requirements into epics along these seams, most-primary first:

- **User Journeys** — a coherent end-to-end journey is the strongest seam; it usually maps to one epic that delivers demonstrable value on its own.
- **Scope capabilities** (Must/Should/Could) — a capability that does not belong to a single journey becomes its own epic.
- **Cross-cutting Business Rules and NFRs** — a rule or quality target that serves *several* journeys (identity, data model, permissions, performance) does not belong inside one feature epic; it becomes a **foundation epic** the others depend on.
- **Definition of Done** — when the PRD's DoD requires post-ship validation, that becomes a dedicated **readiness epic**.

## Boundaries

Every candidate carries a one-line boundary: the capability it owns and the adjacent capability it explicitly does not. Boundaries partition the PRD's scope — where one epic's slice ends, the neighbor's begins. Work claimed by two epics means the boundary is wrong, not that the work is shared.

A foundation or readiness epic derived from cross-cutting rules carries the requirement IDs of those rules; an epic derived from purely enabling work with no PRD line legitimately carries none.

## Guidelines

- Cut along journeys first; promote cross-cutting concerns to foundation epics rather than scattering them into feature epics.
- Name the capability, not the mechanism — "secure password storage", not "bcrypt hashing".
- Decide the boundary before the count — the number of epics falls out of the seams, it is not a target.
- Read the PRD as a claim, not authority: where its scope leaves a requirement no epic can plausibly own, or two requirements contradict, surface the disagreement instead of forcing a cut around it.
