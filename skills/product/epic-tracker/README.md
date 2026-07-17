# Epic Tracker

Manages the delivery lifecycle from epic planning through story tracking, in an external tracker.

## What It Does

```mermaid
flowchart TD
    PRD[docs/product/PRD.md] --> DEC[decompose — brain:<br>derive, ICE, order, partition, deps]
    DEC -->|entries| RW[roadmap.md — writer]
    RW -->|writes| RM[(docs/product/ROADMAP.md)]
    DEC -->|checkpoint → each epic| EP[epic.md]
    RM -.reads its entry.-> EP
    DEC -->|epic → stories/tasks| STK[story.md / task.md]
    EP --> SY[sync.md]
    STK -->|AC validated| SY
    BG[bug.md] --> SY
    SY --> LN[(Linear)]
    SY --> GH[(GitHub)]
```

`decompose` is the brain: it derives the epic set from the PRD, writes the plan to the roadmap through `roadmap.md`, and — after a checkpoint — materializes each epic through `epic.md`, then each story and task through `story.md`/`task.md`. `roadmap.md` only writes the record; it decides nothing. A story's acceptance criteria are validated before anything reaches the tracker; a bug hangs under an epic or stands alone.

Every artifact lives in the tracker — Linear via MCP, GitHub via MCP or the `gh` CLI. Nothing but the roadmap is written locally, and the tracker is the single source of truth for state. A tracker is required: without one configured, bootstrap runs first and nothing is created until it completes. `docs/product/ROADMAP.md` is the one local file — committed, alongside `PRD.md` and `PRODUCT.md`.

| Phase | What Happens | Output |
| ----- | ------------ | ------ |
| Discover | Check for existing PRD, roadmap, or context | Context for the draft |
| Draft | Compose epic, story, bug, or task to its canonical template | Body + dispatch inputs |
| Sync | Dispatch to the tracker via its adapter | Tracker artifact + URL |

## Tracker Integration

| Artifact | Linear | GitHub |
| -------- | ------ | ------ |
| Epic | Issue (parent) | Issue (parent) |
| Story | Issue (sub-issue of Epic) | Issue (sub-issue of Epic) |
| Bug | Issue (sub-issue of Epic, or standalone) | Issue (sub-issue of Epic, or standalone) |
| Task | Issue (sub-issue of Epic, or standalone) | Issue (sub-issue of Epic, or standalone) |

Every artifact is an Issue, and sub-issues carry the hierarchy in both trackers. Each one classifies the artifact type its own way (a Linear label, a GitHub issue type or label). On GitHub, Projects v2 is an orthogonal opt-in layer for board views and custom fields.

Configure via `configure tracker` (runs bootstrap once per project). Bootstrap detects what is reachable: GitHub through MCP or the `gh` CLI, with one falling back to the other; Linear through MCP alone. Config is stored in `git config --local`, so it stays with the project.

## Status

An artifact is `planned`, `in-progress`, `done`, or `cancelled`. It holds exactly one at a time, and each adapter maps it to the tracker's own vocabulary in both directions — Linear by workflow-state type, GitHub by open/closed plus its state reason.

`done` and `cancelled` both close the artifact and say different things: `done` is delivered, `cancelled` is dropped. Work abandoned rather than finished is `cancelled`, so the tracker never reports it as shipped.

Blocked is not a status. Work can be started and waiting on another artifact at the same time, so waiting is carried by `blocked_by` — see below.

## Dependencies

Any epic, story, bug, or task can declare `blocked_by` — the artifacts that must finish first, as tracker ids or URLs. It maps to the tracker's native dependency relation (GitHub issue dependencies, Linear issue relations), which both trackers surface in their own UI. Only `blocked_by` is stored — the inverse is derived, and the tracker keeps both sides in sync.

Dependencies are editable for the life of the artifact, not just at creation: "block this on ENG-42", "unblock this".

## Usage

```text
create roadmap             -- derive the epic set from the PRD, write docs/product/ROADMAP.md, then materialize
create epic                -- draft one epic directly (a PRD-less one-off)
decompose                  -- run the ceremony: PRD into a roadmap of epics, or an epic into stories/tasks
create story               -- add a story (a demonstrable slice of user value) to an existing epic
edit story                 -- update an existing story; AC changes re-validate
report bug                 -- document a defect with reproduction steps and severity
create task                -- file a general work item (infra, refactor, tooling, research, ...)
list epics                 -- show the delivery overview from the tracker
mark done                  -- update artifact status in the tracker
cancel this                -- drop an artifact that will not be delivered
move this to epic X        -- reparent a story, bug, or task under another epic
block this on X            -- record a dependency on an existing artifact
configure tracker          -- run bootstrap to set or change tracker config
```

## Story Acceptance Criteria

Stories enforce Given/When/Then 1:1 acceptance criteria. Each AC is a `### AC-N` block with one Given, one When, one Then — no compound clauses — plus an optional `**Satisfies**` line linking the parent-epic requirement it operationalizes. The skill validates on story create and on edits that change AC text, before any tracker round-trip. Resolving each `Satisfies` against the parent epic also flags a Then that promises what the requirement never asked for — a timing, count, threshold, or mechanism with no source — so the story does not quietly owe more than the requirement demands. Artifacts read from the tracker are not validated.

## Requirement Traceability

The **epic** declares the PRD requirement IDs it owns (`FR/BR/EC/NFR`) in a `## Requirements` section, read from the PRD via its PRD link. Each **story** operationalizes them: every `### AC-N` links the requirement it satisfies on a `**Satisfies**` line, which the spec inherits 1:1 downstream. A **task** carries no requirement IDs — it is AC-less work measured by its `## Definition of Done`. `ADR-NNN` is a decision dependency recorded in References, not a requirement. Requirement coverage is an epic↔story relationship: every requirement the epic declares is operationalized by ≥1 story AC.

## Roadmap

The roadmap is `decompose`'s record of the settled plan — the project's epics in an ordered flow, in `docs/product/ROADMAP.md`, committed alongside `PRD.md` and `PRODUCT.md`. `decompose` requires a PRD, derives the epics, and writes the roadmap through `roadmap.md`; there is no separate step that decides the plan elsewhere. Each entry carries the epic's capability, the requirement IDs it owns, and its `Blocked by` dependencies — enough for a re-run to read the plan back instead of re-deriving. Phase headings are cosmetic grouping for the reader. Epics stay self-contained: they never reference the roadmap.

## Milestones

A milestone is the tracker's grouping primitive — a Linear project milestone or a GitHub repo milestone. The skill treats it as the materialization of a roadmap phase: when `decompose` runs on a roadmap grouped into phases, each epic's phase name becomes its milestone, reusing one already in the tracker (including one created by hand in the UI) or creating it with no date. A flat roadmap assigns none.

A milestone is a property of the whole epic subtree: the epic takes its phase name, and every story, bug, and task under it mirrors the epic's milestone, so the tracker groups the epic and its children together. A standalone bug or task carries none. The skill only ever assigns a milestone by deriving it from a phase — never from free text — and on a re-run it reconciles the subtree to the epic's current phase, confirming before it overwrites a milestone changed by hand. A reparent mirrors the new epic's milestone under the same guard: a hand-set milestone is confirmed before it is replaced. Scheduling and progress on the milestone stay in the tracker UI.

## Output

Artifacts live in the tracker; the skill writes no local files for them. The roadmap is the one exception — `docs/product/ROADMAP.md`, committed alongside `PRD.md` and `PRODUCT.md`.

## Requirements

- **Required:** a tracker — Linear through an MCP server, or GitHub through an MCP server or the `gh` CLI. Without one, no artifact can be created.

## FAQ

**Q: Do I have to use a tracker?** A: Yes. The tracker is the single source of truth; the skill keeps no local copy of an epic, story, bug, or task. When no MCP or CLI is detected, bootstrap stops and tells you what to set up.

**Q: Am I asked before every push?** A: No. Bootstrap asks once per project and stores the answer in `epic-tracker.kind`. After that, creates follow the config without re-asking. Name a destination in the request to override it for a single artifact — "create the issue on GitHub" when the config says Linear. The override never rewrites the config; only `configure tracker` does. It does not apply to a story, whose parent epic lives in the configured tracker.

**Q: Can I plan without creating anything in the tracker?** A: Yes. `decompose` writes the roadmap first and confirms before materializing — decline the checkpoint and the plan is saved to `docs/product/ROADMAP.md` with nothing created. Run `decompose` again later to materialize.

**Q: How do I switch trackers?** A: Run `configure tracker`. Bootstrap re-detects what is reachable and updates the git config. Artifacts already created stay in the old tracker — the switch applies to what you create next.

**Q: What happens when I push and the tracker is unavailable?** A: On GitHub, the skill tries the other channel (MCP when `gh` fails, or the reverse). On Linear, which runs on MCP alone, there is no second channel. When no channel is left, it holds the draft in the session, surfaces the error, and offers to retry — the drafted content is never discarded. No partial state is left in the tracker.

**Q: What if someone edits the issue while I'm editing it here?** A: Every write to an existing artifact refetches immediately before it lands. When the tracker moved underneath, the skill surfaces the divergence and asks before overwriting — a teammate's edit is never silently destroyed.

**Q: Can a bug or task exist outside an epic?** A: Yes. Standalone means no parent epic — the artifact is created without an `epic_id`. Stories always have a parent epic.
