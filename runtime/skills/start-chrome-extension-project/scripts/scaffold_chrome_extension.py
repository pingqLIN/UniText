from __future__ import annotations

import argparse
import re
import shutil
from datetime import datetime, UTC
from pathlib import Path


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "chrome-extension-project"


def replace_tokens(text: str, replacements: dict[str, str]) -> str:
    for key, value in replacements.items():
        text = text.replace(key, value)
    return text


def is_text_file(path: Path) -> bool:
    text_suffixes = {
        ".json",
        ".md",
        ".ts",
        ".mjs",
        ".html",
        ".txt",
        ".yaml",
        ".yml",
    }
    return path.suffix in text_suffixes or path.name == ".gitignore"


def scaffold(source: Path, target: Path, replacements: dict[str, str]) -> None:
    if target.exists() and any(target.iterdir()):
        raise SystemExit(f"Target directory is not empty: {target}")

    target.mkdir(parents=True, exist_ok=True)

    for item in source.rglob("*"):
        relative = item.relative_to(source)
        destination = target / relative

        if item.is_dir():
            destination.mkdir(parents=True, exist_ok=True)
            continue

        destination.parent.mkdir(parents=True, exist_ok=True)

        if is_text_file(item):
            destination.write_text(
                replace_tokens(item.read_text(encoding="utf-8"), replacements),
                encoding="utf-8",
            )
            continue

        shutil.copy2(item, destination)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a Chrome extension project from the bundled starter template."
    )
    parser.add_argument("--target", required=True, help="Target project directory")
    parser.add_argument("--name", required=True, help="Extension display name")
    parser.add_argument(
        "--description",
        required=True,
        help="Short extension description used in manifest and README",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    skill_dir = Path(__file__).resolve().parents[1]
    template_dir = skill_dir / "assets" / "template"
    target_dir = Path(args.target).resolve()
    project_slug = slugify(args.name)
    replacements = {
        "__EXTENSION_NAME__": args.name,
        "__EXTENSION_DESCRIPTION__": args.description,
        "__PROJECT_SLUG__": project_slug,
        "__YEAR__": str(datetime.now(UTC).year),
    }

    scaffold(template_dir, target_dir, replacements)
    print(f"Scaffolded Chrome extension starter at: {target_dir}")
    print(f"Project slug: {project_slug}")


if __name__ == "__main__":
    main()
