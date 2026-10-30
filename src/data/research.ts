import { astraPreview, ptmManuscript } from "./manuscripts";

export type ResearchArea = {
  id: string;
  tag: string;
  label: string;
  name: string;
  description: string;
  work: string[];
};

export const researchAreas: ResearchArea[] = [
  {
    id: "generative",
    tag: "01 · DYNAMICS & TRANSPORT",
    label: "Generative Dynamics & Transport",
    name: "Generative Dynamics & Transport",
    description:
      "Transport maps, stochastic dynamics, and diffusion bridges for continuous generative modeling.",
    work: ["astra", "transport", "lighttransporter"],
  },
  {
    id: "inference",
    tag: "02 · INFERENCE & INVERSE PROBLEMS",
    label: "Probabilistic Inference & Inverse Problems",
    name: "Probabilistic Inference & Inverse Problems",
    description:
      "Posterior sampling, Bayesian inverse problems, and sequential Monte Carlo design.",
    work: ["transport", "smc"],
  },
  {
    id: "scientific-ai",
    tag: "03 · SCIENTIFIC AI",
    label: "Scientific AI",
    name: "Scientific AI",
    description:
      "Two-sided Kantorovich transport attention and physics-aware neural architectures for global Earth system forecasting.",
    work: ["astra"],
  },
];

export type ResearchWork = {
  id: string;
  title: string;
  shortTitle: string;
  place: string;
  description: string;
  href: string;
  forthcoming?: boolean;
  /** Status label shown on the research map for forthcoming work. */
  status?: string;
  links?: { label: string; href: string }[];
};

// Shared experience records link research interests to papers and the CV.
export const researchWork: ResearchWork[] = [
  {
    id: "astra",
    title: astraPreview.title,
    shortTitle: astraPreview.title,
    place: "SNU",
    status: "arXiv:2610.35545",
    forthcoming: true,
    description:
      "Two-sided Kantorovich Attention (pull & push) for 0.25° global ensemble weather forecasting. Trained on a single 8-GPU node, Astra has lower CRPS and ensemble-mean RMSE than ECMWF IFS ENS on all 600 variable–level–lead-time combinations, verified against ERA5.",
    href: "/papers/#astra",
    links: [
      { label: "Read paper", href: astraPreview.arxiv },
      { label: "Code", href: astraPreview.code },
      { label: "Interactive preview", href: "/papers/#ka-title" },
    ],
  },
  {
    id: "transport",
    title: ptmManuscript.title,
    shortTitle: ptmManuscript.title,
    place: "SNU",
    description:
      "Pairing numerical transport maps with stochastic input updates for measurement-consistent posterior sampling in inverse problems.",
    href: "/papers/#ptm",
    forthcoming: true,
    status: ptmManuscript.status,
    links: [
      { label: "Manuscript preview", href: "/papers/#ptm" },
      { label: "Interactive preview", href: "/papers/#geometry-title" },
    ],
  },
  {
    id: "lighttransporter",
    title: "LightTransporter: Diffusion Relighting with Light-Image Conditioning",
    shortTitle: "LightTransporter",
    place: "KAIST",
    status: "Earlier Research",
    forthcoming: true,
    description:
      "Diffusion relighting framework conditioning on source and target environment maps and camera pose via a dedicated Light-Image Encoder.",
    href: "/cv/#lighttransporter",
    links: [
      { label: "Code (team repository)", href: "https://github.com/j-mayo/LightTransporter" },
      { label: "Hugging Face", href: "https://huggingface.co/LightTransporter/DiffRelight-OpenIllumination" },
    ],
  },
  {
    id: "smc",
    title: "Population-Simulated Resampling for Sequential Monte Carlo",
    shortTitle: "SMC Resampling",
    place: "KAIST",
    status: "Earlier Research",
    forthcoming: true,
    description:
      "Investigated population-simulated resampling schemes to improve particle diversity and variance reduction in sequential Monte Carlo samplers.",
    href: "/cv/#kaist-visual-ai",
    links: [
      { label: "CV details", href: "/cv/#kaist-visual-ai" },
    ],
  },
];
