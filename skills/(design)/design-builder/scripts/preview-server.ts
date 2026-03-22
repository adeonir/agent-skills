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
 * - Records click events to .events file (JSON lines, append-only)
 * - Wraps HTML fragments in a minimal frame template
 *
 * Events format (one JSON per line in .events):
 *   { "type": "choice", "choice": "a", "text": "Option Label", "timestamp": "..." }
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
  </style>
  <script>
    document.addEventListener("click", async (e) => {
      const option = e.target.closest("[data-choice]");
      if (!option) return;
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
  </script>
</head>
<body>${content}</body>
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
