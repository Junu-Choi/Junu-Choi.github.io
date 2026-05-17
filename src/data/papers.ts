export type PaperLink = { label: string; href: string };

export type Paper = {
  year: number;
  title: string;
  /** Author list as a single string; the literal "Junu Choi" will be auto-bolded. */
  authors: string;
  venue: string;
  links?: PaperLink[];
  /** Show on the about page's "Selected" preview. */
  selected?: boolean;
};

/**
 * Add new papers here. The /papers page lists all entries (newest first);
 * the about page renders only entries with `selected: true`.
 *
 * For papers under review, leave `title` as a placeholder ("Manuscript
 * under review") and update once the venue announces accepted titles.
 * Replace `authors` with the full author list when public.
 */
export const papers: Paper[] = [
  {
    year: 2026,
    // Title withheld during review; switch to "Space–Time Aligned Diffusion Dynamics"
    // once ECCV 2026 acceptance is announced.
    title: "Manuscript under review",
    authors: "Junu Choi, Youngjoon Hong†",
    venue: "ECCV 2026 — post-rebuttal · †corresponding",
    selected: true,
  },
  {
    year: 2026,
    title: "Manuscript under review",
    authors: "Junu Choi, Hyunwoo J. Kim†, Youngjoon Hong†",
    venue: "NeurIPS 2026 — submitted · †equal advising",
    selected: true,
  },
];
