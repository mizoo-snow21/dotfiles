---
name: git-safety
description: Use before force-pushing, merging, rebasing, removing a worktree, or judging whether a branch is merged or pushed. In each of these, the obvious check reports success it never verified.
---

# Git Safety

Every rule here exists because a plausible check gives the wrong answer. Apply the ones that match what you are about to do.

## Judging a command that branches on success

`rebase` / `merge` / `cherry-pick` decide what you do next, so their exit code has to be read directly. A trailing `tail` or `head` returns 0 and reports success the git command never had.

```bash
git rebase origin/main; rc=$?
```

Check `$rc`. Never judge these through a pipe.

## Before force-push or merge

Three guards, all of them:

```bash
git diff --check                              # conflict markers left in files
git status --porcelain | grep -E '^(UU|AA|DD)' # unresolved paths
test -d "$(git rev-parse --git-path rebase-merge)" -o -d "$(git rev-parse --git-path rebase-apply)"
```

The third one detects an in-progress rebase. `--git-path` only prints a path, so `test -d` it rather than running it bare, and it works in a linked worktree where `.git` is a file.

Force-push only with conflicts resolved and no rebase in progress.

## Is this branch merged?

Use the PR, not the commit graph:

```bash
gh pr list --head <branch> --state merged
```

`git branch --merged` and `git merge-base --is-ancestor` both report "not merged" for a squash-merged branch, because the squash commit is a new commit and the branch's own commits never become ancestors of main.

## Is this branch pushed?

Confirm the upstream is `origin/<the branch's own name>`.

`git worktree add -b X origin/main` sets the upstream to `origin/main`, so a branch that has never been pushed still has an upstream. Reading "has an upstream" as "has been pushed" deletes unpushed work.

## Removing a worktree

Delete with `git worktree remove`, and check first that no process is still using it.

`~/.claude/bin/worktree-reap.sh` already runs at SessionStart and stashes untracked files into `~/.local/state/claude/worktree-attic/` before deleting, expiring them after 30 days. The attic lives outside the dotfiles repo so a `git clean -fdx` in there cannot take the stashed data with it.

## Where permanent artifacts go

Findings (`tasks/lessons.md` and the like), measurement scripts, and investigation notes belong either committed to the repo or written outside the worktree — `~/.claude/artifacts/<repo>/<issue>/`, for example. The attic is an accident-recovery layer, not a storage location.

Real case: on 2026-08-22, 161 lines of findings piled up untracked in `tasks/lessons.md` and were nearly lost when the worktree was removed. None of it had reached main.
