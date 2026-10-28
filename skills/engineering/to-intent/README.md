# To Intent

Turn an input into concrete intents with the user.

## What It Does

```mermaid
flowchart TD
    A[Receive input] --> B[Make concrete]
    B --> C[Calibrate outcomes]
    C --> D[Draft issue bodies]
    D --> E[User review]
    E -->|Corrections| D
    E -->|Approved| F[Register issues]
```

| Phase | Output |
|-------|--------|
| Receive | Input and claims to check |
| Make concrete | Template fields filled; unknowns kept explicit |
| Calibrate | One intent per independent outcome |
| Draft | Issue bodies with problem, outcome, affected users and systems, constraints, and open questions |
| Review | User-approved issue bodies |
| Register | Verified tracker issues and links |

## Usage

```text
/to-intent Customers call to ask for claim status; let them check it in the portal using their existing login.
Turn this incident into an intent and keep unknowns as open questions.
Capture the independent outcomes in this document as intents for review.
```

## Output

One tracker issue per approved intent. Drafts stay in the conversation; no local intent file is written.

## Requirements

A connected tracker tool or authenticated CLI is required for registration. Without tracker access, the skill returns approved issue bodies and reports the blocker.
