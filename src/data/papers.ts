export type PaperLink = { label: string; href: string };

export type Paper = {
  /** Year used both for sorting and as the section header on /papers. */
  year: number;
  title: string;
  /** Author list as a single string; the literal "Junu Choi" will be auto-bolded. */
  authors: string;
  /** Short venue label that goes inside the badge: "ECCV", "NeurIPS", "JMLR", etc. */
  venue: string;
  /** Optional grade / award shown next to the venue badge: "Oral", "Spotlight", "Highlight", "Best Paper", … */
  grade?: string;
  /** Free-form status text (e.g. "under review", "post-rebuttal"). */
  status?: string;
  /** Footnote-style annotation for dagger / star marks (e.g. "†corresponding"). */
  note?: string;
  links?: PaperLink[];
  /** Show on the about page's "Selected" preview. */
  selected?: boolean;
};

/**
 * Add new papers here. The /papers page lists all entries (newest first);
 * the about page renders only entries with `selected: true`. The CV page
 * also pulls from this same array.
 */
// Latest-first within each year. PaperList and the CV publications mapper
// both year-sort with a stable algorithm, so the order here is preserved.
export const papers: Paper[] = [
  {
    year: 2026,
    title: "Efficient probabilistic weather forecasting at quarter-degree resolution with two-sided transport attention",
    authors: "Junu Choi, Youngjoon Hong",
    venue: "arXiv",
    status: "Preprint · arXiv:2610.35545",
    links: [
      { label: "https://arxiv.org/abs/2610.35545", href: "https://arxiv.org/abs/2610.35545" },
      { label: "PDF", href: "https://arxiv.org/pdf/2610.35545" },
      { label: "Code", href: "https://github.com/Junu-Choi/astra-wx" },
      { label: "Preview", href: "/papers/#astra" },
    ],
  },
  {
    year: 2026,
    title: "Posterior Transport Matching for Inverse Problems",
    authors: "Junu Choi, Youngjoon Hong",
    venue: "Under review",
    status: "ICLR 2027",
    links: [
      { label: "Preview", href: "/papers/#ptm" },
    ],
  },
];
