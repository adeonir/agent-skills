#!/usr/bin/env bun
/**
 * check-contrast.ts — WCAG 2.x contrast checker for DESIGN.md color tokens.
 *
 * Execute this script; never read it as reference.
 *
 * Usage:
 *   bun run check-contrast.ts <path-to-DESIGN.md> [--json]
 *   bun run check-contrast.ts --pair <#RRGGBB> <#RRGGBB>
 *
 * File mode checks:
 *   - every `colors.<base>` / `colors.<base>-foreground` pair at 4.5:1
 *     (`foreground` itself pairs with `background`)
 *   - `colors.muted-foreground` against `colors.background` and
 *     `colors.card` at 4.5:1 (it doubles as secondary text there)
 *   - every `components.<name>` with both `backgroundColor` and
 *     `textColor` resolved, at 4.5:1 (3:1 noted for large text / UI)
 *   - `-disabled` component variants reported SKIP (inactive UI is
 *     exempt under WCAG 1.4.3)
 *
 * Object-form colors ({ hex, oklch }) are checked through their `hex`
 * member; hex↔oklch agreement is a separate validate rule.
 *
 * Exit codes: 0 = no failures, 1 = at least one FAIL, 2 = usage/IO error.
 */

// Force module scope so the declarations below stay file-local instead
// of merging into the global scope shared with sibling scripts.
export {};

// Standalone script — no tsconfig or @types/node alongside it. Declaring
// the exact runtime members used here keeps editor diagnostics clean
// without a types dependency; exit() typed `never` restores TS flow
// narrowing after early exits.
declare const process: { argv: string[]; exit(code?: number): never };
declare function require(id: "fs"): {
  readFileSync(path: string, encoding: "utf8"): string;
};
const { readFileSync } = require("fs");

type Rgb = { r: number; g: number; b: number };

type Finding = {
  status: "PASS" | "FAIL" | "SKIP";
  ratio: number | null;
  pair: string;
  note?: string;
};

// Thresholds from WCAG 2.x SC 1.4.3 (AA): 4.5:1 for body text,
// 3:1 for large text and UI components.
const BODY_TEXT_RATIO = 4.5;
const LARGE_TEXT_RATIO = 3.0;

function unquote(value: string): string {
  return value.trim().replace(/^["']|["']$/g, "");
}

function parseHex(value: string): Rgb | null {
  const hex = unquote(value);
  const short = /^#([0-9a-f])([0-9a-f])([0-9a-f])$/i.exec(hex);
  if (short) {
    return {
      r: parseInt(short[1] + short[1], 16),
      g: parseInt(short[2] + short[2], 16),
      b: parseInt(short[3] + short[3], 16),
    };
  }
  const full = /^#([0-9a-f]{2})([0-9a-f]{2})([0-9a-f]{2})$/i.exec(hex);
  if (full) {
    return {
      r: parseInt(full[1], 16),
      g: parseInt(full[2], 16),
      b: parseInt(full[3], 16),
    };
  }
  return null;
}

// WCAG 2.x relative luminance: linearize each sRGB channel with the
// spec's piecewise curve (0.04045 threshold, 12.92 linear slope,
// 2.4 gamma), then weight by the Rec. 709 luma coefficients.
function relativeLuminance({ r, g, b }: Rgb): number {
  const linearize = (channel: number): number => {
    const c = channel / 255;
    return c <= 0.04045 ? c / 12.92 : Math.pow((c + 0.055) / 1.055, 2.4);
  };
  return 0.2126 * linearize(r) + 0.7152 * linearize(g) + 0.0722 * linearize(b);
}

// WCAG contrast ratio: (L_lighter + 0.05) / (L_darker + 0.05).
// The 0.05 term models ambient screen flare per the spec.
function contrastRatio(a: Rgb, b: Rgb): number {
  const la = relativeLuminance(a);
  const lb = relativeLuminance(b);
  return (Math.max(la, lb) + 0.05) / (Math.min(la, lb) + 0.05);
}

// Composite a translucent foreground over its background in sRGB space,
// matching how browsers blend non-color-managed content.
function blend(fg: Rgb, bg: Rgb, alpha: number): Rgb {
  const mix = (f: number, b: number) => Math.round(f * alpha + b * (1 - alpha));
  return { r: mix(fg.r, bg.r), g: mix(fg.g, bg.g), b: mix(fg.b, bg.b) };
}

function extractFrontmatter(markdown: string): string | null {
  const match = /^---\r?\n([\s\S]*?)\r?\n---/.exec(markdown);
  return match ? match[1] : null;
}

// Minimal parser for the flat `colors:` block: values are hex strings
// or two-key objects whose `hex` member carries the checkable value.
function parseColors(yaml: string): Record<string, string> {
  const colors: Record<string, string> = {};
  let inBlock = false;
  let pendingKey: string | null = null;
  for (const line of yaml.split(/\r?\n/)) {
    if (/^colors:\s*$/.test(line)) {
      inBlock = true;
      continue;
    }
    if (inBlock && /^\S/.test(line)) break; // next top-level key ends the block
    if (!inBlock || !line.trim()) continue;
    const flat = /^ {2}([\w-]+):\s*(\S.*)$/.exec(line);
    const nested = /^ {2}([\w-]+):\s*$/.exec(line);
    const hexProp = /^ {4,}hex:\s*(\S.*)$/.exec(line);
    if (flat) {
      colors[flat[1]] = unquote(flat[2]);
      pendingKey = null;
    } else if (nested) {
      pendingKey = nested[1];
    } else if (hexProp && pendingKey) {
      colors[pendingKey] = unquote(hexProp[1]);
    }
  }
  return colors;
}

// Minimal parser for `components:`: name -> { prop: rawValue }.
function parseComponents(yaml: string): Record<string, Record<string, string>> {
  const components: Record<string, Record<string, string>> = {};
  let inBlock = false;
  let current: string | null = null;
  for (const line of yaml.split(/\r?\n/)) {
    if (/^components:\s*$/.test(line)) {
      inBlock = true;
      continue;
    }
    if (inBlock && /^\S/.test(line)) break;
    if (!inBlock || !line.trim()) continue;
    const name = /^ {2}([\w-]+):\s*$/.exec(line);
    const prop = /^ {4}([\w-]+):\s*(\S.*)$/.exec(line);
    if (name) {
      current = name[1];
      components[current] = {};
    } else if (prop && current) {
      components[current][prop[1]] = unquote(prop[2]);
    }
  }
  return components;
}

// Resolve a component color prop: a literal hex value, or a
// `{colors.<token>}` reference with an optional `/NN` opacity modifier.
function resolveColor(
  raw: string,
  colors: Record<string, string>,
): { rgb: Rgb; alpha: number } | null {
  const ref = /^\{colors\.([\w-]+)\}(?:\/(\d{1,3}))?$/.exec(unquote(raw));
  if (ref) {
    const hex = colors[ref[1]];
    if (!hex) return null;
    const rgb = parseHex(hex);
    if (!rgb) return null;
    const alpha = ref[2] ? Math.min(100, parseInt(ref[2], 10)) / 100 : 1;
    return { rgb, alpha };
  }
  const literal = parseHex(raw);
  return literal ? { rgb: literal, alpha: 1 } : null;
}

function formatRatio(ratio: number): string {
  return `${ratio.toFixed(2)}:1`;
}

function checkFile(path: string, asJson: boolean): never {
  let markdown: string;
  try {
    markdown = readFileSync(path, "utf8");
  } catch {
    console.error(`Cannot read ${path}`);
    process.exit(2);
  }
  const yaml = extractFrontmatter(markdown);
  if (!yaml) {
    console.error(`No YAML frontmatter found in ${path}`);
    process.exit(2);
  }
  const colors = parseColors(yaml);
  if (Object.keys(colors).length === 0) {
    console.error(`No parseable color tokens found in ${path}`);
    process.exit(2);
  }
  const components = parseComponents(yaml);
  const findings: Finding[] = [];

  const check = (bg: Rgb, fg: Rgb, pair: string) => {
    const ratio = contrastRatio(bg, fg);
    findings.push({
      status: ratio >= BODY_TEXT_RATIO ? "PASS" : "FAIL",
      ratio,
      pair,
      note:
        ratio >= BODY_TEXT_RATIO
          ? undefined
          : ratio >= LARGE_TEXT_RATIO
            ? `needs ${BODY_TEXT_RATIO}:1 for body text; passes ${LARGE_TEXT_RATIO}:1 for large text and UI only`
            : `needs ${BODY_TEXT_RATIO}:1`,
    });
  };

  const checkTokenPair = (baseKey: string, fgKey: string) => {
    const bg = parseHex(colors[baseKey]);
    const fg = parseHex(colors[fgKey]);
    if (!bg || !fg) {
      findings.push({
        status: "SKIP",
        ratio: null,
        pair: `colors.${fgKey} on colors.${baseKey}`,
        note: "unparseable hex value",
      });
      return;
    }
    check(bg, fg, `colors.${fgKey} on colors.${baseKey}`);
  };

  for (const name of Object.keys(colors)) {
    if (!name.endsWith("foreground")) continue;
    const base =
      name === "foreground" ? "background" : name.replace(/-foreground$/, "");
    if (base !== name && colors[base]) checkTokenPair(base, name);
  }

  // muted-foreground doubles as secondary text on background and card
  if (colors["muted-foreground"]) {
    for (const surface of ["background", "card"]) {
      if (colors[surface]) checkTokenPair(surface, "muted-foreground");
    }
  }

  for (const [name, props] of Object.entries(components)) {
    const bgRaw = props.backgroundColor;
    const fgRaw = props.textColor;
    if (!bgRaw || !fgRaw) continue;
    if (/-disabled$/.test(name)) {
      findings.push({
        status: "SKIP",
        ratio: null,
        pair: `components.${name}`,
        note: "disabled state exempt (WCAG 1.4.3 excludes inactive UI)",
      });
      continue;
    }
    const bg = resolveColor(bgRaw, colors);
    const fg = resolveColor(fgRaw, colors);
    if (!bg || !fg) {
      findings.push({
        status: "SKIP",
        ratio: null,
        pair: `components.${name}`,
        note: "color did not resolve to a hex value",
      });
      continue;
    }
    // A translucent background composites over the page; approximate the
    // page with colors.background, falling back to opaque white.
    const page = parseHex(colors.background ?? "#FFFFFF") ?? {
      r: 255,
      g: 255,
      b: 255,
    };
    const bgRgb = bg.alpha < 1 ? blend(bg.rgb, page, bg.alpha) : bg.rgb;
    const fgRgb = fg.alpha < 1 ? blend(fg.rgb, bgRgb, fg.alpha) : fg.rgb;
    check(bgRgb, fgRgb, `components.${name} textColor on backgroundColor`);
  }

  if (asJson) {
    console.log(JSON.stringify(findings, null, 2));
  } else {
    for (const f of findings) {
      const ratio = f.ratio === null ? "  --  " : formatRatio(f.ratio).padStart(7);
      console.log(`${f.status.padEnd(4)} ${ratio}  ${f.pair}${f.note ? ` (${f.note})` : ""}`);
    }
    const fails = findings.filter((f) => f.status === "FAIL").length;
    console.log(`\n${findings.length} pairs checked, ${fails} failing`);
  }
  process.exit(findings.some((f) => f.status === "FAIL") ? 1 : 0);
}

function checkPair(a: string, b: string): never {
  const colorA = parseHex(a);
  const colorB = parseHex(b);
  if (!colorA || !colorB) {
    console.error('Usage: check-contrast.ts --pair "#RRGGBB" "#RRGGBB"');
    process.exit(2);
  }
  const ratio = contrastRatio(colorA, colorB);
  const body = ratio >= BODY_TEXT_RATIO ? "PASS" : "FAIL";
  const large = ratio >= LARGE_TEXT_RATIO ? "PASS" : "FAIL";
  console.log(
    `${formatRatio(ratio)} — body text ${BODY_TEXT_RATIO}:1 ${body}, large text and UI ${LARGE_TEXT_RATIO}:1 ${large}`,
  );
  process.exit(ratio >= BODY_TEXT_RATIO ? 0 : 1);
}

const args = process.argv.slice(2);
if (args[0] === "--pair" && args.length >= 3) {
  checkPair(args[1], args[2]);
} else if (args.length >= 1 && args[0] !== "--pair") {
  checkFile(args[0], args.includes("--json"));
} else {
  console.error(
    "Usage:\n  bun run check-contrast.ts <path-to-DESIGN.md> [--json]\n  bun run check-contrast.ts --pair <#RRGGBB> <#RRGGBB>",
  );
  process.exit(2);
}
