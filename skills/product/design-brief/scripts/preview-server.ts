#!/usr/bin/env bun
/**
 * Preview server for design-brief skill.
 * Serves the styleguide and records user interactions.
 *
 * Security: local-only server (127.0.0.1), read-only filesystem access
 * scoped to the served root, append-only event recording.
 *
 * Usage:
 *   bun run scripts/preview-server.ts --root docs/design
 *   bun run scripts/preview-server.ts --root docs/design --session .artifacts/design/preview
 *   bun run scripts/preview-server.ts --root .artifacts/design/preview --port 8080
 *
 * --root    directory served and watched (default docs/design) — the committed
 *           styleguide, or a tuner variant directory under .artifacts.
 * --session directory holding the .events log (default .artifacts/design/preview),
 *           kept out of the served root so events never land in committed docs.
 *
 * The server:
 * - Serves HTML files from the served root only
 * - Records user events to .events (JSON lines, append-only) in the session dir
 * - Injects client interaction + live-reload scripts into served HTML
 * - Live-reloads connected browsers on root changes via SSE
 *   (`/__reload` endpoint, debounced 100ms, ignores hidden files)
 *
 * Event types (one JSON per line in .events):
 *   tune:     { type: "tune",    token: "colors.primary", value: "#3b82f6", timestamp }
 *   comment:  { type: "comment", selector: ".card.primary", text: "too tight", timestamp }
 *
 * Client interactions:
 *   - A color tuner row (`data-tune-row`) wires OKLCH sliders (`data-oklch`)
 *     and an optional hex input (`data-hex`): editing swaps the row's
 *     `--color-*` custom property live, recomputes the paired WCAG contrast,
 *     and records a tune event keyed by the row's token path
 *   - Alt+click any element to open a comment overlay; submit to record a
 *     comment event with the element's CSS selector
 */

import { serve, type Server } from "bun";
import { readdir, readFile, appendFile, mkdir } from "node:fs/promises";
import { join, resolve, relative } from "node:path";
import { existsSync, watch } from "node:fs";

const args: string[] = process.argv.slice(2);
const rootIdx: number = args.indexOf("--root");
const sessionIdx: number = args.indexOf("--session");
const portIdx: number = args.indexOf("--port");
const rootDir: string =
  rootIdx !== -1 ? resolve(args[rootIdx + 1]) : resolve("docs/design");
const sessionDir: string =
  sessionIdx !== -1
    ? resolve(args[sessionIdx + 1])
    : resolve(".artifacts/design/preview");
const port: number = parseInt(portIdx !== -1 ? args[portIdx + 1] : "3456", 10);

if (!Number.isInteger(port) || port < 1024 || port > 65535) {
  console.error(`Invalid --port value: must be an integer between 1024 and 65535 (got: ${args[portIdx + 1]})`);
  process.exit(1);
}

if (!existsSync(rootDir)) {
  await mkdir(rootDir, { recursive: true });
}
if (!existsSync(sessionDir)) {
  await mkdir(sessionDir, { recursive: true });
}

const eventsFile: string = join(sessionDir, ".events");

function isInsideRoot(filePath: string): boolean {
  const rel = relative(rootDir, filePath);
  return !rel.startsWith("..") && !rel.startsWith("/");
}

const reloadClients: Set<ReadableStreamDefaultController<Uint8Array>> = new Set();
const sseEncoder = new TextEncoder();
// 100ms coalesces bursts (multi-file writes, editor save passes) into one reload
let reloadTimer: ReturnType<typeof setTimeout> | null = null;

function broadcastReload(): void {
  for (const controller of reloadClients) {
    try {
      controller.enqueue(sseEncoder.encode("data: reload\n\n"));
    } catch {
      reloadClients.delete(controller);
    }
  }
}

watch(rootDir, { recursive: true }, (_event, filename) => {
  if (!filename) return;
  const name = filename.toString();
  // Skip hidden files to avoid reload loops
  if (name.split("/").pop()?.startsWith(".")) return;
  if (reloadTimer) clearTimeout(reloadTimer);
  reloadTimer = setTimeout(broadcastReload, 100);
});

const reloadScript = `
try {
  const __es = new EventSource("/__reload");
  __es.onmessage = (e) => { if (e.data === "reload") location.reload(); };
} catch {}
`;

// Color math (OKLCH <-> sRGB) per Bjorn Ottosson's OKLab spec
// (https://bottosson.github.io/posts/oklab/) plus WCAG relative luminance.
// Shipped to the browser so the color tuner resolves slider values to hex,
// swaps the CSS custom property live, and recomputes contrast as you drag.
const colorScript = `
function __srgbToLinear(c){ return c <= 0.04045 ? c/12.92 : Math.pow((c+0.055)/1.055, 2.4); }
function __linearToSrgb(c){ return c <= 0.0031308 ? 12.92*c : 1.055*Math.pow(c, 1/2.4) - 0.055; }
function __clamp01(x){ return Math.min(1, Math.max(0, x)); }
function __oklchToRgb(L, C, H){
  var hr = H * Math.PI / 180;
  var a = C * Math.cos(hr), b = C * Math.sin(hr);
  var l_ = L + 0.3963377774*a + 0.2158037573*b;
  var m_ = L - 0.1055613458*a - 0.0638541728*b;
  var s_ = L - 0.0894841775*a - 1.2914855480*b;
  var l = l_*l_*l_, m = m_*m_*m_, s = s_*s_*s_;
  var r = 4.0767416621*l - 3.3077115913*m + 0.2309699292*s;
  var g = -1.2684380046*l + 2.6097574011*m - 0.3413193965*s;
  var bl = -0.0041960863*l - 0.7034186147*m + 1.7076147010*s;
  // clamp to sRGB gamut after gamma encoding
  r = Math.round(__clamp01(__linearToSrgb(r))*255);
  g = Math.round(__clamp01(__linearToSrgb(g))*255);
  bl = Math.round(__clamp01(__linearToSrgb(bl))*255);
  return { r: r, g: g, b: bl };
}
function __rgbToOklch(r, g, b){
  var lr = __srgbToLinear(r/255), lg = __srgbToLinear(g/255), lb = __srgbToLinear(b/255);
  var l = Math.cbrt(0.4122214708*lr + 0.5363325363*lg + 0.0514459929*lb);
  var m = Math.cbrt(0.2119034982*lr + 0.6806995451*lg + 0.1073969566*lb);
  var s = Math.cbrt(0.0883024619*lr + 0.2817188376*lg + 0.6299787005*lb);
  var L = 0.2104542553*l + 0.7936177850*m - 0.0040720468*s;
  var a = 1.9779984951*l - 2.4285922050*m + 0.4505937099*s;
  var bb = 0.0259040371*l + 0.7827717662*m - 0.8086757660*s;
  var C = Math.sqrt(a*a + bb*bb);
  var H = Math.atan2(bb, a) * 180 / Math.PI;
  if (H < 0) H += 360;
  return { L: L, C: C, H: H };
}
function __hexToRgb(hex){
  hex = hex.replace('#','');
  if (hex.length === 3) hex = hex.split('').map(function(c){return c+c;}).join('');
  return { r: parseInt(hex.slice(0,2),16), g: parseInt(hex.slice(2,4),16), b: parseInt(hex.slice(4,6),16) };
}
function __rgbToHex(c){
  return '#' + [c.r,c.g,c.b].map(function(x){ return x.toString(16).padStart(2,'0'); }).join('');
}
// WCAG 2.x relative luminance + contrast ratio; thresholds 4.5 = AA, 7 = AAA.
function __relLum(c){
  var a = [c.r,c.g,c.b].map(function(v){ v/=255; return v<=0.03928 ? v/12.92 : Math.pow((v+0.055)/1.055,2.4); });
  return 0.2126*a[0]+0.7152*a[1]+0.0722*a[2];
}
function __contrast(c1, c2){
  var l1 = __relLum(c1), l2 = __relLum(c2);
  var hi = Math.max(l1,l2), lo = Math.min(l1,l2);
  return (hi+0.05)/(lo+0.05);
}
function __wcagLevel(ratio){ return ratio>=7 ? 'AAA' : ratio>=4.5 ? 'AA' : 'fail'; }
// Resolve any CSS color (hex, oklch, named) to rgb via a hidden probe — the
// browser does the conversion, so the tuner never parses oklch by hand.
// Passing a skin sets data-skin on the probe so [data-skin] override rules
// apply and the var resolves to that skin's value.
var __probe = null;
function __resolveVarRgb(varName, skin){
  if (!__probe){ __probe = document.createElement('span'); __probe.style.display='none'; document.body.appendChild(__probe); }
  if (skin) __probe.setAttribute('data-skin', skin); else __probe.removeAttribute('data-skin');
  __probe.style.color = 'var(' + varName + ')';
  var m = getComputedStyle(__probe).color.match(/\\d+/g);
  return m ? { r:+m[0], g:+m[1], b:+m[2] } : null;
}
// A skinned token path (colors.<skin>.<token>) names the override skin its
// value belongs to; a flat path returns "".
function __rowSkin(row){
  var parts = (row.dataset.token || '').split('.');
  return parts.length === 3 ? parts[1] : '';
}
// Apply a tuned value in the right scope. Flat tokens go inline on the root
// element; the styleguide's [data-skin] blocks still win inside a switched
// skin, mirroring the frontmatter's inheritance. Skinned tokens rebuild a
// last-position style element whose [data-skin] rules out-cascade the
// styleguide's own skin block (same specificity, later in document order)
// without touching the root values.
var __skinTunes = {};
function __applyVar(skin, varName, hex){
  if (!skin){ document.documentElement.style.setProperty(varName, hex); return; }
  (__skinTunes[skin] = __skinTunes[skin] || {})[varName] = hex;
  var el = document.getElementById('__tune-skin-overrides');
  if (!el){ el = document.createElement('style'); el.id = '__tune-skin-overrides'; document.head.appendChild(el); }
  var css = '';
  Object.keys(__skinTunes).forEach(function(s){
    css += '[data-skin="' + s + '"]{';
    Object.keys(__skinTunes[s]).forEach(function(v){ css += v + ':' + __skinTunes[s][v] + ';'; });
    css += '}';
  });
  el.textContent = css;
}
function __applyColorTune(row, target){
  var varName = row.dataset.var;
  var rgb;
  if (target.matches('[data-hex]')) {
    var hv = target.value.trim();
    if (!/^#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})$/.test(hv)) return null;
    rgb = __hexToRgb(hv);
    var o = __rgbToOklch(rgb.r, rgb.g, rgb.b);
    var ls = row.querySelector('[data-oklch="l"]'), cs = row.querySelector('[data-oklch="c"]'), hs = row.querySelector('[data-oklch="h"]');
    if (ls) ls.value = o.L; if (cs) cs.value = o.C; if (hs) hs.value = o.H;
  } else {
    var L = parseFloat(row.querySelector('[data-oklch="l"]').value);
    var C = parseFloat(row.querySelector('[data-oklch="c"]').value);
    var H = parseFloat(row.querySelector('[data-oklch="h"]').value);
    rgb = __oklchToRgb(L, C, H);
    var picker = row.querySelector('[data-hex]');
    if (picker) picker.value = __rgbToHex(rgb);
  }
  var hex = __rgbToHex(rgb);
  var skin = __rowSkin(row);
  __applyVar(skin, varName, hex);
  var hexEl = row.querySelector('[data-hex-new]');
  if (hexEl) hexEl.textContent = hex;
  var pairVar = row.dataset.pairVar;
  if (pairVar) {
    var pair = __resolveVarRgb(pairVar, skin);
    if (pair) {
      var ratio = __contrast(rgb, pair), lvl = __wcagLevel(ratio);
      var ratioEl = row.querySelector('[data-ratio-new]');
      var badge = row.querySelector('[data-badge-new]');
      if (ratioEl) ratioEl.textContent = ratio.toFixed(2) + ':1';
      if (badge) { badge.textContent = lvl; badge.dataset.level = lvl; }
    }
  }
  return hex;
}
// Compute Current and New contrast from the row's original hex on load, so
// displayed ratios are always engine-derived — never hand-entered (and wrong).
function __initRow(row){
  var orig = row.dataset.original ? __hexToRgb(row.dataset.original) : null;
  if (!orig) return;
  var skin = __rowSkin(row);
  // Assert the original only for flat tokens — an inline root assertion of a
  // skinned original would bleed the skin's value into the default scope.
  if (!skin) document.documentElement.style.setProperty(row.dataset.var, row.dataset.original);
  var hexEl = row.querySelector('[data-hex-new]');
  if (hexEl) hexEl.textContent = row.dataset.original;
  var pairVar = row.dataset.pairVar;
  if (!pairVar) return;
  var pair = __resolveVarRgb(pairVar, skin);
  if (!pair) return;
  var ratio = __contrast(orig, pair), lvl = __wcagLevel(ratio);
  ['[data-ratio-current]','[data-ratio-new]'].forEach(function(s){ var el = row.querySelector(s); if (el) el.textContent = ratio.toFixed(2) + ':1'; });
  ['[data-badge-current]','[data-badge-new]'].forEach(function(s){ var el = row.querySelector(s); if (el) { el.textContent = lvl; el.dataset.level = lvl; } });
}
`;

const clientScript = `
document.addEventListener("input", async (e) => {
  const row = e.target.closest("[data-tune-row]");
  if (row) {
    const hex = __applyColorTune(row, e.target);
    if (hex) await fetch("/event", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type: "tune", token: row.dataset.token, value: hex, timestamp: new Date().toISOString() }),
    });
    return;
  }
  const control = e.target.closest("[data-tune]");
  if (!control) return;
  const token = control.dataset.tune;
  const value = control.value;
  document.documentElement.style.setProperty(token, value);
  const label = control.parentElement?.querySelector("[data-tune-value]");
  if (label) label.textContent = value;
  await fetch("/event", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ type: "tune", token, value, timestamp: new Date().toISOString() }),
  });
});

document.addEventListener("click", async (e) => {
  const resetBtn = e.target.closest("[data-reset]");
  if (!resetBtn) return;
  e.preventDefault();
  const row = resetBtn.closest("[data-tune-row]");
  const slider = resetBtn.parentElement?.querySelector('input[type="range"]');
  if (!row || !slider) return;
  slider.value = slider.getAttribute("value");
  const hex = __applyColorTune(row, slider);
  if (hex) await fetch("/event", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ type: "tune", token: row.dataset.token, value: hex, timestamp: new Date().toISOString() }),
  });
});

function cssPath(el) {
  if (!(el instanceof Element)) return "";
  const parts = [];
  while (el && el.nodeType === 1 && el !== document.body) {
    let part = el.nodeName.toLowerCase();
    if (el.id) { part += "#" + el.id; parts.unshift(part); break; }
    const classes = Array.from(el.classList).slice(0, 2).join(".");
    if (classes) part += "." + classes;
    const parent = el.parentElement;
    if (parent) {
      const siblings = Array.from(parent.children).filter((c) => c.nodeName === el.nodeName);
      if (siblings.length > 1) part += ":nth-of-type(" + (siblings.indexOf(el) + 1) + ")";
    }
    parts.unshift(part);
    el = el.parentElement;
  }
  return parts.join(" > ");
}

let overlay = null;
function openCommentOverlay(target) {
  if (overlay) overlay.remove();
  overlay = document.createElement("div");
  overlay.style.cssText = "position:fixed;top:1rem;right:1rem;z-index:99999;background:#111;color:#fff;padding:1rem;border-radius:8px;box-shadow:0 8px 32px rgba(0,0,0,0.4);width:320px;font-family:system-ui,sans-serif;font-size:14px;";
  const selector = cssPath(target);
  overlay.innerHTML = "<div style='margin-bottom:.5rem;opacity:.7;font-size:12px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;'>" + selector + "</div><textarea placeholder='Comment...' style='width:100%;min-height:80px;background:#222;color:#fff;border:1px solid #333;border-radius:4px;padding:.5rem;font:inherit;resize:vertical;'></textarea><div style='margin-top:.5rem;display:flex;gap:.5rem;justify-content:flex-end;'><button data-cancel style='background:transparent;color:#aaa;border:1px solid #333;padding:.25rem .75rem;border-radius:4px;cursor:pointer;'>Cancel</button><button data-submit style='background:#3b82f6;color:#fff;border:0;padding:.25rem .75rem;border-radius:4px;cursor:pointer;'>Submit</button></div>";
  document.body.appendChild(overlay);
  const ta = overlay.querySelector("textarea");
  ta.focus();
  overlay.querySelector("[data-cancel]").addEventListener("click", () => { overlay.remove(); overlay = null; });
  overlay.querySelector("[data-submit]").addEventListener("click", async () => {
    const text = ta.value.trim();
    if (!text) return;
    await fetch("/event", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ type: "comment", selector, text, timestamp: new Date().toISOString() }),
    });
    overlay.remove();
    overlay = null;
  });
}

document.addEventListener("click", (e) => {
  if (!e.altKey) return;
  if (e.target.closest("[data-tune], [data-tune-row]")) return;
  e.preventDefault();
  e.stopPropagation();
  openCommentOverlay(e.target);
}, true);

document.querySelectorAll("[data-tune-row]").forEach(__initRow);
`;

// Builds the color tuner as an overlay over the served styleguide — no separate
// file. Scans color swatches marked data-tune-swatch (carrying token/var/pair/
// original) and creates one OKLCH row each, wired to the engine above. Tuning a
// var cascades to every specimen on the page. A live "Aa" sample renders the
// color on its actual pairing so the contrast target is visible, not just named.
const tunerScript = `
function __mkTunerRow(sw){
  var token = sw.dataset.token, v = sw.dataset.var, pair = sw.dataset.pair || "", orig = sw.dataset.original;
  var c = __hexToRgb(orig), o = __rgbToOklch(c.r, c.g, c.b);
  var fill = pair.indexOf("-foreground") > -1;
  var sBg = fill ? "var(" + v + ")" : "var(" + pair + ")";
  var sFg = fill ? "var(" + pair + ")" : "var(" + v + ")";
  var pairLabel = pair ? pair.replace(/^--color-/, "") : "—";
  var row = document.createElement("div");
  row.className = "__trow";
  row.setAttribute("data-tune-row", "");
  row.dataset.token = token; row.dataset.var = v; row.dataset.pairVar = pair; row.dataset.original = orig;
  // A skinned row carries its skin attribute so [data-skin] override rules
  // apply inside the row — its var() chips and Aa sample render the skin's
  // values regardless of which skin the sheet is switched to.
  var skinSeg = token.split(".").length === 3 ? token.split(".")[1] : "";
  if (skinSeg) row.setAttribute("data-skin", skinSeg);
  row.innerHTML =
    "<div class='__thead'><span class='__tname'>" + token.replace(/^colors\\./, "") + "</span><span class='__tpair'>vs " + pairLabel + "</span></div>" +
    "<div class='__tsw'>" +
      "<div class='__tcell'><span class='__tchip' style='background:" + orig + "'></span><span class='__tlab'>current<br><b data-ratio-current></b> <span class='__tbadge' data-badge-current></span></span></div>" +
      "<div class='__tcell'><span class='__tchip' style='background:var(" + v + ")'></span><span class='__tlab'>new <span data-hex-new></span><br><b data-ratio-new></b> <span class='__tbadge' data-badge-new></span></span></div>" +
      "<span class='__tsample' title='contrast vs " + pairLabel + "' style='background:" + sBg + ";color:" + sFg + "'>Aa</span>" +
    "</div>" +
    "<label>L<input type='range' data-oklch='l' min='0' max='1' step='0.001' value='" + o.L.toFixed(4) + "'><button data-reset>&#8635;</button></label>" +
    "<label>C<input type='range' data-oklch='c' min='0' max='0.4' step='0.001' value='" + o.C.toFixed(4) + "'><button data-reset>&#8635;</button></label>" +
    "<label>H<input type='range' data-oklch='h' min='0' max='360' step='0.1' value='" + o.H.toFixed(2) + "'><button data-reset>&#8635;</button></label>" +
    "<input type='text' data-hex value='" + orig + "' spellcheck='false'>";
  return row;
}
function __buildTuner(){
  var sws = document.querySelectorAll("[data-tune-swatch]");
  if (!sws.length) return null;
  var panel = document.createElement("aside");
  panel.id = "__tuner";
  var head = document.createElement("div");
  head.className = "__tphead";
  head.innerHTML = "<span>Color Tuner</span><button id='__tunerClose' title='close'>&times;</button>";
  panel.appendChild(head);
  sws.forEach(function(sw){ var r = __mkTunerRow(sw); panel.appendChild(r); __initRow(r); });
  var commit = document.createElement("button");
  commit.id = "__tunerCommit"; commit.textContent = "Commit to DESIGN.md";
  commit.addEventListener("click", function(){
    fetch("/event", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ type: "commit", timestamp: new Date().toISOString() }) });
    commit.textContent = "Committed — apply from chat";
    commit.disabled = true;
  });
  panel.appendChild(commit);
  return panel;
}
function __injectTunerStyles(){
  if (document.getElementById("__tuner-css")) return;
  var s = document.createElement("style");
  s.id = "__tuner-css";
  s.textContent =
    "#__tunerBtn{position:fixed;top:16px;right:16px;z-index:99998;background:#111;color:#fff;border:0;border-radius:8px;padding:10px 14px;font:600 13px system-ui;cursor:pointer;box-shadow:0 4px 16px rgba(0,0,0,.3);}" +
    "#__tuner{position:fixed;top:0;right:0;height:100vh;width:340px;overflow:auto;z-index:99997;background:#fff;border-left:1px solid #e7e5e4;padding:16px;display:flex;flex-direction:column;gap:14px;font-family:system-ui,sans-serif;box-shadow:-8px 0 24px rgba(0,0,0,.12);}" +
    "#__tuner .__tphead{display:flex;justify-content:space-between;align-items:center;font:600 12px ui-monospace,monospace;text-transform:uppercase;letter-spacing:.08em;color:#78716c;}" +
    "#__tunerClose{border:0;background:none;color:#78716c;font-size:20px;line-height:1;cursor:pointer;padding:0 4px;}" +
    "#__tunerCommit{margin-top:4px;border:0;border-radius:6px;background:#111;color:#fff;padding:10px;font:600 13px system-ui;cursor:pointer;}#__tunerCommit:disabled{background:#16a34a;cursor:default;}" +
    ".__trow{border:1px solid #e7e5e4;border-radius:6px;padding:12px;display:flex;flex-direction:column;gap:10px;}" +
    ".__thead{display:flex;justify-content:space-between;align-items:baseline;}" +
    ".__tname{font:600 13px ui-monospace,monospace;}.__tpair{font:11px ui-monospace,monospace;color:#78716c;}" +
    ".__tsw{display:flex;gap:10px;align-items:center;}.__tcell{flex:1;display:flex;gap:8px;align-items:center;min-width:0;}" +
    ".__tchip{width:44px;height:44px;border-radius:6px;border:1px solid #e7e5e4;flex-shrink:0;}" +
    ".__tlab{font:11px ui-monospace,monospace;color:#78716c;line-height:1.35;}" +
    ".__tsample{width:44px;height:44px;border-radius:6px;border:1px solid #e7e5e4;display:flex;align-items:center;justify-content:center;font:700 16px system-ui;flex-shrink:0;}" +
    "#__tuner label{display:grid;grid-template-columns:14px 1fr auto;gap:8px;align-items:center;font:11px ui-monospace,monospace;color:#78716c;}" +
    "#__tuner input[type=range]{-webkit-appearance:none;appearance:none;width:100%;height:4px;border-radius:2px;background:#e7e5e4;outline:none;}" +
    "#__tuner input[type=range]::-webkit-slider-thumb{-webkit-appearance:none;appearance:none;width:14px;height:14px;border-radius:50%;background:#6366f1;cursor:pointer;}" +
    "#__tuner input[type=range]::-moz-range-thumb{width:14px;height:14px;border:0;border-radius:50%;background:#6366f1;cursor:pointer;}" +
    "#__tuner input[type=text]{font:12px ui-monospace,monospace;padding:4px 6px;border:1px solid #e7e5e4;border-radius:4px;}" +
    "#__tuner label button{border:1px solid #e7e5e4;background:#fff;color:#78716c;border-radius:4px;width:22px;height:22px;font-size:12px;line-height:1;cursor:pointer;}" +
    ".__tbadge{display:inline-block;padding:1px 6px;border-radius:3px;font:600 10px ui-monospace,monospace;}" +
    ".__tbadge[data-level=AAA]{background:#bbf7d0;color:#14532d;}.__tbadge[data-level=AA]{background:#dcfce7;color:#166534;}.__tbadge[data-level=fail]{background:#fee2e2;color:#991b1b;}";
  document.head.appendChild(s);
}
(function(){
  if (!document.querySelector("[data-tune-swatch]")) return;
  __injectTunerStyles();
  var btn = document.createElement("button");
  btn.id = "__tunerBtn"; btn.textContent = "Tune colors";
  var panel = null;
  function __closeTuner(){ if (panel) panel.style.display = "none"; btn.style.display = "block"; }
  btn.addEventListener("click", function(){
    if (!panel) {
      panel = __buildTuner();
      if (panel) { document.body.appendChild(panel); var x = panel.querySelector("#__tunerClose"); if (x) x.addEventListener("click", __closeTuner); }
    }
    if (panel) panel.style.display = "flex";
    btn.style.display = "none";
  });
  document.body.appendChild(btn);
  if (location.search.indexOf("tune") > -1) btn.click();
})();
`;

function injectClientScripts(html: string): string {
  const tag = `<script>${colorScript}</script><script>${clientScript}</script><script>${tunerScript}</script><script>${reloadScript}</script>`;
  if (html.includes("</body>")) return html.replace("</body>", `${tag}</body>`);
  return html + tag;
}

const frameTemplate = (
  content: string,
  title: string,
): string => `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>${title}</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: system-ui, -apple-system, sans-serif; background: #fafafa; padding: 2rem; }
    .hint { position: fixed; bottom: 1rem; left: 1rem; background: #111; color: #fff; padding: 0.5rem 0.75rem; border-radius: 6px; font: 12px system-ui; opacity: 0.6; pointer-events: none; }
  </style>
  <script>${colorScript}</script>
  <script>${clientScript}</script>
  <script>${tunerScript}</script>
  <script>${reloadScript}</script>
</head>
<body>${content}<div class="hint">Alt+click to comment</div></body>
</html>`;

const contentTypes: Record<string, string> = {
  html: "text/html",
  css: "text/css",
  js: "application/javascript",
  json: "application/json",
  png: "image/png",
  jpg: "image/jpeg",
  svg: "image/svg+xml",
};

const server: Server = serve({
  port,
  hostname: "127.0.0.1",
  async fetch(req: Request): Promise<Response> {
    const url = new URL(req.url);

    if (url.pathname === "/event" && req.method === "POST") {
      const event = await req.json();
      await appendFile(eventsFile, JSON.stringify(event) + "\n");
      return new Response("ok");
    }

    if (url.pathname === "/__reload") {
      const stream = new ReadableStream<Uint8Array>({
        start(controller) {
          reloadClients.add(controller);
          controller.enqueue(sseEncoder.encode(": connected\n\n"));
          req.signal.addEventListener("abort", () => {
            reloadClients.delete(controller);
            try { controller.close(); } catch {}
          });
        },
      });
      return new Response(stream, {
        headers: {
          "Content-Type": "text/event-stream",
          "Cache-Control": "no-cache",
          Connection: "keep-alive",
        },
      });
    }

    const filePath: string = join(
      rootDir,
      url.pathname === "/" ? "styleguide.html" : url.pathname,
    );

    if (!isInsideRoot(filePath)) {
      return new Response("Forbidden", { status: 403 });
    }

    if (existsSync(filePath)) {
      const content: string = await readFile(filePath, "utf-8");

      if (
        filePath.endsWith(".html") &&
        !content.trimStart().startsWith("<!DOCTYPE") &&
        !content.trimStart().startsWith("<!doctype")
      ) {
        const title: string =
          filePath.split("/").pop()?.replace(".html", "") || "Preview";
        return new Response(frameTemplate(content, title), {
          headers: { "Content-Type": "text/html" },
        });
      }

      if (filePath.endsWith(".html")) {
        return new Response(injectClientScripts(content), {
          headers: { "Content-Type": "text/html" },
        });
      }

      const ext: string = filePath.split(".").pop() || "";
      return new Response(content, {
        headers: { "Content-Type": contentTypes[ext] || "text/plain" },
      });
    }

    if (url.pathname === "/") {
      const files: string[] = await readdir(rootDir);
      const htmlFiles: string[] = files.filter((f: string) =>
        f.endsWith(".html"),
      );
      const list: string = htmlFiles
        .map((f: string) => `<li><a href="/${f}">${f}</a></li>`)
        .join("\n");
      return new Response(
        frameTemplate(`<h1>Preview</h1><ul>${list}</ul>`, "Preview"),
        { headers: { "Content-Type": "text/html" } },
      );
    }

    return new Response("Not found", { status: 404 });
  },
});

console.log(`Preview server running at http://localhost:${server.port}`);
console.log(`Served root:    ${rootDir}`);
console.log(`Events file:    ${eventsFile}`);
console.log(`Live-reload: watching ${rootDir} (SSE at /__reload)`);
