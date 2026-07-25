---
name: task-display-triage
description: Use when the real-time task display is missing or broken in Claude Code — TaskCreate/TaskUpdate/TaskList not found by ToolSearch, no task panel in the TUI, TodoWrite absent, or tasks silently vanishing mid-session. Also use before proposing any fallback for task tracking, and when diagnosing whether cmux or a Claude Code update broke the display.
---

# Task Display Triage

Diagnostic procedure for the Claude Code real-time task display (Task tools / TUI task panel). Root causes here were established by binary analysis and a real outage (2026-07-23); don't re-derive them from guesswork.

## Background facts (verified 2026-07-23 **on v2.1.217/218** — re-verify before relying on them in a newer binary)

These came from disassembling those two specific versions. On any later Claude Code version, treat each as a hypothesis to re-check (the gate functions can move or change names between releases), not as settled fact — especially the TodoWrite inversion, the kill-switch mechanics, and the cmux exoneration (a future cmux release could behave differently than the one inspected).

- The 2026-07 harness update **replaced TodoWrite with the Task tools** (TaskCreate / TaskUpdate / TaskList) and made them **deferred** — nothing appears unless loaded via `ToolSearch("select:TaskCreate,TaskUpdate,TaskList")`.
- TodoWrite and the Task tools are **mutually exclusive**: TodoWrite is enabled exactly when tasks are disabled and the kill-switch doesn't match (gates are inverted: `!TH()&&!xZ()` vs `TH()&&!xZ()`).
- Anthropic has a **remote kill-switch**: `tengu_vellum_ash` in `~/.claude.json` `cachedGrowthBookFeatures`. It disables the Task tools **only when an array entry is a substring of the current model id**.
- **cmux is exonerated.** Its wrapper only injects hooks and defensively *unsets* the inherited `CLAUDE_CODE_CHILD_SESSION` marker; it never disables tasks. (The original "cmux broke it" diagnosis was wrong — don't resurrect it.)

## Triage order

1. **Re-run ToolSearch**: `ToolSearch("select:TaskCreate,TaskUpdate,TaskList")`. Deferred tools sometimes just need an explicit load. If found → load and continue working; done.
2. **Check the kill-switch**: read `tengu_vellum_ash` in `~/.claude.json` → `cachedGrowthBookFeatures`.
   - As of v2.1.217/218: an entry matters **only if it is a substring of the current model id** — a non-empty array alone is NOT activation. On a newer binary, confirm the gate still reads this flag the same way before concluding anything.
   - Confirmed match (on a version where the mechanics are verified) → it's **Anthropic-side**. Report to the user as a blocker; nothing local will fix it.
3. **No match** → check in order: session env (`CLAUDE_CODE_ENABLE_TASKS`, `CLAUDE_CODE_CHILD_SESSION`), Claude Code version (did it just update? if so, the v2.1.217/218 facts above may no longer hold — re-verify the gates in the new binary before blaming anything, including cmux), Anthropic infra status.
4. **Try recovery**: re-run ToolSearch again; session restart. **Propose `claude update` to the user rather than running it** — it replaces their installed binary, and mid-investigation it also destroys the evidence (the binary you were inspecting).
5. **Last resort** — `CLAUDE_CODE_ENABLE_TASKS=false` in settings env re-enables the legacy TodoWrite checklist path (code-verified in 2.1.217/218). **Propose it to the user first**; it disables the new Task system session-wide.

## Hard rules

- **A markdown checklist is NOT an acceptable substitute for the real-time task display** (user directive, 2026-07-23). Never silently degrade to plain-text task lists.
- If the Task tools are unavailable, **report it to the user immediately as a blocker** and treat restoring the real display as part of the job.

## Common mistakes

| Mistake | Reality |
|---|---|
| "kill-switch array is non-empty → it's active" | Only a **substring match against the current model id** activates it |
| "cmux wraps claude, so cmux broke it" | Disproven 2026-07-23; wrapper injects hooks only |
| Falling back to a markdown checklist "temporarily" | Explicitly forbidden; report the blocker instead |
| Setting `CLAUDE_CODE_ENABLE_TASKS=false` silently | It's a session-wide downgrade — needs user approval |
