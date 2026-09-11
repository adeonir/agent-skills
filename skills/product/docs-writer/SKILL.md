---
name: docs-writer
description: "Product and technical document creation through guided discovery, including project PRDs, feature PRDs, feature RFCs, positioning docs, Design Docs, and ADRs. Use when defining requirements, feature proposals, strategy, trade-offs, or architecture decisions. Not for UI design, implementation specs, or meeting notes."
---

# Docs Writer

## Triggers

| Type | Load |
|------|------|
| PRD — product requirements | [prd.md](instructions/prd.md) |
| Feature PRD — temporary feature requirements | [feature-prd.md](instructions/feature-prd.md) |
| Feature RFC — temporary feature proposal | [feature-rfc.md](instructions/feature-rfc.md) |
| PRODUCT — strategic positioning and identity | [product.md](instructions/product.md) |
| Design Doc — lean technical design and trade-offs | [design.md](instructions/design.md) |
| ADR — single architecture decision record | [adr.md](instructions/adr.md) |

Detect the document type from the trigger. If ambiguous, ask the user.

For a feature request that asks for both documents, load `feature-prd.md` first and then `feature-rfc.md`.

## Workflow

```text
trigger → detect type → load instruction → check disk → drafting
  document exists → update the requested parts
  document absent → full discovery
  ADR → create a numbered record or update the requested record
```
