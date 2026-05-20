import { chromium } from 'playwright';

const endpoint = process.argv[2] ?? 'http://[::1]:9222';
const browser = await chromium.connectOverCDP(endpoint);
const contexts = browser.contexts();
const pages = contexts.flatMap((context) => context.pages());
const titles = await Promise.all(pages.slice(0, 10).map((page) => page.title()));

console.log(JSON.stringify({
  endpoint,
  contexts: contexts.length,
  pages: pages.length,
  titles,
}, null, 2));
