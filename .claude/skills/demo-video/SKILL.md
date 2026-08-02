---
name: demo-video
description: Generate a Playwright script that records a video walkthrough of a demo flow, then execute it. Use when the user wants a video recording of a demo story.
---

# Demo Video

Generate and execute a Playwright script that records a video walkthrough of a demo flow.

## Workflow

1. **Locate flow definition**: Look for a flow definition in one of these places (in priority order):
   - User-provided steps in the prompt
   - `tasks/todo.md` verification section
   - `tasks/plan.md` verification section
   - Recent `/demo-walkthrough` results in the conversation
   - Ask the user for the flow steps

2. **Prepare output directory**:
   ```bash
   mkdir -p <project>/demo-video
   ```

3. **Ensure dev server is running.** Use the project's actual dev command and port (check `package.json`) — the same port goes into `BASE` in the script below. Launch as a managed background task (not a bare `&`), then poll until it responds:
   ```bash
   ok=""; for i in $(seq 1 30); do curl -sf -o /dev/null http://localhost:<port> && { ok=1; break; }; sleep 1; done
   [ -n "$ok" ] || { echo "dev server not ready — aborting"; exit 1; }
   ```

4. **Generate the Playwright script**: Write a TypeScript file at `e2e/demo-walkthrough-video.ts`:

   ```ts
   import { chromium } from 'playwright';
   import path from 'path';

   const BASE = 'http://localhost:<port>';
   const sleep = (ms: number) => new Promise(r => setTimeout(r, ms));

   (async () => {
       const browser = await chromium.launch({ headless: true });
       const context = await browser.newContext({
           viewport: { width: 1440, height: 900 },
           recordVideo: {
               dir: path.resolve('demo-video'), // cwd-relative — __dirname is undefined in ESM projects
               size: { width: 1440, height: 900 },
           },
       });
       const page = await context.newPage();

       // Steps go here — each step has:
       // 1. Navigation or click action
       // 2. waitForURL or waitForLoadState
       // 3. sleep() for visual pacing (1500-3000ms between steps)

       await context.close();
       await browser.close();
       console.log('✅ Demo video saved to demo-video/');
   })();
   ```

   Key principles for the script:
   - Use `sleep()` between steps for visual pacing (1500-3000ms)
   - Prefer `page.getByRole('button', { name: '...' }).click()` for interactions; fall back to `text=` / `:has-text()` only when the element has no role or accessible name
   - Use `page.waitForURL()` after navigation actions
   - Use `page.evaluate(() => window.scrollTo(...))` to show below-the-fold content
   - Add extra pauses (2000-3000ms) on important screens like dashboards and analysis results
   - For form interactions, use `page.selectOption()` and `page.fill()`

5. **Execute the script**:
   ```bash
   npx tsx e2e/demo-walkthrough-video.ts
   ```

6. **Rename the output**: Playwright saves videos with random UUIDs. Rename to something descriptive:
   ```bash
   mv demo-video/<uuid>.webm demo-video/demo-walkthrough-<date>.webm
   ```

7. **Report**: Print the output path and file size.

## Rules

- Always use `headless: true` — video recording works in headless mode
- Run the script from the project root and avoid `__dirname` in the template — it is undefined in ESM projects; use cwd-relative paths like `path.resolve('demo-video')`
- Default viewport: 1440x900 (widescreen, good for demos)
- Default video size matches viewport
- Use `context.close()` (not `browser.close()`) first — this finalizes the video file
- The script MUST `await context.close()` before `browser.close()`, otherwise the video may be truncated
- If the `playwright` npm package is missing, install it first (`npm i -D playwright`) — `npx playwright install chromium` only downloads the browser binary, not the package the script imports
- The video format is always `.webm` (VP8 codec)
- For long flows, keep total duration under 60 seconds for shareability
- If the user provides an existing script path, execute it directly instead of generating a new one
- If the flow opens a popup/new tab, register the listener before the click (`const popupPromise = page.waitForEvent('popup');` → click → `await popupPromise`) — a listener added after the click misses the event

## Example invocation

User: `/demo-video`
→ Generates script from todo.md verification steps, executes it, saves webm.

User: `/demo-video e2e/demo-walkthrough-video.ts`
→ Executes the existing script directly.

## Output

Video file saved to `demo-video/demo-walkthrough-<date>.webm`.
