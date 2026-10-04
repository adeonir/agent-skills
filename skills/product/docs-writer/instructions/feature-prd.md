# Feature PRD

Create a temporary, focused product requirements document for one feature.

## Workflow

```text
check feature artifact
├ absent → focused discovery → validation → write
└ present → requested update → write
```

1. Load [discovery.md](../references/discovery.md) for the interview method and trust boundary, and [feature-document.md](../references/feature-document.md) for lifecycle, update, source, and archive rules.
2. Resolve the feature slug and read `.artifacts/features/<feature-slug>/PRD.md` when it exists. Read repository documents only for context, and treat their claims as claims to verify. Do not copy roadmap, release, task, or implementation language into this document.
3. Run focused discovery for the problem, affected users, goals, scope, user journeys, business rules, edge cases, risks, dependencies, assumptions, and open questions. Keep the unit of planning to one feature.
4. Validate the scope. Mark unknowns as assumptions or open questions instead of inventing them.
5. Run the checks in [quality.md](../references/quality.md) before writing. Read `<this-skill>/assets/feature-prd.template.md`, use its exact structure, remove every optional section or subsection that has no content, delete comments, and replace every remaining square-bracket slot.
6. Populate `sources` from supplied files or URLs, or leave it `[]` when none were supplied. Write `.artifacts/features/<feature-slug>/PRD.md` with the lifecycle status set by [feature-document.md](../references/feature-document.md), then reread it per [quality.md](../references/quality.md) `## Reread`.
7. Identify content that should become durable project knowledge. Recommend promoting stable product context to the project PRD or Design Doc, general codebase knowledge to `PROJECT.md`, and permanent architectural decisions to an ADR. Do not update those documents automatically.
8. Report the path and approval status. The paired-document order is controlled by the entrypoint.

## Boundaries

Use journeys and goals, not tracker User Stories. Do not include PRODUCT, roadmap, architecture, detailed technical contracts, implementation tasks, or release plans. Do not invoke or mention another skill. The document ends at approval.
