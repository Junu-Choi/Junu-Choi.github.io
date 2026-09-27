import { ptmManuscript } from "./manuscripts";

export type ResearchArea = {
  id: string;
  label: string;
  name: string;
  description: string;
  work: string[];
};

export const researchAreas: ResearchArea[] = [
  {
    id: "generative",
    label: "Generative dynamics",
    name: "Generative dynamics & transport",
    description:
      "I study transport maps and stochastic dynamics for generative modeling.",
    work: ["transport", "lighttransporter", "speech"],
  },
  {
    id: "inference",
    label: "Inference",
    name: "Inference & inverse problems",
    description:
      "I develop sampling methods for posterior inference and inverse problems.",
    work: ["transport", "smc"],
  },
  {
    id: "attention",
    label: "ML architectures",
    name: "Machine learning architectures",
    description:
      "I design efficient model architectures for scientific prediction.",
    work: ["red"],
  },
  {
    id: "learning",
    label: "Efficient learning",
    name: "Efficient & multimodal learning",
    description:
      "I work on efficient adaptation and inference for language and multimodal models.",
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
  links?: { label: string; href: string }[];
};

// Shared experience records link research interests to the CV. The two SNU
// projects remain forthcoming, separate from publication metadata.
export const researchWork: ResearchWork[] = [
  {
    id: "transport",
    title: ptmManuscript.title,
    shortTitle: ptmManuscript.title,
    place: "SNU",
    description: "Minimum-energy transport matching with numerical maps for posterior sampling.",
    href: "/cv/#snu-research",
    forthcoming: true,
    links: [{ label: "Manuscript preview", href: "/papers/#ptm" }],
  },
  {
    id: "red",
    title: "RED attention",
    shortTitle: "RED attention",
    place: "SNU",
    description: "Routed encode–decode attention for efficient global weather forecasting.",
    href: "/cv/#snu-research",
    forthcoming: true,
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
