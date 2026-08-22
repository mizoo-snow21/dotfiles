---
name: codex-review
description: Run a codex (GPT-5.6 Sol) review via `codex exec` and iterate until no critical findings remain. Use for code (PR or staged changes) before merging, and for implementation plans, specs, and todo docs before they are shown. Not for issue / PR bodies — codex usage limit is tight, so it is reserved for the documents where review pays off most.
---

# Codex Review

Run a GPT-5.6 Sol review via `codex exec`, then iterate fixes until clean.

## What this covers

Two review targets, same loop:

- **Code**: the current PR or staged changes, before merging.
- **Documents**: implementation plans, specs, todo docs. Run the loop **before** showing the document to the user — draft → review → zero findings → present, so it is right the first time.

> **issue / PR bodies are out of scope** (user directive, 2026-08-22). The usage limit is tight, so it is spent on plans and specs, where a defect costs a whole implementation round. When an externally published document needs fact-checking, dispatch a subagent (Fable) instead.

## Workflow

1. **Gather context**: Determine what to review.
   - Code with a PR: if a PR number is mentioned, `gh pr diff <number>`.
   - Code on a feature branch **without** a PR (the normal pre-PR case — branch review happens before the PR exists): diff the branch itself, `git diff "$(git merge-base <base-branch> HEAD)"...HEAD`. If the branch isn't fully committed yet, add `git diff <base-branch>` for tracked changes — and for **untracked** files, list them with `git status --porcelain` and include their **full contents** in the review scope. A newly created file has no diff; names alone let it escape review entirely.
   - If the diff is small (report-only, config-only), also include the full source files that the diff touches.
   - Documents: pass the document's full path, and the path of the project's `CLAUDE.md` as reference so codex judges against the actual rules.
   - Always include `plan.md` or `CLAUDE.md` as reference context if they exist.

> **REQUIRED**: Every `codex exec` invocation MUST end with `< /dev/null` (close stdin). Without it, codex hangs forever waiting on the stdin pipe when the shell call is backgrounded (observed 2026-07-09: 100% hang when backgrounded, 1-3 min completion in foreground).

> **Outside a git repo**: add `--skip-git-repo-check`. Without it codex exits 1 with "Not inside a trusted directory and --skip-git-repo-check was not specified" — this bites whenever the file under review lives in a scratch directory rather than the project.

2. **Initial review**: Run codex with the gathered files, **using the prompt that matches the target type**. **Record the session id it prints** — every follow-up resumes that id (see step 4).

   **Code:**
   ```bash
   codex exec -m gpt-5.6-sol "Review this code. Do not nitpick. Only point out critical issues (bugs, data loss, incorrect logic, missing error handling that would cause crashes, security issues).

   Focus areas:
   - Correctness of core logic
   - Data integrity (records lost or duplicated?)
   - Issues that would break downstream pipeline
   - Silent failures that should fail fast

   === <file paths and contents> ===

   === Reference: plan.md ===
   <plan.md content if exists>
   " < /dev/null
   ```

   **Documents** (plans, specs, todo docs) — do not reuse the code prompt; its focus areas miss specification-level defects:
   ```bash
   codex exec -m gpt-5.6-sol "Review this document. Do not nitpick. Only point out critical issues.

   Focus areas:
   - Internal contradictions, and contradictions with the referenced rules/spec
   - Unverified claims stated as fact; missing evidence for key assertions
   - Steps that cannot be executed as written (missing prerequisites, wrong order, references to things that don't exist)
   - Scope gaps: requirements the document silently drops or quietly expands

   === <document full path and contents> ===

   === Reference: CLAUDE.md / spec ===
   <reference content>
   " < /dev/null
   ```

3. **Triage findings**: For each finding, determine:
   - **Valid critical**: real defect, needs a fix.
   - **False positive**: Note why it's a false positive (e.g., header rows counted differently).

   Then check what you are allowed to do with it, against the authorization table below. If the target is something you are producing or implementing in this task, apply the fix and continue the loop. **If the user only asked you to review, stop here**: report the findings and ask before touching the file — a review-only request never becomes edit authority, no matter how clearly correct the fix looks.

4. **Re-review**: After fixes, resume **the session id recorded in step 2** — never `--last`. Keep the target type's wording: "code" for code, "document" for documents (the session already carries the matching focus areas from step 2):
   ```bash
   # Code:
   codex exec resume <REVIEW_SESSION_ID> -m gpt-5.6-sol "The code was updated. Changes:
   1. Finding #N: <what was fixed or why it's a false positive>

   Review the updated code. Do not nitpick. Only point out critical issues:
   <updated file contents>
   " < /dev/null

   # Documents — same shape, document wording:
   codex exec resume <REVIEW_SESSION_ID> -m gpt-5.6-sol "The document was updated. Changes:
   1. Finding #N: <what was fixed or why it's a false positive>

   Review the updated document again with the same focus areas. Do not nitpick. Only point out critical issues:
   <updated document contents>
   " < /dev/null
   ```
   `--last` resumes whatever codex session ran most recently. Implementation sessions, other tasks' reviews, and plan reviews all create codex sessions, so `--last` frequently attaches the follow-up to the wrong conversation — and the wrong review then answers as if it had seen these changes.

5. **Iterate** steps 3-4 until codex returns no critical findings.

6. **Report result**: tell the user the review passed and what was fixed. Committing, pushing, or posting a PR comment happens **only after the user asks for it** — report first, then act on their go-ahead.

## Model fallback on rate limit

Use models in this priority order. If a `codex exec` call fails with a rate limit error (429, "rate limit", "too many requests", etc.), retry with the next model down:

1. `gpt-5.6-sol`
2. `gpt-5.5`
3. `gpt-5.4`
3. `gpt-5.3-codex`
4. `gpt-5.2-codex`
5. `gpt-5.2`
6. `gpt-5.1-codex`
7. `gpt-5.1`
8. `gpt-5-codex`
9. `gpt-5`

When falling back, start a **new session** (do not use `resume --last` since the session was on a different model). Mention the fallback to the user.

## Rules

- Default to `-m gpt-5.6-sol` for reviews. Fall back per the model priority above on rate limit.
- **Resume by recorded session id, never `--last`** (step 4). Same model only — a fallback to a different model starts a new session and needs its own id recorded.
- Include the instruction "Do not nitpick. Only point out critical issues" in every review prompt.
- When a finding is a false positive, explain why clearly in the resume prompt so codex doesn't re-raise it.
- If codex cannot run files (missing deps), fall back to static analysis of the code.
- **Re-review from the working tree. Do not commit or push to get there** — the loop needs the updated file contents in the prompt, not a pushed branch.

## What the review authorizes

Running a review never authorizes shipping. Match the action to what the user actually asked for:

| Action | Allowed without asking again? |
|---|---|
| Run codex, report findings | Yes — that is the request |
| Edit a draft **you are producing** (your plan / spec), then re-review | Yes — iterating to zero findings is the point |
| Edit code **you are implementing** in this task, then re-review | Yes |
| Edit files the user only asked you to **look at** | No — report the findings and ask |
| `git commit` / `git push` | No — ask |
| Post a PR comment or any other external publication | No — ask |
