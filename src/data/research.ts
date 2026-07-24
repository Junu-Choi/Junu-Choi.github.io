export type ResearchArea = {
  name: string;
  description: string;
};

export const researchAreas: ResearchArea[] = [
  {
    name: "Generative Dynamics",
    description:
      "Design of the dynamics behind generative models — diffusion, flows, stochastic interpolants: which process to run, along which path, and how to sample from it.",
  },
  {
    name: "Optimal Transport & Geometry",
    description:
      "Wasserstein geometry, couplings, and curvature — the transport structure that organises high-dimensional generative paths.",
  },
];
