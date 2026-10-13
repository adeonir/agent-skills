<!--
Design Doc skeleton. Remove an optional section that has no content. Delete every comment and replace every square-bracket slot before writing the file.

ALWAYS use this exact template structure.
-->
---
name: [document-name]
created: [YYYY-MM-DD]
updated: [YYYY-MM-DD]
sources: []
---

# Design Doc: [Project Name]

## Overview

[One paragraph: the system and what it does.]

```mermaid
[System-context or component diagram]
```

## Stack

- **[Layer]:** [technology] — [one-line justification] ([ADR-NNN, when an ADR records the choice])

## Architecture

[Modules or layers, how they communicate, and where each responsibility lives. Add Mermaid diagrams when they clarify the design.]

## Data Model

<!-- Optional. -->

[Main entities and their relationships.]

## External Integrations

<!-- Optional. -->

- **[Service]:** [use, and behavior on failure]

## Infra & Deploy

- **Hosting:** [where the system runs]
- **Environments:** [the environments in use]
- **CI/CD:** [how a change reaches production]

## Non-Functional Requirements

[For each NFR-N the design must satisfy, how the design meets it. Cite the NFR by ID; do not restate it. Cover only the requirements that shape the design.]

- **[NFR-N]:** [how it is met]

## Conventions

<!-- Optional: only what is not documented elsewhere. -->

- [Folder structure, code patterns, or testing approach.]

## References

- [Typed reference to a related document that exists, such as the PRD or an ADR.]

MUST NOT contain: product KPIs, personas, journey walkthroughs, or restated PRD prose or requirement text — cite the PRD and NFR IDs instead; nor product framing; nor conversation narrative ("as discussed", "we agreed", "the user confirmed").
