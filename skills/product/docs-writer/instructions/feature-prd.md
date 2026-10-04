# Feature PRD

Create a temporary, focused product requirements document for one feature.

## Workflow

```text
resolve location → check feature artifact
├ upload requested → upload → report
├ absent → focused discovery → validation → write
└ present → requested update → write
```

1. Load [discovery.md](../references/discovery.md) for the interview method and trust boundary, and [feature-document.md](../references/feature-document.md) for lifecycle, update, source, and archive rules. When the `## Issue tracker` section of the repository `AGENTS.md` or `CLAUDE.md` names Linear, also load [tracker-document.md](../references/tracker-document.md) for a document that lives on a Linear issue.
2. Resolve the feature slug. When `tracker-document.md` is loaded, resolve the location per its `## Resolve the Location`, and when the user asks to upload the document to an issue, run its `## Upload` and stop. Otherwise the location is the local path, and an upload request reports that no Linear tracker is configured. Read the existing document from its location when it exists: the `PRD: ` document on the issue, or `.artifacts/features/<feature-slug>/PRD.md`. Read repository documents only for context, and treat their claims as claims to verify. Do not copy roadmap, release, task, or implementation language into this document.
3. Run focused discovery for the problem, affected users, goals, scope, user journeys, business rules, edge cases, risks, dependencies, assumptions, and open questions. Keep the unit of planning to one feature.
4. Validate the scope. Mark unknowns as assumptions or open questions instead of inventing them.
5. Run the checks in [quality.md](../references/quality.md) before writing. Read `<this-skill>/assets/feature-prd.template.md`, use its exact structure, remove every optional section or subsection that has no content, delete comments, and replace every remaining square-bracket slot.
6. When the document lives on the issue, write it per [tracker-document.md](../references/tracker-document.md) `## Edit on the Issue`, then reread it per [quality.md](../references/quality.md) `## Reread`. Otherwise populate `sources` from supplied files or URLs, or leave it `[]` when none were supplied. Write `.artifacts/features/<feature-slug>/PRD.md` with the lifecycle status set by [feature-document.md](../references/feature-document.md), then reread it per [quality.md](../references/quality.md) `## Reread`.
7. Identify content that should become durable project knowledge. Recommend promoting stable product context to the project PRD or Design Doc, general codebase knowledge to `PROJECT.md`, and permanent architectural decisions to an ADR. Do not update those documents automatically.
8. **Report.** Report the path or the document URL, what the document holds in one to three sentences with its approval status for a local document — what changed, on an update — and any open question it carries. Never paste the document. The paired-document order is controlled by the entrypoint.

## Boundaries

Use journeys and goals, not tracker User Stories. Do not include PRODUCT, roadmap, architecture, detailed technical contracts, implementation tasks, or release plans. Do not invoke or mention another skill. The document ends at approval.
