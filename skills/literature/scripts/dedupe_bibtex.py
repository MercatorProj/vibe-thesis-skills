# -*- coding: utf-8 -*-
"""Merge multiple .bib files and drop duplicate entries.

Deduplication key (first match wins, later duplicates skipped):
  1) DOI (normalized: lower, strip https://doi.org/ prefix)
  2) Else normalized title + year (weak; review conflicts manually)

No network access. Stdlib only.
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def _split_entries(text: str) -> list[str]:
    text = text.strip()
    if not text:
        return []
    # Entries typically start with @Article{key, ... at line beginning
    parts = re.split(r"(?m)^(?=@)", text)
    return [p.strip() for p in parts if p.strip().startswith("@")]


def _field_brace_or_quote(block: str, name: str) -> str | None:
    """Extract first simple field value { ... } or " ... " for name = value."""
    # name = {content} — non-greedy, one level (nested braces may break)
    m = re.search(
        rf"{name}\s*=\s*\{{([^}}]*)\}}",
        block,
        flags=re.IGNORECASE | re.DOTALL,
    )
    if m:
        return m.group(1).strip()
    m = re.search(rf'{name}\s*=\s*"([^"]*)"', block, flags=re.IGNORECASE | re.DOTALL)
    if m:
        return m.group(1).strip()
    return None


def _normalize_doi(raw: str | None) -> str | None:
    if not raw:
        return None
    s = raw.strip().lower()
    s = re.sub(r"^https?://(dx\.)?doi\.org/", "", s)
    s = s.strip().rstrip(".,;)")
    return s or None


def _normalize_title(raw: str | None) -> str:
    if not raw:
        return ""
    s = raw.lower()
    s = re.sub(r"\s+", " ", s)
    s = re.sub(r"[^\w\u4e00-\u9fff\s]", "", s)
    return s.strip()


def _entry_key(entry: str) -> tuple[str, str]:
    """Return (kind, value) where kind is 'doi' or 'titleyear'."""
    doi = _normalize_doi(_field_brace_or_quote(entry, "doi"))
    if doi:
        return ("doi", doi)
    title = _field_brace_or_quote(entry, "title") or ""
    year = _field_brace_or_quote(entry, "year") or ""
    m = re.search(r"\b(19|20)\d{2}\b", year)
    yr = m.group(0) if m else year.strip()[:4]
    return ("titleyear", f"{_normalize_title(title)}|{yr}")


def merge_dedupe(files: list[Path]) -> tuple[str, int, int]:
    seen: set[tuple[str, str]] = set()
    out_blocks: list[str] = []
    total = 0
    dropped = 0
    for path in files:
        raw = path.read_text(encoding="utf-8", errors="replace")
        for ent in _split_entries(raw):
            total += 1
            k = _entry_key(ent)
            if k in seen:
                dropped += 1
                continue
            seen.add(k)
            out_blocks.append(ent.rstrip() + "\n")
    merged = "\n".join(out_blocks)
    if merged and not merged.endswith("\n"):
        merged += "\n"
    return merged, total, dropped


def main() -> None:
    parser = argparse.ArgumentParser(description="Merge BibTeX files and remove duplicates.")
    parser.add_argument(
        "bib_files",
        nargs="+",
        type=Path,
        help="Input .bib files (order preserved for first-seen entries)",
    )
    parser.add_argument("-o", "--output", type=Path, required=True, help="Output .bib path")
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print counts only, do not write",
    )
    args = parser.parse_args()
    for p in args.bib_files:
        if not p.is_file():
            print(f"Error: not a file: {p}", file=sys.stderr)
            sys.exit(1)
    merged, total, dropped = merge_dedupe(args.bib_files)
    if args.dry_run:
        print(f"entries_read={total} duplicates_dropped={dropped} kept={total - dropped}")
        return
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(merged, encoding="utf-8")
    print(f"Wrote {args.output} (kept {total - dropped} of {total} entries, dropped {dropped})")


if __name__ == "__main__":
    main()
