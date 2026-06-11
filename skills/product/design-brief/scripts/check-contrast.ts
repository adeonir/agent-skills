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
 * The `colors:` block may be flat, or grouped into skins (light/dark
 * or any other name). Skin groups are detected structurally — a child
 * map without a `hex`/`oklch` member is a group — never by name. Each
 * skin's pairs are checked independently; component references resolve
 * once per skin.
 *
 * Object-form colors are checked through their `hex` member, in both
 * block form (nested `hex:` line) and inline flow form
 * (`{ hex: "#...", oklch: "..." }`); hex↔oklch agreement is a separate
 * validate rule.
 *
 * A run where every pair skips verifies nothing and exits 2 — an
 * all-SKIP result must never read as a passing gate.
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

type ColorMap = Record<string, string>;
// Skin name -> token -> raw color value. The "" key is the default
// skin holding flat (ungrouped) tokens.
type Skins = Record<string, ColorMap>;

type YamlNode = string | { [key: string]: YamlNode };

// Minimal indentation walker: returns the subtree under a column-0
// `rootKey:` as nested maps of raw string values. Inline flow values
// (`{ ... }`) stay as the raw string for the caller to inspect.
function parseSubtree(yaml: string, rootKey: string): YamlNode | null {
  const lines = yaml.split(/\r?\n/);
  let start = -1;
  for (let i = 0; i < lines.length; i++) {
    if (lines[i] === `${rootKey}:` || lines[i].startsWith(`${rootKey}: `)) {
      start = i;
      break;
    }
  }
  if (start === -1) return null;
  const root: { [key: string]: YamlNode } = {};
  const stack: Array<{ indent: number; node: { [key: string]: YamlNode } }> = [
    { indent: 0, node: root },
  ];
  for (let i = start + 1; i < lines.length; i++) {
    const line = lines[i];
    if (!line.trim() || /^\s*#/.test(line)) continue;
    const entry = /^( +)([\w-]+):\s*(.*)$/.exec(line);
    if (!entry) break; // column-0 key or non-key line ends the block
    const indent = entry[1].length;
    while (stack.length > 1 && indent <= stack[stack.length - 1].indent) {
      stack.pop();
    }
    const parent = stack[stack.length - 1].node;
    if (entry[3]) {
      parent[entry[2]] = unquote(entry[3]);
    } else {
      const child: { [key: string]: YamlNode } = {};
      parent[entry[2]] = child;
      stack.push({ indent, node: child });
    }
  }
  return root;
}

// A color leaf carries its checkable value as a literal string, an
// inline flow map with a `hex:` member, or a block map with a `hex`
// key. Returns the raw candidate (parseHex validates later); a leaf
// with only `oklch` returns that string so the pair surfaces as SKIP
// instead of vanishing.
function colorLeafValue(node: YamlNode): string | null {
  if (typeof node === "string") {
    const flow = /^\{.*\bhex:\s*([^,}]+)/.exec(node);
    return flow ? unquote(flow[1]) : node;
  }
  if (typeof node.hex === "string") return unquote(node.hex);
  if (typeof node.oklch === "string") return unquote(node.oklch);
  return null;
}

function isColorLeaf(node: YamlNode): boolean {
  return typeof node === "string" || "hex" in node || "oklch" in node;
}

// Interpret the `colors:` subtree. Flat tokens land in the "" skin; a
// child map without a `hex`/`oklch` member is a skin group (light,
// dark, any name — groups are structural, never name-matched) holding
// its own token map.
function parseColors(yaml: string): Skins {
  const tree = parseSubtree(yaml, "colors");
  const skins: Skins = {};
  if (!tree || typeof tree === "string") return skins;
  const put = (skin: string, token: string, raw: string) => {
    (skins[skin] ??= {})[token] = raw;
  };
  for (const [key, value] of Object.entries(tree)) {
    if (isColorLeaf(value)) {
      const raw = colorLeafValue(value);
      if (raw !== null) put("", key, raw);
      continue;
    }
    for (const [token, tokenValue] of Object.entries(value)) {
      const raw = isColorLeaf(tokenValue) ? colorLeafValue(tokenValue) : null;
      if (raw !== null) put(key, token, raw);
    }
  }
  return skins;
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
// `{colors.<token>}` reference with an optional `/NN` opacity
// modifier. References resolve in the active skin first, then the
// flat default skin; a dotted path (`{colors.<skin>.<token>}`) pins a
// specific skin.
function resolveColor(
  raw: string,
  colors: ColorMap,
  skins: Skins,
): { rgb: Rgb; alpha: number } | null {
  const ref = /^\{colors\.([\w.-]+)\}(?:\/(\d{1,3}))?$/.exec(unquote(raw));
  if (ref) {
    let hex: string | undefined = colors[ref[1]] ?? skins[""]?.[ref[1]];
    if (!hex && ref[1].includes(".")) {
      const dot = ref[1].indexOf(".");
      hex = skins[ref[1].slice(0, dot)]?.[ref[1].slice(dot + 1)];
    }
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
  const skins = parseColors(yaml);
  const skinNames = Object.keys(skins);
  if (skinNames.length === 0) {
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

  for (const skinName of skinNames) {
    const colors = skins[skinName];
    const label = (token: string) =>
      skinName ? `colors.${skinName}.${token}` : `colors.${token}`;

    const checkTokenPair = (baseKey: string, fgKey: string) => {
      const bg = parseHex(colors[baseKey]);
      const fg = parseHex(colors[fgKey]);
      if (!bg || !fg) {
        findings.push({
          status: "SKIP",
          ratio: null,
          pair: `${label(fgKey)} on ${label(baseKey)}`,
          note: "unparseable hex value",
        });
        return;
      }
      check(bg, fg, `${label(fgKey)} on ${label(baseKey)}`);
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
  }

  // Component references carry no skin name, so each pair resolves and
  // checks once per skin that can resolve it; a single SKIP surfaces
  // only when no skin resolves the pair.
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
    let resolvedAny = false;
    for (const skinName of skinNames) {
      const colors = skins[skinName];
      const bg = resolveColor(bgRaw, colors, skins);
      const fg = resolveColor(fgRaw, colors, skins);
      if (!bg || !fg) continue;
      resolvedAny = true;
      // A translucent background composites over the page; approximate the
      // page with colors.background, falling back to opaque white.
      const page = parseHex(
        colors.background ?? skins[""]?.background ?? "#FFFFFF",
      ) ?? { r: 255, g: 255, b: 255 };
      const bgRgb = bg.alpha < 1 ? blend(bg.rgb, page, bg.alpha) : bg.rgb;
      const fgRgb = fg.alpha < 1 ? blend(fg.rgb, bgRgb, fg.alpha) : fg.rgb;
      const suffix = skinName ? ` [${skinName}]` : "";
      check(
        bgRgb,
        fgRgb,
        `components.${name} textColor on backgroundColor${suffix}`,
      );
    }
    if (!resolvedAny) {
      findings.push({
        status: "SKIP",
        ratio: null,
        pair: `components.${name}`,
        note: "color did not resolve to a hex value",
      });
    }
  }

  const fails = findings.filter((f) => f.status === "FAIL").length;
  const skips = findings.filter((f) => f.status === "SKIP").length;
  if (asJson) {
    console.log(JSON.stringify(findings, null, 2));
  } else {
    for (const f of findings) {
      const ratio = f.ratio === null ? "  --  " : formatRatio(f.ratio).padStart(7);
      console.log(`${f.status.padEnd(4)} ${ratio}  ${f.pair}${f.note ? ` (${f.note})` : ""}`);
    }
    console.log(`\n${findings.length} pairs checked, ${fails} failing, ${skips} skipped`);
  }
  // An all-SKIP run verified nothing; never let it read as a pass.
  if (findings.length > 0 && skips === findings.length) {
    console.error(
      "Every pair was skipped — nothing verified. Check the color token shapes.",
    );
    process.exit(2);
  }
  process.exit(fails > 0 ? 1 : 0);
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
