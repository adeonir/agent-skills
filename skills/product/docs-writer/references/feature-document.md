# Feature Document Rules

Shared lifecycle, update, and source rules for temporary feature PRDs and RFCs.

## When to Use

Load before creating or updating a feature PRD or RFC.

## Lifecycle

Set a new document to `proposed`. Set it to `accepted` only after explicit approval. An accepted document may become `deprecated` or `superseded by <feature-slug>`.

## Updates

Preserve `created`, `sources`, and the existing status unless the user requests a status change. Set `updated` when changing an existing document. Preserve sections outside the requested change.

## Sources

Populate `sources` with user-supplied files or URLs that informed the document; use `[]` only when no source was supplied. Never archive the feature folder while writing a document.

Keep the approved feature document self-contained. A source link in a later delivery artifact is provenance only.
