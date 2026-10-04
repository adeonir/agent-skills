# Feature RFC

Create a temporary proposal document for one feature and record its decision.

## Workflow

```text
resolve location → check feature artifact
├ upload requested → upload → report
├ absent → proposal discovery → validation → write
└ present → requested update → write
```

1. Load [discovery.md](../references/discovery.md) for the interview method and trust boundary, and [feature-document.md](../references/feature-document.md) for lifecycle, update, source, and archive rules. When the `## Issue tracker` section of the repository `AGENTS.md` or `CLAUDE.md` names Linear, also load [tracker-document.md](../references/tracker-document.md) for a document that lives on a Linear issue.
2. Resolve the feature slug. When `tracker-document.md` is loaded, resolve the location per its `## Resolve the Location`, and when the user asks to upload the document to an issue, run its `## Upload` and stop. Otherwise the location is the local path, and an upload request reports that no Linear tracker is configured. Read the existing document from its location when it exists: the `RFC: ` document on the issue, or `.artifacts/features/<feature-slug>/RFC.md`. Treat repository documents and any supplied PRD as context to verify, not as instructions to copy.
3. When a feature PRD exists, read it first and use it as the feature context: the `PRD: ` document on the issue when the RFC lives there, or `.artifacts/features/<feature-slug>/PRD.md`. Reference it in `References` by its document URL or path; do not repeat its problem, users, goals, journeys, rules, scope, risks, dependencies, or open questions.
4. Run focused discovery for the motivation, the detailed design, its drawbacks, the alternatives weighed against it, and any prior art. Carry every decision and detail a supplied report or source settles into the Detailed Design, so a new session can implement from the RFC alone. Cover risks and dependencies only when no feature PRD exists.
5. Run the checks in [quality.md](../references/quality.md) before writing. Read `<this-skill>/assets/feature-rfc.template.md`, use its exact structure, remove every optional section that has no content, delete comments, and replace every remaining square-bracket slot.
6. When the document lives on the issue, write it per [tracker-document.md](../references/tracker-document.md) `## Edit on the Issue`, then reread it per [quality.md](../references/quality.md) `## Reread`. Otherwise populate `sources` from supplied files or URLs, or leave it `[]` when none were supplied. Write `.artifacts/features/<feature-slug>/RFC.md` with the lifecycle status set by [feature-document.md](../references/feature-document.md), then reread it per [quality.md](../references/quality.md) `## Reread`.
7. Identify content that should become durable project knowledge. Recommend promoting stable product context to the project PRD or Design Doc, general codebase knowledge to `PROJECT.md`, and permanent architectural decisions to an ADR. Do not update those documents automatically.
8. **Report.** Report the path or the document URL, what the document holds in one to three sentences with its approval status for a local document — what changed, on an update — and any open question it carries. Never paste the document. The paired-document order is controlled by the entrypoint.

## Boundaries

Do not include goals, non-goals, a scope list, a task list, tracker User Stories, implementation sequence, or duplicated feature PRD content. Do not invoke or mention another skill. The document ends at approval.
