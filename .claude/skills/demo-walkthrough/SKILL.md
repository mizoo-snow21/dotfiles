---
name: demo-walkthrough
description: Run a Playwright MCP walkthrough of a demo flow, taking screenshots at each step and verifying expected state. Use when the user wants to verify a demo story end-to-end visually.
---

# Demo Walkthrough

Run a step-by-step Playwright MCP walkthrough of a demo flow, capturing screenshots and verifying each step.

## Workflow

1. **Locate flow definition**: Look for a flow definition in one of these places (in priority order):
   - User-provided steps in the prompt
   - `tasks/todo.md` verification section
   - `tasks/plan.md` verification section
   - Ask the user for the flow steps

2. **Prepare output directory**:
   ```bash
   mkdir -p <project>/demo-video/frames
   ```

3. **Start dev server** if not already running:
   ```bash
   npm run dev &
   # Wait for server to be ready
   curl -s -o /dev/null -w "%{http_code}" http://localhost:3000
   ```

4. **Execute each step** using Playwright MCP tools:
   For each step in the flow:
   a. **Navigate or click** using `browser_navigate` or `browser_click`
   b. **Wait for expected state** using `browser_wait_for` or `browser_snapshot`
   c. **Verify** the snapshot matches expectations (check for expected text, elements, URLs)
   d. **Screenshot** using `browser_take_screenshot` with a numbered filename:
      ```
      demo-video/frames/NN-step-name.png
      ```
   e. **Report** pass/fail for each step

5. **Summary**: After all steps, output a table:
   | Step | Action | Expected | Result |
   |------|--------|----------|--------|
   | 01   | ...    | ...      | PASS/FAIL |

## Rules

- Always use `browser_snapshot` (not screenshot) to determine element refs before clicking
- Use descriptive filenames: `01-home.png`, `02-projects.png`, `03-project-detail.png`, etc.
- If a step fails, report it but continue with remaining steps
- Take a `fullPage` screenshot when the page has significant below-the-fold content
- Close the browser when done if no further interaction is expected
- If the flow definition references a specific URL, navigate directly; if it references a UI action, use click

## Example invocation

User: `/demo-walkthrough`
```
Steps:
1. / → click "デモを開始する" → expect /solution-2/projects
2. Click "詳細・履歴" on first row → expect /solution-2/projects/prj-001
3. Click "新規ファイル投入" → expect /solution-2/upload?project=prj-001
```

## Output

Screenshots are saved to `demo-video/frames/` and a summary table is printed to the conversation.
