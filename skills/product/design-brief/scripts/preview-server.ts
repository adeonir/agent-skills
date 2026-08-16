#!/usr/bin/env bun
/**
 * Preview server for the design-brief skill.
 * Serves transient document and styleguide views, and records one feedback
 * batch across both views.
 *
 * Security: local-only server (127.0.0.1), read-only filesystem access
 * scoped to session directory, append-only event recording.
 *
 * Usage:
 *   bun run scripts/preview-server.ts --session .artifacts/design/preview
 *   bun run scripts/preview-server.ts --session .artifacts/design/preview --port 8080
 *
 * The server:
 * - Serves design.html at /design and styleguide.html at /styleguide
 * - Serves a shell at "/" with tabs, section navigation, an inspector, and a
 *   comment mode that queues comments across views
 * - Records user events to .events file (JSON lines, append-only)
 * - Injects the interaction client into every served file, whether the file
 *   is a full document or a fragment
 * - Live-reloads connected browsers on session-directory changes via SSE
 *   (`/__reload` endpoint, debounced 100ms, ignores .events and hidden files)
 *
 * Event type (one JSON line per sent round):
 *   feedback: { type: "feedback", comments: [{ view, selector, text }],
 *               adjustments: [{ view, token, old, new }], timestamp }
 *
 * Client interactions:
 *   - Switch views or sections without losing the feedback queue
 *   - Turn Comment on, select an element, queue a comment, and send the batch
 *   - Tune color swatches temporarily in the inspector; Send records the delta
 *   - With Comment off the served file behaves normally: no click is intercepted
 */

import { serve, type Server } from "bun";
import { readdir, readFile, appendFile, mkdir } from "node:fs/promises";
import { join, resolve, relative } from "node:path";
import { existsSync, watch } from "node:fs";

const args: string[] = process.argv.slice(2);
const sessionIdx: number = args.indexOf("--session");
const portIdx: number = args.indexOf("--port");
const viewportIdx: number = args.indexOf("--viewport");

if (sessionIdx === -1 || !args[sessionIdx + 1]) {
  console.error("Missing --session: pass the transient preview directory, e.g. --session .artifacts/design/preview");
  process.exit(1);
}

const sessionDir: string = resolve(args[sessionIdx + 1]);
// 3456: arbitrary high port outside the common dev range (3000/5173/8080) to
// avoid colliding with the project's own dev server; override with --port
const port: number = parseInt(portIdx !== -1 ? args[portIdx + 1] : "3456", 10);

if (!Number.isInteger(port) || port < 1024 || port > 65535) {
  console.error(`Invalid --port value: must be an integer between 1024 and 65535 (got: ${args[portIdx + 1]})`);
  process.exit(1);
}

// 375 / 768 / 1440: the widths the gallery switches between, named by the device
// class each one stands for; --viewport takes the name, and desktop is the default
const VIEWPORTS: Record<string, number> = { mobile: 375, tablet: 768, desktop: 1440 };
const viewportName: string = viewportIdx !== -1 ? args[viewportIdx + 1] : "desktop";

if (!(viewportName in VIEWPORTS)) {
  console.error(`Invalid --viewport value: must be one of ${Object.keys(VIEWPORTS).join(", ")} (got: ${args[viewportIdx + 1]})`);
  process.exit(1);
}

const viewport: number = VIEWPORTS[viewportName];
const SECTIONS: string[] = [
  "overview",
  "colors",
  "typography",
  "layout",
  "elevation-depth",
  "shapes",
  "components",
  "motion-interaction",
  "responsive-behavior",
  "dos-donts",
  "agent-prompt-guide",
];

if (!existsSync(sessionDir)) {
  await mkdir(sessionDir, { recursive: true });
}

const eventsFile: string = join(sessionDir, ".events");

function isInsideSessionDir(filePath: string): boolean {
  const rel = relative(sessionDir, filePath);
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

watch(sessionDir, { recursive: true }, (_event, filename) => {
  if (!filename) return;
  const name = filename.toString();
  // Skip the event log (server writes on every interaction) and hidden files to avoid reload loops
  if (name === ".events" || name.split("/").pop()?.startsWith(".")) return;
  if (reloadTimer) clearTimeout(reloadTimer);
  reloadTimer = setTimeout(broadcastReload, 100);
});

const reloadScript = `
try {
  const __es = new EventSource("/__reload");
  __es.onmessage = (e) => { if (e.data === "reload") location.reload(); };
} catch {}
`;

// Runs inside every served file. It owns nothing: comment mode is switched on
// from the gallery, and a click only reports the element back up to it.
const clientScript = `
function cssPath(el) {
  if (!(el instanceof Element)) return "";
  const parts = [];
  while (el && el.nodeType === 1 && el !== document.body) {
    let part = el.nodeName.toLowerCase();
    if (el.id) { part += "#" + el.id; parts.unshift(part); break; }
    // 2: enough class tokens to disambiguate siblings without pinning the
    // selector to a long utility-class string that any restyle would break
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

let commentMode = false;

function resolvedRgb(variable) {
  const probe = document.createElement("span");
  probe.style.color = "var(" + variable + ")";
  probe.style.display = "none";
  document.body.appendChild(probe);
  const channels = getComputedStyle(probe).color.match(/[\d.]+/g);
  probe.remove();
  return channels ? channels.slice(0, 3).map(Number) : null;
}

function contrastRatio(first, second) {
  const luminance = (channels) => {
    const linear = channels.map((channel) => {
      const value = channel / 255;
      return value <= 0.04045 ? value / 12.92 : Math.pow((value + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * linear[0] + 0.7152 * linear[1] + 0.0722 * linear[2];
  };
  const firstLuminance = luminance(first);
  const secondLuminance = luminance(second);
  return (Math.max(firstLuminance, secondLuminance) + 0.05) / (Math.min(firstLuminance, secondLuminance) + 0.05);
}

window.addEventListener("message", (e) => {
  if (e.source !== window.parent || !e.data) return;
  if (e.data.designbrief === "mode") {
    commentMode = !!e.data.on;
    document.documentElement.style.cursor = commentMode ? "crosshair" : "";
  }
  if (e.data.designbrief === "navigate") {
    const target = document.getElementById(e.data.section);
    if (target) target.scrollIntoView({ behavior: "smooth", block: "start" });
  }
  if (e.data.designbrief === "tune") {
    document.documentElement.style.setProperty(e.data.variable, e.data.value);
    const swatch = Array.from(document.querySelectorAll("[data-tune-swatch]")).find((element) => element.dataset.var === e.data.variable);
    if (swatch && swatch.dataset.pair) {
      const first = resolvedRgb(e.data.variable);
      const second = resolvedRgb(swatch.dataset.pair);
      if (first && second) {
        window.parent.postMessage({ designbrief: "contrast", token: swatch.dataset.token, ratio: contrastRatio(first, second) }, location.origin);
      }
    }
  }
});

document.addEventListener("click", (e) => {
  // Standalone (not framed): nothing to report to, so the page behaves normally
  if (window.parent === window || !commentMode) return;
  e.preventDefault();
  e.stopPropagation();
  window.parent.postMessage({ designbrief: "target", selector: cssPath(e.target) }, location.origin);
}, true);

if (window.parent !== window) {
  const swatches = Array.from(document.querySelectorAll("[data-tune-swatch]")).map((element) => ({
    token: element.dataset.token,
    variable: element.dataset.var,
    pair: element.dataset.pair || "",
    original: element.dataset.original,
  })).filter((item) => item.token && item.variable && item.original);
  window.parent.postMessage({ designbrief: "ready", swatches }, location.origin);
}
`;

function injectClientScripts(html: string): string {
  const tag = `<script>${clientScript}</script><script>${reloadScript}</script>`;
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
  </style>
  <script>${clientScript}</script>
  <script>${reloadScript}</script>
</head>
<body>${content}</body>
</html>`;

const galleryTemplate = (files: string[]): string => `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Preview</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: system-ui, -apple-system, sans-serif; background: #f4f4f5; color: #18181b; }
    header { position: sticky; top: 0; z-index: 10; display: flex; align-items: center; gap: 1rem; padding: 0.6rem 1.25rem; background: #fff; border-bottom: 1px solid #e4e4e7; flex-wrap: wrap; }
    .tabs { display: flex; gap: 0.25rem; margin-right: auto; overflow-x: auto; }
    .tabs button { font: inherit; font-size: 0.8rem; padding: 0.3rem 0.7rem; border: 1px solid #d4d4d8; background: #fff; border-radius: 6px; cursor: pointer; white-space: nowrap; }
    .tabs button[aria-selected="true"] { background: #18181b; color: #fff; border-color: #18181b; }
    .controls { display: flex; align-items: center; gap: 0.25rem; }
    .controls button, .controls a { font: inherit; font-size: 0.8rem; padding: 0.3rem 0.7rem; border: 1px solid #d4d4d8; background: #fff; color: inherit; text-decoration: none; border-radius: 6px; cursor: pointer; }
    .controls button[aria-pressed="true"] { background: #18181b; color: #fff; border-color: #18181b; }
    .controls .sep { width: 1px; height: 1.4rem; background: #e4e4e7; margin: 0 0.4rem; }
    .workspace { display: grid; grid-template-columns: 190px minmax(0,1fr) 280px; min-height: calc(100vh - 54px); }
    .sidebar, .inspector { background: #fff; padding: 1rem; overflow-y: auto; }
    .sidebar { border-right: 1px solid #e4e4e7; }
    .inspector { border-left: 1px solid #e4e4e7; }
    .sidebar h2, .inspector h2 { font-size: 0.72rem; text-transform: uppercase; letter-spacing: 0.08em; color: #71717a; margin-bottom: 0.75rem; }
    .sidebar button { display: block; width: 100%; text-align: left; border: 0; background: transparent; padding: 0.4rem 0.5rem; border-radius: 5px; color: #3f3f46; cursor: pointer; }
    .sidebar button:hover { background: #f4f4f5; }
    .inspector label { display: grid; grid-template-columns: 1fr auto; gap: 0.5rem; align-items: center; padding: 0.55rem 0; border-bottom: 1px solid #f4f4f5; font-size: 0.75rem; }
    .inspector input[type=color] { width: 34px; height: 26px; border: 0; background: transparent; cursor: pointer; }
    .inspector .empty-inspector { color: #71717a; font-size: 0.78rem; line-height: 1.4; }
    .stage { display: flex; justify-content: center; padding: 1.25rem; min-width: 0; }
    iframe { border: 1px solid #d4d4d8; border-radius: 8px; background: #fff; height: 85vh; width: ${viewport}px; }
    iframe[hidden] { display: none; }
    .empty { padding: 3rem 1.25rem; color: #71717a; font-size: 0.9rem; }
    .queue { position: fixed; right: 1rem; bottom: 1rem; z-index: 50; width: 320px; background: #111; color: #fff; border-radius: 8px; box-shadow: 0 8px 32px rgba(0,0,0,0.4); font-size: 13px; overflow: hidden; }
    .queue[hidden] { display: none; }
    .queue h2 { font-size: 12px; font-weight: 600; padding: 0.6rem 0.75rem; border-bottom: 1px solid #262626; }
    .queue ol { list-style: none; max-height: 40vh; overflow-y: auto; }
    .queue li { padding: 0.5rem 0.75rem; border-bottom: 1px solid #1f1f1f; }
    .queue li small { display: block; opacity: 0.55; font-size: 11px; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .queue footer { display: flex; gap: 0.5rem; justify-content: flex-end; padding: 0.6rem 0.75rem; }
    .queue button { font: inherit; font-size: 12px; padding: 0.3rem 0.75rem; border-radius: 5px; border: 1px solid #333; background: transparent; color: #aaa; cursor: pointer; }
    .queue button[data-send] { background: #3b82f6; border-color: #3b82f6; color: #fff; }
    .composer { position: fixed; right: 1rem; top: 4rem; z-index: 60; width: 320px; background: #111; color: #fff; padding: 0.75rem; border-radius: 8px; box-shadow: 0 8px 32px rgba(0,0,0,0.4); font-size: 13px; }
    .composer[hidden] { display: none; }
    .composer p { opacity: 0.55; font-size: 11px; margin-bottom: 0.5rem; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
    .composer textarea { width: 100%; min-height: 80px; background: #222; color: #fff; border: 1px solid #333; border-radius: 4px; padding: 0.5rem; font: inherit; resize: vertical; }
    .composer footer { display: flex; gap: 0.5rem; justify-content: flex-end; margin-top: 0.5rem; }
    .composer button { font: inherit; font-size: 12px; padding: 0.3rem 0.75rem; border-radius: 5px; border: 1px solid #333; background: transparent; color: #aaa; cursor: pointer; }
    .composer button[data-add] { background: #3b82f6; border-color: #3b82f6; color: #fff; }
  </style>
</head>
<body>
${
  files.length === 0
    ? `  <p class="empty">Nothing to serve in this session yet.</p>`
    : `  <header>
    <div class="tabs" role="tablist">
      ${files.map((f, i) => `<button role="tab" data-file="${f}" aria-selected="${i === 0}">${f}</button>`).join("\n      ")}
    </div>
    <div class="controls" role="group" aria-label="Viewport width">
      ${Object.values(VIEWPORTS).map((w) => `<button data-width="${w}" aria-pressed="${w === viewport}">${w}</button>`).join("\n      ")}
    </div>
    <div class="controls">
      <span class="sep"></span>
      <button data-comment aria-pressed="false">Comment</button>
      <a data-open href="/${files[0].replace(/\.html$/, "")}" target="_blank" rel="noopener">Open</a>
    </div>
  </header>
  <div class="workspace">
  <nav class="sidebar" aria-label="Sections">
    <h2>Sections</h2>
    ${SECTIONS.map((section) => `<button data-section="${section}">${section.replaceAll("-", " ")}</button>`).join("\n    ")}
  </nav>
  <div class="stage">
    ${files.map((f, i) => `<iframe data-file="${f}" src="/${f.replace(/\.html$/, "")}" title="${f}"${i === 0 ? "" : " hidden"}></iframe>`).join("\n    ")}
  </div>
  <aside class="inspector" aria-label="Color inspector">
    <h2>Inspector</h2>
    <div data-inspector><p class="empty-inspector">Open the styleguide to tune declared colors. Adjustments stay temporary until the feedback round is confirmed in chat.</p></div>
  </aside>
  </div>
  <section class="composer" hidden aria-label="New comment">
    <p data-selector></p>
    <textarea placeholder="Comment..."></textarea>
    <footer>
      <button data-cancel>Cancel</button>
      <button data-add>Add</button>
    </footer>
  </section>
  <aside class="queue" hidden aria-label="Queued comments">
    <h2>Queued <span data-count>0</span></h2>
    <ol></ol>
    <footer>
      <button data-clear>Clear</button>
      <button data-send>Send round</button>
    </footer>
  </aside>`
}
  <script>
    const tabs = Array.from(document.querySelectorAll(".tabs button"));
    const frames = Array.from(document.querySelectorAll("iframe"));
    const openLink = document.querySelector("[data-open]");
    const commentBtn = document.querySelector("[data-comment]");
    const composer = document.querySelector(".composer");
    const composerText = composer && composer.querySelector("textarea");
    const composerSelector = composer && composer.querySelector("[data-selector]");
    const queueBox = document.querySelector(".queue");
    const queueList = queueBox && queueBox.querySelector("ol");
    const queueCount = queueBox && queueBox.querySelector("[data-count]");
    const inspector = document.querySelector("[data-inspector]");

    // The queue lives here rather than in the served file, so it survives a tab
    // switch. Text still being typed does not: the composer resets on every open.
    const queue = [];
    const adjustments = [];
    let activeFile = tabs.length ? tabs[0].dataset.file : null;
    let pendingSelector = null;
    let commentMode = false;

    function post(payload) {
      return fetch("/event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      }).catch(() => {});
    }

    function tellFrames() {
      frames.forEach((frame) => {
        try {
          frame.contentWindow.postMessage({ designbrief: "mode", on: commentMode }, location.origin);
        } catch {}
      });
    }

    function esc(value) {
      return String(value).replace(/[<&]/g, (c) => (c === "<" ? "&lt;" : "&amp;"));
    }

    function renderQueue() {
      if (!queueBox) return;
      queueCount.textContent = String(queue.length);
      queueList.innerHTML = queue
        .map((item) => "<li>" + esc(item.text) + "<small>" + esc(item.view) + " · " + esc(item.selector) + "</small></li>")
        .concat(adjustments.map((item) => "<li>" + esc(item.token) + ": " + esc(item.old) + " → " + esc(item.new) + "<small>" + esc(item.view) + " · temporary adjustment</small></li>"))
        .join("");
      queueCount.textContent = String(queue.length + adjustments.length);
      queueBox.hidden = queue.length + adjustments.length === 0;
    }

    function closeComposer() {
      if (!composer) return;
      composer.hidden = true;
      composerText.value = "";
      pendingSelector = null;
    }

    tabs.forEach((tab) => {
      tab.addEventListener("click", () => {
        activeFile = tab.dataset.file;
        tabs.forEach((t) => t.setAttribute("aria-selected", String(t === tab)));
        frames.forEach((f) => { f.hidden = f.dataset.file !== activeFile; });
        if (openLink) openLink.href = "/" + activeFile.replace(/\.html$/, "");
        closeComposer();
      });
    });

    document.querySelectorAll("[data-section]").forEach((button) => {
      button.addEventListener("click", () => {
        const frame = frames.find((candidate) => candidate.dataset.file === activeFile);
        if (frame) frame.contentWindow.postMessage({ designbrief: "navigate", section: button.dataset.section }, location.origin);
      });
    });

    document.querySelectorAll("[data-width]").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll("[data-width]").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
        frames.forEach((f) => { f.style.width = btn.dataset.width + "px"; });
      });
    });

    if (commentBtn) {
      commentBtn.addEventListener("click", () => {
        commentMode = !commentMode;
        commentBtn.setAttribute("aria-pressed", String(commentMode));
        if (!commentMode) closeComposer();
        tellFrames();
      });
    }

    window.addEventListener("message", (e) => {
      if (!e.data || !["target", "ready", "contrast"].includes(e.data.designbrief)) return;
      if (e.data.designbrief === "contrast") {
        const ratio = inspector && inspector.querySelector('[data-ratio="' + CSS.escape(e.data.token) + '"]');
        if (ratio) ratio.textContent = e.data.ratio.toFixed(2) + ":1 " + (e.data.ratio >= 4.5 ? "AA" : "fail");
        return;
      }
      if (e.data.designbrief === "ready") {
        tellFrames();
        if (!inspector || !e.data.swatches || e.data.swatches.length === 0) return;
        inspector.innerHTML = "";
        e.data.swatches.forEach((swatch) => {
          if (!/^#([0-9a-f]{6})$/i.test(swatch.original)) return;
          const label = document.createElement("label");
          const name = document.createElement("span");
          const input = document.createElement("input");
          const ratio = document.createElement("small");
          name.textContent = swatch.token;
          ratio.dataset.ratio = swatch.token;
          ratio.textContent = "contrast pending";
          input.type = "color";
          input.value = swatch.original;
          input.addEventListener("input", () => {
            const view = activeFile.replace(/\.html$/, "");
            const existing = adjustments.find((item) => item.token === swatch.token && item.view === view);
            if (existing) existing.new = input.value;
            else adjustments.push({ token: swatch.token, old: swatch.original, new: input.value, view });
            frames.forEach((frame) => frame.contentWindow.postMessage({ designbrief: "tune", variable: swatch.variable, value: input.value }, location.origin));
            renderQueue();
          });
          name.appendChild(document.createElement("br"));
          name.appendChild(ratio);
          label.append(name, input);
          inspector.appendChild(label);
        });
        return;
      }
      if (!composer) return;
      pendingSelector = e.data.selector;
      composerSelector.textContent = activeFile + " · " + pendingSelector;
      composer.hidden = false;
      composerText.focus();
    });

    if (composer) {
      composer.querySelector("[data-cancel]").addEventListener("click", closeComposer);
      composer.querySelector("[data-add]").addEventListener("click", () => {
        const text = composerText.value.trim();
        if (!text || !pendingSelector) return;
        queue.push({ view: activeFile.replace(/\.html$/, ""), selector: pendingSelector, text });
        closeComposer();
        renderQueue();
      });
    }

    if (queueBox) {
      queueBox.querySelector("[data-clear]").addEventListener("click", () => {
        queue.length = 0;
        adjustments.length = 0;
        renderQueue();
      });
      queueBox.querySelector("[data-send]").addEventListener("click", async () => {
        if (queue.length + adjustments.length === 0) return;
        await post({ type: "feedback", comments: queue.slice(), adjustments: adjustments.slice(), timestamp: new Date().toISOString() });
        queue.length = 0;
        adjustments.length = 0;
        renderQueue();
      });
    }

    document.addEventListener("keydown", (e) => { if (e.key === "Escape") closeComposer(); });
  </script>
  <script>${reloadScript}</script>
</body>
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

const serverOptions = {
  hostname: "127.0.0.1",
  async fetch(req: Request): Promise<Response> {
    const url = new URL(req.url);

    if (url.pathname === "/event" && req.method === "POST") {
      let event: unknown;
      try {
        event = await req.json();
      } catch {
        return new Response("Malformed event body", { status: 400 });
      }
      try {
        await appendFile(eventsFile, JSON.stringify(event) + "\n");
      } catch (err) {
        console.error(`Could not append to ${eventsFile}:`, err);
        return new Response("Event not recorded", { status: 500 });
      }
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

    if (url.pathname === "/") {
      let htmlFiles: string[] = [];
      try {
        const files = await readdir(sessionDir);
        htmlFiles = ["design.html", "styleguide.html"].filter((file) => files.includes(file));
      } catch (err) {
        console.error(`Could not read ${sessionDir}:`, err);
      }
      return new Response(galleryTemplate(htmlFiles), {
        headers: { "Content-Type": "text/html" },
      });
    }

    const routeFile: Record<string, string> = {
      "/design": "design.html",
      "/styleguide": "styleguide.html",
    };
    const requestedFile: string = routeFile[url.pathname] || url.pathname.replace(/^\//, "");
    const filePath: string = join(sessionDir, requestedFile);

    if (!isInsideSessionDir(filePath)) {
      return new Response("Forbidden", { status: 403 });
    }

    if (existsSync(filePath)) {
      let content: string;
      try {
        content = await readFile(filePath, "utf-8");
      } catch (err) {
        console.error(`Could not read ${filePath}:`, err);
        return new Response("Unreadable file", { status: 500 });
      }

      if (filePath.endsWith(".html")) {
        const isFullDocument = content.trimStart().toUpperCase().startsWith("<!DOCTYPE");
        const title: string =
          filePath.split("/").pop()?.replace(".html", "") || "Preview";
        return new Response(
          isFullDocument ? injectClientScripts(content) : frameTemplate(content, title),
          { headers: { "Content-Type": "text/html" } },
        );
      }

      const ext: string = filePath.split(".").pop() || "";
      return new Response(content, {
        headers: { "Content-Type": contentTypes[ext] || "text/plain" },
      });
    }

    return new Response("Not found", { status: 404 });
  },
};

// 10: consecutive ports to walk when the requested one is taken — enough to
// clear a busy range without stalling on a host where nothing is free
const PORT_RETRIES = 10;

let server: Server | null = null;

for (let candidate = port; candidate < port + PORT_RETRIES && candidate <= 65535; candidate++) {
  try {
    server = serve({ ...serverOptions, port: candidate });
    break;
  } catch (err) {
    if ((err as { code?: string }).code !== "EADDRINUSE") {
      console.error(`Could not start the server on port ${candidate}:`, err);
      process.exit(1);
    }
  }
}

if (!server) {
  console.error(`No free port between ${port} and ${port + PORT_RETRIES - 1}. Pass --port with an open one.`);
  process.exit(1);
}

console.log(`Preview server running at http://localhost:${server.port}`);
console.log(`Session directory: ${sessionDir}`);
console.log(`Events file: ${eventsFile}`);
console.log(`Live-reload: watching ${sessionDir} (SSE at /__reload)`);
