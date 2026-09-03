---
paths:
  - "**/*"
---

# Task Management

**Exception**: under CLAUDE.md §1's Minor fixes exception, skip steps 1–3, 4's markdown-record half, and 6. The Task-tools half of step 4 still applies to multi-step fixes, and step 7 still applies.

1. **Plan First**: Load `Skill(superpowers:writing-plans)` **before writing anything** (per CLAUDE.md §1), then write the high-level implementation plan in `tasks/plan.md`
2. **Verify Plan**: Check in before starting implementation
3. **Break Down Work**: After the plan is accepted, break it into tasks following the already-loaded skill's Task Right-Sizing and Bite-Sized Task Granularity rules — do not size tasks by feel. Record the breakdown as checkboxes in `tasks/todo.md`
4. **Track Progress**: Live status goes in the Task tools (see CLAUDE.md "Real-time task display"). **`tasks/todo.md` is the single durable record of the breakdown and its outcomes** — never let its checkboxes stand in for the live display
5. **Explain Changes**: High-level summary at each step
6. **Document Results**: Add a review section to `tasks/todo.md`
7. **Capture Lessons**: Update `tasks/lessons.md` after corrections
