---
paths:
  - "skills/**/*.md"
---

## English, Imperative

**Impact: MEDIUM**

Write repository files in English, and address the agent directly: "Read the issue through the tracker's MCP server", never "The issue is read through the tracker's MCP server".

**Incorrect:**

```markdown
The issue is read through the tracker's MCP server.
```

**Correct:**

```markdown
Read the issue through the tracker's MCP server.
```

## A Reason Only When It Decides

**Impact: MEDIUM**

State the standing fact. Keep a reason when it changes what the agent does: a cost to weigh, the condition that selects between two options, or the intent that lets it apply the rule to a case the rule did not foresee. Drop the account of what was found, tried, or fixed.

**Incorrect:**

```markdown
Rendering the title twice looked wrong on the first pass, so after some
back and forth we settled on stripping the leading H1.
```

**Correct:**

```markdown
The adapter strips a leading H1 that repeats the title.

Strip only when the body opens with the same words, because a different H1
is content.
```

## One Default, One Escape Hatch

**Impact: MEDIUM**

Name one recommended path. Mention the alternative only for the exception it serves, because a menu of three routes makes the agent pick again on every run.

**Incorrect:**

```markdown
You can use pypdf, pdfplumber, or PyMuPDF, or pdf2image for scanned files.
```

**Correct:**

```markdown
Use pdfplumber for text extraction.

For scanned PDFs, use pdf2image with pytesseract.
```

## No Dates

**Impact: MEDIUM**

Skill content stays timeless: no absolute dates, no version pins, no "soon" language. Legacy content that must stay visible goes under a collapsed `<details>` block.

**Incorrect:**

```markdown
As of January 2026, use the v2 endpoint (v3 ships next quarter).
```

**Correct:**

```markdown
Use the v2 endpoint: `api.example.com/v2/messages`.
```
