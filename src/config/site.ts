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
    { label: "github", href: "https://github.com/Junu-Choi" },
    { label: "orcid",  href: "https://orcid.org/0009-0005-6979-9505" },
    // scholar: add once papers accumulate citations and the auto-profile forms.
    // arxiv:   add after first submission. Public author URL is
    //          https://arxiv.org/a/<author_id> — find it at https://arxiv.org/user/
    //          after a paper is posted.
  ],
} as const;
