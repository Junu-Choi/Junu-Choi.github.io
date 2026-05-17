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
 * Leave the array empty to hide the "Selected papers" section on the home page
 * and show an "in preparation" message on /papers.
 */
export const papers: Paper[] = [];
