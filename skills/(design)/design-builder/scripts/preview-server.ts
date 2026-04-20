/**
 * Preview server for design-builder skill.
 * Serves HTML fragments and records user interactions.
 *
 * Security: local-only server (127.0.0.1), read-only filesystem access
 * scoped to session directory, append-only event recording.
 *
 * Usage:
 *   bun run scripts/preview-server.ts --session <path>
 *   bun run scripts/preview-server.ts --session <path> --port 8080
 *
 * The server:
 * - Serves HTML files from the session directory only
 * - Records user events to .events file (JSON lines, append-only)
 * - Wraps HTML fragments in a minimal frame template with interaction scripts
 *
 * Event types (one JSON per line in .events):
 *   choice:  { type: "choice",  choice: "a", text: "Option Label", timestamp }
 *   tune:    { type: "tune",    token: "--color-primary", value: "#3b82f6", timestamp }
 *   comment: { type: "comment", selector: ".card.primary", text: "too tight", timestamp }
 *
 * Client interactions:
 *   - Click elements with `data-choice` to record a choice
 *   - Move/input controls with `data-tune="<token>"` to update a CSS custom
 *     property live on the document and record a tune event
 *   - Alt+click any element to open a comment overlay; submit to record a
 *     comment event with the element's CSS selector
 */

import { serve, type Server } from "bun";
import { readdir, readFile, appendFile, mkdir } from "node:fs/promises";
import { join, resolve, relative } from "node:path";
import { existsSync } from "node:fs";

const args: string[] = process.argv.slice(2);
const sessionIdx: number = args.indexOf("--session");
const portIdx: number = args.indexOf("--port");
const sessionDir: string =
  sessionIdx !== -1
    ? resolve(args[sessionIdx + 1])
    : resolve(".artifacts/design/preview");
const port: number = parseInt(portIdx !== -1 ? args[portIdx + 1] : "3456", 10);

if (!existsSync(sessionDir)) {
  await mkdir(sessionDir, { recursive: true });
}

const eventsFile: string = join(sessionDir, ".events");

function isInsideSessionDir(filePath: string): boolean {
  const rel = relative(sessionDir, filePath);
  return !rel.startsWith("..") && !rel.startsWith("/");
}

const clientScript = `
document.addEventListener("click", async (e) => {
  const option = e.target.closest("[data-choice]");
  if (!option || e.altKey) return;
  const choice = option.dataset.choice;
  const text = option.querySelector("h3")?.textContent || "";
  document.querySelectorAll("[data-choice]").forEach((el) => el.classList.remove("selected"));
  option.classList.add("selected");
  await fetch("/event", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ type: "choice", choice, text, timestamp: new Date().toISOString() }),
  });
});

document.addEventListener("input", async (e) => {
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
  if (e.target.closest("[data-choice], [data-tune]")) return;
  e.preventDefault();
  e.stopPropagation();
  openCommentOverlay(e.target);
}, true);
`;

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
    .options { display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; }
    .option {
      border: 2px solid #e5e5e5; border-radius: 12px; padding: 1.5rem;
      cursor: pointer; transition: border-color 0.2s, transform 0.2s;
    }
    .option:hover { border-color: #3b82f6; transform: translateY(-2px); }
    .option h3 { margin-bottom: 0.75rem; font-size: 1.1rem; }
    .option.selected { border-color: #3b82f6; background: #eff6ff; }
    .tune-panel { display: grid; gap: 1rem; padding: 1rem; background: #fff; border: 1px solid #e5e5e5; border-radius: 8px; margin-bottom: 1.5rem; }
    .tune-panel label { display: grid; gap: 0.25rem; font-size: 0.875rem; }
    .tune-panel input[type="range"] { width: 100%; }
    .hint { position: fixed; bottom: 1rem; left: 1rem; background: #111; color: #fff; padding: 0.5rem 0.75rem; border-radius: 6px; font: 12px system-ui; opacity: 0.6; pointer-events: none; }
  </style>
  <script>${clientScript}</script>
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

    const filePath: string = join(
      sessionDir,
      url.pathname === "/" ? "index.html" : url.pathname,
    );

    if (!isInsideSessionDir(filePath)) {
      return new Response("Forbidden", { status: 403 });
    }

    if (existsSync(filePath)) {
      const content: string = await readFile(filePath, "utf-8");

      if (
        filePath.endsWith(".html") &&
        !content.trimStart().startsWith("<!DOCTYPE")
      ) {
        const title: string =
          filePath.split("/").pop()?.replace(".html", "") || "Preview";
        return new Response(frameTemplate(content, title), {
          headers: { "Content-Type": "text/html" },
        });
      }

      const ext: string = filePath.split(".").pop() || "";
      return new Response(content, {
        headers: { "Content-Type": contentTypes[ext] || "text/plain" },
      });
    }

    if (url.pathname === "/") {
      const files: string[] = await readdir(sessionDir);
      const htmlFiles: string[] = files.filter((f: string) =>
        f.endsWith(".html"),
      );
      const list: string = htmlFiles
        .map((f: string) => `<li><a href="/${f}">${f}</a></li>`)
        .join("\n");
      return new Response(
        frameTemplate(`<h1>Preview Session</h1><ul>${list}</ul>`, "Preview"),
        { headers: { "Content-Type": "text/html" } },
      );
    }

    return new Response("Not found", { status: 404 });
  },
});

console.log(`Preview server running at http://localhost:${server.port}`);
console.log(`Session directory: ${sessionDir}`);
console.log(`Events file: ${eventsFile}`);
