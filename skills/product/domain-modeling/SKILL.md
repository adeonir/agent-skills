---
name: domain-modeling
description: "Builds and sharpens a project's domain vocabulary in GLOSSARY.md. Use when a domain term is ambiguous, renamed, merged, or newly named, when two words mean one concept, when code and documents disagree on a term, or when writing or editing a glossary. Not for recording architecture decisions, writing requirements, or documenting code."
---

# Domain Modeling

Keep one canonical term per domain concept and write each resolution into `GLOSSARY.md` the moment it is settled.

## Workflow

```text
locate glossary → read → work the term → resolve → write inline
                              ^______________|  (term still open)
```

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Locate the glossary
- [ ] Step 2: Read it before answering
- [ ] Step 3: Work the term
- [ ] Step 4: Write inline
- [ ] Step 5: Report
```

**Step 1. Locate the glossary.** Find it at the root as `GLOSSARY.md`. When it does not exist, create it at the first resolved term, from [glossary.template.md](assets/glossary.template.md) · the entry layout. Done when the path is named.

**Step 2. Read it.** Read the glossary before answering anything about vocabulary. Done when the existing entries are read.

**Step 3. Work the term.**

- **Conflict.** Name the glossary definition next to the meaning the user is using, and ask which one holds.
- **Fuzzy or overloaded.** Propose one canonical term and the words it replaces.
- **Edge cases.** Test a relationship between concepts with a concrete scenario that probes the boundary.
- **Code.** When the user states how something works, check the code. Surface a contradiction as a question.

Done when the term has one resolved meaning, or stays open on a named question.

**Step 4. Write inline.** Update `GLOSSARY.md` as each term resolves, never in a batch at the end. A rename updates the definition and the `_Avoid_` line. A merge keeps one entry. A retired term is removed. Done when the file carries the resolution.

**Step 5. Report.** Once the session's glossary work ends, never after each term, report the path, the terms added, changed, or removed in one to three sentences, and any term still open. Never paste the glossary. Done when the path, the summary, and the open terms are reported.

## Entry rules

- Pick one term per concept and list the rejected words under `_Avoid_`.
- Define what the term is in one or two sentences, never what it does.
- Include only terms specific to this project's domain. A general programming concept (timeout, error type, utility pattern) stays out.
- Carry no implementation detail. The glossary is not a spec, a scratch pad, or a record of decisions.
- State each entry as the standing definition, in present tense. A rename or merge rewrites the entry to its new state, never a note of the change, and nothing from the conversation enters it: no "as discussed", "the user confirmed", "we agreed".
- Group entries under subheadings when clusters form; keep a flat list otherwise.

## Guidelines

- Ask for the term's meaning in the user's words before proposing a canonical one.
- Leave a term unresolved rather than guessing; an open term stays out of the file.
