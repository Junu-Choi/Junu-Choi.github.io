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
      "Diffusion, flows, and transport maps.",
    work: ["transport", "speech"],
  },
  {
    id: "inference",
    label: "Inference",
    name: "Inference & inverse problems",
    description:
      "Posterior sampling and inverse problems.",
    work: ["transport", "smc"],
  },
  {
    id: "attention",
    label: "Attention",
    name: "Attention & scientific modeling",
    description:
      "Efficient attention for scientific modeling and weather forecasting.",
    work: ["red"],
  },
  {
    id: "learning",
    label: "Efficient learning",
    name: "Efficient & multimodal learning",
    description:
      "Speech, audio–language models, and efficient inference.",
    work: ["speech", "adaptation", "decoding"],
  },
];

export type ResearchWork = {
  id: string;
  reference: string;
  title: string;
  shortTitle: string;
  place: string;
  description: string;
  href: string;
  forthcoming?: boolean;
  preview?: string;
};

// References stay stable across filters; these are experience records, not
// publication entries. The two SNU projects remain forthcoming.
export const researchWork: ResearchWork[] = [
  {
    id: "transport",
    reference: "a",
    title: "Min-energy Transport Matching",
    shortTitle: "Transport Matching",
    place: "SNU",
    description: "Transport maps and minimum-energy stochastic dynamics for posterior sampling.",
    href: "/cv/#snu-research",
    forthcoming: true,
    preview: "/papers/#ptm",
  },
  {
    id: "red",
    reference: "b",
    title: "RED attention",
    shortTitle: "RED attention",
    place: "SNU",
    description: "Routed encode–decode attention for efficient global weather forecasting.",
    href: "/cv/#snu-research",
    forthcoming: true,
  },
  {
    id: "speech",
    reference: "c",
    title: "Speech & audio–language",
    shortTitle: "Speech & audio",
    place: "Humelo",
    description: "Speech generation, voice conversion, and audio–text understanding.",
    href: "/cv/#humelo-research",
  },
  {
    id: "smc",
    reference: "d",
    title: "Sequential Monte Carlo",
    shortTitle: "Sequential Monte Carlo",
    place: "KAIST",
    description: "Sampling complex distributions with population-simulated resampling.",
    href: "/cv/#kaist-visual-ai",
  },
  {
    id: "adaptation",
    reference: "e",
    title: "LLM adaptation",
    shortTitle: "LLM adaptation",
    place: "KAIST",
    description: "Parameter-efficient fine-tuning and evaluation of conversational models.",
    href: "/cv/#kaist-mlilab",
  },
  {
    id: "decoding",
    reference: "f",
    title: "Speculative decoding",
    shortTitle: "Speculative decoding",
    place: "KAIST",
    description: "Feature-level speculation combined with knowledge distillation.",
    href: "/cv/#kaist-education",
  },
];
