import { build, context } from "esbuild";
import { cpSync, existsSync, mkdirSync, rmSync } from "node:fs";
import { resolve } from "node:path";

const root = process.cwd();
const extensionRoot = resolve(root, "extension");
const watch = process.argv.includes("--watch");
const cleanOnly = process.argv.includes("--clean");

const ensureCleanExtensionRoot = () => {
  rmSync(extensionRoot, { force: true, recursive: true });
  mkdirSync(resolve(extensionRoot, "popup"), { recursive: true });
  mkdirSync(resolve(extensionRoot, "options"), { recursive: true });
};

const copyStaticFiles = () => {
  cpSync(resolve(root, "manifest.json"), resolve(extensionRoot, "manifest.json"));
  cpSync(resolve(root, "src", "popup", "index.html"), resolve(extensionRoot, "popup", "popup.html"));
  cpSync(resolve(root, "src", "options", "index.html"), resolve(extensionRoot, "options", "options.html"));

  if (existsSync(resolve(root, "icons"))) {
    cpSync(resolve(root, "icons"), resolve(extensionRoot, "assets", "icons"), { recursive: true });
  }
};

const bundleOptions = {
  bundle: true,
  entryPoints: {
    background: resolve(root, "src", "background", "index.ts"),
    "popup/popup": resolve(root, "src", "popup", "main.ts"),
    "options/options": resolve(root, "src", "options", "main.ts")
  },
  format: "esm",
  outdir: extensionRoot,
  platform: "browser",
  sourcemap: true,
  target: "chrome120"
};

ensureCleanExtensionRoot();

if (cleanOnly) {
  console.log(`Cleaned ${extensionRoot}`);
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
  console.log(`Built Chrome extension into ${extensionRoot}`);
}
