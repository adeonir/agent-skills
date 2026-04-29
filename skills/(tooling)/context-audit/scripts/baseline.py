#!/usr/bin/env python3
"""
context-audit drift detector.

Compares the current audit JSON against a previously saved baseline
at .claude/.audit-baseline.json. Reports score delta, new issues, and
fixed issues so the user can spot regressions over time.

Usage:
    # Save the current audit as the new baseline:
    python audit.py --out /tmp/audit.json
    python baseline.py --save /tmp/audit.json

    # Compare a fresh audit against the saved baseline:
    python audit.py --out /tmp/audit.json
    python baseline.py --compare /tmp/audit.json

Pure stdlib.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

BASELINE_FILENAME = ".audit-baseline.json"


def baseline_path(project_root: Path) -> Path:
    return project_root / ".claude" / BASELINE_FILENAME


def save_baseline(audit_path: Path, project_root: Path) -> Path:
    data = json.loads(audit_path.read_text())
    target = baseline_path(project_root)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps(data, indent=2, default=str))
    return target


def deduction_set(audit: dict) -> set[str]:
    return {d["reason"] for d in audit.get("scoring", {}).get("deductions", [])}


def compare(current: dict, previous: dict) -> dict:
    cur_score = current.get("scoring", {}).get("score", 0)
    prev_score = previous.get("scoring", {}).get("score", 0)
    cur_issues = deduction_set(current)
    prev_issues = deduction_set(previous)

    return {
        "score_now": cur_score,
        "score_before": prev_score,
        "delta": cur_score - prev_score,
        "new_issues": sorted(cur_issues - prev_issues),
        "resolved_issues": sorted(prev_issues - cur_issues),
        "still_present": sorted(cur_issues & prev_issues),
        "mcp_count_now": current.get("mcp", {}).get("count", 0),
        "mcp_count_before": previous.get("mcp", {}).get("count", 0),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Compare audit to baseline.")
    parser.add_argument("--save", help="Save the given audit JSON as baseline")
    parser.add_argument("--compare", help="Compare the given audit JSON against baseline")
    parser.add_argument("--project-root", default=".",
                        help="Project root (default: cwd)")
    args = parser.parse_args()

    project = Path(args.project_root).resolve()

    if args.save:
        target = save_baseline(Path(args.save), project)
        print(json.dumps({"saved_to": str(target)}, indent=2))
        return 0

    if args.compare:
        baseline = baseline_path(project)
        if not baseline.exists():
            print(json.dumps({
                "error": "No baseline found.",
                "hint": f"Run with --save first to create {baseline}.",
            }, indent=2), file=sys.stderr)
            return 1
        current = json.loads(Path(args.compare).read_text())
        previous = json.loads(baseline.read_text())
        result = compare(current, previous)
        print(json.dumps(result, indent=2))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())
