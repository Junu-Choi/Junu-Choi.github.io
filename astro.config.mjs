// @ts-check
import { defineConfig } from 'astro/config';
import mdx from '@astrojs/mdx';
import remarkMath from 'remark-math';
import rehypeKatex from 'rehype-katex';

// https://astro.build/config
export default defineConfig({
  site: 'https://junu-choi.github.io',
  // user/org pages serve from root, no `base` needed
  trailingSlash: 'always',
  build: {
    format: 'directory',
  },
  integrations: [
    mdx({
      remarkPlugins: [remarkMath],
      rehypePlugins: [rehypeKatex],
      shikiConfig: {
        theme: 'github-light',
        wrap: true,
      },
    }),
  ],
});
