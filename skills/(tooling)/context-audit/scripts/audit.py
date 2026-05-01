#!/usr/bin/env python3
"""
context-audit: deterministic scanner for Claude Code setup.

Scans MCP servers, slash commands, hooks, agents, skills, CLAUDE.md
files (with @import resolution), settings.json keys, and file
permissions. Emits structured JSON to stdout.

Usage:
    python audit.py [--project-root PATH] [--user-home PATH] [--out PATH]

Pure stdlib. No external dependencies.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

# Approximate token cost per Markdown line (rough rule of thumb: 4 tokens/line).
TOKENS_PER_LINE = 4
# Approximate token cost per MCP server when no /context data is provided.
DEFAULT_MCP_TOKEN_ESTIMATE = 15_000

# Effort weights for ranking fixes by savings ÷ effort.
EFFORT_WEIGHTS = {"trivial": 1, "small": 2, "medium": 4, "large": 8}


# ---------- helpers ----------

def read_json(path: Path) -> dict | None:
    """Read JSON file, return None if missing or invalid."""
    if not path.exists():
        return None
    try:
        return json.loads(path.read_text())
    except (json.JSONDecodeError, OSError):
        return None


def read_lines(path: Path) -> list[str]:
    """Read file as list of lines, return [] if missing."""
    if not path.exists():
        return []
    try:
        return path.read_text().splitlines()
    except OSError:
        return []


def parse_frontmatter(text: str) -> tuple[dict[str, str], str]:
    """Split YAML frontmatter from Markdown body. Returns (meta, body).
    Crude but stdlib-only — handles 'key: value' pairs, no nesting."""
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta_block, body = parts[1], parts[2]
    meta: dict[str, str] = {}
    current_key: str | None = None
    for raw in meta_block.splitlines():
        line = raw.rstrip()
        if not line.strip():
            continue
        if re.match(r"^\s+", line) and current_key:
            meta[current_key] += " " + line.strip()
            continue
        if ":" in line:
            key, _, value = line.partition(":")
            current_key = key.strip()
            meta[current_key] = value.strip().lstrip(">|-").strip()
    return meta, body.lstrip("\n")


def resolve_imports(path: Path, seen: set[Path] | None = None) -> str:
    """Recursively resolve @path imports inside a Markdown file.
    Returns the merged text. Cycles are broken by tracking `seen`."""
    if seen is None:
        seen = set()
    if path in seen or not path.exists():
        return ""
    seen.add(path)
    try:
        text = path.read_text()
    except OSError:
        return ""
    out: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^\s*@([^\s]+)\s*$", line)
        if match:
            target = (path.parent / match.group(1)).resolve()
            out.append(resolve_imports(target, seen))
        else:
            out.append(line)
    return "\n".join(out)


# ---------- scanners ----------

def scan_mcp(settings_user: dict | None, settings_project: dict | None,
             cli_alternatives: dict) -> dict:
    """Inspect MCP servers across user + project settings."""
    servers: list[dict] = []
    for scope, data in (("user", settings_user), ("project", settings_project)):
        if not data:
            continue
        mcp = data.get("mcpServers", {}) or {}
        for name, config in mcp.items():
            cli_match = None
            for alt in cli_alternatives.get("alternatives", []):
                if alt["match"].lower() in name.lower():
                    cli_match = alt
                    break
            servers.append({
                "name": name,
                "scope": scope,
                "has_cli_alternative": cli_match is not None,
                "cli": cli_match["cli"] if cli_match else None,
                "cli_note": cli_match["note"] if cli_match else None,
            })
    return {
        "count": len(servers),
        "with_cli_alternative": sum(1 for s in servers if s["has_cli_alternative"]),
        "servers": servers,
    }


def scan_instruction_dir(base: Path, subdir: str, label: str) -> list[dict]:
    """Generic scanner for .claude/{commands, agents}/*.md."""
    results: list[dict] = []
    target = base / ".claude" / subdir
    if not target.exists():
        return results
    for path in sorted(target.glob("*.md")):
        lines = read_lines(path)
        text = path.read_text() if path.exists() else ""
        meta, body = parse_frontmatter(text)
        results.append({
            "kind": label,
            "path": str(path),
            "lines": len(lines),
            "body_lines": len(body.splitlines()),
            "name": meta.get("name") or path.stem,
            "flagged_rules": prefilter_rules(body),
        })
    return results


def scan_skills(base: Path) -> list[dict]:
    """Scan .claude/skills/*/SKILL.md."""
    results: list[dict] = []
    skills_dir = base / ".claude" / "skills"
    if not skills_dir.exists():
        return results
    for skill_path in sorted(skills_dir.iterdir()):
        skill_md = skill_path / "SKILL.md"
        if not skill_md.exists():
            continue
        text = skill_md.read_text()
        meta, body = parse_frontmatter(text)
        body_lines = len(body.splitlines())
        desc = meta.get("description") or ""
        when = meta.get("when_to_use") or ""
        results.append({
            "name": meta.get("name") or skill_path.name,
            "path": str(skill_md),
            "total_lines": len(text.splitlines()),
            "body_lines": body_lines,
            "description_words": len(desc.split()),
            "desc_when_chars": len(desc) + len(when),
            "has_references_dir": (skill_path / "references").exists(),
            "has_scripts_dir": (skill_path / "scripts").exists(),
        })
    return results


# Heuristic patterns for the five filters. Each pattern flags candidate
# rules — the qualitative judgment in references/filters.md still applies,
# but pre-filtering means Claude only reads to confirm or reclassify,
# not to scan every line from scratch.
DEFAULT_BEHAVIOR_PATTERNS = [
    r"\bwrite\s+clean",
    r"\b(use|write)\s+(good|clear|descriptive|meaningful)\s+(naming|names)",
    r"\bhandle\s+errors?\s+(appropriately|properly|correctly)",
    r"\bbe\s+(helpful|accurate|honest|professional|polite|concise|thorough|natural|clear|kind|nice)\b",
    r"\bwrite\s+(readable|maintainable|clean)",
    r"\bdon'?t\s+(expose|leak|log)\s+(secrets|passwords|credentials)",
    r"\bavoid\s+(magic\s+numbers|deeply?\s+nested)",
]
VAGUE_PATTERNS = [
    r"\bbe\s+\w+\s*\.?$",            # "be natural.", "be concise."
    r"\bdon'?t\s+overdo\b",
    r"\b(use\s+good|good\s+(tone|style|vibes))",
    r"\bappropriate(ly)?\b",
    r"\bif\s+possible\b",
    r"\bwhen\s+appropriate\b",
]
BANDAID_PATTERNS = [
    r"#\d+",                          # Issue/PR number
    r"\blike\s+(in|the)\s+(last|previous)",
    r"\bafter\s+the\s+\w+\s+incident",
    r"\bdon'?t\s+repeat\b.*\b(mistake|bug|issue)",
]


def prefilter_rules(text: str) -> list[dict]:
    """Apply quick heuristic filters to find candidate flagged rules.
    Returns list of {line_number, text, candidate_filters[]}.
    The judgment in references/filters.md is still authoritative —
    this just narrows where Claude needs to look."""
    flagged: list[dict] = []
    for idx, raw in enumerate(text.splitlines(), start=1):
        line = raw.strip().lstrip("-*0123456789. ").strip()
        if not line or line.startswith("#"):
            continue
        # Skip @imports (handled by resolve_imports)
        if re.match(r"^@\S+$", line):
            continue
        candidates: list[str] = []
        for pat in DEFAULT_BEHAVIOR_PATTERNS:
            if re.search(pat, line, re.IGNORECASE):
                candidates.append("Default")
                break
        for pat in VAGUE_PATTERNS:
            if re.search(pat, line, re.IGNORECASE):
                candidates.append("Vague")
                break
        for pat in BANDAID_PATTERNS:
            if re.search(pat, line, re.IGNORECASE):
                candidates.append("Bandaid")
                break
        if candidates:
            flagged.append({
                "line": idx,
                "text": line,
                "candidate_filters": candidates,
            })
    return flagged


def scan_claude_md(paths: list[Path]) -> list[dict]:
    """Scan CLAUDE.md files, resolving @imports recursively, and
    pre-filter rules using heuristic patterns."""
    results: list[dict] = []
    for path in paths:
        if not path.exists():
            continue
        resolved = resolve_imports(path)
        results.append({
            "path": str(path),
            "raw_lines": len(read_lines(path)),
            "resolved_lines": len(resolved.splitlines()),
            "flagged_rules": prefilter_rules(resolved),
        })
    return results


def scan_settings(settings: dict | None, scope: str) -> dict:
    """Check for required settings keys."""
    if not settings:
        return {"scope": scope, "present": False}
    bash_max = (settings.get("env") or {}).get("BASH_MAX_OUTPUT_LENGTH")
    deny = ((settings.get("permissions") or {}).get("deny") or [])
    status_line = settings.get("statusLine")
    hooks = settings.get("hooks") or {}
    return {
        "scope": scope,
        "present": True,
        "bash_max_output_length": bash_max,
        "bash_max_ok": bash_max is not None and int(bash_max) >= 100_000,
        "deny_count": len(deny),
        "deny_rules": deny,
        "status_line": status_line,
        "hook_events": list(hooks.keys()),
    }


def detect_project_markers(base: Path) -> list[str]:
    """Return list of project-marker filenames present at base."""
    candidates = [
        "package.json", "Cargo.toml", "go.mod", "pyproject.toml",
        "requirements.txt", "pom.xml", "build.gradle", "build.gradle.kts",
        "composer.json", "Gemfile", "mix.exs",
    ]
    return [m for m in candidates if (base / m).exists()]


def missing_deny_patterns(base: Path, settings: dict | None,
                          bloat_patterns: dict) -> list[str]:
    """Compute deny patterns suggested by bloat_patterns.json that are
    missing from current deny rules and whose target dir actually exists."""
    deny: list[str] = []
    if settings:
        deny = ((settings.get("permissions") or {}).get("deny") or [])
    deny_set = set(deny)

    suggested: list[str] = []
    suggested.extend(bloat_patterns.get("always", []))
    for marker in detect_project_markers(base):
        suggested.extend(bloat_patterns.get("by_marker", {}).get(marker, []))

    missing: list[str] = []
    for pattern in suggested:
        if pattern in deny_set:
            continue
        # Extract dir from "Read(node_modules/**)" → "node_modules"
        match = re.match(r"Read\(([^/*]+)", pattern)
        if match:
            target_dir = base / match.group(1)
            # Only suggest if the directory or pattern target plausibly exists
            if not target_dir.exists() and not match.group(1).startswith("*"):
                continue
        missing.append(pattern)
    return missing


# ---------- scoring ----------

def compute_score(data: dict) -> dict:
    """Apply scoring rules from references/scoring.md with category caps."""
    deductions: list[dict] = []

    # MCP
    cli_alt_count = data["mcp"]["with_cli_alternative"]
    cli_alt_ded = min(cli_alt_count * 3, 15)
    if cli_alt_ded > 0:
        deductions.append({"reason": f"{cli_alt_count} MCP(s) with CLI alternative", "points": cli_alt_ded})
    overflow = max(0, data["mcp"]["count"] - 5)
    overflow_ded = min(overflow * 2, 10)
    if overflow_ded > 0:
        deductions.append({"reason": f"{overflow} MCP(s) beyond threshold of 5", "points": overflow_ded})

    # CLAUDE.md size — soft penalty; the file may be load-bearing in spec-heavy repos.
    for cmd in data["claude_md"]:
        lines = cmd["resolved_lines"]
        if lines > 500:
            deductions.append({"reason": f"{cmd['path']} > 500 lines (resolved)", "points": 10})
        elif lines > 200:
            deductions.append({"reason": f"{cmd['path']} > 200 lines (resolved)", "points": 5})

    # Flagged rules across instruction files (capped at -20)
    flagged_total = 0
    for cmd in data["claude_md"]:
        flagged_total += len(cmd.get("flagged_rules", []))
    for c in data["commands"]:
        flagged_total += len(c.get("flagged_rules", []))
    for a in data["agents"]:
        flagged_total += len(a.get("flagged_rules", []))
    flag_ded = min(flagged_total, 20)
    if flag_ded > 0:
        deductions.append({"reason": f"{flagged_total} rule(s) auto-flagged by filters", "points": flag_ded})

    # Skill descriptions — only `description + when_to_use` (capped at 1,536 chars)
    # loads at session start. Skill bodies load on invocation, so body length is
    # informational, not a per-session token cost.
    desc_overflow = sum(1 for s in data["skills"] if s.get("desc_when_chars", 0) > 1536)
    if desc_overflow:
        deductions.append({
            "reason": f"{desc_overflow} skill(s) with description+when_to_use over 1,536 chars",
            "points": min(desc_overflow * 5, 15),
        })

    # Agents > 150
    agent_ded = sum(3 for a in data["agents"] if a["lines"] > 150)
    agent_ded = min(agent_ded, 10)
    if agent_ded > 0:
        deductions.append({"reason": "Agent prompts over 150 lines", "points": agent_ded})

    # Slash commands > 100
    cmd_ded = sum(2 for c in data["commands"] if c["lines"] > 100)
    cmd_ded = min(cmd_ded, 10)
    if cmd_ded > 0:
        deductions.append({"reason": "Slash commands over 100 lines", "points": cmd_ded})

    # Settings — user scope cascades to every project, so it wins if present.
    # If user scope is missing the key, fall back to project scope before deducting.
    user_settings = data["settings"]["user"]
    project_settings = data["settings"]["project"]

    def effective(key: str) -> Any:
        for source in (user_settings, project_settings):
            if source.get("present") and source.get(key) is not None:
                return source.get(key)
        return None

    if effective("bash_max_output_length") is None:
        deductions.append({"reason": "Missing BASH_MAX_OUTPUT_LENGTH", "points": 5})

    # Permissions
    if data["missing_deny_patterns"] and data["project_markers"]:
        deductions.append({
            "reason": f"{len(data['missing_deny_patterns'])} missing deny rule(s)",
            "points": 10,
        })

    total = sum(d["points"] for d in deductions)
    score = max(0, 100 - total)
    if score >= 90:
        label = "CLEAN"
    elif score >= 70:
        label = "NEEDS WORK"
    elif score >= 50:
        label = "BLOATED"
    else:
        label = "CRITICAL"
    return {"score": score, "label": label, "deductions": deductions}


def estimate_savings(data: dict, context_data: dict | None) -> list[dict]:
    """Compute estimated tokens saved per fix, ranked by savings ÷ effort."""
    fixes: list[dict] = []

    # MCP with CLI alternative
    cli_count = data["mcp"]["with_cli_alternative"]
    if cli_count:
        per_server = (
            context_data.get("mcp_tokens_per_server")
            if context_data else None
        ) or DEFAULT_MCP_TOKEN_ESTIMATE
        fixes.append({
            "action": f"Disconnect {cli_count} MCP(s) with CLI alternatives",
            "savings": cli_count * per_server,
            "effort": "small",
            "approximate": context_data is None or "mcp_tokens_per_server" not in (context_data or {}),
        })

    # Long CLAUDE.md
    for cmd in data["claude_md"]:
        if cmd["resolved_lines"] > 200:
            target = 100
            saved = max(0, cmd["resolved_lines"] - target) * TOKENS_PER_LINE
            fixes.append({
                "action": f"Trim {cmd['path']} from {cmd['resolved_lines']} to ~{target} lines",
                "savings": saved,
                "effort": "medium",
                "approximate": True,
            })

    # Bash output cap (check both scopes)
    has_bash_cap = False
    for source in (data["settings"]["user"], data["settings"]["project"]):
        if source.get("present") and source.get("bash_max_output_length") is not None:
            has_bash_cap = True
            break
    if not has_bash_cap:
        fixes.append({
            "action": "Add BASH_MAX_OUTPUT_LENGTH=150000 to settings",
            "savings": 3_000,
            "effort": "trivial",
            "approximate": True,
        })

    # Deny rules
    if data["missing_deny_patterns"] and data["project_markers"]:
        fixes.append({
            "action": f"Add {len(data['missing_deny_patterns'])} deny rule(s) for bloat dirs",
            "savings": 10_000,
            "effort": "trivial",
            "approximate": True,
        })

    # Skills with bloated descriptions (the only part that loads at session start)
    for skill in data["skills"]:
        if skill.get("desc_when_chars", 0) > 1536:
            fixes.append({
                "action": f"Trim description+when_to_use of {skill['name']} below 1,536 chars",
                "savings": (skill["desc_when_chars"] - 1536) // 4,
                "effort": "trivial",
                "approximate": True,
            })

    # Rank by savings / effort_weight
    for fix in fixes:
        weight = EFFORT_WEIGHTS.get(fix["effort"], 4)
        fix["rank_score"] = fix["savings"] / weight
    fixes.sort(key=lambda f: f["rank_score"], reverse=True)
    return fixes


# ---------- main ----------

def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a Claude Code setup.")
    parser.add_argument("--project-root", default=os.getcwd(),
                        help="Project root (default: cwd)")
    parser.add_argument("--user-home", default=str(Path.home()),
                        help="User home for ~/.claude scan (default: $HOME)")
    parser.add_argument("--out", help="Write JSON to file instead of stdout")
    parser.add_argument("--context", help="Path to a JSON file with /context numbers (optional)")
    args = parser.parse_args()

    project = Path(args.project_root).resolve()
    home = Path(args.user_home).resolve()
    skill_dir = Path(__file__).resolve().parent.parent

    cli_alternatives = read_json(skill_dir / "assets" / "cli_alternatives.json") or {}
    bloat_patterns = read_json(skill_dir / "assets" / "bloat_patterns.json") or {}
    context_data = read_json(Path(args.context)) if args.context else None

    settings_user = (read_json(home / ".claude" / "settings.json")
                     or read_json(home / ".claude" / "settings.local.json"))
    settings_project = (read_json(project / ".claude" / "settings.json")
                        or read_json(project / "settings.json"))

    claude_md_paths = [
        project / "CLAUDE.md",
        project / ".claude" / "CLAUDE.md",
        home / ".claude" / "CLAUDE.md",
    ]

    data: dict[str, Any] = {
        "project_root": str(project),
        "project_markers": detect_project_markers(project),
        "mcp": scan_mcp(settings_user, settings_project, cli_alternatives),
        "commands": (
            scan_instruction_dir(project, "commands", "command")
            + scan_instruction_dir(home, "commands", "command")
        ),
        "agents": (
            scan_instruction_dir(project, "agents", "agent")
            + scan_instruction_dir(home, "agents", "agent")
        ),
        "skills": scan_skills(project) + scan_skills(home),
        "claude_md": scan_claude_md(claude_md_paths),
        "settings": {
            "user": scan_settings(settings_user, "user"),
            "project": scan_settings(settings_project, "project"),
        },
        "missing_deny_patterns": missing_deny_patterns(
            project, settings_project or settings_user, bloat_patterns
        ),
    }

    data["scoring"] = compute_score(data)
    data["fixes"] = estimate_savings(data, context_data)

    output = json.dumps(data, indent=2, default=str)
    if args.out:
        Path(args.out).write_text(output)
    else:
        print(output)
    return 0


if __name__ == "__main__":
    sys.exit(main())
