---
runtime_projection: true
source_of_truth: registry/skills/book-image-renamer/references/decision-rules.md
---

> Runtime projection for consumer agents.
> First-read entrypoint: `runtime/skills/book-image-renamer/references/decision-rules.md`
> Source of truth: `registry/skills/book-image-renamer/references/decision-rules.md`
> Use this runtime file first. Follow rewritten registry links only when this runtime view points you there.
> Consumer scope: `skill-support`
# Decision Rules

## Rename eligibility

- Rename only when the image is confidently a single-book image.
- Do not rename when more than one book is clearly visible in the same image.
- Do not rename when any required metadata field is missing: original author, title, publisher, year, ISBN.
- Do not overwrite an existing file. If the same verified book already has earlier images in the folder, assign the next available numeric suffix instead.
- In title-first mode, title is the primary signal for deciding whether an image belongs to a known book.
- Multi-book scenes are discarded instead of being sent to manual follow-up.
- Non-cover images are discarded instead of being sent to manual follow-up.

## Metadata policy

- `author` means the original book author, not the translator, editor, or reviewer.
- Keep visible translator data in the scan report, but do not include it in the target filename.
- Prefer the edition-level publisher, year, and ISBN that match the photographed copy.
- If OCR and visual reasoning disagree, prefer the interpretation supported by both the image and the OCR text.
- In no-search mode, use only the existing curated metadata file as the source of truth.
- OCR may suggest a match, but OCR alone is not enough to invent edition metadata.
- When OCR is noisy, a strong title match is more valuable than weak author, publisher, or translator matches.

## File naming

- Base format: `原書作者-書名-出版社-年分_ISBN`
- Keep the front cover as the base filename with no numeric suffix when a group contains a clear cover image.
- For other files of the same book, append `_1`, `_2`, and so on.
- Preserve the original file extension, normalized to lowercase.

## Same-book role ordering

- Preferred base image order:
  - `front_plain`
  - `front_with_obi`
  - `back`
  - `spine`
  - `interior`
- A back cover may reuse verified metadata from a front cover or ISBN-backed group only when the title/author signal is strong enough.
- When OCR is too noisy to distinguish books by title, leave the image unresolved instead of forcing a rename.
- If an image is not a clear cover view, prefer skipping it rather than trying to rescue it with weak OCR.

## Stability rules

- Generate a scan report first.
- Fill verified metadata into the metadata template before building a rename plan.
- Execute renames only from a generated plan, never directly from raw OCR output.
- Prefer adding explicit alias entries to curated metadata over loosening fuzzy-match thresholds.
