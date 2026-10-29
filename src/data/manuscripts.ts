// Forthcoming manuscript previews stay separate from published-paper metadata.
// Add authors, venue, and archival links to papers.ts once they are ready.
export const ptmManuscript = {
  id: "ptm",
  title: "Posterior Transport Matching for Inverse Problems",
  description: "Pairing numerical transport maps with stochastic input updates for posterior sampling.",
  status: "Under review, ICLR 2027",
  availability: "Manuscript and links forthcoming.",
  href: "/papers/#ptm",
} as const;

// Preview card for the released Astra preprint (Figure 2 of the paper).
export const astraPreview = {
  id: "astra",
  title: "Efficient probabilistic weather forecasting at quarter-degree resolution with two-sided transport attention",
  description:
    "Astra forecasts on the 0.25° grid with Kantorovich Attention, in which each region chooses both where it reads from and where it writes to, so every region sends and receives information at token resolution. Trained on one node of eight GPUs, it matches GenCast with 9.8% of its hardware-normalised training compute.",
  availability: "Junu Choi, Youngjoon Hong · arXiv:2610.35545",
  arxiv: "https://arxiv.org/abs/2610.35545",
  pdf: "https://arxiv.org/pdf/2610.35545",
  code: "https://github.com/Junu-Choi/astra-wx",
} as const;
