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
      { label: "Generative dynamics · SNU", href: "/cv/#snu-research" },
      { label: "Speech generation · Humelo", href: "/cv/#humelo-research" },
    ],
  },
  {
    name: "Inference & inverse problems",
    description:
      "Sampling under observations and constraints, with a focus on posterior sampling, sequential Monte Carlo, and transport-based reconstruction.",
    experience: [
      { label: "Inverse problems · SNU", href: "/cv/#snu-research" },
      { label: "Sequential Monte Carlo · KAIST", href: "/cv/#kaist-visual-ai" },
    ],
  },
  {
    name: "Geometry & scientific modeling",
    description:
      "Using geometric structure to understand high-dimensional dynamics, with current interests in confinement and generative models for climate.",
    experience: [
      { label: "Confinement & climate · SNU", href: "/cv/#snu-research" },
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
