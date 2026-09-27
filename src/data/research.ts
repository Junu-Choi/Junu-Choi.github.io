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
    work: ["transport", "speech"],
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
  preview?: string;
};

// Shared experience records link research interests to the CV. The two SNU
// projects remain forthcoming, separate from publication metadata.
export const researchWork: ResearchWork[] = [
  {
    id: "transport",
    title: "Min-energy Transport Matching",
    shortTitle: "Min-energy Transport Matching",
    place: "SNU",
    description: "Transport maps and minimum-energy stochastic dynamics for posterior sampling.",
    href: "/cv/#snu-research",
    forthcoming: true,
    preview: "/papers/#ptm",
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
    id: "speech",
    title: "Speech & audio–language",
    shortTitle: "Speech & audio",
    place: "Humelo",
    description: "Speech generation, voice conversion, and audio–text understanding.",
    href: "/cv/#humelo-research",
  },
  {
    id: "smc",
    title: "Sequential Monte Carlo",
    shortTitle: "Sequential Monte Carlo",
    place: "KAIST",
    description: "Sampling complex distributions with population-simulated resampling.",
    href: "/cv/#kaist-visual-ai",
  },
  {
    id: "adaptation",
    title: "LLM adaptation",
    shortTitle: "LLM adaptation",
    place: "KAIST",
    description: "Parameter-efficient fine-tuning and evaluation of conversational models.",
    href: "/cv/#kaist-mlilab",
  },
  {
    id: "decoding",
    title: "Speculative decoding",
    shortTitle: "Speculative decoding",
    place: "KAIST",
    description: "Feature-level speculation combined with knowledge distillation.",
    href: "/cv/#kaist-education",
  },
];
