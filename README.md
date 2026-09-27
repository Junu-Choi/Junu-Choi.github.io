# junu-site

Source for a personal academic website.

Built with [Astro](https://astro.build/), with MDX notes and KaTeX math rendering. Deployed to GitHub Pages via GitHub Actions on every push to `main` (see `.github/workflows/deploy.yml`).

## Structure

```text
src/
├── config/site.ts     # site name, affiliation, nav, external links
├── data/              # cv, papers, research areas (typed content)
├── components/        # SiteHeader, TransportStudy, PaperList, …
├── pages/             # routes: index, papers, cv, notes/
├── content/           # MDX research notes
└── styles/site.css
public/                # static assets (images, etc.)
```

## Commands

Run from the project root:

| Command           | Action                                       |
| :---------------- | :------------------------------------------- |
| `npm install`     | Install dependencies                         |
| `npm run dev`     | Start the dev server at `localhost:4321`     |
| `npm run build`   | Build the production site to `./dist/`       |
| `npm run preview` | Preview the production build locally         |

Requires Node `>=22.12.0`.

## Design and writing

The palette follows PTM Figure 2: blue `#2878B5` distribution contours, teal
`#238A83` paths, charcoal `#30363E` geometry, and a small rust `#C16A43` accent.
Manrope headings and IBM Plex Sans body text sit on a light, spacious grid.
`TransportStudy.astro` is an original SVG illustration, not experimental data;
it stays visible without JavaScript and its optional shape control is keyboard-accessible.

Reference directions: [Peter Holderrieth](https://www.peterholderrieth.com/)
for readable academic structure, and [NVIDIA Research](https://www.nvidia.com/en-us/research/)
for restrained typography and hierarchy. No third-party artwork is reused.

Research notes should lead with one takeaway, then the minimum equation and
evidence needed to support it. State the experiment's scope and link to the
recorded measurements and reproduction code. Prefer a short note over a long
derivation; preserve existing URLs when editing. Paper and CV records remain
in `src/data/`.
