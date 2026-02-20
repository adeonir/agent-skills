# Initialize Feature

Create a new feature specification.

> **LOAD FIRST:** [status-workflow.md](status-workflow.md) - Required for correct status management

## Content Separation (CRITICAL)

Each artifact has a distinct purpose. Never mix these concerns.

| File | Purpose |
|------|---------|
| spec.md | WHAT to build (requirements, acceptance criteria) |
| plan.md | HOW to build (architecture, files, implementation) |
| tasks.md | WHEN to build (ordered tasks with dependencies) |

### spec.md MUST contain ONLY:

- User stories (As a... I want... so that...)
- Functional requirements (what the system must do)
- Acceptance criteria (verifiable conditions)
- Business rules and constraints
- For brownfield: current behavior description (high-level, no code)

### spec.md MUST NOT contain:

- Code snippets or examples
- File paths or directory structures
- Technology choices (React, Node, etc.)
- Implementation approaches
- Database schemas or API designs
- Architecture decisions

These belong in plan.md, created during the `plan` phase.

## Arguments

- `[description]` - Feature description
- `[@file.md]` - Path to PRD/TDD file
- Greenfield: "create new feature for..."
- Brownfield: "modify feature...", "improve..."

## Process

### Step 1: Ensure Project Structure

Check if `.artifacts/project/` exists. If not:
- Load [project-init.md](project-init.md)
- Initialize project first

### Step 2: Generate Feature ID

Scan `.artifacts/features/` for highest ID:

```bash
ls .artifacts/features/ | sort -V | tail -1
```

Next ID = highest + 1 (padded: 001, 002...)

### Step 3: Determine Type (Greenfield vs Brownfield)

**Greenfield triggers:**
- "create new feature"
- "new feature"
- "implement from scratch"

**Brownfield triggers:**
- "modify feature"
- "improve"
- "refactor"
- "extend"

If ambiguous, ask user.

### Step 4: Process Input

**If input is a file (@file.md):**

Load [doc-extraction.md](doc-extraction.md) and:

1. List all files in referenced path
2. Read each file completely
3. Extract rules, constraints, and examples
4. Map relevant items to FRs and ACs
5. Document extraction summary in Notes section

**If input is text:**
- Use as feature description

**If input is empty:**
- Ask user for feature description

### Step 5: Resolve Ambiguities (Inline Q&A)

After drafting the initial requirements, identify any unclear or ambiguous items.

**Process:**
1. Batch 3-5 questions together and ask the user in a single round
2. Maximum 2 rounds of questions
3. Questions unanswered after 2 rounds go to the "Open Questions" section in spec.md
4. Never block spec creation on unresolved questions

**Question format:**
- Be specific: "Should password reset require email verification?" not "How should reset work?"
- Offer options when possible: "Should the session timeout be (a) 30 minutes, (b) 1 hour, or (c) configurable?"

### Step 6: Baseline Discovery (Brownfield)

If type is `brownfield`:

Load [baseline-discovery.md](baseline-discovery.md) and:

1. Search codebase for related code
2. Analyze current user-facing behavior
3. Document gaps and limitations
4. Add Baseline section to spec.md

If `.artifacts/codebase/` doesn't exist:
- Suggest running "map codebase" for better context
- Or proceed with limited codebase understanding

### Step 7: Generate Feature Name

Convert description to kebab-case:
- "Add user authentication" -> `add-user-auth`

### Step 8: Ask About Branch

```
Associate this feature with a branch?
1. Keep on current branch (main)
2. Create new branch: feature/{name}
```

If option 2:
- Create branch: `git checkout -b feature/{name}`
- Store branch name in frontmatter

### Step 9: Create Feature Directory

```bash
mkdir -p .artifacts/features/{ID}-{name}
```

### Step 10: Generate spec.md

**USE TEMPLATE:** `templates/spec.md`

Generate the spec following the template structure:
- Frontmatter with ID, feature name, type, status, branch, created date
- Greenfield: Overview, User Stories, Functional Requirements, Acceptance Criteria, Open Questions, Notes
- Brownfield: Same structure plus Baseline section (Current Behavior, Gaps/Limitations)

### Step 11: Update ROADMAP.md

Add feature to roadmap.

### Step 12: Report

Inform user:
- Created: `.artifacts/features/{ID}-{name}/`
- Type: {greenfield|brownfield}
- Branch: {name}
- Open questions: {count, if any}
- Next: Run `plan`

## Codebase Mapping Note

**codebase-mapping.md** creates `.artifacts/codebase/` (6 docs) for general codebase understanding.

**Baseline in initialize** captures specific current behavior relevant to this feature (from spec perspective, not deep code analysis).

They complement each other:
- codebase-mapping: Macro view (all features)
- baseline: Micro view (this feature only)

## Error Handling

- No project structure: Initialize project first
- ID conflict: Regenerate ID
- Branch exists: Offer to checkout existing
