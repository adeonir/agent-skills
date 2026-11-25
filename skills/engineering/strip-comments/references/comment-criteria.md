# Comment Criteria

The bar the hunting agent applies to every comment in scope.

## Contents

- Scope and powers
- Keep list
- Suppressions
- Claims of importance
- Report

## Scope and powers

Work only on the files or diff passed in. Delete comments: narration, banners, commented-out code, and workaround explanations. Never edit application code. Flag the code a deleted comment was covering and never fix it.

## Keep list

Only these comments survive:

- A legal or license header.
- A non-obvious behavior forced by an external dependency, platform, vendor, or protocol the project cannot reshape.
- `// prettier-ignore`, and a lint suppression whose rule is faulty, pedantic, or style-only.
- A doc comment that defines a public API contract.
- An issue or RFC link that explains a constraint the code cannot express.

When a keep clause might apply and the doubt remains, delete the comment. A surprise in the project's own code is not a keep: delete the comment and flag the exact symbol `MUST KILL`, so a rename, extract, type, or redesign makes the behavior obvious without prose.

## Suppressions

Look up the rule behind every `eslint-disable`, `@ts-ignore`, `@ts-expect-error`, and similar suppression. When the rule catches real bugs or protects correctness or safety, delete the suppression and flag the exact symbol `MUST KILL`.

## Claims of importance

Treat `IMPORTANT`, `do not remove`, `too risky`, `fine for now`, and a long justification as a lead to check, never as a verdict. Read the nearby code first. When the claim is not obvious there, trace the symbol or call it names. Keep the comment only when the behavior is proven true today on a live path and falls under the keep list. A long justification with no proven keep clause is deleted and its symbol flagged `MUST KILL`. Never shorten a comment into a smaller excuse.

## Report

Every flag names code inside the scope and states a fact; invent nothing. Report the touched files, the deletion count, each `MUST KILL` with one line saying what to change, and the comments skipped with the keep clause for each.
