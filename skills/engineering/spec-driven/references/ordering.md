# Task Ordering

The dependency graph and its derived execution waves.

## When to Use

During tasks to build and check the graph, during implement to select and dispatch work, and during audit to verify execution order.

## Dependency graph

`Depends on` is the only normative ordering field in `tasks.md`. Name every prerequisite task there, use `none` when a task has no prerequisite, declare prerequisites before dependents, and keep dependencies acyclic. Slice numbering does not create an ordering edge.

An edge exists in two cases: the dependent task cannot leave the tree green without the other, or both tasks write the same file. Two tasks that write the same file never run in parallel.

A cycle means the cut is wrong: merge the two tasks, or move what they both need into a third task both depend on.

## Waves

`Sequence` is a projection of the graph. A task with no dependencies is in `W-1`; every other task is in the wave after the highest wave of its dependencies. Tasks at the same graph level share a wave and may run in parallel when their dispatch units are independent. List every task exactly once, including completed tasks, in the `Wave` / `Tasks` table.

When the linter reports canonical waves, copy that projection into `Sequence`; do not recalculate or reorder it by intuition.

Do not add a `Wave` field to a task. Do not use `Sequence` to create an ordering that `Depends on` does not express. The linter rejects missing, duplicate, unknown, out-of-order, cyclic, and incompatible entries.

## Dispatch units

The selected argument determines the dispatch units:

| Selection | Dispatch units |
|-----------|----------------|
| `T-N` or a task range | One unit for the selection |
| `S-N` or a slice range | One unit for the selection |
| `W-N` or a wave range | One unit per represented slice; groundwork is one unit |
| No selector | One unit per slice; groundwork is one unit |

Tasks within a unit run sequentially. Sequential mode uses the current worktree. Parallel mode creates one worktree per concurrently running dispatch unit and integrates commits in dependency order.
