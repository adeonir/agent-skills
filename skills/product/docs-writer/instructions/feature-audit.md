# Feature Audit Report

Consolidate supplied audit findings into a feature report.

## Workflow

```text
resolve feature → collect supplied findings → reconcile → write → reread
```

1. Resolve the feature slug and use `.artifacts/features/<feature-slug>/audit.md`. Read an existing report before editing; preserve sections outside the requested change.
2. Read the audit reports, notes, and evidence the user supplied. Treat every finding as a claim from its source. Do not run an audit, inspect the target to validate findings, or implement fixes as part of this document workflow.
3. Consolidate repeated findings when they describe the same issue. Preserve distinct evidence and source attribution. Keep conflicting assessments visible with their sources; do not choose a winner or infer a status. Mark missing details as unknown rather than filling them in.
4. Read `<this-skill>/assets/feature-audit.template.md`. Use its exact structure, remove the optional design-review annex when it has no supplied content, delete comments, and replace every square-bracket slot. Preserve the supplied date, measurements, severity, and status. If a required value is missing, ask the user or state `Unknown`.
5. Populate `Sources` with supplied files or URLs. Include the report or tool name for each finding when available. If no source was supplied, use `[]` and identify the findings as user-provided statements without independent source material.
6. Reread the report and check that every finding traces to supplied material, duplicate findings retain all relevant evidence, disagreements remain explicit, and the summary counts match the findings. If a check fails, correct the report and repeat this step.
7. Report the file path and a one-sentence description of the consolidated material. Name any unresolved disagreement or missing source detail.

## Boundaries

Do not assign a new severity, status, impact, or evidence. Do not convert findings into requirements or implementation tasks. The report records supplied audit output; it does not approve or apply changes.
