# STE-Inspired Principles

Apply selected Simplified Technical English principles to agent output. Do not claim formal conformance.

## When to Use

Read before writing, rewriting, or auditing technical prose. Use the official ASD-STE100 standard when the user requires formal conformance.

These rules apply in every language. English word pairs are examples; use the equivalent pair in the language of the text.

## Word choice

1. Prefer short, familiar words over formal or corporate alternatives: `use` instead of `utilize`, `help` instead of `facilitate`, and `start` instead of `commence`.
2. Give one word one meaning in the same response. Do not alternate terms only for variety.
3. Keep approved domain terms, product names, code identifiers, and protocol names. Define an unfamiliar term at first use when the reader needs the definition.
4. Remove idioms, slang, regional expressions, metaphors, and unexplained abbreviations.
5. Break noun clusters into clear relations. Prefer “the timeout for the database connection” to “database connection timeout configuration.”
6. Remove politeness that adds no fact. Keep wording that changes certainty or adds a condition: `I think` when it signals real uncertainty, `Only while the token is valid` because it states a condition.
7. Write the real symbol, file, flag, or command name, not a synonym or a description of it: `--dry-run`, not "the preview option".
8. Name the specific effect, not the category of risk: "a column rename fails the build", not "schema changes can cause issues".
9. Never write `simply`, `easy`, `just`, or `quickly` in a procedure.
10. Replace Latin abbreviations with the plain words: `for example` instead of `e.g.`, `that is` instead of `i.e.`. End a list with its last real item instead of `etc.`.
11. Avoid `-ing` forms where a plain verb or noun works: "Restart the service to apply the change", not "Restarting the service applies the change".

## Sentence structure

1. In a procedure step, put one action in each sentence. In an explanation, keep a cause and its effect, a condition and what it controls, or a contrast in one sentence, with the connective that shows the relation (`because`, `so`, `but`, `if`). Split a sentence when it joins two unrelated points or passes the length limit in item 12.

   An explanation in its final form:

   ```text
   Before: The cache expires. The service reloads. Latency rises.
   After:  When the cache expires, the service reloads it, so latency rises until the reload ends.
   ```
2. Use active voice when the actor is known: “The server rejects the request,” not “The request is rejected by the server.”
3. State conditions before the action when the condition controls the action: “If the token expires, sign in again.”
4. Use positive instructions when they are equally accurate. Keep explicit negatives for prohibitions, safety rules, and boundary conditions.
5. Make pronoun references clear. Repeat the noun when `it`, `this`, `that`, or `they` could refer to more than one thing. Never use `this` or `which` to point at a whole clause; name the thing instead.
6. When a sentence carries several constraints, split it into one constraint per sentence rather than dropping one.
7. Place `only` and `not` next to the word they change: "Retry only the failed jobs", not "Only retry the failed jobs".
8. Keep the verbs and the small words that show structure, such as `that`: "The log shows that the job failed", not "The log shows the job failed".
9. Make clear which parts `and` or `or` join. Repeat the article or the preposition in a series when it prevents a misread: "the cache and the queue for each region".
10. Write no slashes and no `(s)` between alternatives: "the client or the server", not "client/server"; "one or more files", not "file(s)". Make text in parentheses a full grammatical unit.
11. Use a serial comma before the last item of a series: "the cache, the queue, and the worker".
12. Split an instruction longer than about 20 words and any other sentence longer than about 25 words.
13. Keep `the` and `a`: "Open the file and add a line", not "Open file and add line".
14. End a sentence with a period instead of joining two sentences with a semicolon or an em dash.

## Procedures and explanations

- Address the reader as `you`, in the present tense.
- Start each procedure step with one direct action.
- Put the common case first and the exceptions after it.
- Put supporting information after the action it supports.
- Use numbered steps only when order matters; use bullets for unordered facts.
- Introduce a list with a complete sentence.
- Keep list items parallel: one action or one type of information per item.
- Write link text that names where the link goes: "see the retry policy", not "click here".
- Put code, commands, paths, and identifiers in code font. Put UI elements in bold: **Save**.
- Put a warning or a prerequisite before the step it controls.
- Explain cause and effect directly. Avoid decorative transitions and rhetorical setup.
- State the content instead of announcing it: "Set `TIMEOUT` to 30", not "The next section explains how to set the timeout".
- Never start consecutive sentences with the same phrase.
- Lead with the result, then give only the detail needed to understand or act.

## Precision gate

Before returning the text, check each item:

- The text keeps every requirement, limit, exception, and uncertainty.
- Each technical term has one stable form and meaning.
- Each pronoun has one clear referent.
- Each sentence carries one subject, and the relation between neighboring sentences is explicit, not left for the reader to infer.
- The actor is explicit when the actor matters.
- No simpler word would preserve the same technical meaning better.
- Code, commands, paths, identifiers, values, and quoted interface text are unchanged unless the user asked to change them.

## Audit format

ALWAYS use this exact template structure:

```text
Verdict: clear | needs revision

Findings
- Original: [problem text]
  Problem: [jargon, ambiguity, noun cluster, passive voice, long sentence, broken line of thought, or inconsistent term]
  Revision: [clear alternative]

Rewritten text
[complete revision]
```

Do not add the audit wrapper to a normal writing or rewriting request.
