---
name: git-safety
description: Use before force-pushing, merging (stacked PRs included), rebasing, rewriting the working tree (`reset --hard`, `checkout -- <path>`, `clean`, `rm -rf`), staging a commit, writing to a branch you did not create, adding or removing a worktree, or judging whether a branch is merged or pushed. In each of these, the obvious check reports success it never verified.
---

# Git Safety

Every rule here exists because a plausible check gives the wrong answer. Apply the ones that match what you are about to do.

## Judging a command that branches on success

`rebase` / `merge` / `cherry-pick` decide what you do next, so their exit code has to be read directly. A trailing `tail` or `head` returns 0 and reports success the git command never had.

```bash
git rebase origin/main; rc=$?
```

Check `$rc`. Never judge these through a pipe.

The `; rc=$?` form is for those git commands. Run `gh pr merge` and other allowlisted commands as a bare line: anything appended breaks the permission rule's prefix match and sends the call to the auto-mode classifier, which denies it while the rule is already in place.

## Before rewriting the working tree

Treat every command that rewrites files on disk as destructive — `reset --hard`, `checkout <ref> -- <path>`, `checkout -- .`, `restore`, `clean`, `rm -rf`. Judge by that effect, not by whether the command is named on some list.

1. Look first: `git status --porcelain`, and `find <dir> -type f` before `rm -rf`. Proceed only when everything listed is yours from this session and meant to go. A pre-existing edit or an unfamiliar file stops the command.
2. Delete by file name, then `rmdir` the emptied directory. Untracked and gitignored files have no history to restore from.
3. To move a branch, `git rebase --onto` or create a new branch at the target. To carry uncommitted edits to another branch, `git switch`.

Real cases: `reset --hard` to restack a branch wiped the user's pre-existing edits; `checkout <branch> -- lessons.md` erased the lesson about to be committed; `rm -rf` on a directory assumed to be scratch took untracked reports with it.

## Staging a commit

Stage by path: `git add <path>…`. `git add -A` also sweeps in whatever other sessions, test runs, or the user left in the tree. After committing, read `git show --stat HEAD` and check it matches the message.

`git add` silently skips files flagged skip-worktree, and `git status` does not list them either. `git ls-files -v | grep -v '^H '` shows every flagged file.

## Writing to a branch you did not create

Check the owner before pushing, rebasing, or resolving conflicts on a branch: `gh pr view <n> --json author`. Write only to your own. On anyone else's branch, report its state and leave the action to its owner — undoing a write you already made is a write too, so report what happened with the options and wait. A restore the user approves uses `git push --force-with-lease=<branch>:<SHA your push left on the remote>`, so it stops if anyone pushed since.

## Before force-push or merge

Three guards, all of them:

```bash
git diff --check                              # conflict markers left in files
git status --porcelain | grep -E '^(UU|AA|DD)' # unresolved paths
test -d "$(git rev-parse --git-path rebase-merge)" -o -d "$(git rev-parse --git-path rebase-apply)"
```

The third one detects an in-progress rebase. `--git-path` only prints a path, so `test -d` it rather than running it bare, and it works in a linked worktree where `.git` is a file.

Force-push only with conflicts resolved and no rebase in progress.

## Merging a stack

A PR whose base is another PR's branch is stacked. When the parent's branch is deleted, GitHub closes the child rather than retargeting it.

1. Merge the parent without `--delete-branch`. Retarget the child: `gh pr edit <child> --base main`.
2. A squash merge keeps the parent's original commits out of main's ancestry, so the child now conflicts. Replay only the child's commits — `git rebase --onto origin/main <parent's original tip> <child>` — and push with `--force-with-lease`.
3. Merge one PR at a time, each on a green head. Delete the parent's branch after the child merges.

If `gh pr merge` answers 403 "Merging stacked PRs via this endpoint is not supported", the repo uses GitHub's native stacks, and the only route, `merge-async`, merges every PR above the target too. Get every PR in the stack green first, or retarget the upper PRs to unstack. Re-fetch the whole stack before reporting what merged.

A child already closed: recreate the deleted base at its old SHA (`git push origin <sha>:refs/heads/<base>`), `gh pr reopen`, then retarget.

## Is this branch merged?

Use the PR, not the commit graph:

```bash
gh pr list --head <branch> --state merged
```

`git branch --merged` and `git merge-base --is-ancestor` both report "not merged" for a squash-merged branch, because the squash commit is a new commit and the branch's own commits never become ancestors of main.

`gh pr merge --delete-branch` can print a git error (`Your local changes … would be overwritten by checkout`) after the merge itself succeeded — only the local checkout failed. Read `gh pr view <n> --json state,mergedAt` before retrying.

## Is this branch pushed?

Confirm the upstream is `origin/<the branch's own name>`.

`git worktree add -b X origin/main` sets the upstream to `origin/main`, so a branch that has never been pushed still has an upstream. Reading "has an upstream" as "has been pushed" deletes unpushed work.

## Worktrees

Create with an absolute path, then confirm it with `git worktree list`. Bash's cwd carries over between calls, so a relative path can resolve inside another worktree and nest the new tree there. Aim commands at another tree with `git -C <absolute path>` rather than an earlier `cd`.

Delete with `git worktree remove`, and check first that no process is still using it.

`~/.claude/bin/worktree-reap.sh` already runs at SessionStart and stashes untracked files into `~/.local/state/claude/worktree-attic/` before deleting, expiring them after 30 days. The attic lives outside the dotfiles repo so a `git clean -fdx` in there cannot take the stashed data with it.

## Where permanent artifacts go

Findings (`tasks/lessons.md` and the like), measurement scripts, and investigation notes belong either committed to the repo or written outside the worktree — `~/.claude/artifacts/<repo>/<issue>/`, for example. The attic is an accident-recovery layer, not a storage location.

Real case: on 2026-08-22, 161 lines of findings piled up untracked in `tasks/lessons.md` and were nearly lost when the worktree was removed. None of it had reached main.
