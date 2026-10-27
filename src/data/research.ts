import { ptmManuscript } from "./manuscripts";

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
    tag: "01 · DYNAMICS",
    label: "Generative dynamics",
    name: "Generative dynamics & transport",
    description:
      "Transport maps and stochastic dynamics for continuous generative modeling.",
    work: ["transport", "lighttransporter", "speech"],
  },
  {
    id: "inference",
    tag: "02 · INFERENCE",
    label: "Probabilistic inference",
    name: "Inference & inverse problems",
    description:
      "Posterior sampling, inverse problems, and sequential Monte Carlo design.",
    work: ["transport", "smc"],
  },
  {
    id: "attention",
    tag: "03 · ARCHITECTURES",
    label: "ML architectures",
    name: "Machine learning architectures",
    description:
      "Two-sided transport attention and scalable routing for physical prediction.",
    work: ["ka"],
  },
  {
    id: "learning",
    tag: "04 · EFFICIENCY",
    label: "Efficient learning",
    name: "Efficient & multimodal learning",
    description:
      "Speculative decoding and parameter-efficient multimodal adaptation.",
    work: ["speech", "adaptation", "decoding"],
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

// Shared experience records link research interests to the CV. Forthcoming
// projects stay separate from publication metadata.
export const researchWork: ResearchWork[] = [
  {
    id: "transport",
    title: ptmManuscript.title,
    shortTitle: ptmManuscript.title,
    place: "SNU",
    description: "Minimum-energy transport matching with numerical maps for posterior sampling.",
    href: "/cv/#snu-research",
    forthcoming: true,
    status: ptmManuscript.status,
    links: [{ label: "Manuscript preview", href: "/papers/#ptm" }],
  },
  {
    id: "ka",
    title: "Kantorovich Attention",
    shortTitle: "Kantorovich Attention",
    place: "SNU",
    description: "Two-sided transport attention for efficient quarter-degree probabilistic weather forecasting (Astra).",
    href: "/papers/#astra",
    links: [
      { label: "arXiv", href: "https://arxiv.org/abs/2610.35545" },
      { label: "Preview", href: "/papers/#astra" },
    ],
  },
  {
    id: "lighttransporter",
    title: "LightTransporter",
    shortTitle: "LightTransporter",
    place: "KAIST",
    description: "Led a diffusion relighting project using a Light-Image Encoder to condition on source/target environment maps and camera pose.",
    href: "/cv/#lighttransporter",
    links: [
      { label: "Code", href: "https://github.com/j-mayo/LightTransporter" },
      { label: "Hugging Face", href: "https://huggingface.co/LightTransporter/DiffRelight-OpenIllumination" },
    ],
  },
  {
    id: "speech",
    title: "Speech & audio–language",
    shortTitle: "Speech & audio",
    place: "Humelo",
    description: "Speech generation, voice conversion, and audio–text understanding.",
    href: "/cv/#humelo-research",
  },
  {
    id: "smc",
    title: "Resampling design for SMC",
    shortTitle: "SMC resampling",
    place: "KAIST",
    description: "Investigated population-simulated resampling for sequential Monte Carlo samplers.",
    href: "/cv/#kaist-visual-ai",
  },
  {
    id: "adaptation",
    title: "Medical QA adaptation & evaluation",
    shortTitle: "Medical QA models",
    place: "KAIST",
    description: "Parameter-efficient tuning on medical instruction data and an evaluation protocol addressing GPT-4 judge bias and scoring variability.",
    href: "/cv/#kaist-mlilab",
  },
  {
    id: "decoding",
    title: "Feature-level speculative decoding",
    shortTitle: "Feature-level decoding",
    place: "KAIST",
    description: "Led a team project combining intermediate-feature speculation, knowledge distillation, and sparse rejection.",
    href: "/cv/#kaist-decoding",
  },
];
