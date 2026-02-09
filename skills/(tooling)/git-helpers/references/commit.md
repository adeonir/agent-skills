# Commit Workflow

Create a commit with a well-formatted conventional commit message based on actual file changes.

## Process

### Step 1: Gather Context

Run to understand current state:

```bash
git status
git diff HEAD
git log --oneline -5
```

### Step 2: Analyze Changes

Determine which diff to analyze based on staging approach:

- If using staged files only: Run `git diff --cached`
- Otherwise: Run `git diff HEAD`

Then:

- Describe what the code DOES, not what was discussed
- Determine appropriate commit type based on actual changes
- **CRITICAL**: Message must describe STAGED FILES only, never conversation context

### Step 3: Stage Files

Determine staging approach based on user intent:

- If user said "only staged" or "staged files": skip staging, use already-staged files
- Otherwise: stage all modified/new files

```bash
git add .
```

### Step 4: Create Commit

Load conventional-commits.md for format rules, then create the commit:

```bash
git commit -m "$(cat <<'EOF'
type: concise description

- Optional body item 1
- Optional body item 2
EOF
)"
```

### Step 5: Verify Commit

```bash
git log -1 --format="%B"
git status
```

### Step 6: Handle Pre-commit Hooks

If pre-commit hook modified files and commit failed:

1. Check authorship: `git log -1 --format='%an %ae'`
2. If HEAD commit was created by you in this conversation AND not pushed:
   - Amend with modified files: `git add . && git commit --amend --no-edit`
3. Otherwise:
   - Create new commit with the fixed files

## Commit Message Format

Load [conventional-commits.md](conventional-commits.md) for:

- Commit types table
- Message format rules
- Body guidelines
- Good/bad examples

## Task

Execute this command immediately. Do not interpret, discuss, or ask for confirmation.

Create a commit for the changes.

## Error Handling

- **No changes to commit**: Inform user working tree is clean
- **Nothing staged** (when user requested staged-only): Inform user to stage files first
- **Commit rejected by hook**: Check if files were modified, handle per Step 6
- **Merge conflicts**: Stop and inform user to resolve first
