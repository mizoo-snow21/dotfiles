---
name: handover
description: Generate or update a project HANDOVER.md file that summarizes the current Claude session. Use when ending a session, when context is getting full, or when the user wants a handoff document with progress, decisions, pitfalls, lessons, next steps, and important files.
---

# Handover

Create a handoff document for the next Claude session.

The command name is `handover`, and the output is a serious `HANDOVER.md` file.

## Workflow

1. Inspect the current session state before writing:
   - what the user asked for
   - what was completed
   - what changed but was not finished
   - decisions made and why
   - bugs, pitfalls, or false starts
   - files that matter for the next session
2. Create or update `HANDOVER.md` in the project root.
3. If `HANDOVER.md` already exists, preserve still-relevant context and replace stale details.
4. Do not invent work, tests, or outcomes. Mark uncertain items as unverified.
5. Keep it compact but useful. The next Claude should be able to continue without rereading the whole chat.

## What To Capture

- Current objective
- What got done
- What did not get done
- Important decisions and rationale
- Problems hit and how they were resolved
- Lessons or gotchas worth preserving
- Immediate next steps
- Important files, commands, or references

## Writing Rules

1. Prefer factual bullets over narrative fluff.
2. Be specific about file paths, pending work, and risks.
3. Separate verified facts from assumptions.
4. If code was changed, say whether it was verified and how.
5. If the session corrected an earlier mistake, record that so it is not repeated.
6. If there are existing unrelated repo changes, mention them only if they matter to the next session.
7. Keep the document skimmable.

## Default Template

Use this structure unless the project already has a better established format:

```md
# HANDOVER

## Current Objective
- <What the user is trying to achieve>

## Completed
- <Finished work>

## In Progress / Not Finished
- <Started but incomplete work>

## Decisions
- <Decision>: <why>

## Pitfalls / Lessons
- <Important mistake, constraint, or gotcha>

## Verification
- <What was verified>
- <What was not verified>

## Next Steps
- <Best immediate follow-up actions>

## Important Files
- `<path>`: <why it matters>
```

## Final Step

After writing `HANDOVER.md`, briefly tell the user that it was created or updated and mention any major unverified item in one sentence.
