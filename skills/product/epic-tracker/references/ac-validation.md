# AC Validation

Enforce Given/When/Then 1:1 acceptance criteria on Story create and on
edits that change AC text. The downstream `planner` subagent (cross-repo
consumer) parses `### AC-N` blocks to derive `ac.json`; without strict
upstream enforcement, every Story is escalated as ambiguous.

## When to Use

- Auto-loaded by `story.md` (Step 4 Validate, before save or push)
- Auto-loaded by `update-story.md` when an edit changes AC text
- Direct trigger: "validate AC", "AC validation rules", "story acceptance criteria format"

This ref is the single home for the AC contract. Do not duplicate the
rules in `story.md` or `update-story.md` -- both load this ref at the
validation step.

## AC Schema

Each AC is a `### AC-N` markdown heading followed by three bold-labeled
list items, one per line. No compound clauses.

```
### AC-1

**Given** {single precondition}
**When** {single action}
**Then** {single observable outcome}
```

Rules:

- 1 AC = 1 Given + 1 When + 1 Then.
- Each AC has a stable id (`AC-1`, `AC-2`, ...; dash-separated, no zero-padding).
- IDs unique within the Story.
- Strings non-empty for all three fields.

## Workflow

### 1. Parse

Extract the AC section from the Story body:

- Find the `## Acceptance Criteria` heading.
- Read until the next `## ` heading or end of document.
- Inside that section, every `### AC-N` heading begins a new AC block.
- For each block, read until the next `### ` or the end of the section.
- Within a block, find lines matching `**Given** {value}`, `**When** {value}`, `**Then** {value}` (case-insensitive bold label, whitespace-tolerant).

Tolerate tracker normalization: trailing whitespace, blank lines between
blocks, single vs double newlines around headings. Linear and Jira
occasionally reflow paragraphs; the parser must not break on these.

Output a list of `{id, given, when, then}` tuples plus any malformed
blocks (those that didn't yield all three fields).

### 2. Validate

Run V1-V7 against the parsed tuples and the raw section text.

| # | Rule | Strictness | Trigger |
|---|------|------------|---------|
| V1 | Story has at least one AC | strict | parse yields zero `### AC-N` blocks |
| V2 | Each AC has Given + When + Then | strict | tuple missing any of the three fields, or any field empty |
| V3 | No compound Given | strict | two `**Given**` lines under one `### AC-N`, OR Given line contains case-insensitive substring `and given` |
| V4 | No compound Then | strict | two `**Then**` lines under one `### AC-N`, OR Then line contains ` and ` joining two assertions (heuristic: warn-only sub-rule for `and`-joined Then; hard-strict only on duplicate `Then` lines) |
| V5 | No duplicate AC | strict | two AC tuples with identical normalized {given, when, then} |
| V6 | Then is observable | warn-only with confirm | Then contains a red word from the list below (case-insensitive whole word) |
| V7 | Unique AC ids | strict | two `### AC-N` blocks with the same id |

V6 red-word list:

`feel`, `feels`, `intuitive`, `clean`, `nice`, `elegant`, `seamless`,
`smooth`, `natural`, `obvious`, `simple` (when used as a quality
adjective, not a count).

V4 sub-rule (the `and`-joined Then heuristic) is warn-only because
single-sentence assertions can legitimately use `and` (e.g., "modal
appears and account is not deleted until confirmed"). Hard V4 only
fires on a duplicate `- **Then:**` line under one block.

### 3. Report

On strict failure, surface a structured error per failed rule:

```
AC-{id} fails {V#}: {reason}. {suggested fix}.
```

Examples:

```
AC-1 fails V2: missing Given clause. Add a line "**Given** {precondition}" before the When line.

AC-1 fails V3: compound Given. Split into AC-1 and AC-2, or rephrase as a single precondition. The phrase "and given" is reserved.

AC-2 fails V5: duplicate of AC-1 (same Given/When/Then). Remove or differentiate one of them.

AC-1 fails V7: duplicate id. Renumber to the next free id.
```

On V6 (warn-only):

```
AC-{id} warning V6: Then uses non-observable language: "{word}". Suggest rephrasing as a measurable outcome (e.g., "modal appears within 200ms", "redirect to /login"). Continue anyway? [y/N]
```

Default Y. The user may keep the wording; the warning is informational
so the planner downstream can attach `validator_note`.

If any strict rule fails: do not proceed to save or push. The caller
(`story.md` Step 4 or `update-story.md` validation branch) loops back to
review until the user fixes the AC.

## Read-path tolerance

Read paths do not invoke this ref:

- Pull from tracker (`sync.md` Pull Direction) -- legacy bodies may carry
  pre-Gherkin AC; the planner subagent decides how to handle them.
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

## Next Steps

- On pass: caller proceeds (Save/Push in create flow, or persist edit in edit flow).
- On strict fail: caller loops back to review with the structured error visible to the user.
- Downstream consumer: the `planner` subagent in `ai-tools/.claude/agents/planner.md` parses `### AC-N` blocks back to `{id, given, when, then}` and emits `ac.json`. Do not change the block shape without coordinating that contract.
