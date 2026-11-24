# Epic Derivation

Cluster a PRD into a set of epics, one per user outcome plus the foundations they depend on — the method that turns requirements into candidate epics before they are evaluated and ordered.

## What an Epic Is

An epic groups tasks around **one outcome that users receive and evaluate on their own**, or around a foundation: work other epics depend on, which users may never see. The boundary is where one outcome ends and the next begins. Name an epic for what users get, never for a UI widget, an endpoint, or a technology.

## The Seams

Read the PRD for the natural cut lines. Cluster requirements into epics along these seams, most-primary first:

- **User outcomes** — requirements that serve one outcome users can evaluate on its own form one epic, even when several outcomes serve one product goal. The order of the requirements in the PRD never decides what stays together.
- **Cross-cutting NFRs** — a quality requirement that serves *several* outcomes (identity, data model, permissions, performance) does not belong inside one epic; it becomes a **foundation epic** the others depend on.

## Boundaries

Every candidate carries a one-line boundary: the outcome it owns and the adjacent outcome it explicitly does not. Boundaries partition the PRD's scope — where one epic's slice ends, the neighbor's begins. Work claimed by two epics means the boundary is wrong, not that the work is shared.

A foundation epic derived from cross-cutting NFRs carries the requirement IDs of those NFRs; an epic derived from purely enabling work with no PRD line legitimately carries none.

## Guidelines

- Decide the boundary before the count — the number of epics falls out of the seams, it is not a target.
