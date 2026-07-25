---
paths:
  - "**/*"
---

# Task Management

**Exception**: minor fixes under CLAUDE.md §1's sanctioned exception (user directive, 2026-07-06 — few files, no schema / API-contract / shared-env blast radius) skip steps 1–3, 4's markdown-record half, and 6 (no `tasks/todo.md` is created, so there is no durable-record file and nothing to add a review section to; the Task-tools half of step 4 still applies when the fix is multi-step, and step 7 still applies if the user corrects you). Announce "implementing directly", then still run tests + a lightweight review before commit. Everything larger follows all steps.

1. **Plan First**: Load `Skill(superpowers:writing-plans)` **before writing anything** (per CLAUDE.md §1), then write the high-level implementation plan in `tasks/plan.md`
2. **Verify Plan**: Check in before starting implementation
3. **Break Down Work**: After the plan is accepted, break it into tasks following the already-loaded skill's Task Right-Sizing and Bite-Sized Task Granularity rules — do not size tasks by feel. Record the breakdown as checkboxes in `tasks/todo.md`
4. **Track Progress**: Live progress belongs in the **Task tools** (TaskCreate / TaskUpdate), not in a markdown checklist — see CLAUDE.md "Real-time task display". **`tasks/todo.md` is the single durable record of the breakdown and its outcomes**; the Task tools are the live status display. Keep both roles separate, and never let the checkboxes stand in for the display
5. **Explain Changes**: High-level summary at each step
6. **Document Results**: Add a review section to `tasks/todo.md`
7. **Capture Lessons**: Update `tasks/lessons.md` after corrections
