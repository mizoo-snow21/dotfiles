---
name: codex-adversarial-review
description: Run a single adversarial codex pass that attacks the design of a change rather than hunting implementation defects — it asks whether this approach should ship at all, what assumptions it rests on, and how it fails under real conditions. Use before merging anything with real blast radius (schema or migration changes, auth and permissions, money, shared contracts, irreversible state, bulk production writes), when a change "looks fine but feels off", when you want a second opinion on an approach you already committed to, or whenever the user says 敵対的レビュー / adversarial review / challenge review / "try to break this" / "why shouldn't this ship". This is deliberately separate from codex-review, which iterates on implementation defects until clean — reach for this one when the risk is that the whole approach is wrong.
---

# Codex Adversarial Review

One pass. Codex is told to break confidence in the change, not to validate it.

The prompt and output schema are OpenAI's, copied verbatim from
[`openai/codex-plugin-cc`](https://github.com/openai/codex-plugin-cc)
(`plugins/codex/prompts/adversarial-review.md`, `plugins/codex/schemas/review-output.schema.json`).
Do not rewrite or paraphrase them — fill the placeholders and pass them through. They are tuned;
a reworded copy is a different review.

This is not a stricter `codex-review`. `codex-review` asks "is this implemented correctly?" and
loops until clean. This asks "should this ship at all?" and stops after one answer, because the
useful output is a judgment, not a fix list.

## Workflow

### 1. Gather the target

- PR: `gh pr diff <number>`
- Feature branch, no PR yet: `git diff "$(git merge-base <base> HEAD)"...HEAD`
- Uncommitted work: `git diff` plus `git diff --cached`
- **Untracked files**: list with `git status --porcelain` and include their **full contents**.
  A new file has no diff, and a design flaw hides just as well in a file that never appears in one.

If the diff is small, include the full source of the files it touches — design questions need the
surrounding code. Include `plan.md` / `CLAUDE.md` when they exist: the strongest adversarial
findings come from comparing what the code does against what the plan claimed it would do.

### 2. Fill the placeholders

Read `prompts/adversarial-review.md` and substitute its four template variables:

| Placeholder | Value |
|---|---|
| `{{TARGET_LABEL}}` | what is under review — `working tree`, `feat/x vs main`, `PR #42` |
| `{{USER_FOCUS}}` | the user's focus text, or `No extra focus provided.` when they gave none |
| `{{REVIEW_COLLECTION_GUIDANCE}}` | `Use the repository context below as primary evidence.` when the diff is inline. If the change is too large to inline and you are passing a summary instead: `The repository context below is a lightweight summary. Inspect the target diff yourself with read-only git commands before finalizing findings.` |
| `{{REVIEW_INPUT}}` | the gathered diff / file contents |

These values come from the plugin's own runtime (`scripts/lib/git.mjs`), so they keep the prompt
behaving the way OpenAI tuned it.

### 3. Run

```bash
codex exec -m gpt-6-astra \
  --output-schema ~/.claude/skills/codex-adversarial-review/schemas/review-output.schema.json \
  "<filled prompt>" < /dev/null
```

**`< /dev/null` is required.** Without it codex hangs forever waiting on stdin when the call is
backgrounded. Outside a git repo, add `--skip-git-repo-check`. On a rate limit, fall back down the
model list in `codex-review` — same runtime, same order.

The schema returns `verdict` (`approve` / `needs-attention`), `summary`, `findings[]` (severity,
title, body, file, line_start, line_end, confidence, recommendation) and `next_steps[]`.

### 4. Report

Give the user the verdict, then the findings sorted by severity. Then stop.

**Do not fix anything.** Running this review is never authority to edit. Even when a finding is
obviously right, report it and wait — the pass exists to inform a go/no-go decision that belongs
to the user.

Say which findings you think hold and which do not. Codex was instructed to be aggressive and will
sometimes reach; `confidence` is its own estimate, not a verdict. Passing an unfiltered list through
trains the user to ignore the next one.

### 5. When a finding lands on the design

If the answer is "the approach itself is wrong", do not translate it into a patch list and grind
through it. Take it back to planning. A design rejected by review and then patched around comes out
the far side labeled "reviewed" — worse than never having run the review, because now the bad
approach carries a stamp.

## Relationship to codex-review

Run this **before** `codex-review`. Finding out the approach is wrong is cheap while the
implementation is still soft, expensive after a fix-until-clean loop has polished it.

Typical order on a risky change: plan → **adversarial review** → implement → `codex-review` → PR.

This costs a full extra codex pass, so spend it where being wrong is expensive, not on every diff.
