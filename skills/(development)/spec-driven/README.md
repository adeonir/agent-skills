# Spec-Driven Development

Structured development workflow with specification, planning, task breakdown, and implementation.

## What It Does

Structured workflow for building software with clarity and traceability:

```mermaid
flowchart LR
    A[Initialize] --> D[Plan]
    D --> E[Tasks]
    E --> F[Implement]
    F --> G{Validate}
    G -->|Pass| H[Archive]
    G -->|Fail| F
    H --> I[Done]
```

| Phase | Purpose |
| ----- | ------- |
| **Initialize** | Create feature spec (greenfield or brownfield), resolve ambiguities inline |
| **Plan** | Technical architecture, codebase exploration, research |
| **Tasks** | Granular, atomic tasks with dependencies |
| **Implement** | Execute tasks against the spec |
| **Validate** | Verify implementation against acceptance criteria |
| **Archive** | Consolidate documentation for future reference

## Project Structure

```
.artifacts/                          # Working directory
├── project/
│   ├── PROJECT.md               # Vision, goals
│   ├── ROADMAP.md               # Planned features
│   └── CHANGELOG.md             # Completed features
├── codebase/                    # Code analysis (optional)
├── research/                    # Research cache (optional)
└── features/                    # Active features
    └── 001-feature/
        ├── spec.md              # Requirements
        ├── plan.md              # Architecture
        └── tasks.md             # Implementation tasks

docs/features/                   # Archived features
└── feature.md                   # Consolidated docs
```

## Usage

### Start a Project

```
initialize project
setup project for my app
```

Creates `.artifacts/project/` with PROJECT.md, ROADMAP.md, CHANGELOG.md.

### Create a Feature (Greenfield)

```
create new feature for user authentication
new feature: payment processing
```

**Greenfield** = new feature not related to existing code, or a completely new project. Creates `.artifacts/features/001-auth/` with spec.md (type: greenfield, status: draft).

### Create a Feature (Brownfield)

```
modify existing auth flow
improve cache performance
refactor user registration
```

**Brownfield** = new feature that modifies existing code, or refactoring an existing feature. Creates feature with baseline analysis documenting current behavior and gaps.

### Development Workflow

```
# Create technical plan (includes codebase exploration + research)
create technical plan

# Break into tasks
create tasks for auth

# Implement
implement auth feature

# Validate
validate auth implementation

# Archive
archive auth feature
```

## Examples

### Example 1: New Feature (Greenfield)

```
# Greenfield = new functionality (no existing code to modify)
# Can be in a new OR existing project

create new feature for user authentication

# Agent asks for requirements, resolves ambiguities inline (up to 2 Q&A rounds)
# Creates: .artifacts/features/001-user-auth/spec.md (status: draft)
# Type: greenfield

# Create technical plan
create technical plan

# For greenfield: focuses on architecture design
# For brownfield: explores existing similar features
# Creates: .artifacts/features/001-user-auth/plan.md
# Status: ready

# Break into tasks
create tasks for auth

# Creates: .artifacts/features/001-user-auth/tasks.md
# With: T001 [P] Create auth types, T002 [B:T001] Implement login...

# Implement
implement auth feature

# Validate
validate auth implementation

# Archive
archive auth feature

# Creates: docs/features/user-auth.md
```

### Example 2: Brownfield Feature (Existing Codebase)

```
# Map existing codebase (first time)
map codebase

# Creates .artifacts/codebase/ with STACK.md, ARCHITECTURE.md, etc.

# Create feature that modifies existing code
modify existing auth flow to add 2FA

# Creates .artifacts/features/002-add-2fa/spec.md
# Includes Baseline section with current auth behavior

# Continue with plan -> tasks -> implement -> validate -> archive
```

### Example 3: Feature with Research

```
# Create feature requiring new technology
create new feature for stripe payments

# During plan phase, agent detects "stripe" is new
# Checks .artifacts/research/stripe.md (doesn't exist)
# Researches Stripe API, creates research cache

# Research is now cached for future features using Stripe
```

### Example 4: Using PRD/TDD

```
# Initialize with PRD document
initialize feature @docs/prd.md

# Agent reads PRD, extracts requirements
# Creates spec.md with mapped FRs and ACs
```

### Example 5: Partial Workflow

```
# Just planning, no implementation yet
create new feature for notifications
create technical plan
create tasks

# Later...
implement notifications
validate
archive
```

## Details

### Initialize
Creates the feature specification. Detects greenfield vs brownfield, resolves ambiguities through inline Q&A (up to 2 rounds of 3-5 questions).
Defines WHAT to build. Generates spec.md with:
- User stories with priority levels (P1/P2/P3)
- Functional requirements
- Acceptance criteria (WHEN/THEN format)
- Open questions section (for unresolved items)

### Plan
Defines HOW to build. Creates plan.md with:
- Architecture decisions
- Codebase exploration (similar features, patterns)
- Data model (entities, relationships, API contracts)
- Research for new technologies (cached in .artifacts/research/)
- Component breakdown

### Tasks
Defines WHEN to build. Creates tasks.md with:
- Atomic tasks (T001, T002...)
- Dependencies [P] or [B:T001]
- Requirements coverage table

### Implement
Executes tasks from tasks.md:
- Loads coding principles before writing code
- Implements each task following the spec
- Updates task checkboxes
- Status: in-progress -> to-review

### Validate
Verifies implementation against spec:
- Adaptive: checks whatever artifacts exist
- Edge case verification (errors, boundaries, concurrency)
- Checks acceptance criteria are met
- Status: to-review -> done

### Archive
Generates consolidated documentation:
- Creates docs/features/{name}.md
- Updates CHANGELOG.md
- Optionally removes .artifacts/features/{ID}-{name}/

## State Management

Features track status in spec.md frontmatter:
- **draft**: Created, may have open questions
- **ready**: Spec complete, ready for plan
- **in-progress**: Implementation started
- **to-review**: All tasks done, needs validation
- **done**: Validated and complete
- **archived**: Moved to docs/

## Requirements

- Git (for branch association)

Works with any agent supporting standard skill format.

## FAQ

**Q: What's the difference between .artifacts/ and docs/?**
A: .artifacts/ is working directory (temporary), docs/ is permanent documentation.

**Q: Can I delete .artifacts/ after archive?**
A: Yes, but you'll lose ability to modify archived features.

**Q: How does research caching work?**
A: Research about new technologies is saved to .artifacts/research/{topic}.md and reused across features.

**Q: What's the difference between greenfield and brownfield?**
A: Greenfield is new functionality. Brownfield modifies existing code and includes baseline analysis.

**Q: Can I use this with existing git-helpers skill?**
A: Yes. Git-helpers handles commits and PRs, spec-driven handles planning and implementation.
