#!/usr/bin/env bun
/**
 * Render server for the craft-ui skill (render mode).
 * Serves generated variants side by side and records user interactions.
 *
 * Security: local-only server (127.0.0.1), read-only filesystem access
 * scoped to session directory, append-only event recording.
 *
 * Usage:
 *   bun run scripts/render-server.ts --session <path>
 *   bun run scripts/render-server.ts --session <path> --port 8080
 *   bun run scripts/render-server.ts --session <path> --viewport mobile
 *
 * The server:
 * - Serves HTML files from the session directory only
 * - Serves a gallery at "/" holding every variant in an iframe, side by side,
 *   with viewport controls (375 / 768 / 1440) and a Choose button per variant
 * - Opens the gallery at --viewport: mobile | tablet | desktop (default desktop)
 * - Records user events to .events file (JSON lines, append-only)
 * - Injects the interaction client into every served variant, whether the file
 *   is a full document or a fragment
 * - Live-reloads connected browsers on session-directory changes via SSE
 *   (`/__reload` endpoint, debounced 100ms, ignores .events and hidden files)
 *
 * Event types (one JSON per line in .events):
 *   choice:  { type: "choice",  choice: "editorial.html", timestamp }
 *   comment: { type: "comment", selector: ".card.primary", text: "too tight", timestamp }
 *
 * Client interactions:
 *   - Click a variant's Choose button in the gallery to record the pick
 *   - Alt+click any element inside a variant to open a comment overlay; submit
 *     to record a comment event with the element's CSS selector
 */

import { serve, type Server } from "bun";
import { readdir, readFile, appendFile, mkdir } from "node:fs/promises";
import { join, resolve, relative } from "node:path";
import { existsSync, watch } from "node:fs";

const args: string[] = process.argv.slice(2);
const sessionIdx: number = args.indexOf("--session");
const portIdx: number = args.indexOf("--port");
const viewportIdx: number = args.indexOf("--viewport");
const sessionDir: string =
  sessionIdx !== -1
    ? resolve(args[sessionIdx + 1])
    : resolve(".artifacts/design/variants");
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
    try {
      await fetch("/event", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ type: "comment", selector, text, timestamp: new Date().toISOString() }),
      });
    } catch {}
    overlay.remove();
    overlay = null;
  });
}

document.addEventListener("click", (e) => {
  if (!e.altKey) return;
  e.preventDefault();
  e.stopPropagation();
  openCommentOverlay(e.target);
}, true);
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
    .hint { position: fixed; bottom: 1rem; left: 1rem; background: #111; color: #fff; padding: 0.5rem 0.75rem; border-radius: 6px; font: 12px system-ui; opacity: 0.6; pointer-events: none; }
  </style>
  <script>${clientScript}</script>
  <script>${reloadScript}</script>
</head>
<body>${content}<div class="hint">Alt+click to comment</div></body>
</html>`;

const galleryTemplate = (files: string[]): string => `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Variants</title>
  <style>
    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: system-ui, -apple-system, sans-serif; background: #f4f4f5; color: #18181b; }
    header { position: sticky; top: 0; z-index: 10; display: flex; align-items: center; gap: 1rem; padding: 0.75rem 1.25rem; background: #fff; border-bottom: 1px solid #e4e4e7; }
    header h1 { font-size: 0.95rem; font-weight: 600; margin-right: auto; }
    .viewports { display: flex; gap: 0.25rem; }
    .viewports button { font: inherit; font-size: 0.8rem; padding: 0.3rem 0.7rem; border: 1px solid #d4d4d8; background: #fff; border-radius: 6px; cursor: pointer; }
    .viewports button[aria-pressed="true"] { background: #18181b; color: #fff; border-color: #18181b; }
    .hint { font-size: 0.75rem; color: #71717a; }
    .rail { display: flex; gap: 1.25rem; align-items: flex-start; padding: 1.25rem; overflow-x: auto; }
    .variant { flex: 0 0 auto; display: flex; flex-direction: column; gap: 0.5rem; }
    .variant figcaption { display: flex; align-items: center; gap: 0.6rem; font-size: 0.8rem; }
    .variant figcaption span { font-weight: 600; margin-right: auto; }
    .variant a, .variant button { font: inherit; font-size: 0.75rem; padding: 0.25rem 0.6rem; border-radius: 5px; border: 1px solid #d4d4d8; background: #fff; color: inherit; text-decoration: none; cursor: pointer; }
    .variant button.chosen { background: #18181b; color: #fff; border-color: #18181b; }
    .variant iframe { border: 1px solid #d4d4d8; border-radius: 8px; background: #fff; height: 80vh; width: ${viewport}px; }
    .empty { padding: 3rem 1.25rem; color: #71717a; font-size: 0.9rem; }
  </style>
</head>
<body>
  <header>
    <h1>Variants</h1>
    <div class="viewports" role="group" aria-label="Viewport width">
      ${Object.values(VIEWPORTS).map((w) => `<button data-width="${w}" aria-pressed="${w === viewport}">${w}</button>`).join("\n      ")}
    </div>
    <span class="hint">Alt+click inside a variant to comment</span>
  </header>
  ${
    files.length === 0
      ? `<p class="empty">No variants in this session yet.</p>`
      : `<div class="rail">${files
          .map(
            (f) => `<figure class="variant">
      <figcaption>
        <span>${f}</span>
        <a href="/${f}" target="_blank" rel="noopener">Open</a>
        <button data-choice="${f}">Choose</button>
      </figcaption>
      <iframe src="/${f}" title="${f}" loading="lazy"></iframe>
    </figure>`,
          )
          .join("\n")}</div>`
  }
  <script>
    const frames = document.querySelectorAll(".variant iframe");
    document.querySelectorAll(".viewports button").forEach((btn) => {
      btn.addEventListener("click", () => {
        document.querySelectorAll(".viewports button").forEach((b) => b.setAttribute("aria-pressed", String(b === btn)));
        frames.forEach((f) => { f.style.width = btn.dataset.width + "px"; });
      });
    });
    document.querySelectorAll("[data-choice]").forEach((btn) => {
      btn.addEventListener("click", async () => {
        document.querySelectorAll("[data-choice]").forEach((b) => b.classList.remove("chosen"));
        btn.classList.add("chosen");
        try {
          await fetch("/event", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ type: "choice", choice: btn.dataset.choice, timestamp: new Date().toISOString() }),
          });
        } catch {}
      });
    });
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
        htmlFiles = files.filter((f: string) => f.endsWith(".html")).sort();
      } catch (err) {
        console.error(`Could not read ${sessionDir}:`, err);
      }
      return new Response(galleryTemplate(htmlFiles), {
        headers: { "Content-Type": "text/html" },
      });
    }

    const filePath: string = join(sessionDir, url.pathname);

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
