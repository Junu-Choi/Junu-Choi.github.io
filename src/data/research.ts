export type ResearchArea = {
  name: string;
  description: string;
};

export const researchAreas: ResearchArea[] = [
  {
    name: "Stochastic Dynamics",
    description:
      "SDE, SPDE, and stochastic analysis — mathematical structure and applications of dynamics under noise.",
  },
  {
    name: "Deep Geometric Analysis",
    description:
      "Curvature, optimal transport, and the geometry of high-dimensional data and neural representations.",
  },
  {
    name: "Generative Modeling",
    description:
      "Foundations and design of generative models — diffusion, flow, score- and energy-based, likelihood-based, and beyond — from theoretical structure to controllable generation.",
  },
];
