/**
 * CV content. Each section sorted newest-first.
 *
 * `details` items are bullet lines. Keep them tight — a CV is a curation,
 * not a log. Aim for 2–4 bullets per role; condense or drop the rest.
 */

export type CVEntry = {
  title: string;
  place: string;
  date: string;
  details?: string[];
};

export type CVSection = readonly CVEntry[];

export const cv = {
  lastUpdated: "July 2026",

  education: [
    {
      title: "M.S., Interdisciplinary Program in Artificial Intelligence",
      place: "Seoul National University",
      date: "2025 – present",
      details: ["GPA: 4.30 / 4.30 (in progress)"],
    },
    {
      title: "B.S. (Double Major), School of Computing × Mathematical Sciences",
      place: "Korea Advanced Institute of Science and Technology",
      date: "2017 – 2025",
      details: [
        "On leave 2020 – 2024 — industry R&D at Humelo, Inc., including two years of alternative military service.",
        "Led a team project on speculative-decoding acceleration — feature-level speculation combined with knowledge distillation.",
      ],
    },
  ] satisfies CVSection,

  // Publications are sourced from src/data/papers.ts to keep the
  // CV, /papers tab, and home page in lockstep. See cv.astro.

  experience: [
    {
      title: "Graduate Researcher",
      place: "Seoul National University",
      date: "Sep 2025 – present",
      details: [
        "Design of generative dynamics — to be published.",
        "Transport-map–based inverse problem solver — to be published.",
        "Confined generative dynamics and generative modeling for climate — to be published.",
      ],
    },
    {
      title: "Undergraduate Researcher",
      place: "Visual AI Group, KAIST",
      date: "Jan – Mar 2025",
      details: [
        "Sequential Monte Carlo for sampling complex distributions — design-space expansion via population-simulated resampling.",
      ],
    },
    {
      title: "Undergraduate Researcher",
      place: "MLILAB, KAIST",
      date: "Mar – Aug 2024",
      details: [
        "PEFT fine-tuning of conversational LLMs on instruction-based medical Q&A data.",
        "Designed a novel evaluation methodology for LLM output quality that mitigates GPT-4 evaluator bias and instability.",
      ],
    },
    {
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
