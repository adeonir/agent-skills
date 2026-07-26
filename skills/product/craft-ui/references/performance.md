# Performance

Performance is a feature. Find the actual bottleneck for *this* interface — don't optimize what isn't slow. Loading, rendering, network, framework, and Core Web Vitals: how to build fast, what to check, and how to measure.

## When to Use

Composed by `audit.md` (the Performance dimension — static checks, plus runtime measurement when a perf tool is available). Animation performance lives in [motion.md](motion.md); responsive images in [responsive.md](responsive.md). Not a direct trigger.

## Loading

- **Images** — modern formats (WebP/AVIF); size to display (don't ship a 3000px image for a 300px slot); compress (80–85% is usually imperceptible); `loading="lazy"` below the fold; never lazy-load above-fold/LCP images.
- **JavaScript** — code-split (route- and component-based), tree-shake, drop unused deps, dynamic-import large/non-critical components.
- **CSS** — inline critical CSS, async the rest; remove unused; `contain` for independent regions.
- **Fonts** — `font-display: swap`/`optional`, subset (`unicode-range`), preload the critical weight, limit weights loaded (see [typography.md](typography.md)).
- **Strategy** — critical resources first (defer/async the rest); `preload` key assets; `prefetch` likely next pages; `preconnect` to CDN/asset domains; HTTP/2-3 multiplexing; service worker for caching/offline.

## Rendering

- Virtualize long lists (50+ items), or `content-visibility: auto` with a `contain-intrinsic-size` estimate.
- `contain` for independent regions; minimize DOM depth and node count (flatter, fewer = faster).
- **No layout reads in the render path** (`getBoundingClientRect`, `offsetHeight`, `scrollTop`); batch DOM reads then writes, never interleave (interleaving forces reflow).
- **GPU-friendly movement** — animate `transform`/`opacity`, not layout-driving properties (`left`, `width`, `top`, margins).
- Minimize re-renders, debounce expensive operations, memoize computed values, lazy-load routes and heavy regions.

## Network

- Reduce requests: combine small files, SVG sprites for icons, inline small critical assets, drop unused third-party scripts.
- Pagination over loading everything; response compression (gzip/brotli); HTTP cache headers; CDN for static assets.
- Slow connections: adaptive loading (`navigator.connection`), request prioritization, progressive enhancement.

## Core Web Vitals

| Metric | Target | Key fixes |
|--------|--------|-----------|
| **LCP** (Largest Contentful Paint) | < 2.5s | optimize hero image, inline critical CSS, preload key resources, CDN, SSR |
| **INP** (Interaction to Next Paint) | < 200ms | break up long tasks, defer non-critical JS, web workers for heavy compute |
| **CLS** (Cumulative Layout Shift) | < 0.1 | set image/video dimensions, `aspect-ratio`, don't inject above existing content, reserve space for embeds |

## Measurement (for the audit)

Measure rather than guess, through the browser-automation MCP when it is available — `claude-in-chrome:read_network_requests` for the request waterfall, payload sizes, and count; `claude-in-chrome:javascript_tool` to read `PerformanceObserver` entries for LCP, INP, and CLS. It is an optional dependency: detect it before invoking it. Key metrics: LCP, INP, CLS (Core Web Vitals), plus FCP, TBT, bundle size, request count. Measured numbers come from the machine and network at hand — desktop Chrome on fast wifi is not representative, so report the conditions alongside the figures.

**Absent that channel** → score the dimension from the static checks above and say in the report that it was scored without measurement, so the number is read as a static judgment rather than a run.

## Performance anti-defaults

- Optimizing without measuring (premature optimization).
- `will-change` everywhere (creates layers, burns memory) — reserve for known expensive ops.
- Lazy-loading above-fold / LCP content.
- Micro-optimizing while the biggest bottleneck goes untouched.
- Sacrificing accessibility for performance; ignoring mobile (slower devices and connections).
