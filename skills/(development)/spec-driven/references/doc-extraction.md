# Documentation Extraction

Extract and transform requirements from referenced documentation into feature-level specifications.

## Core Principle

Extraction is **transformation**, not copying. Source documents (PRD, TDD) define product-level or system-level requirements. The spec defines feature-level, implementation-ready requirements. Every extracted item must be narrowed to the feature scope and refined with implementation detail.

| Source (PRD/TDD) | spec.md |
|-------------------|---------|
| Product-wide user stories | Feature-scoped stories prioritized by implementation order (P1/P2/P3) |
| Directional requirements (must/should/could) | Implementable FRs with measurable criteria |
| High-level acceptance criteria | Testable ACs in WHEN/THEN/SHALL format |
| Product KPIs and success metrics | Feature-specific success criteria (demo-able) |
| No edge cases | Edge cases (boundaries, errors, invalid inputs) |

## When to Use

- User provides `@path` to PRD, TDD, or documentation
- Need to map external requirements to spec format

## Process

### Step 1: List Files

If path is a directory, list all files:

```bash
find {path} -type f -name "*.md"
```

### Step 2: Read Each File

Read files completely to extract:

| Pattern | What to Extract | Examples |
|---------|-----------------|----------|
| Rules | "must", "cannot", "always", "never", "required", "shall" | "Users must verify email before login" |
| Constraints | "only if", "when", "unless", "if...then" | "Only if user is admin" |
| Examples | Code blocks, diagrams, sample data | API response examples |

### Step 3: Filter to Feature Scope

For each item extracted, ask: "Is this relevant to THIS specific feature?"

**If relevant:**
- Proceed to Step 4 (Transform)

**If not relevant:**
- Note WHY in Notes section (e.g., "Skipped: applies to billing feature, not auth")

**If partially relevant:**
- Extract only the part that applies to this feature

### Step 4: Transform to Implementation-Ready

Never copy source text verbatim. Each item must be transformed:

**User stories: Narrow and add detail**

```markdown
PRD: "As a user, I want to manage my account so that I stay in control"
  --> Too broad for a feature spec

Spec: ### P1: Password Reset
      - As a user, I want to reset my password via email so that I can regain access
      - **Independent Test:** Can demo by requesting reset, receiving email, clicking link, setting new password
```

**Requirements: Make measurable**

```markdown
PRD: "System must support password reset" (directional)
  --> Spec: FR-001: System must send password reset email within 60 seconds of request (measurable)
```

**Acceptance criteria: Make testable as code**

```markdown
PRD: "Reset links should expire" (vague)
  --> Spec: AC-001: WHEN reset link is older than 24 hours THEN system SHALL reject the link and display "Link expired"
```

**Identify what the source document lacks:**
- Edge cases not in the PRD --> add to Edge Cases section
- Measurable success criteria not in the PRD --> add to Success Criteria section
- Boundary conditions --> derive from requirements

### Step 5: Document Extraction

Output extraction summary before generating spec. The "Transformed To" column must show the refined version, not a copy:

```markdown
## Extracted from Documentation

| Source | Original | Relevant | Transformed To |
|--------|----------|----------|----------------|
| prd.md | "Users must verify email" | Yes | FR-001: System must send verification email within 60s of registration |
| prd.md | "SMS verification optional" | No | Skipped: out of scope for this feature |
| prd.md | "Easy onboarding" | Yes | SC-001: New user completes verification in under 2 minutes |
| (none) | -- | -- | Edge case: WHEN user clicks expired verification link THEN system SHALL offer resend |
```

Note: The last row shows content **derived** from requirements but not present in the source. Edge cases and success criteria often need to be inferred.

## Mapping Guidelines

### Rules --> Functional Requirements (make measurable)

```markdown
Source: "Users must be able to reset password via email"
--> FR-001: System must send password reset email within 60 seconds of request
```

### Constraints --> Acceptance Criteria (make testable)

```markdown
Source: "Reset link expires after 24 hours"
--> AC-001: WHEN reset link is older than 24 hours THEN system SHALL reject the request and display "Link expired"
```

### Broad stories --> Feature-scoped stories (narrow and add test)

```markdown
Source: "As a user, I want account security so that my data is safe"
--> ### P1: Password Reset
    - As a user, I want to reset my password via email so that I can regain access
    - **Independent Test:** Request reset, receive email, click link, set new password, login with new password
```

### Vague metrics --> Success criteria (make measurable)

```markdown
Source: "Fast onboarding experience"
--> SC-001: New user completes email verification in under 2 minutes
```

### Missing edge cases --> Derive from requirements

```markdown
Source: FR about email verification (no edge cases in PRD)
--> Edge case: WHEN user submits already-verified email THEN system SHALL display "Email already verified"
--> Edge case: WHEN verification email fails to send THEN system SHALL retry once and display error if still failing
```

## Error Handling

- **File not found**: Inform user, ask for correct path
- **Directory empty**: Inform user no .md files found
- **No relevant items**: Note in spec that docs were reviewed but no applicable requirements
- **Conflicting requirements**: Add to "Open Questions" section in spec.md

## Examples

**PRD Input:**
```
initialize feature @docs/prd.md
```

**Extraction Process:**
1. Read docs/prd.md
2. Find: "Users must verify email before accessing dashboard"
3. Find: "Verification link expires in 1 hour"
4. Find: "Easy onboarding for new users"
5. Transform (not copy) to spec:
   - FR-001: System must send verification email within 60 seconds of registration
   - FR-002: System must block dashboard access for unverified users
   - AC-001: WHEN verification link is older than 1 hour THEN system SHALL reject and offer resend
   - Edge case: WHEN user clicks verification link twice THEN system SHALL display "Already verified"
   - SC-001: New user completes email verification in under 2 minutes

**Spec Output:**
```markdown
## Functional Requirements
- [ ] FR-001: System must send verification email within 60 seconds of registration
- [ ] FR-002: System must block dashboard access for unverified users

## Acceptance Criteria
- [ ] AC-001: WHEN verification link is older than 1 hour THEN system SHALL reject and offer resend

## Edge Cases
- WHEN user clicks verification link twice THEN system SHALL display "Already verified"
- WHEN verification email fails to send THEN system SHALL retry once and show error if still failing

## Success Criteria
- [ ] New user completes email verification in under 2 minutes

## Notes
- Extracted and transformed from: docs/prd.md
- Skipped: "SMS verification optional" (out of scope for this feature)
```
