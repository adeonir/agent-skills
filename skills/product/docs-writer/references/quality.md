# Quality Standards

Quality checks for requirements and document integrity before writing any document to disk.

## When to Use

Load during the Drafting phase, before writing any document to disk, and again after writing it.

## Requirements Quality

Requirements must be concrete across all document types: state the observable behavior or quality, never a vague adjective. Put a number in only when the user supplied it or the project already has it; otherwise state the requirement in words, or mark it TBD when the decision is open. Never invent a figure to fill a field.

| Bad | Good |
|-----|------|
| "Search should be fast" | "Search results appear without a visible wait on mobile networks" |
| "Easy to use" | "A new user completes onboarding without help text" |
| "Intuitive interface" | "The main action is reachable from the first screen" |

## Declare, Don't Narrate

What produced a document is not what the document says. The conversation is input; the document states standing facts in present tense.

A resolved decision enters as fact (`Reset links expire in 15 minutes`), never as its history (`we discussed 24 hours but the user preferred 15 minutes`). Strip conversation narrative — "as discussed", "the user confirmed", "we agreed", "you chose" — and decision history. An updated document states the new state, never the change. An ADR Decision keeps its "We will..." form.

A section that keeps alternatives, such as an ADR's Alternatives Considered, records each rejected option and why it fails, never the exchange that rejected it.

## Review Checklist

Before writing any document to disk, verify:

- [ ] No contradictions: read each statement that excludes or limits (an Out of Scope item, a Won't Have item) against each statement that requires (a Must Have item, a Should Have item, a phase delivery). A pair that cannot both hold is a contradiction — resolve it with the user.
- [ ] No unresolved TBDs that block the document's purpose
- [ ] Scope is focused (one document, one purpose)
- [ ] Cross-references to other docs are valid
- [ ] Requirements are concrete (no vague adjectives) and carry no invented numbers
- [ ] The document declares and does not narrate, per `## Declare, Don't Narrate`

**If any check fails, fix the document, run that check again, and write only after it passes.** Apply all checks to both new and updated documents.

Mark an unknown as TBD rather than inventing a constraint to fill the slot.

## Writing and Reporting

Write the document to its path directly, and reread it per `## Reread`. Then report the path, what the document holds in one to three sentences — what changed, on an update — and any open question or TBD it carries. Never paste the document.

## Reread

After writing, read the written file whole and run the Review Checklist and the gates for its type over it. When a check finds a contradiction or a gap the document cannot settle on its own, interview the user about it, one question at a time, and fix the file from the answer. Read the file again until every check passes; report only after that.

## ADR-Specific Gates

When the document is an ADR, additionally verify:

- [ ] Exactly one decision is recorded (not bundled with others)
- [ ] Decision stated as a positive imperative ("We will...")
- [ ] Context is value-neutral (states forces, does not advocate)
- [ ] Title states the decision in the affirmative imperative
- [ ] Alternatives not selected sit in Alternatives Considered with their reasons, not in Context
- [ ] The ADR fits on one page
- [ ] Consequences capture the material outcomes of the decision
- [ ] Frontmatter contains `name`, `status`, `date`, `updated`, and `sources`
- [ ] References follow the document reference pattern
- [ ] Numbering is sequential and zero-padded (no gaps, no duplicates)
- [ ] When superseding, the prior ADR's `status` names its replacement

## Document Boundaries

Apply these boundaries to the PRD and Design Doc. Keep each subject in its owning document and link to it from related documents.

**When the document is a PRD, verify:**

- [ ] No architecture, tech stack, framework choices, or deployment topology — those belong to the Design Doc
- [ ] No API contracts, endpoint paths, request/response shapes, or database schema details
- [ ] No UI component names, library references, or styling instructions
- [ ] NFRs state the requirement without prescribing the mechanism ("search stays responsive on mobile networks" not "use Redis caching")
- [ ] No positioning (What/Why/Who, personality, anti-references) in any section — it lives in PRODUCT

**When the document is a Design Doc, verify:**

- [ ] Overview is one paragraph plus a diagram and does not duplicate the PRD's Problem or Audience
- [ ] PRD requirements are cited by ID, not restated
- [ ] No product framing prose ("users will love...", "this drives engagement...") in any section

## Design Doc-Specific Gates

When the document is a Design Doc, additionally verify:

- [ ] Every Stack item carries a one-line justification, and `ADR-NNN` where an ADR records the choice
- [ ] Non-Functional Requirements cite each NFR by ID and state how the design meets it, never the requirement text
- [ ] Optional sections appear only where they shape the design — no exhaustive coverage of axes with no decision behind them
- [ ] `sources` lists supplied input; References lists related documents that exist
