# Task Ordering

The dependency graph and the dispatch units it feeds.

## When to Use

During tasks to build and check the graph, and during implement to select and dispatch work.

## Dependency graph

`Depends on` is the only normative ordering field in `tasks.md`. Name every prerequisite task there, use `none` when a task has no prerequisite, declare prerequisites before dependents, and keep dependencies acyclic. Slice numbering does not create an ordering edge.

An edge exists when the dependent task cannot leave the tree green without the other.

A cycle means the cut is wrong: merge the two tasks, or move what they both need into a third task both depend on.

## Dispatch units

The selected argument determines the dispatch units:

| Selection | Dispatch units |
|-----------|----------------|
| `T-N` or a task range | One unit for the selection |
| `S-N` or a slice range | One unit for the selection |
| No selector | One unit per slice; groundwork is one unit |

Tasks within a unit run sequentially. Units with no dependency path between them that write no file in common may run in parallel; the agent decides how to isolate each one.
