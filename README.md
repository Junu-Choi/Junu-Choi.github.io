# junu-site

Source for a personal academic website.

Built with [Astro](https://astro.build/), with MDX notes and KaTeX math rendering. Deployed to GitHub Pages via GitHub Actions on every push to `main` (see `.github/workflows/deploy.yml`).

## Structure

```text
src/
├── config/site.ts     # site name, affiliation, nav, external links
├── data/              # cv, papers, research areas (typed content)
├── components/        # SiteHeader, PublicationPreview, PaperList, …
├── pages/             # routes: index, papers, cv, notes/
├── content/           # MDX research notes
└── styles/            # shared styles and the home layout
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
The home page uses a cool blue-gray `#EDF3F9` background. A compact, nearly square
portrait sits between the two parts of the name, centered as one group. Below,
four research interests occupy a narrow left column; a short introduction sits
above Related work in the right column. On mobile, the introduction comes first.
`ResearchAreas.astro` uses the experience records in `src/data/research.ts` to link
each interest directly to stable CV entry IDs defined in `src/data/cv.ts`.
All four topics start folded, and Related work initially shows the two forthcoming
SNU projects, each marked “To be published.” “All research” opens a concise
overview: one sentence describing the work in each area, plus all six project
titles with affiliations and forthcoming status. It omits duplicate experience
links and full project summaries. Selecting one topic focuses that area, reveals
its experience links, and shows the matching project summaries. Closing the
active topic or toggling “All research” off restores the initial two projects.
Native topic disclosures also work without JavaScript; in that case, Related work
keeps the two initial projects and the all-research control is hidden. A single
short research note closes the column. The layout lives in `src/styles/home.css`.

The previous home layout is preserved on the remote branch
`backup/home-before-mineral-20260927` at `2a921d0`. That snapshot includes the
publication's Figure 2 banner and animation disclosure. The subsequent static
layout is also preserved on `backup/home-mineral-20260927` at `85965d2`, and the
interactive index on `backup/home-research-index-20260927` at `a3bfb5d`.
Revert the corresponding home-layout commit on `main` to restore a prior design
without rewriting history.

`PublicationPreview.astro` holds the first manuscript placeholder. Its navy
left rule and pale background follow the manuscript's theorem style. The
placeholder stays separate from `src/data/papers.ts` until publication metadata
is ready, so it does not create an incomplete publication in the CV.

The publication banner pairs its title and description with the manuscript's
fully labelled Figure 2 (`public/figures/ptm/figure-2.svg`). The SVG is a vector
export of the original LaTeX figure, and clicking it opens the full-size image.
On smaller screens it sits beneath the publication text.

The publication's two GIFs show analytic volume change and observation-dependent
Gaussian kernel geometry. They use the manuscript illustration's map and mixture
parameters; they are not experiment results. They sit in a native, initially
collapsed “Geometry in motion” disclosure. GIFs load when opened and return to
stills when closed. Stills appear without JavaScript or when reduced motion is
preferred, and a button switches between stills and playback.
Regenerate with `python scripts/figures/geometry_in_motion.py` (NumPy, Matplotlib,
and Pillow). The script verifies cell areas, covariance eigenvalues, density mass,
and contour bounds, and writes `public/figures/ptm/geometry.json` alongside the assets.
The website build uses the checked-in assets and does not require Python.

Reference directions: [Peter Holderrieth](https://www.peterholderrieth.com/)
for readable academic structure and direct research links,
[Michael Albergo](https://malbergo.me/) for personal identity with limited content,
and [NVIDIA Research](https://www.nvidia.com/en-us/research/) for heading hierarchy
and spacing. The centered name-and-portrait composition, cool background, and
compact text columns form this site's own arrangement. No third-party artwork
is reused.

Research notes should lead with one takeaway, then the minimum equation and
evidence needed to support it. State the experiment's scope and link to the
recorded measurements and reproduction code. Prefer a short note over a long
derivation; preserve existing URLs when editing. Paper and CV records remain
in `src/data/`.
