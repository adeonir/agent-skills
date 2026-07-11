# Story Slicing

What makes a story one vertical slice, and how to tell a vertical slice from a horizontal one.

## When to Use

When authoring user stories in specify, and when validating story grouping in tasks. Read it whenever a story feels too big, or a task list will not group cleanly under one story.

## Vertical vs horizontal

A story is **one vertical slice**: it cuts through every layer it needs to deliver one benefit, demonstrable on its own — that demonstration is its Independent Test. A **horizontal slice** cuts one layer across the whole feature — all the data model, then all the endpoints, then all the UI — and nothing it produces is demonstrable until the last layer lands.

Slice vertically. A vertical slice can be shown to the user and tested on its own; a horizontal slice can only be shown once its siblings exist, so it carries no benefit of its own and its acceptance criteria have nothing observable to assert.

A story carrying two distinct benefits is two stories — split it. A "story" that is one layer of many is not a story — reslice the feature vertically.

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
