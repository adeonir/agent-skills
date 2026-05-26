# Quality Standards

Quality gates for requirements and document integrity before presenting
any draft to the user.

## When to Use

Load during the Drafting phase, before presenting any document to the user.

## Requirements Quality

Requirements must be concrete and measurable across all document types.

| Bad | Good |
|-----|------|
| "Search should be fast" | "Search returns results within 200ms" |
| "Easy to use" | "New users complete onboarding in under 2 minutes" |
| "Intuitive interface" | "Task completion rate above 90% without help text" |

## Review Checklist

Before presenting any document to the user, verify:

- [ ] No contradictions between sections
- [ ] No unresolved TBDs that block the document's purpose
- [ ] Scope is focused (one document, one purpose)
- [ ] Cross-references to other docs are valid
- [ ] Requirements are concrete and measurable (no vague adjectives)

## ADR-Specific Gates

When the document is an ADR, additionally verify:

- [ ] Exactly one decision is recorded (not bundled with others)
- [ ] Decision stated as a positive imperative ("We will...")
- [ ] Context is value-neutral (states forces, does not advocate)
- [ ] Consequences include both positive AND negative outcomes
- [ ] At least one alternative is recorded with a rejection reason
- [ ] Numbering is sequential and zero-padded (no gaps, no duplicates)
- [ ] When superseding, frontmatter `supersedes` and prior ADR's
      `superseded-by` are both populated

If issues found: fix inline before presenting.
