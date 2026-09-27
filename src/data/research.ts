export type ResearchArea = {
  name: string;
  description: string;
  experience: { label: string; href: string }[];
};

export const researchAreas: ResearchArea[] = [
  {
    name: "Generative dynamics & transport",
    description:
      "Designing diffusion and flow dynamics: how the choice of paths, couplings, and transport maps shapes a generative model.",
    experience: [
      { label: "Min-energy Transport Matching · SNU", href: "/cv/#snu-research" },
      { label: "Speech generation · Humelo", href: "/cv/#humelo-research" },
    ],
  },
  {
    name: "Inference & inverse problems",
    description:
      "Sampling under observations and constraints, with a focus on posterior sampling, sequential Monte Carlo, and transport-based reconstruction.",
    experience: [
      { label: "Min-energy Transport Matching · SNU", href: "/cv/#snu-research" },
      { label: "Sequential Monte Carlo · KAIST", href: "/cv/#kaist-visual-ai" },
    ],
  },
  {
    name: "Attention & scientific modeling",
    description:
      "Designing scalable attention for physical systems, including content-routed interactions across spatial scales for global weather forecasting.",
    experience: [
      { label: "RED attention · SNU", href: "/cv/#snu-research" },
    ],
  },
  {
    name: "Efficient & multimodal learning",
    description:
      "Learning across speech, audio, and language, with an emphasis on parameter-efficient adaptation, stable training, and faster inference.",
    experience: [
      { label: "Speech & audio–language · Humelo", href: "/cv/#humelo-research" },
      { label: "LLM adaptation · KAIST", href: "/cv/#kaist-mlilab" },
      { label: "Speculative decoding · KAIST", href: "/cv/#kaist-education" },
    ],
  },
];
