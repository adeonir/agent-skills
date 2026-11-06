# Artifact Content

What may enter an artifact's body, and what the inputs that produced it never contribute.

## When to Use

Loaded by every instruction that drafts or edits an artifact body, before writing it.

## The template holds either way

Create and edit both conform the artifact to its canonical template: the structure and the MUST-NOT boundaries hold on an edit exactly as on a create, never a free-form write.

## Declare, don't narrate

What produced an artifact is not what the artifact says. The conversation is input; the body states standing facts in present tense.

A resolved decision enters as fact (`Reset links expire in 15 minutes`), never as its history (`we discussed 24 hours but the user preferred 15 minutes`). Strip conversation narrative — "as discussed", "the user confirmed", "we agreed" — and decision history. An unresolved decision goes to Open Questions, never into the prose as though it were settled.

## Translate, don't replicate

Upstream sources — a project PRD, feature PRD, feature design doc, design doc, ADR, parent epic, pasted log or advisory — stay read-only. Extract only what maps to this artifact, then say it in the artifact's own language: strip section numbers, reference and ticket codes, code identifiers, and document or sibling-artifact names. The artifact carries the facts, not the source's tokens. Where a stripped token still has to survive, the drafting instruction names the field that holds it.

## Title

A title is a short human-readable phrase, slug-safe. No commands, flags, file paths, parentheses, brackets, or pipes — it becomes a branch name slug downstream. It is declarative:

- **Epic** — names what users get (`User authentication`), never a narrative outcome (`Users can sign in securely`).
- **Task** — names the deliverable (`Reset password flow`), never a narrative outcome (`User can reset their password to regain access`).
- **Spike** — names the subject of the question (`Queue provider choice`), never the question itself (`Which queue provider should we use?`) and never an answer.
- **Bug** — names the defect (`Login fails with expired token`), never a narrative of the fix or its outcome (`Users stay logged in after token refresh`).

The name is translated from its source, not copied: strip any borrowed token — reference or ticket codes, section numbers, code identifiers, document or sibling-artifact names — which travel in the body, in References, or on a bug in Signals, never the title. The title maps to the tracker's summary field; outcome prose lives only in the body.

## Every line traces to a source

A constraint or a criterion is written only when it traces to a source — a file in the repository, a linked doc, the parent epic, pasted context, or what the user stated.

Filling an acceptance criterion, a success criterion, or an open question with generic best-practice lore — "a slow pre-commit hook trains the developer to skip it", "this will not scale", "cache invalidation gets tricky here" — states a concern the project never reported. It reads as a finding and behaves as scope: the invented concern pulls an implementation decision nobody asked for, and the reader cannot tell it apart from the constraints that came from the repository.

When one feels real but has no source, ask instead of asserting. The answer either becomes a sourced line or does not enter the artifact.
