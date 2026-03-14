#!/usr/bin/env python3
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "requests",
#     "python-dotenv",
# ]
# ///
"""Sync local Markdown files to Notion pages.

Creates a Notion page for each .md file under the given parent page.
Automatically uploads local images referenced in the markdown.
"""

import argparse
import mimetypes
import re
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv(dotenv_path=Path.cwd() / ".env")
load_dotenv()  # fallback: walk up to find .env

NOTION_API = "https://api.notion.com/v1"
NOTION_VERSION = "2025-09-03"

IMAGE_PATTERN = re.compile(r"!\[([^\]]*)\]\(([^)]+)\)")


def resolve_token(cli_token: str | None) -> str:
    """Resolve Notion token: CLI arg → env var → error."""
    import os

    if cli_token:
        return cli_token

    env_token = os.environ.get("NOTION_TOKEN")
    if env_token:
        return env_token

    print("Error: No Notion token found.", file=sys.stderr)
    print("  Provide --token or set NOTION_TOKEN in .env", file=sys.stderr)
    sys.exit(1)


def _parse_page_id(raw: str) -> str:
    """Extract and normalize a Notion page ID from a UUID or URL.

    Supports:
    - UUID with dashes: 16a90b30-2399-809c-9dfa-dd5bd40ac798
    - UUID without dashes: 16a90b302399809c9dfadd5bd40ac798
    - Notion URL: https://www.notion.so/Page-16a90b302399809c9dfadd5bd40ac798
    - Notion URL with query: ...?pvs=4

    Returns a dash-formatted UUID string.
    """
    # Try dash-formatted UUID first
    uuid_match = re.search(
        r"[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}",
        raw,
        re.IGNORECASE,
    )
    if uuid_match:
        return uuid_match.group(0).lower()

    # Try 32 contiguous hex chars (no dashes) in the original string
    hex32 = re.search(r"[0-9a-f]{32}", raw, re.IGNORECASE)
    if hex32 is None:
        print(f"Error: Cannot extract page ID from: {raw}", file=sys.stderr)
        sys.exit(1)

    h = hex32.group(0).lower()
    return f"{h[:8]}-{h[8:12]}-{h[12:16]}-{h[16:20]}-{h[20:]}"


def resolve_parent_page_id(cli_id: str | None) -> str:
    """Resolve parent page ID: CLI arg → env var → error."""
    import os

    raw = cli_id or os.environ.get("NOTION_PARENT_PAGE_ID")
    if not raw:
        print("Error: No parent page ID found.", file=sys.stderr)
        print(
            "  Provide --parent-page-id or set NOTION_PARENT_PAGE_ID in .env",
            file=sys.stderr,
        )
        sys.exit(1)
    return _parse_page_id(raw)


def make_headers(token: str, content_type: str | None = "application/json") -> dict:
    headers = {
        "Authorization": f"Bearer {token}",
        "Notion-Version": NOTION_VERSION,
    }
    if content_type:
        headers["Content-Type"] = content_type
    return headers


def title_from_filename(filename: str) -> str:
    """Generate a page title from a markdown filename.

    Examples:
        1_3_preprocessing.md  → "1.3 Preprocessing"
        2_1_vectordb_build.md → "2.1 Vectordb Build"
        my_notes.md           → "My Notes"
    """
    stem = Path(filename).stem
    parts = stem.split("_", 2)
    if len(parts) >= 3 and parts[0].isdigit() and parts[1].isdigit():
        section = f"{parts[0]}.{parts[1]}"
        name = parts[2].replace("_", " ").title()
        return f"{section} {name}"
    return stem.replace("_", " ").title()


def parse_images_from_markdown(md_text: str) -> list[dict]:
    """Extract image references from markdown.

    Returns list of {"alt": ..., "path": ...} in order of appearance.
    """
    images = []
    for m in IMAGE_PATTERN.finditer(md_text):
        alt, path = m.group(1), m.group(2)
        # Skip URLs — only handle local paths
        if path.startswith(("http://", "https://", "data:")):
            continue
        images.append({"alt": alt, "path": path})
    return images


def find_existing_pages(token: str, parent_page_id: str, title: str) -> list[str]:
    """Find existing child pages under parent with the given title.

    Returns list of page IDs that match.
    """
    matching_ids: list[str] = []
    # Search by title, then filter by parent
    resp = requests.post(
        f"{NOTION_API}/search",
        headers=make_headers(token),
        json={
            "query": title,
            "filter": {"value": "page", "property": "object"},
            "page_size": 100,
        },
    )
    resp.raise_for_status()
    for page in resp.json().get("results", []):
        # Must be a direct child of the target parent
        page_parent = page.get("parent", {})
        if (
            page_parent.get("type") != "page_id"
            or page_parent.get("page_id") != parent_page_id
        ):
            continue
        # Must not be trashed
        if page.get("in_trash"):
            continue
        # Title must match exactly
        title_prop = page.get("properties", {}).get("title", {}).get("title", [])
        page_title = "".join(t.get("plain_text", "") for t in title_prop)
        if page_title == title:
            matching_ids.append(page["id"])
    return matching_ids


def archive_page(token: str, page_id: str) -> None:
    """Move a page to trash."""
    resp = requests.patch(
        f"{NOTION_API}/pages/{page_id}",
        headers=make_headers(token),
        json={"in_trash": True},
    )
    resp.raise_for_status()


def create_page(token: str, parent_page_id: str, title: str, markdown: str) -> dict:
    """Create a Notion page with markdown content."""
    payload = {
        "parent": {"type": "page_id", "page_id": parent_page_id},
        "properties": {
            "title": {"title": [{"type": "text", "text": {"content": title}}]}
        },
        "markdown": markdown,
    }
    resp = requests.post(
        f"{NOTION_API}/pages",
        headers=make_headers(token),
        json=payload,
    )
    resp.raise_for_status()
    return resp.json()


def get_all_blocks(token: str, page_id: str) -> list[dict]:
    """Retrieve all child blocks of a page (handles pagination)."""
    blocks = []
    url = f"{NOTION_API}/blocks/{page_id}/children?page_size=100"
    while url:
        resp = requests.get(url, headers=make_headers(token))
        resp.raise_for_status()
        data = resp.json()
        blocks.extend(data.get("results", []))
        cursor = data.get("next_cursor")
        url = (
            f"{NOTION_API}/blocks/{page_id}/children?page_size=100&start_cursor={cursor}"
            if cursor
            else None
        )
    return blocks


def find_broken_image_blocks(blocks: list[dict]) -> list[dict]:
    """Find image blocks with empty external URL (broken images)."""
    broken = []
    for block in blocks:
        if block.get("type") != "image":
            continue
        img = block.get("image", {})
        if img.get("type") == "external" and img.get("external", {}).get("url") == "":
            broken.append(block)
    return broken


def get_block_caption_text(block: dict) -> str:
    """Extract plain text from an image block's caption."""
    caption = block.get("image", {}).get("caption", [])
    return "".join(t.get("plain_text", "") for t in caption)


def upload_file(token: str, filepath: Path) -> str:
    """Upload a local file to Notion. Returns file_upload_id."""
    content_type = mimetypes.guess_type(str(filepath))[0] or "application/octet-stream"

    # Step 1: Create file upload
    resp = requests.post(
        f"{NOTION_API}/file_uploads",
        headers=make_headers(token),
        json={"name": filepath.name, "content_type": content_type},
    )
    resp.raise_for_status()
    upload_id = resp.json()["id"]

    # Step 2: Send the file bytes
    with open(filepath, "rb") as f:
        resp2 = requests.post(
            f"{NOTION_API}/file_uploads/{upload_id}/send",
            headers=make_headers(token, content_type=None),
            files={"file": (filepath.name, f, content_type)},
        )
    resp2.raise_for_status()
    return upload_id


def patch_image_block(token: str, block_id: str, file_upload_id: str) -> None:
    """Patch an image block to use a Notion file upload."""
    resp = requests.patch(
        f"{NOTION_API}/blocks/{block_id}",
        headers=make_headers(token),
        json={"image": {"file_upload": {"id": file_upload_id}}},
    )
    resp.raise_for_status()


def fix_images_for_page(
    token: str, page_id: str, md_images: list[dict], md_dir: Path
) -> tuple[int, int]:
    """Fix broken image blocks on a Notion page.

    Matches broken image blocks to local files by comparing the block's
    caption text with the alt text from the markdown image references.

    Returns (fixed_count, unmatched_count).
    """
    # Check for missing local image files first
    alt_path_pairs: list[tuple[str, Path]] = []
    missing_files = 0
    for img in md_images:
        resolved = (md_dir / img["path"]).resolve()
        if resolved.exists():
            alt_path_pairs.append((img["alt"], resolved))
        else:
            print(f"    WARN: Image file not found: {img['path']}")
            missing_files += 1

    blocks = get_all_blocks(token, page_id)
    broken = find_broken_image_blocks(blocks)
    if not broken:
        return 0, missing_files

    # Match broken blocks to local files by caption-to-alt correspondence.
    # Use positional consumption: each matched pair is removed to avoid
    # one-to-many mismatches when multiple images share the same alt text.
    remaining_pairs = list(alt_path_pairs)
    fixed = 0
    unmatched = 0
    upload_cache: dict[Path, str] = {}

    for block in broken:
        caption = get_block_caption_text(block)
        local_path: Path | None = None
        match_idx: int = -1

        # Try exact match first, then prefix match
        for i, (alt, path) in enumerate(remaining_pairs):
            if alt == caption:
                local_path = path
                match_idx = i
                break
        if local_path is None:
            for i, (alt, path) in enumerate(remaining_pairs):
                if caption and alt.startswith(caption):
                    local_path = path
                    match_idx = i
                    break

        if local_path is None:
            print(f"    WARN: No local file for caption '{caption}'")
            unmatched += 1
            continue

        # Consume the match so it won't be reused
        remaining_pairs.pop(match_idx)

        # Upload (cached per file path)
        if local_path not in upload_cache:
            print(f"    Uploading {local_path.name}...", end=" ", flush=True)
            upload_cache[local_path] = upload_file(token, local_path)
            print("OK")

        patch_image_block(token, block["id"], upload_cache[local_path])
        fixed += 1

    return fixed, unmatched + missing_files


def collect_md_files(paths: list[str]) -> list[Path]:
    """Collect .md files from the given file/directory paths (deduplicated)."""
    seen: set[Path] = set()
    files: list[Path] = []
    for p in paths:
        path = Path(p)
        if path.is_file() and path.suffix == ".md":
            resolved = path.resolve()
            if resolved not in seen:
                seen.add(resolved)
                files.append(path)
        elif path.is_dir():
            for f in sorted(path.glob("*.md")):
                resolved = f.resolve()
                if resolved not in seen:
                    seen.add(resolved)
                    files.append(f)
        else:
            print(
                f"WARN: Skipping '{p}' (not a .md file or directory)", file=sys.stderr
            )
    return files


def main():
    parser = argparse.ArgumentParser(description="Sync Markdown files to Notion pages.")
    parser.add_argument(
        "paths",
        nargs="+",
        help="Markdown files or directories containing .md files",
    )
    parser.add_argument(
        "--parent-page-id",
        default=None,
        help="Notion parent page ID or URL (fallback: NOTION_PARENT_PAGE_ID env)",
    )
    parser.add_argument(
        "--token",
        default=None,
        help="Notion API token (fallback: NOTION_TOKEN env)",
    )
    args = parser.parse_args()

    token = resolve_token(args.token)
    parent_page_id = resolve_parent_page_id(args.parent_page_id)
    md_files = collect_md_files(args.paths)

    if not md_files:
        print("No .md files found.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(md_files)} file(s) to sync.\n")

    results: list[dict] = []

    for md_file in md_files:
        title = title_from_filename(md_file.name)
        print(f"[{title}]")

        try:
            content = md_file.read_text(encoding="utf-8")
        except OSError as e:
            print(f"  FAILED to read file: {e}")
            results.append({"file": md_file.name, "status": "error", "error": str(e)})
            continue

        md_images = parse_images_from_markdown(content)

        # Archive existing pages with the same title (upsert)
        try:
            existing = find_existing_pages(token, parent_page_id, title)
            for old_id in existing:
                print(f"  Archiving existing page: {old_id}")
                archive_page(token, old_id)
        except requests.RequestException as e:
            print(f"  WARN: Could not check for existing pages: {e}")

        # Create the page
        try:
            page = create_page(token, parent_page_id, title, content)
        except requests.RequestException as e:
            print(f"  FAILED to create page: {e}")
            results.append({"file": md_file.name, "status": "error", "error": str(e)})
            continue

        page_id = page["id"]
        print(f"  Created: {page_id}")

        # Fix images if any
        images_fixed = 0
        images_unmatched = 0
        status = "ok"
        if md_images:
            print(f"  Fixing {len(md_images)} image reference(s)...")
            try:
                images_fixed, images_unmatched = fix_images_for_page(
                    token, page_id, md_images, md_file.parent
                )
            except (requests.RequestException, OSError) as e:
                print(f"  ERROR: Image fix failed: {e}")
                status = "partial"

        if images_unmatched > 0:
            status = "partial"

        results.append(
            {
                "file": md_file.name,
                "status": status,
                "page_id": page_id,
                "images_total": len(md_images),
                "images_fixed": images_fixed,
                "images_unmatched": images_unmatched,
            }
        )
        print()

    # Summary
    ok = [r for r in results if r["status"] == "ok"]
    partial = [r for r in results if r["status"] == "partial"]
    failed = [r for r in results if r["status"] == "error"]
    total_images = sum(r.get("images_fixed", 0) for r in results)

    print("=" * 50)
    print(f"Pages created: {len(ok) + len(partial)}/{len(results)}")
    print(f"Images fixed:  {total_images}")
    if partial:
        print(f"Partial:       {len(partial)} (page created but some images broken)")
        for r in partial:
            print(f"  - {r['file']}: {r.get('images_unmatched', 0)} image(s) unmatched")
    if failed:
        print(f"Failures:      {len(failed)}")
        for r in failed:
            print(f"  - {r['file']}: {r.get('error', 'unknown')}")
    print("=" * 50)

    if failed or partial:
        sys.exit(1)


if __name__ == "__main__":
    main()
