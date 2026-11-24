---
name: tracker-config
description: "Configures a project's issue tracker and performs tracker operations through Linear or GitHub. Use when setting up or changing the tracker, resolving its destination, or reading and writing issues with an existing body. Not for drafting intents or delivery requirements, decomposing work, writing specifications, managing pull requests, or implementing code."
argument-hint: "configure | [operation]"
compatibility: Requires python3 and a Linear or GitHub tracker.
---

# Tracker Config

Configure the project's issue tracker and run its operations.

## Triggers

- **Configure** — set up, inspect, repair, or change the tracker → [configure.md](references/configure.md) · the configuration files and the resolved destination
- **Operate** — read or write issues, status, hierarchy, dependencies, milestones, or metadata → [operate.md](references/operate.md) · the tracker operation and its result

## Workflow

```mermaid
flowchart LR
    configure --> persisted
    operate --> resolved --> adapter --> verified
```
