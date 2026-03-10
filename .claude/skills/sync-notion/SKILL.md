---
name: sync-notion
description: Sync local Markdown files to Notion pages with automatic image upload
user-invocable: true
---

# /sync-notion

Syncs local Markdown files to Notion, creating pages and uploading embedded images.

## Usage

The user will specify:
- **Files/directories**: Which `.md` files or directories to sync
- **Parent page ID** (optional): The Notion page under which to create child pages

If not specified, prompt the user for files/directories. The parent page ID can be omitted if `NOTION_PARENT_PAGE_ID` is set in `.env`.

## Setup

Before first use, set the following in `.env`:

```
NOTION_TOKEN=your-notion-api-token-here
NOTION_PARENT_PAGE_ID=your-notion-parent-page-id-here
```

## How to run

```bash
uv run .claude/skills/sync-notion/sync_to_notion.py <paths...> [--parent-page-id <ID_OR_URL>] [--token <TOKEN>]
```

### Examples

```bash
# Sync a directory (parent page ID from .env)
uv run .claude/skills/sync-notion/sync_to_notion.py docs/

# Sync a single file with explicit parent page ID
uv run .claude/skills/sync-notion/sync_to_notion.py README.md --parent-page-id <PARENT_PAGE_ID>

# Use a Notion URL as parent page ID
uv run .claude/skills/sync-notion/sync_to_notion.py docs/ --parent-page-id "https://www.notion.so/Your-Page-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Multiple paths
uv run .claude/skills/sync-notion/sync_to_notion.py file1.md file2.md
```

## Token resolution

The script resolves the Notion API token in this order:
1. `--token` CLI argument
2. `NOTION_TOKEN` environment variable (`.env`)

## Parent page ID resolution

The script resolves the parent page ID in this order:
1. `--parent-page-id` CLI argument
2. `NOTION_PARENT_PAGE_ID` environment variable (`.env`)

Accepted formats: UUID (with/without dashes), Notion page URL.

## What it does

1. Collects all `.md` files from the given paths
2. For each file:
   - Generates a title from the filename (e.g., `1_3_preprocessing.md` → "1.3 Preprocessing")
   - Creates a Notion page using the `markdown` parameter
   - Finds broken image blocks (empty URL) on the created page
   - Matches them to local image files by comparing caption text with markdown `![alt](path)` alt text
   - Uploads local images and patches the blocks
3. Prints a summary of created pages and fixed images

## Important notes

- **Upsert behavior**: If a page with the same title already exists under the parent, it is archived (trashed) before creating the new one
- Image paths in markdown are resolved relative to the `.md` file's directory
- Images with HTTP(S) URLs are skipped (only local files are uploaded)
