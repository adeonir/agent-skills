#!/usr/bin/env python3
"""Deterministic step inventory and baseline arithmetic for skill-reliability.

Two modes:
  inventory.py <skill-dir>               enumerate workflow files and their steps
  inventory.py --product "0.99 0.93 ..."  multiply baselines, print product + tier

The model assigns each step's nature; this script removes the mechanical work
(step enumeration and the multiplication) from the model's hands.
"""

import argparse
import re
import sys
from pathlib import Path

# Tier thresholds on the end-to-end product (see references/framework.md).
TIER_STRONG = 0.90    # product >= 0.90 -> Strong
TIER_MODERATE = 0.75  # product >= 0.75 -> Moderate, else Fragile

# A step heading: "### Step 3: Stage Files", "### Phase 1: Context", or "### 3. Draft".
STEP_HEADING = re.compile(r"^#{2,4}\s+(?:Step|Phase)\s+(\d+)\s*[:.\-)]?\s*(.*)$", re.IGNORECASE)
NUM_HEADING = re.compile(r"^#{2,4}\s+(\d+)\s*[:.)]\s+(.*)$")
# When a file has no step headings, numbered list items under a procedural
# section (## Workflow, ## Steps, ## Create gates …) are the steps instead.
WORKFLOW_SECTION = re.compile(r"^##\s+.*\b(?:workflow|steps|phases|process|procedure|gates)\b", re.IGNORECASE)
SECTION_HEADING = re.compile(r"^##\s+")
LIST_STEP = re.compile(r"^(\d+)\.\s+(.*)$")


def tier(product):
    if product >= TIER_STRONG:
        return "Strong"
    if product >= TIER_MODERATE:
        return "Moderate"
    return "Fragile"


def find_workflow_files(skill_dir):
    files = []
    skill_md = skill_dir / "SKILL.md"
    if skill_md.is_file():
        files.append(skill_md)
    for sub in ("references", "instructions"):
        subdir = skill_dir / sub
        if subdir.is_dir():
            files.extend(sorted(subdir.glob("*.md")))
    return files


def _clean_title(raw):
    """Reduce a list-item line to a short label (leading bold, or first clause)."""
    bold = re.match(r"\*\*(.+?)\*\*", raw)
    if bold:
        return bold.group(1).strip()
    return re.split(r"\s+[—–-]\s+|(?<=\w)\. ", raw)[0].strip()[:60]


def steps_in(path):
    """Enumerate a file's workflow steps.

    'Step N'/'Phase N' headings are self-signaling and count anywhere. A bare
    '### N.' heading or a numbered list item counts only inside a procedural
    section (## Workflow, ## Create gates …) — outside one, numbered headings
    are catalog entries (heuristics, personas), not steps.
    """
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return []
    steps = []
    in_workflow = False
    section_has_headings = False  # a section uses headings OR a numbered list, never both
    expected = 1
    for line in text.splitlines():
        if SECTION_HEADING.match(line):
            in_workflow = bool(WORKFLOW_SECTION.match(line))
            section_has_headings = False
            expected = 1
            continue
        labeled = STEP_HEADING.match(line)
        if labeled:
            steps.append((int(labeled.group(1)), labeled.group(2).strip()))
            section_has_headings = True
            continue
        numbered = NUM_HEADING.match(line)
        if numbered and in_workflow:
            steps.append((int(numbered.group(1)), numbered.group(2).strip()))
            section_has_headings = True
            continue
        item = LIST_STEP.match(line)
        if item and in_workflow and not section_has_headings and int(item.group(1)) == expected:
            steps.append((expected, _clean_title(item.group(2))))
            expected += 1
    return steps


def run_inventory(skill_dir):
    files = find_workflow_files(skill_dir)
    if not files:
        print(f"no SKILL.md or reference files found under {skill_dir}", file=sys.stderr)
        return 1
    total = 0
    for path in files:
        steps = steps_in(path)
        if not steps:
            continue
        rel = path.relative_to(skill_dir)
        print(f"{rel} — {len(steps)} steps")
        for num, title in steps:
            print(f"  {num}. {title}" if title else f"  {num}.")
        total += len(steps)
    print(f"total numbered steps: {total}")
    return 0


def run_product(raw):
    values = []
    for token in raw.replace(",", " ").split():
        try:
            value = float(token)
        except ValueError:
            print(f"not a number: {token}", file=sys.stderr)
            return 2
        if value > 1:  # accept either 0.93 or 93 (percent form)
            value = value / 100.0
        values.append(value)
    if not values:
        print("no baselines given", file=sys.stderr)
        return 2
    product = 1.0
    for value in values:
        product *= value
    print(f"steps: {len(values)}")
    print(f"end-to-end: {round(product * 100)}% ({tier(product)})")
    return 0


def main():
    parser = argparse.ArgumentParser(
        description="Step inventory + baseline product for skill-reliability",
    )
    parser.add_argument("skill_dir", nargs="?", help="path to the skill directory")
    parser.add_argument(
        "--product",
        help="space/comma-separated baselines to multiply (e.g. '0.99 0.93 0.90')",
    )
    args = parser.parse_args()

    if args.product is not None:
        return run_product(args.product)

    if not args.skill_dir:
        parser.print_usage(sys.stderr)
        return 2
    skill_dir = Path(args.skill_dir)
    if not skill_dir.is_dir():
        print(f"not a directory: {skill_dir}", file=sys.stderr)
        return 1
    return run_inventory(skill_dir)


if __name__ == "__main__":
    sys.exit(main())
