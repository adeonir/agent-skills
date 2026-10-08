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

## Sentence structure

1. In a procedure step, put one action in each sentence. In an explanation, keep a cause and its effect, a condition and what it controls, or a contrast in one sentence, with the connective that shows the relation (`because`, `so`, `but`, `if`). Split a sentence only when it joins two unrelated points.
2. Use active voice when the actor is known: “The server rejects the request,” not “The request is rejected by the server.”
3. State conditions before the action when the condition controls the action: “If the token expires, sign in again.”
4. Use positive instructions when they are equally accurate. Keep explicit negatives for prohibitions, safety rules, and boundary conditions.
5. Make pronoun references clear. Repeat the noun when `it`, `this`, `that`, or `they` could refer to more than one thing.
6. When a sentence carries several constraints, split it into one constraint per sentence rather than dropping one.

## Procedures and explanations

- Start each procedure step with one direct action.
- Put supporting information after the action it supports.
- Use numbered steps only when order matters; use bullets for unordered facts.
- Keep list items parallel: one action or one type of information per item.
- Keep warnings and prerequisites next to the step they control.
- Explain cause and effect directly. Avoid decorative transitions and rhetorical setup.
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
