# Plan Epics

Derive the epic set from the project PRD, settle it, write the roadmap when the user asks for it, and create the epics in the tracker.

## Load first

Read [artifact-content.md](../references/artifact-content.md) before drafting or editing a body — what the conversation and the upstream sources may contribute to it, and what they never do.

Read [tracker.md](../references/tracker.md) and run its Resolve the Tracker step before drafting — read the existing destination without changing its configuration.

## Contents

- When to Use
- Rules for every run
- Roadmap as memory
- Workflow

## When to Use

Requires `docs/product/PRD.md`. When it is absent, stop with this error: "requires `docs/product/PRD.md`; create it first." Never route to PRD creation — that names another skill's artifact.

Not for a single artifact created from scratch: a single epic is a direct [create-epic.md](create-epic.md), with or without a PRD. Not for status or edits, and not for breaking an epic into its children.

## Rules for every run

1. Decide derivation, ICE, ordering, partition, and dependencies here. The roadmap template and the create instructions never re-decide them.
2. Create epics only, never their children.
3. Delegate every epic to [create-epic.md](create-epic.md): canonical shape and validation are non-negotiable, and this instruction drafts no epic body.
4. Write the roadmap only when the user asks for it. Show the draft in the chat and wait for approval before any write, unless the request is to materialize an existing roadmap as written.
5. Settle boundaries with the set — every epic states what it owns and what it does not before any epic is created.
6. Own the milestones: the settled milestone name travels as the `milestone` dispatch input on the epic's create. A set with no milestones passes none. This is the only origin of a milestone name — never hand-typed. On a re-run, reconcile each existing epic's milestone with its settled milestone — `fetch_artifact` reads what it carries now, and when that differs, confirm before dispatching `set_milestone` on the epic and cascading it to each existing child. A manual milestone that disagrees with an adopted epic's settled milestone is a divergence to confirm, never a silent overwrite.

## Roadmap as memory

`docs/product/ROADMAP.md`, when it exists, is this instruction's persisted memory of the settled plan; without it, the epics in the tracker are that memory. A later run reads the decisions back instead of re-deriving them, and `create-epic.md` reads the entry for the epic it is drafting; no other create instruction touches the roadmap. Do the heavy derivation only when there is nothing to read back:

- **No roadmap, no epics in the tracker** (`list_artifacts` filtered to epics) → derive fresh, from Step 1.
- **No roadmap, epics in the tracker** → `fetch_artifact` each epic for its requirements and milestone as data, keep them as the settled set, derive only the delta against the PRD, and show it at Step 6.
- **A roadmap, and the request is to materialize** → read it, skip the derivation and the draft, and materialize from it at Step 8. The request is the authorization.
- **A roadmap, and the request is to change the plan** — an epic added or dropped, a reorder, a PRD that moved → read the roadmap plus the PRD, compute only the delta (epics added/dropped, reordered, requirements or dependencies moved), show it at Step 6, then re-write and materialize. A changed PRD earns the delta, never a fresh derivation: deriving again discards the set the user settled.

With a roadmap, the request picks the branch. Which one applies is in what was asked, not in a state to be inferred — nothing on disk records the PRD the roadmap was derived from.

Drift is surfaced, not detected. Before materializing from an existing roadmap, compare its frontmatter `updated` with the PRD's last commit:

```bash
git log -1 --format=%ad --date=short -- docs/product/PRD.md
```

When the PRD is the newer of the two, say so and ask whether to replan or materialize the roadmap as written. This is a nudge, not a gate — an uncommitted PRD edit does not show up here, and nothing blocks on it.

Adjusting the roadmap means running this instruction again, never editing the roadmap directly.

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Derive the candidate epics
- [ ] Step 2: Score and order them
- [ ] Step 3: Partition the requirement IDs
- [ ] Step 4: Set each epic's blocked_by
- [ ] Step 5: Group into milestones
- [ ] Step 6: Settle with the user. If the user changes the set, return to the step it affects
- [ ] Step 7: Write the roadmap when asked
- [ ] Step 8: Materialize the missing epics
- [ ] Step 9: Report
```

**Step 1. Derive the candidates.** Read [derivation.md](../references/derivation.md) and cluster the PRD into epics by its seams — user outcomes as the primary seams, NFRs that serve several outcomes as foundation epics. Read the PRD as a claim, not authority: where its scope leaves a requirement no epic can own, or two requirements contradict, surface the disagreement instead of forcing a cut around it. **Translate, don't replicate** — PRD tokens (section numbers, doc framing) never cross into an entry. Done when every candidate carries its one-line boundary.

**Step 2. Evaluate and order.** Read [ice-scoring.md](../references/ice-scoring.md) and score the candidates. Order the set: **flow-dependency is primary and bounds the sequence** — an epic never precedes one it depends on — and **ICE decides within that bound**, breaking ties among unblocked peers. The PRD's order of requirements is a claim, not authority: where the ICE order disagrees with it, keep the ICE order and state the disagreement and its reason at Step 6. Done when the set has one order.

**Step 3. Partition the requirements.** Assign every in-scope PRD requirement ID (`FR/NFR`) to **exactly one** epic: no orphans (every ID lands on an epic, or its omission is confirmed), no duplicates (an ID on two epics means the boundary is wrong). An epic with no requirements is legitimate — validation or enabling work derives from no PRD line. The partition works in **IDs only**; the statement behind each ID stays in the PRD, resolved by `create-epic.md` when it drafts the epic body.

Check the partition. Resolve `<this-skill>` to the directory the `SKILL.md` was read from, and pass `{"assignments": {"<epic title>": ["FR-1"]}, "omitted": ["FR-9"]}` on stdin, where `omitted` lists only the IDs whose omission the user confirmed:

```bash
python3 <this-skill>/scripts/check_requirements.py --source docs/product/PRD.md
```

Resolve each `ORPHAN`, `DUPLICATE`, and `UNKNOWN` line it prints, and run it again. Done when the script exits 0.

**Step 4. Decide the dependencies.** Set each epic's `blocked_by` — the epics that must finish before it can start. These are the hard edges the ordering respects; they are recorded per entry so a re-run reads them back instead of re-deriving. Done when each epic has its `blocked_by`, or none.

**Step 5. Group into milestones.** The first milestone is the smallest run of the ordered set, foundation epics included, that resolves the problem the PRD states. The remaining epics form later milestones, or the set stays flat when it needs no grouping. When the user asked for a roadmap file, also state the ordering criteria, each epic's tags, and the Definition of Done: the conditions the release must meet, each with the check that proves it. Done when each epic has its milestone, or the set is flat.

**Step 6. Settle with the user.** Show the proposed set as a draft in the chat — each epic with its one-line boundary (the outcome it owns and the adjacent one it does not), its requirement IDs, its dependencies, its position, and its milestone, plus the tags, ordering criteria, and Definition of Done when Step 5 set them. The user adds, drops, merges, splits, renames, or reorders. **Wait for explicit approval before writing anything**: approval authorizes creating the epics, unless the user asked in the chat for only the roadmap. Without approval, stop and report that nothing was written. Boundaries partition the PRD's scope: work claimed by two epics means the set is wrong, not the boundary. Done when the user approved the set.

**Step 7. Write the roadmap when asked.** When the user did not ask for a roadmap file, skip to Step 8. When the user asked for one, read [roadmap.md](../assets/roadmap.md) and write the settled set through it — title, outcome description, `Driven by`, `Requirements` IDs, `Blocked by`, tags, the tracker link of an epic that already exists, milestone, the ordering criteria, and the Definition of Done. When the user asked for only the roadmap, skip to Step 9: the roadmap is written, nothing is materialized. Done when the roadmap holds the settled set, or none was asked for.

**Step 8. Materialize.** Materialize in **dependency order** — a blocker before its dependents. The settled set records `Blocked by` as epic **titles** (the only stable reference at plan time, before any epic has a tracker id); creating in dependency order means each epic's blockers already exist when it is created, so their titles resolve to tracker ids from the epic's roadmap link, the epics created earlier this run, or `list_artifacts`. Pass those resolved ids as the epic's `blocked_by` dispatch input.

Idempotent: run `list_artifacts` filtered to epics, and dispatch only the **missing** ones to [create-epic.md](create-epic.md), passing the resolved `blocked_by` ids, the epic's milestone, and the requirement IDs it owns. Each epic reads the PRD for their statements, and drafts its body.

When `docs/product/ROADMAP.md` exists, write the tracker link of each epic created in this run into it through the same template.

The partition is not re-validated here. Step 3 settled it with the PRD in hand, which is the only place orphans are visible at all. A roadmap read back from a previous run carries a partition already settled with the user, and `create-epic.md` reads each requirement set as a claim, so an ID that contradicts an epic's scope surfaces there, per epic.

On a re-run, `list_artifacts` also surfaces epics that no longer fit the current plan — offer to cancel (`update_status` `cancelled`), reparent (`set_parent`), or keep them; never auto-delete. A title that conflicts with an existing artifact follows the conflict handling in `tracker.md` "Create". Done when every settled epic exists in the tracker.

**Step 9. Report.** End the run with one report for the whole set, never one per artifact: `docs/product/ROADMAP.md` when written and the epics' URLs, the set written in one to three sentences — what changed, on a re-run — and any open item the run leaves. Never paste the roadmap or an issue body. Done when the report carries the URLs and the set.
