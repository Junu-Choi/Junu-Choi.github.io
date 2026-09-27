import { ptmManuscript } from "./manuscripts";

/**
 * CV content. Each section sorted newest-first.
 *
 * `details` items are bullet lines. Keep them tight — a CV is a curation,
 * not a log. Aim for 2–4 bullets per role; condense or drop the rest.
 */

export type CVEntry = {
  id?: string;
  title: string;
  place: string;
  date: string;
  details?: string[];
  links?: { label: string; href: string }[];
};

export type CVSection = readonly CVEntry[];

export const cv = {
  lastUpdated: "September 2026",

  education: [
    {
      title: "M.S., Interdisciplinary Program in Artificial Intelligence",
      place: "Seoul National University",
      date: "2025 – present",
      details: ["GPA: 4.30 / 4.30 (in progress)"],
    },
    {
      id: "kaist-education",
      title: "B.S. (Double Major), School of Computing × Mathematical Sciences",
      place: "Korea Advanced Institute of Science and Technology",
      date: "2017 – 2025",
      details: [
        "On leave 2020 – 2024 — industry R&D at Humelo, Inc., including two years of alternative military service.",
      ],
    },
  ] satisfies CVSection,

  // Publications are sourced from src/data/papers.ts to keep the
  // CV, /papers tab, and home page in lockstep. See cv.astro.

  experience: [
    {
      id: "snu-research",
      title: "Graduate Researcher (M.S.)",
      place: "Seoul National University",
      date: "Sep 2025 – present",
      details: [
        "RED attention: routed encode–decode attention for efficient global weather forecasting — to be published.",
        `${ptmManuscript.title}: minimum-energy transport matching for posterior sampling — to be published.`,
      ],
    },
    {
      id: "kaist-visual-ai",
      title: "Undergraduate Researcher",
      place: "Visual AI Group, KAIST",
      date: "Jan – Mar 2025",
      details: [
        "Investigated population-simulated resampling to expand the design space of sequential Monte Carlo samplers.",
      ],
    },
    {
      id: "kaist-mlilab",
      title: "Undergraduate Researcher",
      place: "MLILAB, KAIST",
      date: "Mar – Aug 2024",
      details: [
        "Fine-tuned conversational LLMs on medical instruction Q&A using parameter-efficient adaptation.",
        "Developed an evaluation protocol to address GPT-4 evaluator bias and scoring variability.",
      ],
    },
    {
      id: "humelo-research",
      title: "AI Researcher (Speech & Multimodal)",
      place: "Humelo, Inc. — incl. two years of alternative military service (industrial technical personnel)",
      date: "Sep 2020 – Jan 2024",
      details: [
        "Production text-to-speech and voice-conversion systems across multiple product lines.",
        "Proposed Style Contrastive Adversarial Neutralization (SCAN) for vocal-style disentanglement, combining bi-adversarial training with contrastive feature compaction.",
        "Implemented an LTU-2-family audio–text understanding system (Llama × Whisper-AT) with partial LoRA / QLoRA training.",
        "Stabilised auto-regressive TTS via Lipschitz-preserving discriminators and 3-step causal training.",
      ],
    },
    {
      title: "Research Intern",
      place: "Humelo, Inc.",
      date: "Jul – Sep 2020",
      details: [
        "GMM-based emotional control of speaker embeddings; multi-band mel-GAN vocoder.",
      ],
    },
  ] satisfies CVSection,

  projects: [
    {
      id: "lighttransporter",
      title: "LightTransporter — diffusion-based image relighting",
      place: "KAIST · CS492D: Diffusion Models and Their Applications",
      date: "Fall 2024",
      details: [
        "Led a three-person project using a Light-Image Encoder to condition diffusion on source/target environment maps and camera pose; evaluated on OpenIllumination.",
      ],
      links: [
        { label: "Code", href: "https://github.com/j-mayo/LightTransporter" },
        { label: "Hugging Face", href: "https://huggingface.co/LightTransporter/DiffRelight-OpenIllumination" },
        { label: "Report", href: "https://drive.google.com/file/d/1009QskpqLxJRltqiCnim5seDmX1nxwEL/view" },
      ],
    },
    {
      id: "kaist-decoding",
      title: "Feature-level speculative decoding",
      place: "KAIST · Team project",
      date: "Mar – Jun 2024",
      details: [
        "Led a team project combining intermediate-feature speculation, knowledge distillation, and sparse rejection for speculative decoding.",
      ],
    },
  ] satisfies CVSection,

  awards: [
    {
      title: "Full graduate fellowship",
      place: "Seoul National University, Interdisciplinary Program in AI",
      date: "2025 – present",
    },
    {
      title: "Qualcomm Innovation Award",
      place: "KAIST × Qualcomm AI Hackathon",
      date: "2019",
    },
  ] satisfies CVSection,

  skills: {
    Languages: ["Python", "CUDA"],
    "ML frameworks": ["PyTorch", "TensorFlow", "JAX"],
    "Scientific": ["NumPy", "SciPy", "matplotlib"],
    Tools: ["Linux/macOS", "tmux", "vim", "git"],
  } as Record<string, string[]>,
};
