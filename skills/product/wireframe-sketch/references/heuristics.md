# Nielsen Heuristics (structural)

The ten usability heuristics read as **affordance presence in the region tree** —
a design-blind checklist, never a visual score.

## When to Use

Composed by [validate.md](../instructions/validate.md) when checking a wireframe
or an existing plan. Applied to the structure — surfaces, blocks, and flow — not
to any styling. The output is a checklist of missing affordances, not a number.

## How to read these

At wireframe stage you check whether the structure makes **room** for each
heuristic — a status region, an exit, an error state — never whether a finished
UI executes it well. The absence of the affordance is the finding; its quality
is a later, design-aware concern this skill does not judge.

A persistent affordance is a **block** in the region tree — it renders in the
greybox and is checkable here. A **state variant** — the empty, loading, or
error face of one region — lives in the surface's narration; read it there
rather than flag it as a missing block.

## Two kinds of check

- **Deterministic** — `validate_wireframe.py` already decides these from the
  tree: shapes drawn from one fixed vocabulary (consistency), flow reachability,
  and dangling endpoints. They fire or they do not; the script owns them.
- **Judgment** — you read the arrangement and decide. Every item below is
  judgment unless tagged `(script)`.

## Checklist

1. **Visibility of system status** — a region or slot is planned for status,
   loading, and progress feedback where the surface acts on data.
2. **Match the real world** — surface and block labels follow the user's
   language and mental model, not system or implementation jargon.
3. **User control and freedom** — the flow offers a back, cancel, or exit path;
   modals and overlays have a stated way out. `(script)` flags flow that cannot
   reach a surface.
4. **Consistency and standards** — navigation sits in a consistent place across
   surfaces, and patterns are conventional. `(script)` enforces one shape
   vocabulary.
5. **Error prevention** — a confirmation step or constraint precedes a
   destructive or irreversible action in the flow.
6. **Recognition over recall** — information the user needs is visible on the
   surface (breadcrumbs, persistent context) rather than carried in memory
   between screens.
7. **Flexibility and efficiency** — a frequent path has a shortcut or accelerator
   alongside the long route, where it earns one.
8. **Minimalist structure** — each surface carries only the blocks it needs; no
   surface is overloaded with competing regions. The visual-aesthetic half of
   this heuristic is out of scope — design-blind.
9. **Recognize and recover from errors** — an error state and a slot for its
   message are planned where a surface can fail, each with a next action.
10. **Help and documentation** — a help or support affordance is planned where
    the task is non-trivial enough to need one.

## Report

Flag each missing affordance as a finding with its surface and the heuristic it
fails, severity at your judgment. This is a checklist the user resolves in the
plan — never a 0–4 score and never a styling note.
