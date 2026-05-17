export const site = {
  name: "Junu Choi",
  affiliation: "Graduate student, IPAI, Seoul National University",
  affiliationShort: "IPAI · SNU",
  email: "junu.choi.research@gmail.com",
  emailDisplay: "junu.choi.research",
  url: "https://junu-choi.github.io",
  lastUpdated: "2026 May",

  nav: [
    { label: "about",  href: "/" },
    { label: "papers", href: "/papers/" },
    { label: "notes",  href: "/notes/" },
    { label: "cv",     href: "/cv/" },
  ],

  externalLinks: [
    { label: "github",  href: "https://github.com/Junu-Choi" },
    { label: "scholar", href: "https://scholar.google.com/" },
    // arxiv: re-enable after first submission. Use the public author URL,
    //   https://arxiv.org/a/<author_id>  (e.g. choi_j_47 — find it via
    //   https://arxiv.org/user/ once a paper is posted).
  ],
} as const;
