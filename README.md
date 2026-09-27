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
The home page shares the Papers page's white background, navy `#16213E` headings,
and pale `#F6F6F7` panels. Shared `--paper-*` colors keep both pages aligned;
Selected papers repeats the manuscript preview's navy left rule. The name,
affiliation, and short introduction share a centered
profile block with a separate portrait. A local gray-to-blue-gray field uses only
the photographed wall's colors and softly joins the portrait to the white page.
`public/portrait-background.svg` interpolates ten wall-only samples from five
heights on each side of the photo, preserving its horizontal and vertical
lighting variation. The sampled patch coordinates are recorded in the SVG.
The original photo is unchanged; CSS masks soften its edges. The background uses
a soft elliptical falloff that fades quickly outside the photo, reaching full
transparency at 56% of the gradient radius. Its color field stays registered to
the portrait at every breakpoint, so the lighting pattern and fade follow the
image on mobile without horizontal scroll.
On mobile, the introduction spans the width below the name and photo; no separate
About section interrupts the research.

`ResearchMap.astro` presents four research cards in one desktop row, or a 2×2 grid
on smaller screens. Each has a short statement of the work. Selecting a card
reveals its project previews below, linked by restrained SVG branches. A selected
topic uses a pale navy tint and a navy left rule. The connector geometry updates with
layout and font changes; on narrow screens it routes around other cards and uses
one outside rail for stacked work. “All research” shows a compact grid of all seven
projects, with titles, affiliations, and forthcoming status. Selecting a topic
from that overview opens its detailed previews; selecting it again closes them.
Only the four topic cards are visible initially. Without JavaScript, all project
previews and links remain visible, with the filter controls disabled or hidden.

Project data in `src/data/research.ts` points to stable CV entry IDs and the PTM
manuscript preview. The two SNU projects remain “To be published.” The same work
appears only once per view even when it belongs to multiple research areas. The
Selected papers section follows the map. It includes the PTM forthcoming preview
from `src/data/manuscripts.ts`, with its status explicit; Figure 2 and animations
remain on the Papers page. Research notes are available through the Notes page
without an excerpt on the home page. The layout lives in `src/styles/home.css`.

The previous home layout is preserved on the remote branch
`backup/home-before-mineral-20260927` at `2a921d0`. That snapshot includes the
publication's Figure 2 banner and animation disclosure. The subsequent static
layout is also preserved on `backup/home-mineral-20260927` at `85965d2`, and the
interactive index on `backup/home-research-index-20260927` at `a3bfb5d`.
The subsequent centered-name design with folded topics is preserved on
`backup/home-folded-overview-20260927` at `551b236`.
The connected-card layout before these content updates is preserved on
`backup/home-research-cards-20260927` at `28d121e`.
The cool-gray palette before the Papers color alignment is preserved on
`backup/home-before-paper-tint-20260927` at `f0de424`.
The Papers palette before the portrait blend is preserved on
`backup/home-before-portrait-blend-20260927` at `3e8d025`.
Revert the corresponding home-layout commit on `main` to restore a prior design
without rewriting history.

`PublicationPreview.astro` renders the shared PTM manuscript preview. Its navy
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
and spacing. The compact profile, restrained tints, and connected research cards
form this site's own arrangement. No third-party artwork
is reused.

Research notes should lead with one takeaway, then the minimum equation and
evidence needed to support it. State the experiment's scope and link to the
recorded measurements and reproduction code. Prefer a short note over a long
derivation; preserve existing URLs when editing. Paper and CV records remain
in `src/data/`.

## Experience wording and sources

KAIST work is described by its method and task rather than broad subject labels.
The SMC resampling wording and medical Q&A / GPT-4 evaluation details follow the
original CV data (`a2665c9`); the intermediate-feature speculation, distillation,
and sparse-rejection details follow the team-lead entry in `c2d6f51`. No new
speedups, benchmark improvements, or publication claims are inferred.

LightTransporter appears as a led team project in the CV's Selected projects
section and under Generative dynamics on the home page. The project lead role was
confirmed by Junu; the three-person team, Fall 2024 course, Light-Image Encoder,
environment-map / camera-pose conditioning, and OpenIllumination evaluation are
documented in the [project repository](https://github.com/j-mayo/LightTransporter),
[Hugging Face model card](https://huggingface.co/LightTransporter/DiffRelight-OpenIllumination),
and [project report](https://drive.google.com/file/d/1009QskpqLxJRltqiCnim5seDmX1nxwEL/view).
Course projects stay separate from research appointments and publication metadata.
