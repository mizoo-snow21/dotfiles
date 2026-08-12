---
name: github-pr-attachments
description: Upload images or videos (screenshots, before/after evidence, diagrams, screen recordings) to GitHub's native attachment store and embed them in a pull request body, issue body, or comment — without committing the files to the repository. Use this whenever a PR or issue needs an embedded screenshot or recording, whenever you are about to commit evidence images into the repo just so a PR can link them, and whenever an image already embedded in a PR or issue shows up as a broken link. Also use it when asked to verify that images in a PR body actually render. Triggers on "PRにスクリーンショットを貼る", "証跡を添付", "attach a screenshot to the PR", "add before/after images", "the image in my PR is broken".
---

# GitHub PR / Issue Attachments

GitHub stores files dragged into a comment box under `user-attachments`, addressed by an opaque UUID. The same store is reachable from the CLI, so evidence images never have to be committed.

**Why this beats committing the image:**

- A committed image lives in git history forever, even after the PR merges.
- `blob/<branch>/<path>?raw=true` breaks when the branch name contains `/` — GitHub cannot tell where the ref ends and the path begins — and breaks again when the branch is deleted.
- An attachment URL contains no repo name, branch, or path, so renaming a branch, moving the file, or deleting the branch cannot break it.

The trade-off worth naming: attachments live in GitHub, not in your repo. If the requirement is that evidence be version-controlled alongside the code and survive a migration off GitHub, commit the file instead and reference it as `raw.githubusercontent.com/<owner>/<repo>/<full-sha>/<path>` — use the commit SHA, never a branch name.

## Upload

Use the bundled script. It uploads, verifies the served byte count matches the source, and prints ready-to-paste Markdown:

```bash
"<skill-dir>/scripts/gh-attach.sh" -r owner/repo before.png after.png
# ![before](https://github.com/user-attachments/assets/<uuid>)
# ![after](https://github.com/user-attachments/assets/<uuid>)
```

`<skill-dir>` is this skill's own directory — the base directory announced when the skill loads. Resolve it to an absolute path before calling, because you are normally running from the repo's working directory, where a bare `scripts/…` path does not exist.

`-r` is optional inside a repo checkout. The script fails loudly on an unreadable file, a repo you cannot see, or a size mismatch — a mismatch means a truncated upload that would have rendered as a broken image.

Doing it by hand, if you need to adapt it:

```bash
curl -s -X POST \
  "https://uploads.github.com/user-attachments/assets?name=$NAME&content_type=$MIME&repository_id=$(gh api "repos/$REPO" --jq .id)" \
  -H "Authorization: Bearer $(gh auth token)" \
  -H "Accept: application/json" \
  --data-binary "@$FILE"
# → {"url":"https://github.com/user-attachments/assets/<uuid>"}
```

Three things that break a hand-rolled call: send **raw bytes** (`--data-binary "@file"`, not `-F`); `name` and `content_type` are **query parameters**, not headers; `repository_id` is the **numeric** id, not `owner/repo`.

## Embedding

```bash
gh pr edit <number> --body-file body.md
gh api "repos/$REPO/issues/<number>/comments" -X POST -f body="![shot]($ASSET_URL)"
```

One upload is scoped to the repository, so the same URL works in any PR, issue, or comment in that repo.

## Verify it renders

An asset that fetches successfully still renders as nothing if the Markdown is malformed. Ask GitHub for the rendered HTML — this works without a browser:

```bash
gh api repos/OWNER/REPO/pulls/NUMBER -H "Accept: application/vnd.github.html+json" \
  --jq '.body_html' | grep -oE '<img[^>]*src="[^"]*"'
```

A real `src` pointing at `private-user-images.githubusercontent.com/…?jwt=…` means it renders. An empty `src`, or no `<img>` at all, means the Markdown was malformed or sanitized away. Use `issues/NUMBER` for an issue and `issues/comments/ID` for a comment.

Opening the PR in a browser is still the strongest check when one is available.

## Access control

`repository_id` binds the asset to that repository's permissions. Every request to the asset URL is an authorization check:

| Caller | Result |
|---|---|
| No access, or unauthenticated, on a private repo | **404** — hides existence rather than returning 403 |
| Has repo access | **302** to a short-lived pre-signed URL |

An asset uploaded against a **private** repo is therefore not world-readable; a reader's browser session passes the check transparently when the body renders. An asset uploaded against a **public** repo is readable by anyone holding the URL.

Before uploading, check the image: synthetic or test data only, and mask real customer data, personal names, emails, secrets, and internal URLs. Prefer a cropped element screenshot over a full-page one — full-page captures usually include the signed-in user's name in the sidebar. **Assume the upload is permanent**; this endpoint offers no delete.

## What actually serves the bytes

GitHub rewrites the `user-attachments` URL at render time, so the reader's browser never contacts S3 directly:

```
body:   github.com/user-attachments/assets/<uuid>
render: private-user-images.githubusercontent.com/<id>/<file>?jwt=<JWT>
JWT:    iss=github.com   aud=raw.githubusercontent.com   lifetime≈300s
        its path claim embeds a pre-signed S3 query (X-Amz-Signature, X-Amz-Expires)
```

The backing bucket (`github-production-user-asset-*`) is GitHub-managed — GitHub pre-signs the URL, which requires credentials for that bucket — and the delivery host falls under `*.githubusercontent.com` in `gh api /meta --jq .domains.website`.

Both the JWT and the S3 signature expire in about five minutes, so a rendered `src` is a short-lived credential: never paste one anywhere as a durable link.

## Debugging a fetch that looks broken

Checking an asset URL with curl fails in two ways that look like the upload broke when it did not:

1. `curl -L` forwards the `Authorization` header to S3, which rejects it → **403**.
2. `curl -I` (HEAD) against the signed URL → **403**; the signature is scoped to GET.

Follow the redirect manually instead, with GET and no auth header on the second hop — that is what `scripts/gh-attach.sh` does.

## Caveats

- **Undocumented endpoint.** It is what the web UI uses, but GitHub publishes no contract for it, so treat a sudden failure as expected rather than surprising, and fall back to the committed-file route above.
- Bearer-token auth works; the endpoint historically accepted only cookie auth.
- No documented limits on size, MIME type, or rate.

## Verified

2026-08-12, against a private repository: upload returned an asset URL; the redirect target served the source's exact byte count as `image/png`; the rendered PR body carried a real `private-user-images.githubusercontent.com/…?jwt=…` `<img src>`; and an unauthenticated request to the asset URL returned 404. The bundled script was exercised on success, unreadable-file, and unknown-repo paths.
