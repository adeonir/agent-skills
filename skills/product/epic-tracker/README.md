# Epic Tracker

Manages the delivery lifecycle from roadmap and epic planning through task tracking, in an external tracker.

## What It Does

```mermaid
flowchart TD
    USER[User request] --> EP[epic.md]
    USER --> STK[task.md]
    USER --> SPK[spike.md]
    USER --> BG[bug.md]
    PRD[docs/product/PRD.md] -->|project planning| DEC[decompose:<br>ICE framework, order, partition, deps]
    FPRD[feature PRD/design doc] -->|feature source| FT[feature:<br>size into epic or task]
    FT -->|epic| EP
    FT -->|standalone task| STK
    DEC -->|when asked| RW[roadmap.md]
    RW -->|writes| RM[(docs/product/ROADMAP.md)]
    DEC -->|each epic| EP
    RM -.reads its entry.-> EP
    DEC -->|epic → tasks| STK
    EP --> SY[Tracker operations]
    STK --> SY
    SPK --> SY
    BG --> SY
    SY --> LN[(Linear)]
    SY --> GH[(GitHub)]
```

| Phase | Output |
| ----- | ------ |
| Plan | Project PRD only, through `decompose`: the epic set, cut by user outcome and grouped into milestones, shown as a draft in the chat for your approval, then each epic and its tasks sent to Draft; the optional `docs/product/ROADMAP.md` is written after that approval when you ask for it |
| Size | Feature PRD or feature design doc only, through `feature`: the document cut along the epic seams into an epic (two or more units), or a standalone task (one unit); no roadmap is written |
| Discover | Epic only: context for the draft, read from the feature PRD or feature design doc, or from the project PRD, PRODUCT, and roadmap entry |
| Draft | Epic, task, spike, or bug body composed to its canonical template, plus dispatch inputs; the acceptance criteria of a task or bug and the exit criteria of a spike are validated before anything reaches the tracker |
| Sync | Tracker artifact and URL, created and updated through configured tracker access; the tracker is the single source of truth for state |

## Usage

```text
create a roadmap of epics from the PRD
break this epic into tasks
create issues from this feature design doc
create an epic for the billing redesign
add a task to the billing epic
edit the task and update its acceptance criteria
report a bug with reproduction steps and severity
create a task to upgrade the CI runner
create a spike to compare queue providers
list epics and what is in progress
mark this task done
cancel this task because it will not be delivered
move this task to the onboarding epic
block this task on ENG-42
```

## Output

Artifacts live in the tracker; the skill writes no local files for them. `docs/product/ROADMAP.md` is written only when you ask for a roadmap. Tracker configuration and instruction-block maintenance are outside this skill.

## Requirements

- **Required:** a configured tracker destination and access capable of the requested operations. Without those prerequisites, no tracker artifact can be created.

## FAQ

**Q: Do I have to use a tracker?** A: Yes. The tracker is the single source of truth; the skill keeps no local artifact copy. Missing configuration or access is reported without starting setup.

**Q: Am I asked before every push?** A: No. Operations use the existing configured destination; `decompose` and `feature` wait for your approval of the draft. An explicit destination applies to one artifact without changing saved settings; a child must remain in the same tracker as its parent epic.

**Q: Does every feature design doc or PRD become an epic?** A: No. `feature` cuts the document along the same seams `decompose` uses on the project PRD and counts what falls out. Two or more units make it an epic; one unit is a standalone task. Document length is not a seam, and the sized result is settled with you before anything is created. The project PRD is the exception — it describes the whole product, so it always yields epics.

**Q: Can I create an epic, task, spike, or bug without running decompose?** A: Yes. The create ref drafts your request to the canonical template and pushes to the tracker. It runs no derivation, partition, coverage, or ICE — those belong to `decompose`, which derives the plan from a PRD. Creating directly works whether or not a PRD exists.

**Q: Can I plan without creating anything in the tracker?** A: Yes. `decompose` shows the plan as a draft and creates nothing until you approve it. To keep the plan, ask in the chat for only the roadmap: the plan stays in `docs/product/ROADMAP.md` with nothing created. Ask later to create the epics from the roadmap; that request is the authorization, so no second draft is shown.

**Q: What happens when I push and the tracker is unavailable?** A: The draft stays in the session and the failure is reported. Any partial write is reported with its ID and URL. An uncertain write is checked before retrying.

**Q: What if someone edits the issue while I'm editing it here?** A: Every write to an existing artifact refetches immediately before it lands. When the tracker moved underneath, the skill surfaces the divergence and asks before overwriting — a teammate's edit is never silently destroyed.

**Q: Can a task, spike, or bug exist outside an epic?** A: Yes. Standalone means no parent epic — the artifact is created without an `epic_id`. A standalone task carries no requirement link, since no epic declares the requirements it would link to.

**Q: What is the difference between done and cancelled?** A: Both close the artifact. `done` means delivered and `cancelled` means dropped, so work abandoned rather than finished is `cancelled` and the tracker never reports it as shipped. Blocked is not a status; waiting on another artifact is carried by `blocked_by`.

**Q: What happens when I close an epic that still has open children?** A: The skill says how many tasks, spikes, or bugs beneath it are still open and asks before closing. It never closes a child to make the epic's status true.

**Q: Does the skill set priority or estimates for me?** A: No. Priority and estimates travel only when stated, independently of severity, dependencies, scope, and roadmap position. An epic carries no estimate. Unsupported metadata is reported.

**Q: Can I change dependencies after an artifact is created?** A: Yes. "block this on ENG-42" and "unblock this" work for the life of the artifact. Only `blocked_by` is stored, in the tracker's native relation, and no artifact body carries a copy of it, so the tracker's relations panel is what is live.

**Q: How are milestones assigned?** A: When `decompose` groups the epics into milestones, each epic takes its settled milestone, reusing an existing one or creating it with no date, and every task, spike, and bug under the epic mirrors it. An ungrouped set and a standalone artifact carry none, and a milestone changed by hand is confirmed before it is overwritten.
