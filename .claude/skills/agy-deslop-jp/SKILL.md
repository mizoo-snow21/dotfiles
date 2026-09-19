---
name: agy-deslop-jp
description: Delegate Japanese de-slopping to Antigravity CLI (agy), which reads the stop-ai-slop-jp rubric and applies it. agy strips what the source text alone can settle — 偏愛語, 命題型H2, template structure, empty 両論併記 — editing the file in place, and returns what only the author can supply as a punch list. Use whenever a Japanese file needs fixing — blog posts, README, docs, reports, release notes, PR descriptions — and the user says 直して / 推敲して / AI臭いので直して / 読みやすくして / 自然な日本語にして. It pays off most on long or multiple files, since the prose never enters this session's context. For a few lines pasted into chat, read stop-ai-slop-jp and fix them yourself instead — delegating costs more than it saves.
---

# agy Deslop (Japanese)

Claude Code picks the targets, delegates, and inspects the diff. `agy` does the rewriting.

The rubric itself lives in **`stop-ai-slop-jp`**. This skill does not duplicate it — agy reads that file.

## Why delegate

Rewriting a long draft yourself pulls the whole text into context. Ten files, ten drafts. Delegating
returns only a diff. The work is applying one fixed standard across a whole document rather than
making judgment calls, which is what a cheap fast model is good at.

The inverse holds for a few lines: process startup and skill loading cost more than the prose. Fix
those yourself.

## Only half of it can be delegated

`stop-ai-slop-jp` asks for two different things.

| | What | Who |
|---|---|---|
| **Subtractive** | 偏愛語, 全角ダッシュ, 命題型H2, 決めつけ序文, 二項対比, 3項目並列, モノ主語, empty 両論併記, uniform rhythm | agy. The source text alone settles every one of these |
| **Additive** | Concrete experience, numbers, proper nouns, a position the writer owns | The author. agy knows nothing about the subject |

**Without that line drawn explicitly, it falls off one side or the other.** Both failures were measured:

- Hand it the rubric with no scope limit → it fills the empty slots for concreteness with invented
  material. A fabricated anecdote landed in the body text
- Add "don't invent facts" and nothing else → the lying stops, but it retreats into bland paraphrase.
  です・ます survives, 両論併記 survives, and the actual slop is still there

So give it the subtractive half only, and have the additive half come back as a **punch list**. A
sentence it is told to cut gets deleted rather than reworded, and the list is the thing the author
can actually act on.

## Invocation

```bash
cd <directory containing the target file>
agy -p "<prompt>" \
  --model gemini-3.8-flash-high \
  --dangerously-skip-permissions --sandbox \
  --print-timeout 240s </dev/null
```

- **`--dangerously-skip-permissions` is not optional.** Headless mode cannot prompt for tool
  permissions, so it auto-denies them: even `read_file` is refused and the run ends with
  `no output produced`. `--mode accept-edits` is not enough — it permits edits but reads still fail
- **Always pair it with `--sandbox`.** The flag above auto-approves every tool, so shut the terminal
  down. Fixing prose needs no shell
- Append `</dev/null`, or the process hangs waiting on input
- Default to `gemini-3.8-flash-high`. Reserve `gemini-3.1-pro-high` for drafts going outside
- Claude Code's auto-mode classifier sometimes refuses this command over the flag name, and the
  decision is inconsistent. Do not fire the same command again — write the prompt to a file and ask
  the user to run it with `!`

## Prompt shape

```
まず /Users/mizoo/.claude/skills/stop-ai-slop-jp/SKILL.md を読め。
続けて同じディレクトリの references/phrases.md と references/structures.md も読め。
禁止語リストと構造パターンの実体はそこにある。SKILL.md だけでは要約しか見ていない。
そのうえで <ファイル名> を直す。ファイルを直接上書きすること。

ただし指針を全部やるな。お前が担当するのは削る側だけだ。偏愛語、全角ダッシュ、
命題型H2、決めつけ序文、二項対比、3項目並列、モノ主語、中身のない両論併記、
均一なリズム — これらは原文の情報だけで削れる。削れ。

次の2つは実測で飛ばされた。名指しで指示しないと処理されない:
- 文末の均一さ。全文が「です・ます」で終わっているなら崩せ。体言止め、「だ」、
  問いかけ、短い断片を混ぜる
- モノ主語（false agency）。「利用が広がっています」のようにモノが人間の動詞を
  やっている文は、誰がやったかに書き換えろ。書けないならその文を削れ

足す側（具体的な体験、数字、固有名詞、引き受けた立場）は書き手にしか書けない。
原文にない事実を一切作るな。そこは抽象のまま残すか文を削り、最後に
「書き手が埋めるべき箇所」として箇条書きで挙げろ（ファイルには書かず、返答に書け）。

完了したら、読んだ3ファイルそれぞれについて、そこにしか書かれていない具体的な項目を
1つずつ挙げろ。
```

Give the target as an **absolute path**, not a bare filename, and tell it not to search. Handed
`sample4.md`, agy answered "searching for the file" and ended its turn without touching anything.

Keep the prompt in Japanese — the rubric, the target text, and the punch list all are.

Every part of it is load-bearing:

1. **Point at the absolute path.** `stop-ai-slop-jp` exists only under `~/.claude/skills`; it is not
   in `~/.agents/skills`, the pool agy shares, so invoking it by name resolves to nothing and is
   silently ignored. A path also means agy reads the current version every time instead of a
   paste-time snapshot — and it avoids `~/.agents/skills`, whose contents get overwritten on update
2. **Say "don't do all of it".** The rubric demands the additive half too, so a model trying to
   comply will fabricate. Forbidding invention is not enough on its own; the scope has to be named
3. **Punch list in the reply, not the file.** TODO comments left in a draft get shipped
4. **Demand a read-back that can be checked.** Asking for "the key points" gets you a summary that a
   model could write without opening anything — a plausible read-back once covered a run that had
   skipped half the rubric. Asking for one item unique to each file produces citations you can grep
   for, which is the difference between evidence and a vibe

## Receiving the work

**Never truncate the reply.** The read-back and the punch list both live in it — piping through
`head`/`tail` destroys the evidence. Redirect to a file if it is long.

Check the read-back by grepping for what it cited — and confirm the same string is **absent** from
`SKILL.md`, which is what makes it proof the reference file itself was opened:

```bash
R=/Users/mizoo/.claude/skills/stop-ai-slop-jp
grep -c "<cited string>" "$R/references/phrases.md"   # expect ≥1
grep -c "<cited string>" "$R/SKILL.md"                # expect 0
```

If a citation does not exist, or turns out to sit in `SKILL.md` after all, the references never
landed. Throw the diff away and re-dispatch.

Then read the diff:

```bash
git diff -- <file>              # under git
diff <file>.orig <file>         # otherwise, cp beforehand
```

Two things to check:

- **Did facts get added?** Any number, proper noun, anecdote, or assertion absent from the source
  goes back. Scoping the task reduces this but does not eliminate it
- **Did it cut too much?** Removing empty sentences is correct, but a sentence the author actually
  meant can get judged as filler and disappear
- **Did the two known misses get handled?** Check them mechanically rather than by eye — both
  survived a run that otherwise looked clean:

```bash
# sentence endings: all です・ます means the uniform-rhythm rule was skipped
node -e 'const t=require("fs").readFileSync(process.argv[1],"utf8").split("\n").filter(l=>l&&!l.startsWith("#")).join("");
const s=t.split("。").filter(Boolean); console.log(s.length,"sentences");
s.forEach(x=>console.log("  …"+x.slice(-10)))' <file>
```

  Then scan the subjects: a clause like 「利用が広がっています」「課題が浮き彫りになる」 is a thing
  doing a human verb, which is rule A-1 and the second-highest priority in the rubric.

**The read-back proves the rubric was read, not that it was applied.** Those are different claims
and conflating them produces a false all-clear. Only the diff settles the second one.

**What goes to the user is the punch list, not the diff.** The diff only removes things; the draft
gets better once the user answers the list. Hand them the list, and fold their answers back into the
text yourself. That part cannot be delegated.

## Out of scope

- **Not for writing code** — implementation goes to Cursor (`cursor-delegate`). This skill covers
  Japanese prose only
- **Not for English** — `stop-slop` and `humanizer` cover that
- **Not for a few lines in chat** — read `stop-ai-slop-jp` and fix them yourself, it is faster
- **No git or gh operations** — commit, push, and anything touching GitHub stay with Claude Code.
  agy only edits a file on disk

## Issue and PR bodies

They are legitimate targets — they are just not files, so give agy a file and put the result back
yourself:

```bash
gh issue view <n> --json body --jq .body > body.md   # or: gh pr view <n> --json body --jq .body
cp body.md body.orig.md
# run agy on body.md, inspect the diff, resolve the punch list with the user
gh issue edit <n> --body-file body.md                # or: gh pr edit <n> --body-file body.md
```

Two constraints carry over from CLAUDE.md. **Edit in place** — never close and reopen an issue to
replace its text, which destroys the audit trail. And **creating** an issue or PR is a different kind
of action from editing one: load `github-issues` before any `gh issue create` / `gh pr create`,
even if you have been running `gh` commands all along.

Screenshots and other attachments embedded in the body are content agy has never seen. Check the
diff for mangled Markdown — image links and `user-attachments` URLs must come back byte-identical.
