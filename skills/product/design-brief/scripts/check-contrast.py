#!/usr/bin/env python3
"""check-contrast.py — WCAG 2.x contrast checker for DESIGN.md color tokens.

Execute this script; never read it as reference.

Usage:
    python3 check-contrast.py <path-to-DESIGN.md> [--json]
    python3 check-contrast.py --pair <#RRGGBB> <#RRGGBB>

File mode checks:
    - every `colors.<base>` / `colors.<base>-foreground` pair at 4.5:1
      (`foreground` itself pairs with `background`)
    - `colors.muted-foreground` against `colors.background` and
      `colors.card` at 4.5:1 (it doubles as secondary text there)
    - every `components.<name>` with both `backgroundColor` and
      `textColor` resolved, at 4.5:1 (3:1 noted for large text / UI)
    - a `transparent`/`none` component fill resolves to the page
      (`colors.background`) — the text sits on the page; SKIP when no
      background is defined (the page is unknown, never assumed white)
    - `-disabled` component variants reported SKIP (inactive UI is
      exempt under WCAG 1.4.3)

The `colors:` block may be flat, or carry skin groups (light/dark or any
other name). Skin groups are detected structurally — a child map without a
`hex`/`oklch` member is a group — never by name. Flat tokens form the default
skin; each named group is an override skin inheriting every flat token it does
not redefine. Which skin is the default and which overrides is the author's
call. Override skins re-check only the pairs an override touches (the inherited
rest is identical to the default-skin result); a file with only groups and no
flat tokens checks each group standalone.

Object-form colors are checked through their `hex` member, in both block form
(nested `hex:` line) and inline flow form (`{ hex: "#...", oklch: "..." }`);
hex<->oklch agreement is a separate validate rule.

A run where every pair skips verifies nothing and exits 2 — an all-SKIP result
must never read as a passing gate.

Exit codes: 0 = no failures, 1 = at least one FAIL, 2 = usage/IO error.
"""

import json
import math
import re
import sys
from collections import namedtuple

Rgb = namedtuple("Rgb", "r g b")

# Thresholds from WCAG 2.x SC 1.4.3 (AA): 4.5:1 for body text,
# 3:1 for large text and UI components.
BODY_TEXT_RATIO = 4.5
LARGE_TEXT_RATIO = 3.0


def unquote(value):
    return re.sub(r'^["\']|["\']$', "", value.strip())


# Render a threshold the way JS string interpolation does: 4.5 stays "4.5",
# 3.0 collapses to "3" — keeps the notes byte-identical to the prior script.
def js_num(value):
    return str(int(value)) if float(value).is_integer() else repr(value)


# A `transparent`/`none` fill paints nothing; the page shows through.
# Matched case-insensitively after stripping quotes.
def is_transparent_fill(value):
    keyword = unquote(value).lower()
    return keyword == "transparent" or keyword == "none"


def parse_hex(value):
    if value is None:
        return None
    hex_value = unquote(value)
    short = re.match(r"^#([0-9a-f])([0-9a-f])([0-9a-f])$", hex_value, re.I)
    if short:
        return Rgb(
            int(short.group(1) * 2, 16),
            int(short.group(2) * 2, 16),
            int(short.group(3) * 2, 16),
        )
    full = re.match(r"^#([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$", hex_value, re.I)
    if full:
        return Rgb(
            int(full.group(1), 16),
            int(full.group(2), 16),
            int(full.group(3), 16),
        )
    return None


# WCAG 2.x relative luminance: linearize each sRGB channel with the spec's
# piecewise curve (0.04045 threshold, 12.92 linear slope, 2.4 gamma), then
# weight by the Rec. 709 luma coefficients.
def relative_luminance(rgb):
    def linearize(channel):
        c = channel / 255
        return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4

    return (
        0.2126 * linearize(rgb.r)
        + 0.7152 * linearize(rgb.g)
        + 0.0722 * linearize(rgb.b)
    )


# WCAG contrast ratio: (L_lighter + 0.05) / (L_darker + 0.05). The 0.05 term
# models ambient screen flare per the spec.
def contrast_ratio(a, b):
    la = relative_luminance(a)
    lb = relative_luminance(b)
    return (max(la, lb) + 0.05) / (min(la, lb) + 0.05)


# Composite a translucent foreground over its background in sRGB space,
# matching how browsers blend non-color-managed content. Channels are
# non-negative, so floor(x + 0.5) reproduces JS Math.round (round half up)
# rather than Python's round-half-to-even.
def blend(fg, bg, alpha):
    def mix(f, b):
        return math.floor(f * alpha + b * (1 - alpha) + 0.5)

    return Rgb(mix(fg.r, bg.r), mix(fg.g, bg.g), mix(fg.b, bg.b))


def extract_frontmatter(markdown):
    match = re.match(r"^---\r?\n(.*?)\r?\n---", markdown, re.S)
    return match.group(1) if match else None


# Minimal indentation walker: returns the subtree under a column-0 `root_key:`
# as nested maps of raw string values. Inline flow values (`{ ... }`) stay as
# the raw string for the caller to inspect.
def parse_subtree(yaml, root_key):
    lines = re.split(r"\r?\n", yaml)
    start = -1
    for i, line in enumerate(lines):
        if line == f"{root_key}:" or line.startswith(f"{root_key}: "):
            start = i
            break
    if start == -1:
        return None
    root = {}
    stack = [{"indent": 0, "node": root}]
    for i in range(start + 1, len(lines)):
        line = lines[i]
        if not line.strip() or re.match(r"^\s*#", line):
            continue
        entry = re.match(r"^( +)([\w-]+):\s*(.*)$", line)
        if not entry:
            break  # column-0 key or non-key line ends the block
        indent = len(entry.group(1))
        while len(stack) > 1 and indent <= stack[-1]["indent"]:
            stack.pop()
        parent = stack[-1]["node"]
        if entry.group(3):
            parent[entry.group(2)] = unquote(entry.group(3))
        else:
            child = {}
            parent[entry.group(2)] = child
            stack.append({"indent": indent, "node": child})
    return root


# A color leaf carries its checkable value as a literal string, an inline flow
# map with a `hex:` member, or a block map with a `hex` key. Returns the raw
# candidate (parse_hex validates later); a leaf with only `oklch` returns that
# string so the pair surfaces as SKIP instead of vanishing.
def color_leaf_value(node):
    if isinstance(node, str):
        flow = re.match(r"^\{.*\bhex:\s*([^,}]+)", node)
        return unquote(flow.group(1)) if flow else node
    if isinstance(node.get("hex"), str):
        return unquote(node["hex"])
    if isinstance(node.get("oklch"), str):
        return unquote(node["oklch"])
    return None


def is_color_leaf(node):
    return isinstance(node, str) or "hex" in node or "oklch" in node


# Interpret the `colors:` subtree. Flat tokens land in the "" skin; a child map
# without a `hex`/`oklch` member is a skin group (light, dark, any name —
# groups are structural, never name-matched) holding its own token map.
def parse_colors(yaml):
    tree = parse_subtree(yaml, "colors")
    skins = {}
    if tree is None or isinstance(tree, str):
        return skins

    def put(skin, token, raw):
        skins.setdefault(skin, {})[token] = raw

    for key, value in tree.items():
        if is_color_leaf(value):
            raw = color_leaf_value(value)
            if raw is not None:
                put("", key, raw)
            continue
        for token, token_value in value.items():
            raw = color_leaf_value(token_value) if is_color_leaf(token_value) else None
            if raw is not None:
                put(key, token, raw)
    return skins


# Minimal parser for `components:`: name -> { prop: raw_value }.
def parse_components(yaml):
    components = {}
    in_block = False
    current = None
    for line in re.split(r"\r?\n", yaml):
        if re.match(r"^components:\s*$", line):
            in_block = True
            continue
        if in_block and re.match(r"^\S", line):
            break
        if not in_block or not line.strip():
            continue
        name = re.match(r"^ {2}([\w-]+):\s*$", line)
        prop = re.match(r"^ {4}([\w-]+):\s*(\S.*)$", line)
        if name:
            current = name.group(1)
            components[current] = {}
        elif prop and current:
            components[current][prop.group(1)] = unquote(prop.group(2))
    return components


# Resolve a component color prop: a literal hex value, or a `{colors.<token>}`
# reference with an optional `/NN` opacity modifier. References resolve in the
# active skin first, then the flat default skin; a dotted path
# (`{colors.<skin>.<token>}`) pins a specific skin.
def resolve_color(raw, colors, skins):
    ref = re.match(r"^\{colors\.([\w.-]+)\}(?:/(\d{1,3}))?$", unquote(raw))
    if ref:
        token = ref.group(1)
        hex_value = colors.get(token)
        if hex_value is None:
            hex_value = skins.get("", {}).get(token)
        if hex_value is None and "." in token:
            dot = token.index(".")
            sub = token[dot + 1:]
            hex_value = skins.get(token[:dot], {}).get(sub)
            if hex_value is None:
                hex_value = skins.get("", {}).get(sub)
        if hex_value is None:
            return None
        rgb = parse_hex(hex_value)
        if rgb is None:
            return None
        alpha = min(100, int(ref.group(2))) / 100 if ref.group(2) else 1.0
        return (rgb, alpha)
    # A `transparent`/`none` fill has no surface of its own; for contrast the
    # text sits on the page, which is `colors.background`. Resolve to that
    # token at alpha 1 so it never enters the translucent blend path (and that
    # path's "#FFFFFF" page fallback). With no background defined the page is
    # genuinely unknown — return None so the caller SKIPs instead of assuming
    # white and reporting a fabricated ratio.
    if is_transparent_fill(raw):
        page_hex = colors.get("background")
        if page_hex is None:
            page_hex = skins.get("", {}).get("background")
        rgb = parse_hex(page_hex) if page_hex is not None else None
        return (rgb, 1.0) if rgb is not None else None
    literal = parse_hex(raw)
    return (literal, 1.0) if literal is not None else None


def format_ratio(ratio):
    return f"{ratio:.2f}:1"


def check_file(path, as_json):
    try:
        with open(path, "r", encoding="utf8") as handle:
            markdown = handle.read()
    except OSError:
        print(f"Cannot read {path}", file=sys.stderr)
        return 2
    yaml = extract_frontmatter(markdown)
    if yaml is None:
        print(f"No YAML frontmatter found in {path}", file=sys.stderr)
        return 2
    skins = parse_colors(yaml)
    if len(skins) == 0:
        print(f"No parseable color tokens found in {path}", file=sys.stderr)
        return 2

    # Flat tokens form the default skin; each named group is an override skin
    # inheriting every flat token it does not redefine. No group name is
    # special — the author picks which skin is the default.
    flat = skins.get("", {})
    flat_has_tokens = len(flat) > 0
    skin_entries = []
    if flat_has_tokens:
        skin_entries.append(
            {"name": "", "colors": flat, "overrides": set(flat.keys())}
        )
    for name in skins:
        if name == "":
            continue
        skin_entries.append(
            {
                "name": name,
                "colors": {**flat, **skins[name]},
                "overrides": set(skins[name].keys()),
            }
        )
    components = parse_components(yaml)
    findings = []

    def check(bg, fg, pair):
        ratio = contrast_ratio(bg, fg)
        finding = {
            "status": "PASS" if ratio >= BODY_TEXT_RATIO else "FAIL",
            "ratio": ratio,
            "pair": pair,
        }
        if ratio < BODY_TEXT_RATIO:
            if ratio >= LARGE_TEXT_RATIO:
                finding["note"] = (
                    f"needs {js_num(BODY_TEXT_RATIO)}:1 for body text; "
                    f"passes {js_num(LARGE_TEXT_RATIO)}:1 for large text and UI only"
                )
            else:
                finding["note"] = f"needs {js_num(BODY_TEXT_RATIO)}:1"
        findings.append(finding)

    for entry in skin_entries:
        skin_name = entry["name"]
        colors = entry["colors"]
        overrides = entry["overrides"]

        def label(token):
            return f"colors.{skin_name}.{token}" if skin_name else f"colors.{token}"

        # In an override skin, a pair neither side of which is overridden is
        # byte-identical to the default-skin check — skip the duplicate.
        def touches_override(a, b):
            return a in overrides or b in overrides

        def check_token_pair(base_key, fg_key):
            bg = parse_hex(colors[base_key])
            fg = parse_hex(colors[fg_key])
            if bg is None or fg is None:
                findings.append(
                    {
                        "status": "SKIP",
                        "ratio": None,
                        "pair": f"{label(fg_key)} on {label(base_key)}",
                        "note": "unparseable hex value",
                    }
                )
                return
            check(bg, fg, f"{label(fg_key)} on {label(base_key)}")

        for name in list(colors.keys()):
            if not name.endswith("foreground"):
                continue
            base = "background" if name == "foreground" else re.sub(
                r"-foreground$", "", name
            )
            if base != name and colors.get(base) and touches_override(base, name):
                check_token_pair(base, name)

        # muted-foreground doubles as secondary text on background and card
        if colors.get("muted-foreground"):
            for surface in ["background", "card"]:
                if colors.get(surface) and touches_override(surface, "muted-foreground"):
                    check_token_pair(surface, "muted-foreground")

    # A `{colors.<token>}` reference varies with the active skin; a skin-pinned
    # (`{colors.<skin>.<token>}`) or literal value does not.
    def skin_varying_token(raw):
        ref = re.match(r"^\{colors\.([\w.-]+)\}", unquote(raw))
        return ref.group(1) if ref and "." not in ref.group(1) else None

    def has_opacity(raw):
        return re.search(r"\}/\d{1,3}$", unquote(raw)) is not None

    # `transparent`/`none` fills resolve to the page (`colors.background`).
    # Establish once whether any skin defines a usable hex page; without one a
    # transparent component cannot be checked and must never fall back to an
    # assumed white page.
    page_is_known = any(
        parse_hex(entry["colors"].get("background", "")) is not None
        for entry in skin_entries
    )

    # Component references carry no skin name, so each pair resolves and checks
    # once per skin that can resolve it; a single SKIP surfaces only when no
    # skin resolves the pair. In an override skin the pair re-checks only when
    # an override touches it — via either referenced token, or via `background`
    # when a translucent value blends over it.
    for name, props in components.items():
        bg_raw = props.get("backgroundColor")
        fg_raw = props.get("textColor")
        if not bg_raw or not fg_raw:
            continue
        if re.search(r"-disabled$", name):
            findings.append(
                {
                    "status": "SKIP",
                    "ratio": None,
                    "pair": f"components.{name}",
                    "note": "disabled state exempt (WCAG 1.4.3 excludes inactive UI)",
                }
            )
            continue
        # A transparent/none fill sits on the page (colors.background). With no
        # page defined the result would rest on an assumed white page, so SKIP
        # rather than report a fabricated ratio.
        if is_transparent_fill(bg_raw) and not page_is_known:
            findings.append(
                {
                    "status": "SKIP",
                    "ratio": None,
                    "pair": f"components.{name}",
                    "note": "transparent fill sits on the page, but no colors.background is defined; the page is unknown and never assumed white",
                }
            )
            continue
        bg_token = skin_varying_token(bg_raw)
        fg_token = skin_varying_token(fg_raw)
        # A pair depends on the page when a translucent value blends over it or
        # a transparent fill resolves to it; either way an override skin that
        # redefines `background` changes the result and must re-check.
        depends_on_page = (
            has_opacity(bg_raw) or has_opacity(fg_raw) or is_transparent_fill(bg_raw)
        )
        resolved_any = False
        for entry in skin_entries:
            skin_name = entry["name"]
            colors = entry["colors"]
            overrides = entry["overrides"]
            inherited = (
                skin_name != ""
                and flat_has_tokens
                and not (bg_token and bg_token in overrides)
                and not (fg_token and fg_token in overrides)
                and not (depends_on_page and "background" in overrides)
            )
            if inherited:
                continue  # identical to the default-skin check
            bg = resolve_color(bg_raw, colors, skins)
            fg = resolve_color(fg_raw, colors, skins)
            if bg is None or fg is None:
                continue
            resolved_any = True
            # A translucent background composites over the page; approximate
            # the page with colors.background, falling back to opaque white.
            page_src = colors.get("background")
            if page_src is None:
                page_src = skins.get("", {}).get("background")
            if page_src is None:
                page_src = "#FFFFFF"
            page = parse_hex(page_src) or Rgb(255, 255, 255)
            bg_rgb = blend(bg[0], page, bg[1]) if bg[1] < 1 else bg[0]
            fg_rgb = blend(fg[0], bg_rgb, fg[1]) if fg[1] < 1 else fg[0]
            suffix = f" [{skin_name}]" if skin_name else ""
            check(bg_rgb, fg_rgb, f"components.{name} textColor on backgroundColor{suffix}")
        if not resolved_any:
            findings.append(
                {
                    "status": "SKIP",
                    "ratio": None,
                    "pair": f"components.{name}",
                    "note": "color did not resolve to a hex value",
                }
            )

    fails = sum(1 for f in findings if f["status"] == "FAIL")
    skips = sum(1 for f in findings if f["status"] == "SKIP")
    if as_json:
        # JS JSON.stringify drops the trailing ".0" of integer-valued numbers
        # (a 21.0 ratio serializes as 21); mirror that so JSON output matches.
        serializable = []
        for f in findings:
            item = dict(f)
            ratio = item.get("ratio")
            if isinstance(ratio, float) and ratio.is_integer():
                item["ratio"] = int(ratio)
            serializable.append(item)
        print(json.dumps(serializable, indent=2, ensure_ascii=False))
    else:
        for f in findings:
            ratio = "  --  " if f["ratio"] is None else format_ratio(f["ratio"]).rjust(7)
            note = f" ({f['note']})" if f.get("note") else ""
            print(f"{f['status'].ljust(4)} {ratio}  {f['pair']}{note}")
        print(f"\n{len(findings)} pairs checked, {fails} failing, {skips} skipped")
    # An all-SKIP run verified nothing; never let it read as a pass.
    if len(findings) > 0 and skips == len(findings):
        print(
            "Every pair was skipped — nothing verified. Check the color token shapes.",
            file=sys.stderr,
        )
        return 2
    return 1 if fails > 0 else 0


def check_pair(a, b):
    color_a = parse_hex(a)
    color_b = parse_hex(b)
    if color_a is None or color_b is None:
        print('Usage: check-contrast.py --pair "#RRGGBB" "#RRGGBB"', file=sys.stderr)
        return 2
    ratio = contrast_ratio(color_a, color_b)
    body = "PASS" if ratio >= BODY_TEXT_RATIO else "FAIL"
    large = "PASS" if ratio >= LARGE_TEXT_RATIO else "FAIL"
    print(
        f"{format_ratio(ratio)} — body text {js_num(BODY_TEXT_RATIO)}:1 {body}, "
        f"large text and UI {js_num(LARGE_TEXT_RATIO)}:1 {large}"
    )
    return 0 if ratio >= BODY_TEXT_RATIO else 1


def main(argv):
    args = argv[1:]
    if len(args) >= 3 and args[0] == "--pair":
        return check_pair(args[1], args[2])
    if len(args) >= 1 and args[0] != "--pair":
        return check_file(args[0], "--json" in args)
    print(
        "Usage:\n"
        "  python3 check-contrast.py <path-to-DESIGN.md> [--json]\n"
        "  python3 check-contrast.py --pair <#RRGGBB> <#RRGGBB>",
        file=sys.stderr,
    )
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
