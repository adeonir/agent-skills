# AC Validation

Enforce the checklist of conditions on Task and Spike create and on edits that change a condition. Each condition is one checklist line, optionally ending with one requirement link. A well-formed line keeps each condition testable and parseable; a malformed one is ambiguous to anything that consumes it. Shape is what this ref judges — how many outcomes a condition carries is settled while it is drafted, and what it promises is measured against the requirement it links, upstream, where the epic is in hand.

## When to Use

- Auto-loaded by `task.md` and `spike.md` (Step 3 Validate, before the artifact is dispatched)
- Auto-loaded by the edit branch of `task.md` and `spike.md` when an edit changes a condition
- Not a direct trigger

This ref is the single home for the condition contract. Do not duplicate the rules in `task.md` or `spike.md` -- their create and edit paths load this ref at the validation step.

## Condition Schema

Each condition is a checklist line under `## Acceptance Criteria` (`## Exit Criteria` on a spike): `- [ ]`, then the condition, then an optional requirement link — ` — ` followed by one `FR/NFR` id.

````markdown
## Acceptance Criteria

- [ ] A signed-in user can reset their password without contacting support — FR-3
- [ ] A reset link stops working 15 minutes after it is issued — FR-4
- [ ] The reset screen is reachable from the sign-in screen
````

Rules:

- One line is one condition, one outcome.
- The line starts with `- [ ]`.
- The condition text is non-empty.
- The requirement link is optional; when present it is the final element of the line and names exactly one id matching `FR/NFR-<n>` — a single id, never a list.
- A spike's conditions carry no requirement link.
- No two conditions share the same text once their requirement links are removed.
- Keep this shape stable; the link is parsed from the end of the line.

## Workflow

### 1. Parse

Extract the conditions from the Task or Spike body:

- Find the `## Acceptance Criteria` heading, or `## Exit Criteria` on a spike.
- Read until the next `## ` heading or end of document.
- Inside that section, every line opening with a checklist marker begins a new condition. A following line that opens with no marker continues the condition above it.
- Split the requirement link off each condition at its last spaced dash (`—`, `–`, or `-`) when the text after that dash begins with `FR` or `NFR`. A dash followed by anything else is prose and stays in the condition text. Text after the dash that is not exactly one well-formed id is a malformed link, and rule V4 reports it.

Tolerate tracker normalization: trailing whitespace, blank lines between items, `*` for `-`, a checked box `[x]` for `[ ]`, escaped brackets, and items rewrapped across lines. Linear occasionally reflows paragraphs; the parser must not break on these.

Output a list of `{n, text, link}` tuples plus any malformed lines. `n` is the condition's position, 1-based; `link` is null when absent.

### 2. Validate

Run V1-V4 against the parsed tuples and the raw section text. Every rule is strict.

| # | Rule | Trigger |
|---|------|---------|
| V1 | The artifact has at least one condition | parse yields zero checklist lines |
| V2 | Each condition has text | a checklist line with no text after the marker, or text under the heading before the first checklist line |
| V3 | No duplicate condition | two conditions with identical normalized text, requirement link excluded |
| V4 | The requirement link is one well-formed id | a spaced dash followed by `FR` or `NFR` is present but its value is not exactly one `FR/NFR-<n>` id (a list, or malformed), or a spike condition carries any requirement link |

What a condition asserts beyond its requirement — a timing, a count, a threshold, a mechanism, an extra outcome — is not checked here. Its source is the requirement the condition links, and this ref holds the id, never the epic that carries the statement. See Requirement linkage below.

### 3. Report

On failure, surface a structured error per failed rule:

```text
Condition {n} fails {V#}: {reason}. {suggested fix}.
```

Examples:

```text
Artifact fails V1: no checklist lines under the criteria heading. Add at least one `- [ ]` condition.

Condition 2 fails V2: empty condition. Write the condition after the marker, or remove the line.

Condition 3 fails V3: duplicate of condition 1. Remove or differentiate one of them.

Condition 1 fails V4: link "FR-3, FR-4" names two ids. Name exactly one requirement per condition; split the condition if it operationalizes two.
```

If any rule fails: do not dispatch. The caller (Step 3 of `task.md` or `spike.md`, or an edit branch) loops back to Draft until the user fixes the conditions.

## Requirement linkage

V4 checks the shape of a requirement link. Three further relations hold across the epic↔task boundary — none parsed here (this ref reads the task's section in isolation), all owned by the create/edit flow that has the parent epic in hand:

- **Link validity** — a present link references a requirement the parent epic declares in its `## Requirements`. This ref cannot check it: it reads the task in isolation and holds the id, never the epic. `task.md` Step 3 runs it, right after V1-V4, with the epic it fetched in Step 1; a dangling id routes back to fix.
- **Bound provenance** — a bound in a condition traces to the statement of the requirement it links. Resolving the id yields the statement, so `task.md` Step 3 runs this on the same resolution as link validity.
- **Requirement coverage** — every requirement the epic declares is operationalized by ≥1 link across its children: a condition on a task. It is settled in two halves, neither here: `decompose.md` assigns each of the epic's requirement IDs to the child that will carry it, and the create ref confirms that child wrote a link for every ID it was assigned. Coverage then holds by construction — no pass re-checks it across the children afterward.

The link stays optional per condition: a condition may be implied quality with no backing requirement. What this ref enforces is shape (V4); the three relations above hold upstream.

This section is the single home for what the requirement link means and who settles it. A ref that writes one states its own half and never restates the relation.

## Read-path tolerance

Read paths do not invoke this ref:

- `fetch_artifact` from the tracker -- a task or spike fetched to be read, or fetched as the first step of an edit, is not validated on arrival. A fetched body may carry conditions in any shape; the consumer decides how to handle it.
- Status and overview reads -- no body inspection.

Edits that do not change a condition skip validation (see the edit branch of `task.md` and `spike.md`) — validation fires on the write path, when a condition changed, never on the read that precedes it.

## Guidelines

**DO:**
- Parse the section with whitespace-tolerant matching so tracker normalization does not break the validator
- Surface every failure with the condition number, rule name, and a concrete suggested fix
- Run validation locally before any tracker round-trip so failures cost no dispatch latency

**DON'T:**
- Invent a condition for the user (contrasts: surface failures, let the user fix)
- Validate on a `fetch_artifact` read (contrasts: validate only on create and condition-changing edits)
- Judge a bound in a condition here (contrasts: its source is the requirement statement, which only the flow holding the epic can read)
- Embed validation logic in `task.md` or `spike.md` (contrasts: this ref is the single home; both load it on create and edit)

## Error Handling

- Section missing entirely: V1 fires; ask the user to add at least one condition.
- Text under the heading before the first checklist line: V2 fires.
- Tracker body returns malformed markdown (Linear collapsed list items): widen the parser tolerance; if still unparseable, route to manual fix in the tracker UI.

## Outcomes

- On pass: caller proceeds to dispatch — the create flow pushes the new artifact, the edit flow writes the update.
- On fail: caller loops back to review with the structured error visible to the user.
