---
name: docs-writer
description: "Product and technical document creation through guided discovery, including project PRDs, feature PRDs, feature RFCs, audit reports, positioning docs, Design Docs, and ADRs, plus archiving of feature folders. Use when defining requirements, consolidating findings from external audits, feature proposals, strategy, trade-offs, or architecture decisions, or when archiving a feature. Not for running audits, UI design, implementation, or meeting notes."
---

# Docs Writer

## Triggers

| Type | Load |
|------|------|
| PRD — product requirements | [prd.md](instructions/prd.md) |
| Feature PRD — temporary feature requirements | [feature-prd.md](instructions/feature-prd.md) |
| Feature RFC — temporary feature proposal | [feature-rfc.md](instructions/feature-rfc.md) |
| Audit report — consolidated findings from supplied audit outputs | [feature-audit.md](instructions/feature-audit.md) |
| PRODUCT — strategic positioning and identity | [product.md](instructions/product.md) |
| Design Doc — lean technical design and trade-offs | [design.md](instructions/design.md) |
| ADR — single architecture decision record | [adr.md](instructions/adr.md) |
| Archive feature — move feature folders to cold storage | [feature-archive.md](instructions/feature-archive.md) |

Detect the document type from the trigger. If ambiguous, ask the user.

For a feature request that asks for both documents, load `feature-prd.md` first and then `feature-rfc.md`.

## Workflow

```text
trigger → detect type → load instruction → locate document → drafting
  document exists → update the requested parts
  document absent → full discovery
  ADR → create a numbered record or update the requested record

archive → select feature folders → move to .artifacts/archive/features/
```
