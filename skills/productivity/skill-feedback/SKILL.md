---
name: skill-feedback
argument-hint: "[skill-name]"
description: 'Writes a normalized improvement report about a skill used in the current session, built from evidence in the conversation and printed in chat for a later editing session. Use when a skill misbehaved, missed a case, or gave an unclear instruction during the session, or when the user says "report this skill issue", "skill feedback", or "write a report for the skill". Not for editing, auditing, or creating a skill, scoring trigger precision, or session handoffs.'
---

# Skill Feedback

## Quick start

Turn what went wrong with a skill in this session into a report another session can act on without this conversation. Write nothing to disk and change no skill file; the report goes to chat only.

## Workflow

Copy this checklist and tick it off:

```text
Progress:
- [ ] Step 1: Identify the skill
- [ ] Step 2: Settle the findings
- [ ] Step 3: Gather the evidence
- [ ] Step 4: Print the report
```

**Step 1. Identify the skill.** Take the skill from `$ARGUMENTS`, or from the user's request. With neither, take the skill this session loaded before this one; when it loaded several, ask which one. Read every file of that skill the findings touch, from the path the runtime loaded it from, in full. Done when you know the skill's name, its path, and the text of each file in question.

**Step 2. Settle the findings.** Take each problem the user named as a finding. When the user named none, list the deviations the session shows (a step skipped, an instruction read two ways, a correction the user had to give, a skill that fired on the wrong request or failed to fire) and ask the user which to report. Done when the user confirmed the list.

**Step 3. Gather the evidence.** For each finding, find in the session the turn that shows it: the user's message, the tool output, or the agent's reply. Quote only text you can still see in the conversation; when the turn was summarized away, write the summary's words, label them `(from summary)`, and mark the finding `inferred`. Locate the instruction involved and quote its text as written, never a line number, since the installed copy and the source may differ. Name the cause, and mark a finding `ambiguous` only when you can state both readings of the quoted instruction; with one reading, the cause is `not followed`:

- `missing`: no instruction covers the case
- `ambiguous`: the instruction reads two ways and the agent took the wrong one
- `contradictory`: two instructions conflict
- `wrong`: the instruction is clear and produces a bad result
- `not followed`: the instruction is clear and the agent ignored it
- `trigger`: the description fired on the wrong request or failed to fire

Mark a finding `observed` when a turn shows the failure and `inferred` when you reason from the instruction alone. Done when each finding has a cause, a basis, and either a quoted turn or the `inferred` mark.

**Step 4. Print the report.** Write it in English and quote the evidence verbatim in its original language. Reply with the report alone, with no text before or after it, so the whole reply copies as one block. If the user corrects a finding, return to Step 3 and print the full report again.

ALWAYS use this exact template structure:

```markdown
# Skill feedback: [skill name]

**Skill path:** [path the runtime loaded the skill from]
**Session task:** [one line: what the user was doing when the skill ran]

## Finding 1: [the defect, in one short sentence]

- **Where:** `[file relative to the skill folder]`, "[step or section heading]"
- **Instruction:** "[quoted instruction text, or none when the cause is missing]"
- **Expected:** [what the user needed from the skill at that point]
- **Observed:** [what the agent did and what came of it]
- **Evidence:** "[verbatim excerpt from the session, or the summary's words labeled (from summary)]"
- **Cause:** [missing | ambiguous | contradictory | wrong | not followed | trigger]
- **Basis:** [observed | inferred]
- **Direction:** [optional: the change the evidence supports, stated as a claim for the editing session to check]
```

MUST NOT contain: text before the H1 or after the last finding; a partial report after a correction; secrets, tokens, or personal data from the session; a rewritten skill file or a diff; a finding with no evidence and no `inferred` mark; a fix for a `not followed` finding that adds emphasis to the instruction instead of naming why it was missed.
