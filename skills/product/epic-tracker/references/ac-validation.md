# AC Validation

Enforce Given/When/Then 1:1 acceptance criteria on Story create and on
edits that change AC text. Strict, atomic blocks keep each AC testable
and let it reshape cleanly downstream; a compound or malformed AC is
ambiguous to anything that consumes it.

## When to Use

- Auto-loaded by `story.md` (Step 3 Validate, before save or push)
- Auto-loaded by `update-story.md` when an edit changes AC text
- Direct trigger: "validate AC", "AC validation rules", "story acceptance criteria format"

This ref is the single home for the AC contract. Do not duplicate the
rules in `story.md` or `update-story.md` -- both load this ref at the
validation step.

## AC Schema

Each AC is a `### AC-N` markdown heading followed by three bold-labeled
list items, one per line, plus an optional `**Satisfies**` line. No
compound clauses.

```markdown
### AC-1

**Given** {single precondition}
**When** {single action}
**Then** {single observable outcome}
**Satisfies** {one parent-epic requirement id — optional}
```

Rules:

- 1 AC = 1 Given + 1 When + 1 Then.
- Each AC has a stable id (`AC-1`, `AC-2`, ...; dash-separated, no zero-padding).
- IDs unique within the Story.
- Strings non-empty for all three required fields.
- `**Satisfies**` is optional; when present it names exactly one
  requirement id matching `FR/BR/EC/NFR-<n>` — a single id, never a list.

## Workflow

### 1. Parse

Extract the AC section from the Story body:

- Find the `## Acceptance Criteria` heading.
- Read until the next `## ` heading or end of document.
- Inside that section, every `### AC-N` heading begins a new AC block.
- For each block, read until the next `### ` or the end of the section.
- Within a block, find lines matching `**Given** {value}`, `**When** {value}`, `**Then** {value}`, and an optional `**Satisfies** {value}` (case-insensitive bold label, whitespace-tolerant).

Tolerate tracker normalization: trailing whitespace, blank lines between
blocks, single vs double newlines around headings. Linear occasionally
reflows paragraphs; the parser must not break on these.

Output a list of `{id, given, when, then, satisfies}` tuples (`satisfies`
null when the line is absent) plus any malformed blocks (those that
didn't yield all three required fields).

### 2. Validate

Run V1-V8 against the parsed tuples and the raw section text.

| # | Rule | Strictness | Trigger |
|---|------|------------|---------|
| V1 | Story has at least one AC | strict | parse yields zero `### AC-N` blocks |
| V2 | Each AC has Given + When + Then | strict | tuple missing any of the three fields, or any field empty |
| V3 | No compound Given | strict | two `**Given**` lines under one `### AC-N`, OR Given line contains case-insensitive substring `and given` |
| V4 | No compound Then | strict + confirm | two `**Then**` lines under one `### AC-N` is strict; a single Then line that ` and `-joins two assertions is confirm-to-continue (split or confirm — see sub-rule below) |
| V5 | No duplicate AC | strict | two AC tuples with identical normalized {given, when, then} |
| V6 | Then is observable | warn-only with confirm | Then contains a red word from the list below (case-insensitive whole word) |
| V7 | Unique AC ids | strict | two `### AC-N` blocks with the same id |
| V8 | Satisfies is one well-formed id | strict | a `**Satisfies**` line is present but its value is not exactly one `FR/BR/EC/NFR-<n>` id (empty, a list, or malformed) |

V6 red-word list:

`feel`, `feels`, `intuitive`, `clean`, `nice`, `elegant`, `seamless`,
`smooth`, `natural`, `obvious`, `simple` (when used as a quality
adjective, not a count).

V4 sub-rule (the `and`-joined Then heuristic) is confirm-to-continue, not
hard-reject, because single-sentence assertions can legitimately use
`and` (e.g., "modal appears and account is not deleted until confirmed").
The confirm forces the atomicity decision — split a genuine two-assertion
Then into separate AC, or confirm a single assertion — so every AC that
passes is atomic and reshapes 1:1 into the spec's EARS-lite form
downstream. A duplicate `**Then**` line under one block is always
hard-strict.

### 3. Report

On strict failure, surface a structured error per failed rule:

```text
AC-{id} fails {V#}: {reason}. {suggested fix}.
```

Examples:

```text
AC-1 fails V2: missing Given clause. Add a line "**Given** {precondition}" before the When line.

AC-1 fails V3: compound Given. Split into AC-1 and AC-2, or rephrase as a single precondition. The phrase "and given" is reserved.

AC-2 fails V5: duplicate of AC-1 (same Given/When/Then). Remove or differentiate one of them.

AC-1 fails V7: duplicate id. Renumber to the next free id.

AC-1 fails V8: Satisfies "FR-3, FR-4" names two ids. Name exactly one requirement per AC; split the AC if it operationalizes two.
```

On V6 (warn-only):

```text
AC-{id} warning V6: Then uses non-observable language: "{word}". Suggest rephrasing as a measurable outcome (e.g., "modal appears within 200ms", "redirect to /login"). Continue anyway? [y/N]
```

Default Y. The user may keep the wording; the warning is informational
and does not block.

On V4 (`and`-joined Then, confirm-to-continue):

```text
AC-{id} V4 check: Then joins two assertions with "and": "{then}". Two outcomes -> split into AC-{id} and a new AC. Single assertion -> keep. [split/keep]
```

Default keep. A split routes back to add the second AC; keep records a
single-assertion confirmation so the AC stays atomic for the downstream
1:1 reshape.

If any strict rule fails: do not proceed to save or push. The caller
(`story.md` Step 3 or `update-story.md` validation branch) loops back to
review until the user fixes the AC.

## Satisfies linkage

V8 checks the shape of a `**Satisfies**` value. Two further relations hold
across the epic↔story boundary — neither parsed here (this ref reads the
story's AC section in isolation), both owned by the create/edit flow that
has the parent epic in hand:

- **Link validity** — a present `Satisfies` references a requirement the
  parent epic declares in its `## Requirements`. `story.md` checks this
  when the parent epic is loaded; a dangling id routes back to fix.
- **Requirement coverage** — every requirement the epic declares is
  operationalized by ≥1 AC `Satisfies` across its child stories. This is
  an epic-level relationship, documented not gated.

`Satisfies` stays optional per AC: an AC may be implied quality with no
backing requirement. What is enforced is shape (V8); the two relations
above hold upstream.

## Read-path tolerance

Read paths do not invoke this ref:

- Pull from tracker (`sync.md` Pull Direction) -- legacy bodies may carry
  pre-Gherkin AC; the implementation consumer decides how to handle them.
- Read-only navigation from epic checklist -- no validation runs.
- `status.md` overview reads -- no body inspection.

Stories created before this ref existed are not retroactively validated.
Edits that do not change AC text also skip validation (see
`update-story.md` diff branch 1).

## Guidelines

**DO:**
- Parse the AC section with whitespace-tolerant matching so tracker normalization does not break the validator
- Surface every strict failure with AC id, rule name, and a concrete suggested fix
- Keep V6 warn-only with a default-allow confirm to avoid blocking on heuristic false positives
- Treat the V6 red-word list as small and stable; expand it only when a documented false negative recurs
- Run validation locally before any tracker round-trip so failures cost no MCP latency

**DON'T:**
- Invent AC content for the user (contrasts: surface failures, let the user fix)
- Validate on pull or read-only navigation (contrasts: validate only on create and AC-text-changing edits)
- Block on V6 (contrasts: warn-only with confirm)
- Embed validation logic in `story.md` or `update-story.md` (contrasts: this ref is the single home; both load it)

## Error Handling

- AC section missing entirely: V1 fires; ask the user to add at least one `### AC-N` block.
- Block has heading but no Given/When/Then lines: V2 fires per missing field.
- User explicitly wants compound semantics: V3/V4 still reject; route them to split into multiple AC blocks.
- Tracker body returns malformed markdown (Linear collapsed list items): widen the parser regex tolerance; if still unparseable, route to manual fix in the tracker UI.
- V6 false positive (e.g., "the user feels confident" where intent is observable): user accepts the warning; nothing blocks.

## Outcomes

- On pass: caller proceeds (Save/Push in create flow, or persist edit in edit flow).
- On strict fail: caller loops back to review with the structured error visible to the user.
- Block shape is a stable contract: each `### AC-N` is `id` + Given/When/Then plus an optional `**Satisfies**` line. Keep the shape stable so any downstream consumer that parses these blocks does not break.
