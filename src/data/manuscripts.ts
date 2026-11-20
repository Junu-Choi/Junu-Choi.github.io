// Forthcoming manuscript previews stay separate from published-paper metadata.
// Add authors, venue, and archival links to papers.ts once they are ready.
export const ptmManuscript = {
  id: "ptm",
  title: "Posterior Transport Matching for Inverse Problems",
  description:
    "Posterior Transport Matching sets up training-free posterior sampling with two separate dynamics—a map from a noisy input to a clean endpoint and an endpoint-only kernel to the next noisy input—meeting in the input law from which the next map returns the posterior. On truths drawn from the prior, PTM achieves a lower energy score than every baseline on every task, the highest PSNR on all eight FFHQ tasks and seven of eight ImageNet tasks, and the best primary metric on four scientific inverse problems.",
  status: "Under review",
  availability: "Manuscript and links forthcoming.",
  href: "/papers/#ptm",
} as const;

// Preview card for the released Astra preprint (Figure 2 of the paper).
export const astraPreview = {
  id: "astra",
  title: "Efficient probabilistic weather forecasting at quarter-degree resolution",
  description:
    "Astra forecasts on the 0.25° grid with Kantorovich Attention, in which each region chooses both where it reads from and where it writes to, so every region sends and receives information at token resolution. Trained on one node of eight GPUs, it matches GenCast with 10.3 times less hardware-normalised training compute.",
  availability: "Junu Choi, Youngjoon Hong · arXiv:2610.35545",
  arxiv: "https://arxiv.org/abs/2610.35545",
  pdf: "https://arxiv.org/pdf/2610.35545",
  code: "https://github.com/Junu-Choi/astra-wx",
  weatherbench: "https://sites.research.google/gr/weatherbench/",
  weatherbenchProbabilistic: "https://sites.research.google/gr/weatherbench/probabilistic-scores/",
  weatherbenchScorecards: "https://sites.research.google/gr/weatherbench/scorecards-2020/",
} as const;
