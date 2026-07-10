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

- Virtualize long lists (50+ items: `virtua`, `react-window`) or `content-visibility: auto`.
- `contain` for independent regions; minimize DOM depth and node count (flatter, fewer = faster).
- **No layout reads in the render path** (`getBoundingClientRect`, `offsetHeight`, `scrollTop`); batch DOM reads then writes, never interleave (interleaving forces reflow).
- **GPU-friendly movement** — animate `transform`/`opacity`, not layout-driving properties (`left`, `width`, `top`, margins).

## Network

- Reduce requests: combine small files, SVG sprites for icons, inline small critical assets, drop unused third-party scripts.
- Pagination over loading everything; response compression (gzip/brotli); HTTP cache headers; CDN for static assets.
- Slow connections: adaptive loading (`navigator.connection`), request prioritization, progressive enhancement.

## Framework

- **React** — `memo()` for expensive components, `useMemo`/`useCallback` for expensive computations, virtualize lists, code-split routes, avoid creating inline functions in render.
- **Agnostic** — minimize re-renders, debounce expensive operations, memoize computed values, lazy-load routes and components.

## Core Web Vitals

| Metric | Target | Key fixes |
|--------|--------|-----------|
| **LCP** (Largest Contentful Paint) | < 2.5s | optimize hero image, inline critical CSS, preload key resources, CDN, SSR |
| **INP** (Interaction to Next Paint) | < 200ms | break up long tasks, defer non-critical JS, web workers for heavy compute |
| **CLS** (Cumulative Layout Shift) | < 0.1 | set image/video dimensions, `aspect-ratio`, don't inject above existing content, reserve space for embeds |

## Measurement (for the audit)

When a perf tool is available, measure — don't guess. Tools: Lighthouse, Chrome DevTools Performance panel, WebPageTest. Key metrics: LCP, INP, CLS (Core Web Vitals), plus FCP, TBT, bundle size, request count. Measure on real / throttled mid-range devices and slow connections — desktop Chrome on fast wifi isn't representative. When no tool is available, judge from the static checks above.

## Performance anti-defaults

- Optimizing without measuring (premature optimization).
- `will-change` everywhere (creates layers, burns memory) — reserve for known expensive ops.
- Lazy-loading above-fold / LCP content.
- Micro-optimizing while the biggest bottleneck goes untouched.
- Sacrificing accessibility for performance; ignoring mobile (slower devices and connections).
