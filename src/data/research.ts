export type ResearchArea = {
  name: string;
  description: string;
  experience: { label: string; href: string }[];
};

export const researchAreas: ResearchArea[] = [
  {
    name: "Generative dynamics & transport",
    description:
      "Diffusion, flows, and transport maps for designing and understanding generative processes.",
    experience: [
      { label: "Min-energy Transport Matching · SNU", href: "/cv/#snu-research" },
      { label: "Speech generation · Humelo", href: "/cv/#humelo-research" },
    ],
  },
  {
    name: "Inference & inverse problems",
    description:
      "Posterior sampling and reconstruction with transport methods and sequential Monte Carlo.",
    experience: [
      { label: "Min-energy Transport Matching · SNU", href: "/cv/#snu-research" },
      { label: "Sequential Monte Carlo · KAIST", href: "/cv/#kaist-visual-ai" },
    ],
  },
  {
    name: "Attention & scientific modeling",
    description:
      "Scalable, content-routed attention for scientific modeling and global weather forecasting.",
    experience: [
      { label: "RED attention · SNU", href: "/cv/#snu-research" },
    ],
  },
  {
    name: "Efficient & multimodal learning",
    description:
      "Speech and audio–language models, parameter-efficient adaptation, and efficient inference.",
    experience: [
      { label: "Speech & audio–language · Humelo", href: "/cv/#humelo-research" },
      { label: "LLM adaptation · KAIST", href: "/cv/#kaist-mlilab" },
      { label: "Speculative decoding · KAIST", href: "/cv/#kaist-education" },
    ],
  },
];
