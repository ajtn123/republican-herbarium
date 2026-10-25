# 共和历 · 时间的自然史

A Chinese, static-first illustrated guide to the French Republican calendar, built with Astro. No React, hydration, server rendering, remote data runtime, analytics or account system.

## Run

Requires Node 22+ and Python 3. Python uses only the standard library for the production build.

```sh
npm ci
npm run build
npm run dev
```

`npm run build` exports the structured editorial data, runs Astro's static production build, then validates all generated routes, local links, anchors, assets, metadata and rendered serif glyph coverage. Deployment serves `dist/` directly.

## Structure

- `content.py`: original Chinese editorial content, 12 months, 360 ordinary days, six festivals and ten decade-day names.
- `export_data.py`: produces `src/data/calendar.json` and the on-demand search index.
- `src/layouts/Base.astro`: shared document, navigation, metadata, footer and native search dialog.
- `public/assets/months/`: twelve independent SVG drawings, shared by month cards, month details and the atlas headings.
- `src/components/`: genuinely shared clock, converter, month card and decorative linework.
- `src/pages/`: independent home, history, time, atlas and source pages; data-driven routes for months, days, festivals and decade names.
- `src/styles/global.css`: shared design tokens, typography, responsive layout and thematic details.
- `src/lib/day-navigation.ts`: shared reading sequence for all 360 ordinary and six complementary days, grouped by the twelve months and a separate complementary-day section.
- `src/lib/calendar.ts`: calendar arithmetic. Historical dates are supported from 1792-09-22; modern displays use an explicitly documented fixed four-year extension. See `/method/`.
- `scripts/validate.mjs`: complete static route and internal-link validation.
- `scripts/browser_qa.py`: optional browser interaction checks, requires Playwright and Chromium in a development environment. Not needed to build or serve.
- `scripts/subset_font.py`: optional font asset maintenance utility requiring fontTools and the source Noto CJK font. The generated font and its coverage manifest are already included. Collection includes component props and data-driven titles; rebuilds fail if rendered serif text lacks a glyph.

397 HTML pages are generated, including the 404 page. The sitemap includes the 396 content pages. All essays remain readable without JavaScript; clock, search, filtering and conversion use small native scripts. The search index is fetched only when search is opened. All images and fonts are local.

## Editorial and image notes

Historical references and uncertain old plant names are documented on `/sources/`. Cultural stories are distinguished from official naming motives. Site linework represents categories and seasonal imagery, not botanical or zoological identification. The home botanical image was generated for this project. Noto Serif CJK's license is in `public/assets/font-license.txt`.

## Hosting

`.openai/hosting.json` identifies the existing private Site and its static directory. Preserve its project ID. Source and production output should be kept in sync when publishing.
