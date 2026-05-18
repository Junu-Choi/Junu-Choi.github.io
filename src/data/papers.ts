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
export const papers: Paper[] = [
  {
    year: 2026,
    // Title withheld during review; switch to "Space–Time Aligned Diffusion Dynamics"
    // once ECCV 2026 acceptance is announced.
    title: "Manuscript under review",
    authors: "Junu Choi, Youngjoon Hong†",
    venue: "ECCV",
    status: "under review · post-rebuttal",
    note: "†corresponding author",
    selected: true,
  },
  {
    year: 2026,
    title: "Manuscript under review",
    authors: "Junu Choi, Hyunwoo J. Kim†, Youngjoon Hong†",
    venue: "NeurIPS",
    status: "under review",
    note: "†equal advising",
    selected: true,
  },
];
