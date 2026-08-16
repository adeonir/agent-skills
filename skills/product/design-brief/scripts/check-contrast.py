#!/usr/bin/env python3
"""Check semantic DESIGN.md color pairs with WCAG 2.x contrast."""

import colorsys
import json
import math
import re
import sys
from pathlib import Path

BODY_TEXT_RATIO = 4.5

NAMED_COLORS = {
    "black": "#000000",
    "white": "#ffffff",
    "red": "#ff0000",
    "green": "#008000",
    "blue": "#0000ff",
    "yellow": "#ffff00",
    "gray": "#808080",
    "grey": "#808080",
    "orange": "#ffa500",
    "purple": "#800080",
    "rebeccapurple": "#663399",
    "transparent": "#00000000",
}


def unquote(value):
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


def extract_frontmatter(markdown):
    match = re.match(r"^---\r?\n(.*?)\r?\n---", markdown, re.S)
    return match.group(1) if match else None


def parse_subtree(yaml_text, root_key):
    lines = yaml_text.splitlines()
    start = next((index for index, line in enumerate(lines) if line == f"{root_key}:"), -1)
    if start < 0:
        return {}

    root = {}
    stack = [(0, root)]
    for line in lines[start + 1 :]:
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        match = re.match(r"^( +)([\w-]+):\s*(.*)$", line)
        if not match:
            break
        indent = len(match.group(1))
        while len(stack) > 1 and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1]
        key = match.group(2)
        value = match.group(3)
        if value:
            parent[key] = unquote(value.split(" #", 1)[0])
        else:
            child = {}
            parent[key] = child
            stack.append((indent, child))
    return root


def parse_channel(value):
    value = value.strip()
    if value.endswith("%"):
        return max(0.0, min(255.0, float(value[:-1]) * 2.55))
    return max(0.0, min(255.0, float(value)))


def parse_alpha(value):
    value = value.strip()
    if value.endswith("%"):
        return max(0.0, min(1.0, float(value[:-1]) / 100.0))
    return max(0.0, min(1.0, float(value)))


def parse_hex(value):
    digits = value.removeprefix("#")
    if len(digits) in (3, 4):
        digits = "".join(character * 2 for character in digits)
    if len(digits) not in (6, 8) or not re.fullmatch(r"[0-9a-fA-F]+", digits):
        return None
    red, green, blue = (int(digits[index : index + 2], 16) for index in (0, 2, 4))
    alpha = int(digits[6:8], 16) / 255.0 if len(digits) == 8 else 1.0
    return red, green, blue, alpha


def parse_rgb(value):
    match = re.fullmatch(r"rgba?\((.*)\)", value, re.I)
    if not match:
        return None
    body = match.group(1).replace(",", " ")
    color_part, separator, alpha_part = body.partition("/")
    parts = color_part.split()
    if len(parts) == 4 and not separator:
        alpha_part = parts.pop()
    if len(parts) != 3:
        return None
    try:
        red, green, blue = (parse_channel(part) for part in parts)
        alpha = parse_alpha(alpha_part) if alpha_part else 1.0
    except ValueError:
        return None
    return red, green, blue, alpha


def parse_hsl(value):
    match = re.fullmatch(r"hsla?\((.*)\)", value, re.I)
    if not match:
        return None
    body = match.group(1).replace(",", " ")
    color_part, separator, alpha_part = body.partition("/")
    parts = color_part.split()
    if len(parts) == 4 and not separator:
        alpha_part = parts.pop()
    if len(parts) != 3 or not parts[1].endswith("%") or not parts[2].endswith("%"):
        return None
    try:
        hue = float(re.sub(r"(deg|turn|rad|grad)$", "", parts[0]))
        saturation = float(parts[1][:-1]) / 100.0
        lightness = float(parts[2][:-1]) / 100.0
        alpha = parse_alpha(alpha_part) if alpha_part else 1.0
    except ValueError:
        return None
    red, green, blue = colorsys.hls_to_rgb((hue % 360.0) / 360.0, lightness, saturation)
    return red * 255.0, green * 255.0, blue * 255.0, alpha


def parse_oklch(value):
    match = re.fullmatch(
        r"oklch\(\s*([\d.]+)%?\s+([\d.]+)\s+([\d.]+)(?:deg)?(?:\s*/\s*([\d.]+%?))?\s*\)",
        value,
        re.I,
    )
    if not match:
        return None
    lightness = float(match.group(1))
    if "%" in match.group(0).split()[0]:
        lightness /= 100.0
    chroma = float(match.group(2))
    hue_radians = math.radians(float(match.group(3)))
    alpha = parse_alpha(match.group(4)) if match.group(4) else 1.0
    axis_a = chroma * math.cos(hue_radians)
    axis_b = chroma * math.sin(hue_radians)
    light_l = lightness + 0.3963377774 * axis_a + 0.2158037573 * axis_b
    light_m = lightness - 0.1055613458 * axis_a - 0.0638541728 * axis_b
    light_s = lightness - 0.0894841775 * axis_a - 1.2914855480 * axis_b
    linear_red = 4.0767416621 * light_l**3 - 3.3077115913 * light_m**3 + 0.2309699292 * light_s**3
    linear_green = -1.2684380046 * light_l**3 + 2.6097574011 * light_m**3 - 0.3413193965 * light_s**3
    linear_blue = -0.0041960863 * light_l**3 - 0.7034186147 * light_m**3 + 1.7076147010 * light_s**3

    def encode(channel):
        encoded = 12.92 * channel if channel <= 0.0031308 else 1.055 * channel ** (1 / 2.4) - 0.055
        return max(0.0, min(255.0, encoded * 255.0))

    return encode(linear_red), encode(linear_green), encode(linear_blue), alpha


def parse_color(value):
    normalized = unquote(str(value)).strip().lower()
    if normalized in NAMED_COLORS:
        normalized = NAMED_COLORS[normalized]
    if normalized.startswith("#"):
        return parse_hex(normalized)
    return parse_rgb(normalized) or parse_hsl(normalized) or parse_oklch(normalized)


def composite(color, background):
    red, green, blue, alpha = color
    if alpha >= 1.0:
        return red, green, blue
    return tuple(
        foreground * alpha + backdrop * (1.0 - alpha)
        for foreground, backdrop in zip((red, green, blue), background)
    )


def luminance(color):
    def linearize(channel):
        channel /= 255.0
        return channel / 12.92 if channel <= 0.04045 else ((channel + 0.055) / 1.055) ** 2.4

    red, green, blue = color
    return 0.2126 * linearize(red) + 0.7152 * linearize(green) + 0.0722 * linearize(blue)


def contrast_ratio(first, second):
    first_luminance = luminance(first)
    second_luminance = luminance(second)
    return (max(first_luminance, second_luminance) + 0.05) / (
        min(first_luminance, second_luminance) + 0.05
    )


def resolve_reference(value, colors):
    match = re.fullmatch(r"\{colors\.([\w-]+)\}", str(value))
    return colors.get(match.group(1)) if match else value


def semantic_pairs(colors):
    pairs = []
    for token in colors:
        if token.endswith("-foreground"):
            base = token[: -len("-foreground")]
            if base in colors:
                pairs.append((base, token))
        if token.startswith("on-"):
            base = token[len("on-") :]
            if base in colors:
                pairs.append((base, token))
    if "foreground" in colors and "background" in colors:
        pairs.append(("background", "foreground"))
    secondary_text = "muted-foreground" if "muted-foreground" in colors else "on-muted" if "on-muted" in colors else None
    if secondary_text:
        for surface in ("background", "surface", "card", "muted"):
            if surface in colors and (surface, secondary_text) not in pairs:
                pairs.append((surface, secondary_text))
    return pairs


def check_pair(label, background_value, text_value):
    background = parse_color(background_value)
    text = parse_color(text_value)
    if background is None or text is None:
        return {
            "label": label,
            "status": "ERROR",
            "ratio": None,
            "message": "required CSS color could not be parsed",
        }
    if background[3] < 1.0:
        return {
            "label": label,
            "status": "ERROR",
            "ratio": None,
            "message": "translucent background has no known backdrop",
        }
    background_rgb = background[:3]
    text_rgb = composite(text, background_rgb)
    ratio = contrast_ratio(background_rgb, text_rgb)
    return {
        "label": label,
        "status": "PASS" if ratio >= BODY_TEXT_RATIO else "FAIL",
        "ratio": round(ratio, 2),
        "message": f"requires {BODY_TEXT_RATIO}:1",
    }


def run_file(path):
    try:
        markdown = Path(path).read_text(encoding="utf-8")
    except OSError as error:
        return [], f"could not read {path}: {error}"
    frontmatter = extract_frontmatter(markdown)
    if frontmatter is None:
        return [], "missing YAML frontmatter"
    colors = parse_subtree(frontmatter, "colors")
    components = parse_subtree(frontmatter, "components")
    results = []
    for background_key, text_key in semantic_pairs(colors):
        results.append(
            check_pair(
                f"colors.{text_key} on colors.{background_key}",
                colors[background_key],
                colors[text_key],
            )
        )
    for component_name, properties in components.items():
        if not isinstance(properties, dict):
            continue
        if "backgroundColor" not in properties or "textColor" not in properties:
            continue
        background_value = resolve_reference(properties["backgroundColor"], colors)
        text_value = resolve_reference(properties["textColor"], colors)
        results.append(
            check_pair(
                f"components.{component_name}",
                background_value,
                text_value,
            )
        )
    if not results:
        return [], "no checkable semantic or component color pair"
    return results, None


def main(arguments):
    if len(arguments) < 2:
        print("usage: check-contrast.py DESIGN.md [--json]", file=sys.stderr)
        return 2
    path = arguments[1]
    json_output = "--json" in arguments[2:]
    results, error = run_file(path)
    if error:
        payload = {"status": "error", "message": error, "results": []}
        print(json.dumps(payload) if json_output else f"ERROR {error}")
        return 2
    failures = [result for result in results if result["status"] != "PASS"]
    payload = {
        "status": "failed" if failures else "passed",
        "summary": {
            "checks": len(results),
            "passed": len(results) - len(failures),
            "failed": len(failures),
        },
        "results": results,
    }
    if json_output:
        print(json.dumps(payload, indent=2))
    else:
        for result in results:
            ratio = f" {result['ratio']}:1" if result["ratio"] is not None else ""
            print(f"{result['status']} {result['label']}{ratio} — {result['message']}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
