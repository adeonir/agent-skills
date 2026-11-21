# TDD

Build a change test-first, with tests anchored to the source of truth at public seams.

## What It Does

```mermaid
flowchart LR
    A[Read source of truth] --> B[Choose seams]
    B --> C[Red-green-refactor loop per criterion]
```

| Phase | Output |
|-------|--------|
| Source | Acceptance criteria |
| Seams | One seam per criterion, taken from the spec or from the tests already there |
| Loop | One failing test, the minimum code to pass, then a refactor with the tests green, per criterion, or the closest executable check when a test is impractical |

## Usage

```text
implement this issue test-first
fix this bug starting with a test that reproduces it
build this slice with red-green against the spec
```
