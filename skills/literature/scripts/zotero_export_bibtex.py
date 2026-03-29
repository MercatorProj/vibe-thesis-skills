import argparse
import os
import re
import sys
from typing import Iterable

try:
    import requests
except ImportError:
    print("Error: requests library not found. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)


_CITEKEY_RE = re.compile(r"@\w+\s*\{\s*([^,\s]+)\s*,", re.IGNORECASE)


def _build_headers(api_key: str | None) -> dict:
    if not api_key:
        return {}
    # Local API: add both headers for compatibility + zotero-allowed-request for DNS rebinding protection
    return {
        "Zotero-API-Key": api_key,
        "Authorization": f"Bearer {api_key}",
        "zotero-allowed-request": "1",
    }


def _extract_citekeys(bibtex_text: str) -> list[str]:
    return [m.group(1) for m in _CITEKEY_RE.finditer(bibtex_text)]


def _load_existing_citekeys(bib_path: str) -> set[str]:
    if not os.path.exists(bib_path):
        return set()
    with open(bib_path, "r", encoding="utf-8", errors="ignore") as f:
        text = f.read()
    return set(_extract_citekeys(text))


def export_item_bibtex(base_url: str, user_id: str, item_key: str, headers: dict, timeout_sec: int = 20) -> str:
    base_url = base_url.rstrip("/") + "/"
    url = f"{base_url}users/{user_id}/items/{item_key}?format=bibtex"
    resp = requests.get(url, headers=headers, timeout=timeout_sec)
    resp.raise_for_status()
    return resp.text


def append_unique_bibtex(bib_path: str, bibtex_blocks: Iterable[str]) -> dict:
    os.makedirs(os.path.dirname(bib_path), exist_ok=True)
    existing = _load_existing_citekeys(bib_path)
    appended = 0
    skipped = 0
    new_citekeys: list[str] = []

    with open(bib_path, "a", encoding="utf-8") as f:
        for block in bibtex_blocks:
            keys = _extract_citekeys(block)
            if not keys:
                skipped += 1
                continue
            # If any citekey already exists, skip the whole block to avoid duplicates
            if any(k in existing for k in keys):
                skipped += 1
                continue
            if not block.endswith("\n"):
                block += "\n"
            f.write("\n" + block.strip() + "\n")
            appended += 1
            for k in keys:
                existing.add(k)
                new_citekeys.append(k)

    return {"appended_blocks": appended, "skipped_blocks": skipped, "new_citekeys": new_citekeys}


def main() -> int:
    parser = argparse.ArgumentParser(description="Export Zotero items as BibTeX and append to a .bib file (dedup by citekey).")
    parser.add_argument("--base-url", default="http://localhost:23119/api/", help="Zotero Local API base URL")
    parser.add_argument("--user-id", default="0", help="User ID for local API (usually 0)")
    parser.add_argument("--api-key", default=None, help="Local API key (or env ZOTERO_LOCAL_API_KEY / ZOTERO_API_KEY)")
    parser.add_argument("--bib-path", required=True, help="Target .bib file to append to")
    parser.add_argument("--item-key", action="append", default=[], help="Zotero item key (repeatable)")
    parser.add_argument("--timeout-sec", type=int, default=20, help="HTTP timeout seconds")
    args = parser.parse_args()

    api_key = args.api_key or os.environ.get("ZOTERO_LOCAL_API_KEY") or os.environ.get("ZOTERO_API_KEY")
    if not api_key:
        print("Error: missing Zotero API key. Provide --api-key or set ZOTERO_LOCAL_API_KEY.", file=sys.stderr)
        return 2

    if not args.item_key:
        print("Error: at least one --item-key is required.", file=sys.stderr)
        return 2

    headers = _build_headers(api_key)
    blocks: list[str] = []
    for key in args.item_key:
        try:
            blocks.append(export_item_bibtex(args.base_url, args.user_id, key, headers=headers, timeout_sec=args.timeout_sec))
        except requests.RequestException as e:
            print(f"Error exporting item {key}: {e}", file=sys.stderr)
            return 1

    summary = append_unique_bibtex(args.bib_path, blocks)
    print(
        f"OK appended_blocks={summary['appended_blocks']} skipped_blocks={summary['skipped_blocks']} "
        f"new_citekeys={','.join(summary['new_citekeys'])}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

