---
name: domain-modeling
description: "Builds and sharpens a project's domain vocabulary in GLOSSARY.md. Use when a domain term is ambiguous, renamed, merged, or newly named, when two words mean one concept, when code and documents disagree on a term, or when writing or editing a glossary. Not for recording architecture decisions, writing requirements, or documenting code."
---

# Domain Modeling

Keep one canonical term per domain concept and write each resolution into `GLOSSARY.md` the moment it is settled.

## Triggers

- A term conflicts with its glossary definition, or two words name one concept
- A word covers two concepts, or a concept has no name yet
- A term is renamed, merged, or retired
- Code or documents use a name the glossary does not define
- The user asks to write or edit the glossary

## Workflow

```text
locate glossary → read → work the term → resolve → write inline
                              ^______________|  (term still open)
```

1. **Locate the glossary** at the root as `GLOSSARY.md`. When it does not exist, create it at the first resolved term, from [glossary.template.md](assets/glossary.template.md).
2. **Read it** before answering anything about vocabulary.
3. **Work the term:**
   - **Conflict.** Name the glossary definition next to the meaning the user is using, and ask which one holds.
   - **Fuzzy or overloaded.** Propose one canonical term and the words it replaces.
   - **Edge cases.** Test a relationship between concepts with a concrete scenario that probes the boundary.
   - **Code.** When the user states how something works, check the code. Surface a contradiction as a question.
4. **Write inline.** Update `GLOSSARY.md` as each term resolves, never in a batch at the end. A rename updates the definition and the `_Avoid_` line. A merge keeps one entry. A retired term is removed.

## Entry rules

- Pick one term per concept and list the rejected words under `_Avoid_`.
- Define what the term is in one or two sentences, never what it does.
- Include only terms specific to this project's domain. A general programming concept (timeout, error type, utility pattern) stays out.
- Carry no implementation detail. The glossary is not a spec, a scratch pad, or a record of decisions.
- Group entries under subheadings when clusters form; keep a flat list otherwise.

## Guidelines

- Ask for the term's meaning in the user's words before proposing a canonical one.
- Leave a term unresolved rather than guessing; an open term stays out of the file.
