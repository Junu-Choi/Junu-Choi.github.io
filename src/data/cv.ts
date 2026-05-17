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
  lastUpdated: "May 2026",

  education: [
    {
      title: "M.S., Interdisciplinary Program in Artificial Intelligence",
      place: "Seoul National University",
      date: "2025 – present",
    },
    {
      title: "B.S. (Double Major), School of Computing × Mathematical Sciences",
      place: "Korea Advanced Institute of Science and Technology",
      date: "2017 – 2025",
    },
  ] satisfies CVSection,

  experience: [
    {
      title: "Visiting Researcher",
      place: "Visual AI Group, KAIST",
      date: "Jan – Mar 2025",
      details: [
        "Sequential Monte Carlo for sampling complex distributions — design-space expansion via population-simulated resampling.",
      ],
    },
    {
      title: "Visiting Researcher",
      place: "MLILAB, KAIST",
      date: "Mar – Aug 2024",
      details: [
        "PEFT fine-tuning of conversational LLMs on instruction-based medical Q&A data.",
        "Designed a novel evaluation methodology for LLM output quality that mitigates GPT-4 evaluator bias and instability.",
      ],
    },
    {
      title: "AI Researcher (Speech & Multimodal)",
      place: "Humelo, Inc.",
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
      title: "Speculative decoding via intermediate features",
      place: "Personal research, KAIST",
      date: "Mar – Jun 2024",
      details: [
        "Reduced compute risk in speculative decoding via feature-distribution speculation and intermediate-feature-level decoding; combined knowledge distillation with sparse rejection.",
      ],
    },
  ] satisfies CVSection,

  awards: [
    {
      title: "Qualcomm Innovation Award",
      place: "KAIST × Qualcomm AI Hackathon",
      date: "2019",
      details: [
        "CNN-based emotion-recognition system for video.",
      ],
    },
  ] satisfies CVSection,

  skills: {
    Languages: ["Python"],
    "ML frameworks": ["PyTorch", "TensorFlow", "JAX"],
    "Scientific": ["NumPy", "SciPy", "matplotlib"],
    Tools: ["Linux/macOS", "tmux", "vim", "git"],
  } as Record<string, string[]>,
};
