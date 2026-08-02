---
name: playwright-generate-test
description: 'Generate a Playwright test based on a scenario using Playwright MCP. Use whenever the user wants to create, record, or scaffold an E2E/UI test — "write a test for this flow", "テスト書いて", converting a verified demo flow into a persistent test, or growing an existing e2e/ suite.'
---

# Test Generation with Playwright MCP

Your goal is to generate a Playwright test based on the provided scenario after completing all prescribed steps.

## Workflow

1. You are given a scenario. If the user does not provide one, ask them for it.
2. Before touching the browser, inspect the repo's existing test setup: `playwright.config.ts` (testDir, baseURL, projects, fixtures) and the naming/helper conventions of existing tests. The generated test must land in the configured test directory and follow the existing style — don't invent a parallel structure.
3. Confirm the target is a local or test/staging environment (the config's `baseURL` is a strong hint). Never execute state-changing steps against production. If a scenario step is destructive or irreversible (deletion, payment, sending notifications), get explicit user confirmation before running it live.
4. DO NOT generate test code prematurely based solely on the scenario. Run the steps one by one using the Playwright MCP tools — the real page reveals selectors, waits, and states that a scenario description hides.
5. After executing the steps, propose the test items you detected (actions, assertions, edge cases) as a short list and get the user's approval before writing code. Wrong assumptions are cheapest to fix here.
6. Only after approval, emit a Playwright TypeScript test using `@playwright/test` based on message history.
7. Save the generated test file in the repo's configured test directory, following existing naming conventions.
8. Execute the test file and iterate until it passes.
9. Generated assertions encode *current* behavior, not necessarily *correct* behavior. Flag any assertion you are not sure matches the intended spec — confirming spec-correctness is the human's job.

## Selector strategy

Pick the highest option that uniquely matches; inspect the real page via MCP to confirm stability:

1. `getByRole('...', { name: '...' })` — survives DOM refactors and matches what users perceive
2. `getByText(...)` / `getByLabel(...)`
3. Stable attributes: `data-testid`, `input[name="..."]`
4. CSS classes — last resort

Never use auto-generated or dynamic IDs.

## Suite architecture — scale to the situation

**1–2 one-off tests:** write them inline. No page objects, no helper layers — abstraction before repetition is waste.

**A growing suite (3+ tests sharing screens or flows):**

- **Screen Object + fluent chaining** — each business action returns a `Promise` of a fresh screen instance, so steps stay independent and tests read like a spec:

  ```typescript
  await OrderPortal.new(page, "stg-1")
    .then(p => p.申込数量を選択する({ new: 1 }))
    .then(p => p.商品カテゴリを選択する("スタンダード"));
  ```

- **Locator function dictionary** — store locators as `(page: Page) => Locator` functions, not resolved locators. Lazy evaluation lets the same dictionary serve the main page, popups, and new tabs:

  ```typescript
  const orderPortal = {
    見積もり作成に進む: (page: Page) =>
      page.getByRole("link", { name: "見積もり作成に進む" }),
  };
  ```

- **Naming:** business-flow methods mirror the exact UI label (Japanese when the UI is Japanese) so non-developers map code to screen 1:1; infrastructure methods (`login`, `gotoHome`) stay English.
- **Environment switching:** type it (`env: "stg-1" | "stg-2"`) so a typo is a compile error, not a mysterious failure against the wrong environment.

## Fixture vs common class

| Situation | Use |
|---|---|
| Every test needs the same guaranteed initial state (logged-in page, seeded data) | Fixture (`base.extend`) |
| The test exercises a state-changing business flow (add → remove → re-add) | Common class the test drives step by step |

Fixtures buy setup reuse and a stable starting point; classes buy flexibility when the state changes ARE the test. Avoid stacking many fixtures — combined state becomes hard to trace.

## Reliability rules

- **Popups/new tabs:** register the listener *before* the click, or the event is lost:

  ```typescript
  const popupPromise = page.waitForEvent('popup');
  await page.getByRole('link', { name: '新規タブで開く' }).click();
  const popup = await popupPromise;
  ```

- **Unique test data:** `Date.now()` alone collides under parallel workers and retries — combine identity and time, e.g. `testuser-${testInfo.workerIndex}-${Date.now()}`, or use `crypto.randomUUID()`.
- **Viewport matters:** a test that passes at 375px can fail at tablet width once the layout reflows. If the scenario is device-dependent, run it at each target width before finalizing assertions.
- **CI runs committed tests only.** Agent-driven generation belongs in development — it is slow, token-expensive, and non-deterministic. Commit the generated tests and let CI just execute them.
