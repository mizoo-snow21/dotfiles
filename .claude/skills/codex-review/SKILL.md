---
name: codex-review
description: Run a codex (GPT-5.6 Sol) code review on the current PR or staged changes. Use when the user wants an external AI review before merging. Iterates until no critical findings remain.
---

# Codex Review

Run a GPT-5.6 Sol code review via `codex exec` on the current PR or staged changes, then iterate fixes until clean.

## Workflow

1. **Gather context**: Determine what to review.
   - If a PR number is mentioned or a feature branch is checked out, use `gh pr diff <number>` to get the diff.
   - If the diff is small (report-only, config-only), also include the full source files that the diff touches.
   - Always include `plan.md` or `CLAUDE.md` as reference context if they exist.

> **REQUIRED**: Every `codex exec` invocation MUST end with `< /dev/null` (close stdin). Without it, codex hangs forever waiting on the stdin pipe when the shell call is backgrounded (observed 2026-07-09: 100% hang when backgrounded, 1-3 min completion in foreground).

2. **Initial review**: Run codex with the gathered files.
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

3. **Triage findings**: For each finding, determine:
   - **Valid critical**: Fix the code, commit, push.
   - **False positive**: Note why it's a false positive (e.g., header rows counted differently).

4. **Re-review**: After fixes, resume the codex session:
   ```bash
   codex exec resume --last -m gpt-5.6-sol "The code was updated. Changes:
   1. Finding #N: <what was fixed or why it's a false positive>

   Review the updated code. Do not nitpick. Only point out critical issues:
   <updated file contents>
   " < /dev/null
   ```

5. **Iterate** steps 3-4 until codex returns no critical findings.

6. **Post result**: Comment on the PR with a summary of the review, or tell the user the review passed.

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
- Always use `resume --last` for follow-up reviews to preserve session context (same model only).
- Include the instruction "Do not nitpick. Only point out critical issues" in every review prompt.
- When a finding is a false positive, explain why clearly in the resume prompt so codex doesn't re-raise it.
- If codex cannot run files (missing deps), fall back to static analysis of the code.
- Commit fixes to the same branch and push before re-reviewing.
