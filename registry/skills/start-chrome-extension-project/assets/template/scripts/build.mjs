import { build, context } from "esbuild";
import { cpSync, existsSync, mkdirSync, rmSync } from "node:fs";
import { resolve } from "node:path";

const root = process.cwd();
const dist = resolve(root, "dist");
const watch = process.argv.includes("--watch");
const cleanOnly = process.argv.includes("--clean");

const ensureCleanDist = () => {
  rmSync(dist, { force: true, recursive: true });
  mkdirSync(dist, { recursive: true });
};

const copyStaticFiles = () => {
  cpSync(resolve(root, "manifest.json"), resolve(dist, "manifest.json"));
  cpSync(resolve(root, "README.md"), resolve(dist, "README.md"));
  cpSync(resolve(root, "src", "popup", "index.html"), resolve(dist, "popup.html"));
  cpSync(resolve(root, "src", "options", "index.html"), resolve(dist, "options.html"));

  if (existsSync(resolve(root, "docs"))) {
    cpSync(resolve(root, "docs"), resolve(dist, "docs"), { recursive: true });
  }

  if (existsSync(resolve(root, "icons"))) {
    cpSync(resolve(root, "icons"), resolve(dist, "icons"), { recursive: true });
  }
};

const bundleOptions = {
  bundle: true,
  entryPoints: {
    background: resolve(root, "src", "background", "index.ts"),
    content: resolve(root, "src", "content", "index.ts"),
    popup: resolve(root, "src", "popup", "main.ts"),
    options: resolve(root, "src", "options", "main.ts")
  },
  format: "esm",
  outdir: dist,
  platform: "browser",
  sourcemap: true,
  target: "chrome120"
};

ensureCleanDist();

if (cleanOnly) {
  console.log(`Cleaned ${dist}`);
  process.exit(0);
}

if (watch) {
  const watcher = await context(bundleOptions);
  await watcher.watch();
  copyStaticFiles();
  console.log("Watching Chrome extension sources...");
} else {
  await build(bundleOptions);
  copyStaticFiles();
  console.log(`Built Chrome extension into ${dist}`);
}
