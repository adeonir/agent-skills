# Product Slicing

What makes a product slice one vertical slice, and how to tell a vertical slice from a horizontal one.

## When to Use

When authoring user stories in specify, and when validating slice grouping in tasks. Read it whenever a slice feels too big, or a task list will not group cleanly under one slice.

## Vertical vs horizontal

A product slice (`S-N`) is **one vertical slice**: it cuts through every layer it needs to deliver one benefit, demonstrable on its own — that demonstration is its Independent Test. It is not a tracker story or a task. A **horizontal slice** cuts one layer across the whole feature — all the data model, then all the endpoints, then all the UI — and nothing it produces is demonstrable until the last layer lands.

Slice vertically: a horizontal slice carries no benefit of its own, so its acceptance criteria have nothing observable to assert.

A product slice carrying two distinct benefits is two slices — split it. A tracker story that is one layer of many is not a product slice — reslice the feature vertically.

## One benefit, several consumers

Name the benefit by what changes for whoever the slice serves, never by what reads the result. One outcome delivered to a preview card, a crawler, and a sitemap is one benefit reaching three consumers, so it is one slice — split it by consumer and each slice delivers a line, while every Independent Test demonstrates the same change under a different name.

Two slices whose statements differ only in who consumes the outcome are one slice: merge them, and let their criteria sit under it. Read the `so that [benefit]` clauses side by side — where the same sentence serves both once the consumer is struck out, the split was by channel.

## Where to cut

Start from one slice. Run these checks over every slice, in order, and merge where one fails:

1. **Same behavior across items** — a rule every kind of item follows is one criterion in one slice, a `Scenario Outline` over the kinds; never one copy per kind, and never a slice of its own cut across every kind. A new slice starts only where the behavior differs for a group of items.
2. **Same change** — an outcome the change behind another slice also delivers joins that slice, even when it serves another actor.
3. **Demonstrable alone** — a slice whose Independent Test cannot run without another slice merges into it.

## Example

Feature: image optimization.

Cut by kind of item — every shared rule written once per kind:

```text
S-1: carousel images: size, sharpness, format, alt text
S-2: section images: size, sharpness, format, alt text
S-3: maintainer: one source file per image
```

Cut by behavior — shared rules once, the difference on its own:

```text
S-1: every image built from its source file, the shared rules over each kind
S-2: the first screen loads first
```

Feature: password reset.

Vertical — each slice is demonstrable on its own:

```text
S-1: request a reset link
S-2: set a new password from the link
```

Horizontal — nothing is demonstrable until the last slice lands:

```text
S-1: add the password_resets table
S-2: add the reset endpoints
S-3: add the reset UI
```
