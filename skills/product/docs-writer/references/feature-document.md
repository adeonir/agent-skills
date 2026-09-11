# Feature Document Rules

Shared lifecycle, update, source, and archival rules for temporary feature PRDs and RFCs.

## When to Use

Load before creating or updating a feature PRD or RFC.

## Lifecycle

Set a new document to `Proposed`. Set it to `Accepted` only after explicit approval. An accepted document may become `Deprecated` or `Superseded by <feature-slug>`.

## Updates

Preserve `created`, `sources`, and the existing status unless the user requests a status change. Set `updated` when changing an existing document. Preserve sections outside the approved change.

## Sources and archive

Populate `sources` with user-supplied files or URLs that informed the document; use `[]` only when no source was supplied. Archive the complete feature folder manually at `.artifacts/archive/features/<created>-<feature-slug>/`. Do not archive automatically.

Keep the approved feature document self-contained. A source link in a later delivery artifact is provenance only.
