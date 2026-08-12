# Viz brief — DC MW additions site

Build a single-page interactive visualization of `docs/data.json` (22 countries × 5 years of data-center IT MW additions, medians, 2026 = full-year estimate; each country-year has a `reasoning` string containing markdown links).

**Output**: `docs/index.html` — fully self-contained except D3 (or Chart.js) from a CDN. No build step, no framework, vanilla JS. Loads `data.json` via fetch (same dir).

**Required elements**:
1. `<meta name="robots" content="noindex, nofollow">` in head — MANDATORY.
2. Main chart: MW additions per year, by country. Default view: stacked or grouped presentation that copes with US (24,000) dwarfing Taiwan (44) — use a log-scale toggle AND a "top N / all" or US+China separate treatment; your call, justify in a code comment.
3. Reactivity: hover tooltip per data point showing country, year, MW, and the reasoning text (render its markdown links as clickable); click a country in the legend to isolate/compare; toggle annual additions vs cumulative-since-2022; linear/log toggle.
4. Mobile-responsive; readable in light and dark (prefers-color-scheme).
5. Footer: "Data: Konstantin's Claude research team, 2026-08-12. Medians; 2026 is a full-year estimate. Definitions: IT (critical) MW, colo + hyperscale + AI campuses." plus a caveat line: "China 2024–25 partly reflects a statistical series change; US 2026 follows SemiAnalysis's construction-backed forecast."
6. Title: "Data-center capacity additions by country, 2022–2026". Clean, minimal, no clutter.

**Design**: restrained palette (color-blind safe), US and China visually distinct, whitespace, no chartjunk, axis labels with thousands separators, sans-serif system font stack. Keep total page weight small.

Verify your HTML parses and the JSON loads (you can run a quick local check with python3 -m http.server on 127.0.0.1 and curl). Do not create any other pages.
