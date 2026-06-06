# junu-site

Personal academic website for **Junu Choi** — graduate student, IPAI, Seoul National University.

Live at **https://junu-choi.github.io**.

Built with [Astro](https://astro.build/), with MDX research notes and KaTeX math rendering. Deployed to GitHub Pages via GitHub Actions on every push to `main` (see `.github/workflows/deploy.yml`).

## Structure

```text
src/
├── config/site.ts     # site name, affiliation, nav, external links
├── data/              # cv, papers, research areas (typed content)
├── components/        # Rail, PaperList, ResearchAreas, …
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
