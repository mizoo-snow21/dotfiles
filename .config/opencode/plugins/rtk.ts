import { Plugin } from "@opencode/plugin"
import { execFile } from "node:child_process"
import { promisify } from "node:util"

const run = promisify(execFile)

// RTK OpenCode plugin (v2) — rewrites shell commands to use rtk for token savings.
// Requires: rtk >= 0.23.0 in PATH.
//
// All rewrite logic lives in `rtk rewrite`, which is the single source of truth
// (src/discover/registry.rs). To add or change rules, edit the Rust registry —
// not this file.
export default Plugin.define({
  id: "rtk",
  async setup(ctx) {
    try {
      await run("rtk", ["--version"])
    } catch {
      console.warn("[rtk] rtk binary not found in PATH — plugin disabled")
      return
    }

    // ponytail: shell.create.before covers every shell command, so no per-tool
    // allowlist is needed the way the v1 plugin filtered on bash/shell.
    await ctx.shell.hook("create.before", async (input) => {
      if (!input.command) return
      try {
        const { stdout } = await run("rtk", ["rewrite", input.command])
        const rewritten = stdout.trim()
        if (rewritten && rewritten !== input.command) {
          if (process.env.RTK_PLUGIN_DEBUG) console.warn(`[rtk] ${input.command} -> ${rewritten}`)
          input.command = rewritten
        }
      } catch {
        // rtk rewrite failed — pass through unchanged
      }
    })
  },
})
