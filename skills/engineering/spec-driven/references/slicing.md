# Product Slicing

What makes a product slice one vertical slice, and how to tell a vertical slice from a horizontal one.

## When to Use

When authoring user stories in specify, and when validating slice grouping in tasks. Read it whenever a slice feels too big, or a task list will not group cleanly under one slice.

## Vertical vs horizontal

A product slice (`S-N`) is **one vertical slice**: it cuts through every layer it needs to deliver one benefit, demonstrable on its own — that demonstration is its Independent Test. It is not a tracker story or a task. A **horizontal slice** cuts one layer across the whole feature — all the data model, then all the endpoints, then all the UI — and nothing it produces is demonstrable until the last layer lands.

Slice vertically: a horizontal slice carries no benefit of its own, so its acceptance criteria have nothing observable to assert.

A product slice carrying two distinct benefits is two slices — split it. A tracker story that is one layer of many is not a product slice — reslice the feature vertically.

## Example

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
