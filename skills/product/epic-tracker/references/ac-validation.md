# AC Validation

Enforce Gherkin acceptance criteria on Story create and on edits that change AC text. Each AC is one markdown heading followed by one Gherkin scenario; `And` and `But` may continue any step block. A well-formed scenario keeps each AC testable and lets it reshape cleanly downstream; a malformed AC is ambiguous to anything that consumes it. Shape is what this ref judges — how many outcomes an AC carries is settled while it is drafted, and what it promises is measured against the requirement it satisfies, upstream, where the epic is in hand.

## When to Use

- Auto-loaded by `story.md` (Step 3 Validate, before the story is dispatched)
- Auto-loaded by `story.md`'s edit branch when an edit changes AC text
- Not a direct trigger

This ref is the single home for the AC contract. Do not duplicate the rules in `story.md` -- its create and edit paths load this ref at the validation step.

## AC Schema

Each AC is a `### AC-N` markdown heading followed by a fenced Gherkin block and an optional `**Satisfies**` line. Inside the block, the scenario uses `Given`, `When`, `Then`, `And` and `But`.

````markdown
### AC-1

```gherkin
Scenario: {short description}
  Given {precondition}
  And {additional precondition}
  When {action}
  Then {observable outcome}
  But {negative observable outcome}
```

**Satisfies** {one parent-epic requirement id — optional}
````

Example of a valid AC:

````markdown
### AC-1

```gherkin
Scenario: User signs in with registered credentials
  Given the user is on the sign-in page
  And the user has a registered account
  When they submit a valid email and password
  Then they are authenticated
  And they are redirected to the dashboard
```

**Satisfies** FR-1
````

Example with a Scenario Outline:

````markdown
### AC-2

```gherkin
Scenario Outline: Rate limit by plan
  Given the user is on the <plan> plan
  When they request <count> reset links within 1 minute
  Then the system <result>

  Examples:
    | plan | count | result             |
    | free | 3     | blocks the request |
    | pro  | 10    | allows the request |
```

**Satisfies** FR-7
````

Rules:

- 1 AC = 1 Gherkin scenario.
- The scenario must start with `Scenario:` or `Scenario Outline:`.
- The scenario must contain at least one `Given`, one `When` and one `Then`.
- `And` and `But` continue the preceding `Given`, `When` or `Then` block.
- Each AC has a stable id (`AC-1`, `AC-2`, ...; dash-separated, no zero-padding).
- IDs unique within the Story.
- Strings non-empty for every step line.
- `Scenario Outline` must have an `Examples` section.
- `**Satisfies**` is optional; when present it names exactly one requirement id matching `FR/BR/EC/NFR-<n>` — a single id, never a list.
- Keep this shape stable; downstream consumers (implementation specs, test generators) parse these blocks and rely on the format.

## Workflow

### 1. Parse

Extract the AC section from the Story body:

- Find the `## Acceptance Criteria` heading.
- Read until the next `## ` heading or end of document.
- Inside that section, every `### AC-N` heading begins a new AC block.
- For each block, read until the next `### ` or the end of the section.
- Within a block, find the fenced code block tagged `gherkin`.
- Read its opening `Scenario:` or `Scenario Outline:` line, then the steps that follow.
- Group the steps by keyword: the first `Given`, `When` and `Then` open the `given`, `when` and `then` groups, and every following `And` or `But` joins the group open at that point. Two lines break the grouping instead of opening a group of their own — an `And` or `But` before any group is open, and a keyword repeating one already open. Record both on the group they land in; V3 and V4 read them. A `Scenario Outline`'s `Examples` table is not a step — carry it whole, outside the groups.
- Parse the optional `**Satisfies**` line (case-insensitive bold label, whitespace-tolerant).

Tolerate tracker normalization: trailing whitespace, blank lines between blocks, single vs double newlines around headings. Linear occasionally reflows paragraphs; the parser must not break on these.

Output a list of `{id, scenario, given, when, then, examples, satisfies}` tuples plus any malformed blocks. `given`, `when` and `then` are the step groups, each a list of non-empty strings carrying their keyword; `examples` and `satisfies` are null when absent.

### 2. Validate

Run V1-V9 against the parsed tuples and the raw section text.

| # | Rule | Strictness | Trigger |
|---|------|------------|---------|
| V1 | Story has at least one AC | strict | parse yields zero `### AC-N` blocks |
| V2 | Each AC has a well-formed Gherkin scenario | strict | the block is missing or empty, carries no `Scenario:` / `Scenario Outline:` opening line or more than one, lacks one of the required step types, has an empty step line, or is a `Scenario Outline` with no `Examples` table |
| V3 | Given step group starts with `Given` | strict | the first `Given` step is preceded by `And`/`But`, or the group contains a second standalone `Given` line |
| V4 | Then step group starts with `Then` | strict | the first `Then` step is preceded by `And`/`But`, or the group contains a second standalone `Then` line |
| V5 | No duplicate AC | strict | two AC tuples with identical normalized {given, when, then} |
| V6 | Then is observable | warn-only with confirm | Then step group contains a red word from the list below (case-insensitive whole word) |
| V7 | Unique AC ids | strict | two `### AC-N` blocks with the same id |
| V8 | Satisfies is one well-formed id | strict | a `**Satisfies**` line is present but its value is not exactly one `FR/BR/EC/NFR-<n>` id (empty, a list, or malformed) |
| V9 | Story stays inside one outcome | confirm | parse yields more than five `### AC-N` blocks |

What a Then asserts beyond its requirement — a timing, a count, a threshold, a mechanism, an extra outcome — is not checked here. Its source is the requirement the AC satisfies, and this ref holds the id, never the epic that carries the statement. See Satisfies linkage below.

V6 red-word list:

`feel`, `feels`, `intuitive`, `clean`, `nice`, `elegant`, `seamless`, `smooth`, `natural`, `obvious`, `simple` (when used as a quality adjective, not a count).

`simple` is the most context-dependent word on the list — it often appears in legitimate technical contexts ("a simple redirect"). Flag it only when it is clearly used as a subjective quality judgment ("the UI feels simple"), not as a structural descriptor.

V3 and V4 preserve Gherkin's keyword order: `And` and `But` continue a block, they do not start one, and the keyword that opens a block (`Given` or `Then`) appears exactly once. A `When` block follows the same rule, surfaced under V2. This keeps each AC one scenario while allowing natural Gherkin continuations.

V9 is the only rule about the block as a set rather than any one AC — V1 is its floor, V9 its ceiling. Past five criteria a story has usually stopped being one outcome, and it is the create path's only sizing signal: a story brought straight to `story.md` never passes through decomposition, where the other granularity tests live. Confirm-to-continue, never strict — five is a heuristic, and a genuinely single outcome sometimes needs six criteria to demonstrate.

### 3. Report

On strict failure, surface a structured error per failed rule:

```text
AC-{id} fails {V#}: {reason}. {suggested fix}.
```

Examples:

```text
AC-1 fails V2: missing Gherkin block or missing Given/When/Then. Add a fenced ```gherkin block opening with Scenario: and carrying at least one Given, one When and one Then.

AC-2 fails V2: Scenario Outline has no Examples table. Add an Examples table binding every placeholder the steps use, or rewrite the block as a plain Scenario.

AC-1 fails V3: Given step group does not start with "Given" (starts with And/But) or contains a second standalone Given. Open the group with Given and continue with And/But.

AC-1 fails V4: Then step group does not start with "Then" (starts with And/But) or contains a second standalone Then. Open the group with Then and continue with And/But.

AC-2 fails V5: duplicate of AC-1 (same Given/When/Then). Remove or differentiate one of them.

AC-1 fails V7: duplicate id. Renumber to the next free id.

AC-1 fails V8: Satisfies "FR-3, FR-4" names two ids. Name exactly one requirement per AC; split the AC if it operationalizes two.
```

On V6 (warn-only):

```text
AC-{id} warning V6: Then uses non-observable language: "{word}". Suggest rephrasing as an observable outcome (e.g., "modal appears", "redirect to /login"). Continue anyway? [y/N]
```

Default Y. The user may keep the wording; the warning is informational and does not block. The rewrite names the observable the vague adjective stands for — it never adds a bound the requirement did not state. A timing, a count, or a threshold enters an AC only when the requirement asks for one.

On V9 (story size, confirm-to-continue):

```text
Story V9 check: {n} acceptance criteria. More than five usually means two stories -> split, or keep one whole. [split/keep]
```

Default keep. A split routes back to Draft to divide the story; keep records the size as deliberate and validation proceeds.

If any strict rule fails: do not dispatch. The caller (`story.md` Step 3 or its edit branch) loops back to Draft until the user fixes the AC.

## Satisfies linkage

V8 checks the shape of a `**Satisfies**` value. Three further relations hold across the epic↔story boundary — none parsed here (this ref reads the story's AC section in isolation), all owned by the create/edit flow that has the parent epic in hand:

- **Link validity** — a present `Satisfies` references a requirement the parent epic declares in its `## Requirements`. This ref cannot check it: it reads the story in isolation and holds the id, never the epic. `story.md` Step 3 runs it, right after V1-V9, with the epic it fetched in Step 1; a dangling id routes back to fix.
- **Bound provenance** — a bound in a Then traces to the statement of the requirement the AC satisfies. Resolving the id yields the statement, so `story.md` Step 3 runs this on the same resolution as link validity.
- **Requirement coverage** — every requirement the epic declares is operationalized by ≥1 `Satisfies` across its children: an AC on a story, or a done-condition on a task where no story can carry it. It is settled in two halves, neither here: `decompose.md` assigns each of the epic's requirement IDs to the child that will carry it, and the create ref confirms that child wrote a `Satisfies` line for every ID it was assigned. Coverage then holds by construction — no pass re-checks it across the children afterward.

`Satisfies` stays optional per AC: an AC may be implied quality with no backing requirement. What this ref enforces is shape (V8); the three relations above hold upstream.

This section is the single home for what the `Satisfies` link means and who settles it. A ref that writes one states its own half — a story's AC, a task's done-condition — and never restates the relation.

## Read-path tolerance

Read paths do not invoke this ref:

- `fetch_artifact` from the tracker -- a story fetched to be read, or fetched as the first step of an edit, is not validated on arrival. A fetched body may carry AC in any shape; the implementation consumer decides how to handle it.
- Status and overview reads -- no body inspection.

Edits that do not change AC text skip validation (see `story.md`'s edit branch) — validation fires on the write path, when AC text changed, never on the read that precedes it.

## Guidelines

**DO:**
- Parse the AC section with whitespace-tolerant matching so tracker normalization does not break the validator
- Surface every strict failure with AC id, rule name, and a concrete suggested fix
- Keep non-blocking checks default-allow — V6's red words and V9's count; only a structural failure is strict
- Run V9 on every story, however it was drafted — the create path has no other sizing signal
- Treat the V6 red-word list as small and stable; expand it only when a documented false negative recurs
- Run validation locally before any tracker round-trip so failures cost no dispatch latency

**DON'T:**
- Invent AC content for the user (contrasts: surface failures, let the user fix)
- Validate on a `fetch_artifact` read (contrasts: validate only on create and AC-text-changing edits)
- Block on V6 (contrasts: warn-only with confirm)
- Judge a bound in a Then here (contrasts: its source is the requirement statement, which only the flow holding the epic can read)
- Embed validation logic in `story.md` (contrasts: this ref is the single home; story.md loads it on create and edit)

## Error Handling

- AC section missing entirely: V1 fires; ask the user to add at least one `### AC-N` block.
- Block has heading but no Gherkin block, or a block that opens with no `Scenario` line: V2 fires.
- `Scenario Outline` written with no `Examples` table: V2 fires; add the table or rewrite it as a plain `Scenario`.
- User explicitly wants a second standalone `Given` or `Then` keyword inside one AC: still rejected — route them to use `And`/`But` continuations or split the AC.
- Tracker body returns malformed markdown (Linear collapsed list items): widen the parser regex tolerance; if still unparseable, route to manual fix in the tracker UI.
- V6 false positive (e.g., "the user feels confident" where intent is observable): user accepts the warning; nothing blocks.

## Outcomes

- On pass: caller proceeds to dispatch — the create flow pushes the new story, the edit flow writes the update.
- On strict fail: caller loops back to review with the structured error visible to the user.
- Block shape is a stable contract: each `### AC-N` is `id` + one fenced ```` ```gherkin ```` block with one `Scenario` or `Scenario Outline`, plus an optional `**Satisfies**` line. Keep the shape stable so any downstream consumer that parses these blocks does not break.
