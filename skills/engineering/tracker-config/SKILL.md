---
name: tracker-config
description: "Configures a project's issue tracker and performs tracker operations through Linear or GitHub. Use when setting up or changing the tracker, resolving its destination, or reading and writing issues with an existing body. Not for drafting intents or delivery requirements, decomposing work, writing specifications, managing pull requests, or implementing code."
argument-hint: "configure | [operation]"
---

# Tracker Config

## Triggers

- Configure, inspect, repair, or change the project's tracker → [configure.md](instructions/configure.md).
- Read or write tracker issues, status, hierarchy, dependencies, milestones, or metadata → [operate.md](instructions/operate.md).

## Workflow

```text
configure → persisted destination
operate → resolved destination → adapter → verified result
```

## References

- [configuration.md](references/configuration.md) — loaded by configure and operate.
- [operations.md](references/operations.md) — loaded by operate.
- [adapter-linear.md](references/adapter-linear.md) — loaded by operate for Linear.
- [adapter-github.md](references/adapter-github.md) — loaded by operate for GitHub.
