#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import json
import os
import re
import tempfile
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import requests
from PIL import Image, ImageOps

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".bmp", ".tif", ".tiff"}
FENCE_RE = re.compile(r"```(?:json)?\s*(.*?)```", re.DOTALL | re.IGNORECASE)
INVALID_FILENAME_CHARS = r'<>:"/\|?*'
ISBN_RE = re.compile(r"(?:97[89][\-\s]?)?\d[\d\-\s]{8,}\d")
SKIP_OCR_KEYWORDS = ("晚宴", "慶祝", "荣譽", "荣誉", "博士", "大學", "大学", "學位", "学位")
OBI_HINT_KEYWORDS = (
    "推薦",
    "推荐",
    "導讀",
    "导读",
    "榮獲",
    "荣获",
    "紀念",
    "纪念",
    "電影",
    "电影",
    "改編",
    "改编",
    "新版",
    "新譯",
    "新译",
    "收錄",
    "收录",
    "典藏",
    "限量",
    "得獎",
    "得奖",
    "好評",
    "好评",
    "專序",
    "专序",
    "專文",
    "专文",
)


@dataclass
class OcrLine:
    text: str
    score: float


def utc_now_iso() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def list_images(folder: Path) -> list[Path]:
    return sorted(
        [
            path
            for path in folder.iterdir()
            if path.is_file() and path.suffix.lower() in IMAGE_EXTENSIONS
        ],
        key=lambda path: path.name.lower(),
    )


def sanitize_filename_part(value: str) -> str:
    cleaned = value.strip()
    cleaned = "".join("_" if ch in INVALID_FILENAME_CHARS else ch for ch in cleaned)
    cleaned = re.sub(r"\s+", " ", cleaned)
    cleaned = cleaned.strip(". ")
    return cleaned


def normalize_group_key(author: str | None, title: str | None) -> str | None:
    if not author or not title:
        return None
    normalized = f"{author}__{title}"
    normalized = re.sub(r"\s+", "", normalized)
    return normalized


def normalize_match_text(value: str | None) -> str:
    if not value:
        return ""
    normalized = re.sub(r"[\s:：\-—_·•○●（）()\[\]【】'\"，,。、\.]+", "", value)
    return normalized.casefold()


def text_variants(value: str | None) -> set[str]:
    if not value:
        return set()

    variants = {normalize_match_text(value)}
    trimmed = re.sub(r"[（(].*?[）)]", "", value).strip()
    if trimmed:
        variants.add(normalize_match_text(trimmed))
    for part in re.split(r"[：:]", value):
        part = part.strip()
        if part:
            variants.add(normalize_match_text(part))
    return {variant for variant in variants if len(variant) >= 1}


def metadata_title_variants(metadata: dict[str, Any]) -> set[str]:
    title = str(metadata.get("title") or "")
    variants = {normalize_match_text(title)}
    trimmed = re.sub(r"[（(].*?[）)]", "", title).strip()
    if trimmed:
        variants.add(normalize_match_text(trimmed))
    main_title = re.split(r"[：:]", title, maxsplit=1)[0].strip()
    if main_title:
        variants.add(normalize_match_text(main_title))
    normalized_title = normalize_match_text(title)

    if normalized_title == normalize_match_text("鑰匙"):
        variants.add(normalize_match_text("鍵"))
    if "萬字" in title:
        variants.add(normalize_match_text("萬字"))
        variants.add(normalize_match_text("卍"))
    if "細雪" in title:
        variants.add(normalize_match_text("細雪"))
        if "上" in title:
            variants.add(normalize_match_text("細雪上卷"))
        if "下" in title:
            variants.add(normalize_match_text("細雪下卷"))
    if "武士道" in title:
        variants.add(normalize_match_text("武士道"))

    return {variant for variant in variants if len(variant) >= 1}


def collect_ocr_texts(item: dict[str, Any]) -> list[str]:
    return [
        str(line.get("text", "")).strip()
        for line in item.get("ocr_lines", [])
        if str(line.get("text", "")).strip()
    ]


def has_close_partial_match(left: str, right: str) -> bool:
    shorter = min(len(left), len(right))
    longer = max(len(left), len(right))
    if shorter < 2:
        return False
    if shorter / longer < 0.6:
        return False
    return left in right or right in left


def titleish_line_variants(item: dict[str, Any]) -> list[str]:
    llm = item.get("llm", {})
    item_author = normalize_match_text(llm.get("visible_author"))
    variants: list[str] = []
    seen: set[str] = set()

    for text in collect_ocr_texts(item)[:8]:
        normalized = normalize_match_text(text)
        if len(normalized) < 1 or len(normalized) > 18:
            continue
        if normalized == item_author:
            continue
        if re.search(r"(譯|译|著|作|監修|监修|主編|主编)$", text):
            continue
        if len(normalized) <= 4 and any(keyword in text for keyword in ("文學", "文学", "文化", "書局", "书局", "出版社", "出版")):
            continue
        if normalized in seen:
            continue
        variants.append(normalized)
        seen.add(normalized)

    return variants


def role_priority(role: str | None) -> tuple[int, str]:
    rank = {
        "front_plain": 0,
        "front_with_obi": 1,
        "back": 2,
        "spine": 3,
        "interior": 4,
        "other": 5,
        "front-cover": 0,
        "cover": 0,
        "front": 0,
        "back-cover": 2,
    }
    role_text = (role or "other").lower()
    return (rank.get(role_text, 9), role_text)


def infer_effective_role(item: dict[str, Any]) -> str:
    llm_role = str(item.get("llm", {}).get("role") or "").lower()
    if llm_role in {"spine", "interior"}:
        return llm_role

    line_texts = collect_ocr_texts(item)
    ocr_text = "\n".join(line_texts)
    isbn_candidates = extract_isbn_candidates(ocr_text)
    long_line_count = sum(len(normalize_match_text(text)) >= 16 for text in line_texts)
    short_title_like_count = sum(
        2 <= len(normalize_match_text(text)) <= 14 and mostly_cjk(text)
        for text in line_texts[:8]
    )
    has_obi_copy = any(keyword in ocr_text for keyword in OBI_HINT_KEYWORDS)

    if isbn_candidates or llm_role == "back-cover":
        return "back"
    if long_line_count >= 5 and short_title_like_count <= 1:
        return "back"
    if has_obi_copy and short_title_like_count >= 1:
        return "front_with_obi"
    if llm_role in {"front-cover", "cover", "front"} or short_title_like_count >= 1:
        return "front_plain"
    return "other"


def score_metadata_match(item: dict[str, Any], metadata: dict[str, Any]) -> int:
    llm = item.get("llm", {})
    ocr_texts = collect_ocr_texts(item)
    ocr_blob = normalize_match_text(" ".join(ocr_texts))
    llm_title = normalize_match_text(llm.get("visible_title"))
    llm_author = normalize_match_text(llm.get("visible_author"))
    top_line_variants = titleish_line_variants(item)
    title_variants = metadata_title_variants(metadata)
    author_variants = text_variants(metadata.get("author"))
    isbn = str(metadata.get("isbn") or "")
    score = 0

    for variant in title_variants:
        if llm_title and llm_title == variant:
            score = max(score, 10)
        elif llm_title and has_close_partial_match(llm_title, variant):
            score = max(score, 8)

        if any(line == variant for line in top_line_variants):
            score = max(score, 9)
        elif any(has_close_partial_match(line, variant) for line in top_line_variants):
            score = max(score, 7)
        elif len(variant) >= 2 and variant in ocr_blob:
            score = max(score, 5)

    if score == 0:
        return 0

    for variant in author_variants:
        if llm_author and llm_author == variant:
            score += 3
            break
        if llm_author and has_close_partial_match(llm_author, variant):
            score += 2
            break
        if variant and variant in ocr_blob:
            score += 2
            break

    if isbn and isbn in extract_isbn_candidates("\n".join(ocr_texts)):
        score += 12

    return score


def best_metadata_match(
    item: dict[str, Any],
    complete_metadata: list[dict[str, Any]],
) -> dict[str, Any] | None:
    scored: list[tuple[int, dict[str, Any]]] = []
    for metadata in complete_metadata:
        score = score_metadata_match(item, metadata)
        if score > 0:
            scored.append((score, metadata))

    if not scored:
        return None

    scored.sort(
        key=lambda pair: (
            pair[0],
            str(pair[1].get("author") or ""),
            str(pair[1].get("title") or ""),
            str(pair[1].get("isbn") or ""),
        ),
        reverse=True,
    )
    best_score, best_metadata = scored[0]
    second_score = scored[1][0] if len(scored) > 1 else -999
    if best_score < 8:
        return None
    if best_score - second_score < 3:
        return None
    return best_metadata


def extract_isbn_candidates(text: str) -> list[str]:
    candidates = []
    for raw_line in text.splitlines():
        line = raw_line.replace('"', "").replace("ISBN", "").replace("isbn", "")
        for match in ISBN_RE.findall(line):
            compact = re.sub(r"[\-\s]", "", match)
            if len(compact) in {10, 13}:
                candidates.append(compact)
    return sorted(set(candidates))


def image_size(image_path: Path) -> tuple[int, int]:
    with Image.open(image_path) as image:
        return image.size


def quick_route(image_path: Path, ocr_lines: list[OcrLine]) -> str:
    width, height = image_size(image_path)
    ocr_text = "\n".join(line.text for line in ocr_lines)
    if extract_isbn_candidates(ocr_text):
        return "candidate"
    if width > height and (not ocr_text or any(keyword in ocr_text for keyword in SKIP_OCR_KEYWORDS)):
        return "skip"
    if width > height and len(ocr_text) < 24:
        return "skip"
    if height >= width and len(ocr_lines) >= 2:
        return "candidate"
    return "review"


def mostly_cjk(text: str) -> bool:
    content = re.sub(r"\s+", "", text)
    if not content:
        return False
    cjk_count = sum(
        1
        for ch in content
        if "\u3400" <= ch <= "\u9fff" or "\u3040" <= ch <= "\u30ff"
    )
    return cjk_count / len(content) >= 0.6


def ocr_based_analysis(ocr_lines: list[OcrLine], route: str) -> dict[str, Any]:
    ocr_text = "\n".join(line.text for line in ocr_lines)
    isbn_candidates = extract_isbn_candidates(ocr_text)
    title_candidates: list[str] = []
    author_candidates: list[str] = []
    translator = None

    for line in ocr_lines:
        text = line.text.strip()
        translator_match = re.search(r"([^\s]{2,20})(譯|译|主編|主编)$", text)
        if translator_match:
            translator = translator_match.group(1)
            continue

        author_match = re.search(r"([^\s]{2,20})(原著|著|作)$", text)
        if author_match:
            author_candidates.append(author_match.group(1))
            continue

        compact = re.sub(r"[·•●○\-—_ 　]", "", text)
        if 1 <= len(compact) <= 12 and mostly_cjk(text):
            title_candidates.append(text)
            if 2 <= len(compact) <= 8:
                author_candidates.append(text)

    title = title_candidates[0] if title_candidates else None
    author = author_candidates[-1] if author_candidates else None
    role = "back-cover" if isbn_candidates else "front-cover"
    confidence = 0.85 if route == "candidate" else 0.6
    notes = "Derived from OCR heuristics."

    return {
        "is_book_image": route != "skip",
        "book_count": 1 if route != "skip" else 0,
        "visible_title": title,
        "visible_author": author if author != title else None,
        "visible_translator": translator,
        "visible_publisher": None,
        "visible_year": None,
        "visible_isbn": isbn_candidates[0] if isbn_candidates else None,
        "role": role if route != "skip" else "other",
        "confidence": confidence,
        "notes": notes,
    }


class PaddleOcrEngine:
    def __init__(self) -> None:
        os.environ.setdefault("PADDLE_PDX_DISABLE_MODEL_SOURCE_CHECK", "True")
        from paddleocr import PaddleOCR

        self.engine = PaddleOCR(
            lang="ch",
            use_doc_orientation_classify=False,
            use_doc_unwarping=False,
            use_textline_orientation=False,
        )

    def _prepare_image(self, image_path: Path) -> Path:
        with Image.open(image_path) as image:
            prepared = ImageOps.exif_transpose(image).convert("RGB")
            with tempfile.NamedTemporaryFile(
                prefix="book_ocr_",
                suffix=".jpg",
                delete=False,
            ) as handle:
                temp_path = Path(handle.name)
            prepared.save(temp_path, format="JPEG", quality=95, optimize=True)
        return temp_path

    def extract(self, image_path: Path) -> list[OcrLine]:
        prepared_path = self._prepare_image(image_path)
        try:
            result = self.engine.predict(str(prepared_path))
            if not result:
                return []

            first = result[0]
            texts = first.get("rec_texts") or []
            scores = first.get("rec_scores") or []
            lines: list[OcrLine] = []
            for text, score in zip(texts, scores):
                text_value = str(text).strip()
                if not text_value:
                    continue
                lines.append(OcrLine(text=text_value, score=float(score)))
            return lines
        finally:
            prepared_path.unlink(missing_ok=True)


class HereticClient:
    def __init__(
        self,
        base_url: str = "http://127.0.0.1:1234/v1",
        model: str = "gemma-4-e4b-it-heretic",
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model

    def available(self) -> bool:
        try:
            response = requests.get(f"{self.base_url}/models", timeout=5)
            response.raise_for_status()
            data = response.json()
            models = {item.get("id") for item in data.get("data", [])}
            return self.model in models
        except Exception:
            return False

    def analyze(self, image_path: Path, ocr_lines: list[OcrLine]) -> dict[str, Any]:
        ocr_text = "\n".join(line.text for line in ocr_lines[:40])
        prompt = (
            "You validate OCR for possible book photos. "
            "Return JSON only with keys: "
            "is_book_image (boolean), "
            "book_count (integer), "
            "visible_title (string or null), "
            "visible_author (string or null), "
            "visible_translator (string or null), "
            "visible_publisher (string or null), "
            "visible_year (string or null), "
            "visible_isbn (string or null), "
            "role (front-cover|back-cover|spine|interior|other), "
            "confidence (0-1 number), "
            "notes (short string). "
            "If the image is mainly an event photo, signboard, room scene, or people, set is_book_image to false "
            "unless a physical book cover, spine, or open page is the clear main subject. "
            "Treat images with more than one clearly visible book as book_count > 1. "
            "Use the OCR text as a hint, but correct OCR mistakes when the image is clear. "
            f"\nOCR text:\n{ocr_text}"
        )
        image_b64 = base64.b64encode(image_path.read_bytes()).decode("ascii")
        payload = {
            "model": self.model,
            "temperature": 0.1,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt},
                        {
                            "type": "image_url",
                            "image_url": {"url": f"data:image/jpeg;base64,{image_b64}"},
                        },
                    ],
                }
            ],
        }
        response = requests.post(
            f"{self.base_url}/chat/completions",
            json=payload,
            timeout=180,
        )
        response.raise_for_status()
        content = response.json()["choices"][0]["message"]["content"]
        return parse_json_block(content)


def parse_json_block(content: str) -> dict[str, Any]:
    match = FENCE_RE.search(content)
    candidate = match.group(1) if match else content
    return json.loads(candidate)


def search_urls(title: str | None, author: str | None) -> list[str]:
    parts = [part for part in [title, author] if part]
    if not parts:
        return []
    query = " ".join(parts)
    encoded = requests.utils.quote(query)
    return [
        f"https://duckduckgo.com/?q={encoded}",
        f"https://www.google.com/search?q={encoded}",
    ]


def scan_folder(
    folder: Path,
    limit: int | None = None,
    start_index: int = 0,
    verbose: bool = False,
) -> dict[str, Any]:
    images = list_images(folder)
    if start_index:
        images = images[start_index:]
    if limit is not None:
        images = images[:limit]

    ocr_engine = PaddleOcrEngine()
    heretic = HereticClient()
    heretic_available = heretic.available()
    results: list[dict[str, Any]] = []
    groups: dict[str, list[str]] = {}

    for index, image_path in enumerate(images, start=1):
        started_at = time.perf_counter()
        if verbose:
            print(f"[scan] {index}/{len(images)} {image_path.name}", flush=True)
        try:
            ocr_lines = ocr_engine.extract(image_path)
            ocr_error = None
        except Exception as exc:
            ocr_lines = []
            ocr_error = str(exc)

        route = quick_route(image_path, ocr_lines)
        ocr_text = "\n".join(line.text for line in ocr_lines)
        isbn_candidates = extract_isbn_candidates(ocr_text)

        if route == "skip":
            llm = {
                "is_book_image": False,
                "book_count": 0,
                "visible_title": None,
                "visible_author": None,
                "visible_translator": None,
                "visible_publisher": None,
                "visible_year": None,
                "visible_isbn": isbn_candidates[0] if isbn_candidates else None,
                "role": "other",
                "confidence": 0.9,
                "notes": "Skipped Heretic by fast OCR/image heuristic.",
            }
            llm_error = None
        elif route == "candidate":
            llm = ocr_based_analysis(ocr_lines, route)
            llm_error = "Heretic not invoked for candidate route"
        elif heretic_available:
            try:
                llm = heretic.analyze(image_path, ocr_lines)
                llm_error = None
            except Exception as exc:
                llm = {}
                llm_error = str(exc)
        else:
            llm = {}
            llm_error = "Heretic endpoint unavailable"

        if isbn_candidates and not llm.get("visible_isbn"):
            llm["visible_isbn"] = isbn_candidates[0]

        author = llm.get("visible_author")
        title = llm.get("visible_title")
        isbn = llm.get("visible_isbn")
        group_key = f"isbn__{isbn}" if isbn else normalize_group_key(author, title)
        if group_key is None and title:
            compact_title = re.sub(r"\s+", "", title)
            group_key = f"title__{compact_title}"
        if group_key:
            groups.setdefault(group_key, []).append(str(image_path))

        status = "review"
        if llm.get("is_book_image") is False:
            status = "skip"
        elif llm.get("is_book_image") and int(llm.get("book_count", 0) or 0) == 1 and title:
            status = "candidate"

        results.append(
            {
                "source_path": str(image_path),
                "source_name": image_path.name,
                "elapsed_seconds": round(time.perf_counter() - started_at, 3),
                "ocr_lines": [asdict(line) for line in ocr_lines],
                "ocr_error": ocr_error,
                "llm": llm,
                "llm_error": llm_error,
                "candidate_group_key": group_key,
                "fast_route": route,
                "status": status,
                "search_urls": search_urls(title, author),
                "metadata_needed": {
                    "author": author,
                    "title": title,
                    "publisher": None,
                    "year": None,
                    "isbn": isbn,
                },
                "suggested_target_name": None,
                "applied_target_name": None,
                "scan_index": index,
            }
        )

    return {
        "generated_at": utc_now_iso(),
        "folder": str(folder),
        "heretic_available": heretic_available,
        "images": results,
        "groups": groups,
        "metadata_template": {
            "groups": {
                group_key: {
                    "author": None,
                    "title": None,
                    "publisher": None,
                    "year": None,
                    "isbn": None,
                }
                for group_key in sorted(groups)
            }
        },
    }


def metadata_matches_item(item: dict[str, Any], metadata: dict[str, Any]) -> bool:
    return score_metadata_match(item, metadata) >= 8


def assign_target_names(scan_data: dict[str, Any], metadata_data: dict[str, Any]) -> dict[str, Any]:
    group_meta = metadata_data.get("groups", {})
    resolved_candidates: dict[str, list[dict[str, Any]]] = {}
    resolved_metadata: dict[str, dict[str, Any]] = {}
    passthrough: list[dict[str, Any]] = []
    required = ["author", "title", "publisher", "year", "isbn"]
    complete_metadata_by_signature = {
        "||".join(str(metadata[field]) for field in required): metadata
        for metadata in group_meta.values()
        if all(metadata.get(field) for field in required)
    }
    complete_metadata = list(complete_metadata_by_signature.values())
    existing_names = {
        path.name
        for path in list_images(Path(scan_data["folder"]))
    }

    for item in scan_data["images"]:
        cloned = dict(item)
        cloned["rename_reason"] = None
        cloned["suggested_target_name"] = None
        cloned["effective_role"] = infer_effective_role(cloned)
        group_key = cloned.get("candidate_group_key")
        if cloned["status"] != "candidate":
            passthrough.append(cloned)
            continue

        metadata = group_meta.get(group_key)
        if metadata and all(metadata.get(field) for field in required):
            matched_metadata = metadata
        else:
            matched_metadata = best_metadata_match(cloned, complete_metadata)

        if not matched_metadata:
            missing = []
            if metadata:
                missing = [field for field in required if not metadata.get(field)]
            cloned["rename_reason"] = (
                f"Missing metadata: {', '.join(missing)}"
                if missing
                else "No verified metadata match"
            )
            passthrough.append(cloned)
            continue

        metadata = matched_metadata
        signature = "||".join(str(metadata[field]) for field in required)
        resolved_candidates.setdefault(signature, []).append(cloned)
        resolved_metadata[signature] = metadata

    renamed: list[dict[str, Any]] = []
    for signature, items in resolved_candidates.items():
        metadata = resolved_metadata[signature]
        author = sanitize_filename_part(str(metadata["author"]))
        title = sanitize_filename_part(str(metadata["title"]))
        publisher = sanitize_filename_part(str(metadata["publisher"]))
        year = sanitize_filename_part(str(metadata["year"]))
        isbn = sanitize_filename_part(str(metadata["isbn"]))
        sorted_items = sorted(
            items,
            key=lambda item: (
                role_priority(item.get("effective_role") or item.get("llm", {}).get("role")),
                item["source_name"].lower(),
            ),
        )
        base = f"{author}-{title}-{publisher}-{year}_{isbn}"
        next_suffix = 0
        for item in sorted_items:
            source_path = Path(item["source_path"])
            while True:
                suffix = "" if next_suffix == 0 else f"_{next_suffix}"
                candidate_name = f"{base}{suffix}{source_path.suffix.lower()}"
                if candidate_name == source_path.name or candidate_name not in existing_names:
                    item["suggested_target_name"] = candidate_name
                    existing_names.add(candidate_name)
                    break
                next_suffix += 1
            next_suffix += 1
            renamed.append(item)

    merged = passthrough + renamed
    merged.sort(key=lambda item: item["scan_index"])
    return {
        "generated_at": utc_now_iso(),
        "folder": scan_data["folder"],
        "images": merged,
    }


def execute_renames(plan_data: dict[str, Any]) -> dict[str, Any]:
    for item in plan_data["images"]:
        target_name = item.get("suggested_target_name")
        if not target_name:
            continue
        source_path = Path(item["source_path"])
        target_path = source_path.with_name(target_name)
        if target_path.exists() and target_path != source_path:
            item["rename_reason"] = f"Target already exists: {target_name}"
            continue
        if source_path.name == target_name:
            item["applied_target_name"] = target_name
            continue
        source_path.rename(target_path)
        item["applied_target_name"] = target_name
        item["source_path"] = str(target_path)
        item["source_name"] = target_path.name
    plan_data["generated_at"] = utc_now_iso()
    return plan_data


def save_json(path: Path, payload: dict[str, Any]) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scan book images and build safe rename plans.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scan_parser = subparsers.add_parser("scan", help="Analyze a folder and produce a scan report.")
    scan_parser.add_argument("folder", type=Path)
    scan_parser.add_argument("--limit", type=int, default=None)
    scan_parser.add_argument("--start-index", type=int, default=0)
    scan_parser.add_argument("--verbose", action="store_true")
    scan_parser.add_argument(
        "--output",
        type=Path,
        default=Path("book_rename_scan.json"),
    )

    plan_parser = subparsers.add_parser("plan", help="Combine a scan report with verified metadata.")
    plan_parser.add_argument("scan_json", type=Path)
    plan_parser.add_argument("metadata_json", type=Path)
    plan_parser.add_argument(
        "--output",
        type=Path,
        default=Path("book_rename_plan.json"),
    )

    apply_parser = subparsers.add_parser("apply", help="Execute renames from a generated plan.")
    apply_parser.add_argument("plan_json", type=Path)
    apply_parser.add_argument(
        "--output",
        type=Path,
        default=Path("book_rename_applied.json"),
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "scan":
        payload = scan_folder(args.folder, args.limit, args.start_index, args.verbose)
        save_json(args.output, payload)
        print(f"Wrote scan report: {args.output}")
        return

    if args.command == "plan":
        scan_data = load_json(args.scan_json)
        metadata_data = load_json(args.metadata_json)
        payload = assign_target_names(scan_data, metadata_data)
        save_json(args.output, payload)
        print(f"Wrote rename plan: {args.output}")
        return

    if args.command == "apply":
        plan_data = load_json(args.plan_json)
        payload = execute_renames(plan_data)
        save_json(args.output, payload)
        print(f"Wrote applied report: {args.output}")
        return


if __name__ == "__main__":
    main()
