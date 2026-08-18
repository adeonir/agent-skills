# Update an Existing Document

Read an existing PRD, PRODUCT, or Design Doc and update only the requested parts.

## When to Use

When `docs/product/PRD.md`, `docs/product/PRODUCT.md`, or `docs/tech/design-doc.md` already exists. Discover any absent document; see [discovery.md](discovery.md) `## Discovery or Update by Document State`. Load this reference when the target document exists. Do not use it as a direct trigger.

## Procedure

```text
read → scope → validate changes → state unchanged parts → confirm → write
```

1. **Read.** Apply [discovery.md](discovery.md) `## Reading Project Files`, then read the existing documents. Identify the supported content already present. Do not ask for this information again.
2. **Set the scope.** Identify what the user wants to change and what the change directly affects. If the request is unclear, ask for the missing detail.
3. **Validate the changes.** Apply [discovery.md](discovery.md) `## Critical Review` only to the planned changes. Ask what evidence supports the change. Report conflicts with unchanged sections, such as a metric that conflicts with a persona or a rule that breaks a journey.
4. **State unchanged parts.** Before writing, name the sections that will change and those that will remain unchanged. Let the user correct this boundary.
5. **Confirm the plan.** Get explicit agreement on the planned changes before editing.
6. **Write.** Preserve every section outside the confirmed scope. Use the matching template only to check the existing structure; never copy a template over unchanged content. Write the document to its path, then briefly state what changed and where. Do not paste the full document.

## Reading the Sibling Artifact

If either PRD or PRODUCT is absent, read the existing document for context only. Do not copy its prose. Keep requirements in the PRD. Keep audience relationship, refused aesthetics, and differentiation in PRODUCT. Use confirmed facts from the existing document to avoid repeated questions. This rule applies only to the PRD and PRODUCT pair.

## Frontmatter on Reconcile

Preserve `created` and `sources`. Set `updated` to the current date. Preserve the PRD or PRODUCT `status` unless the user explicitly changes it. The Design Doc has no `status` field.
