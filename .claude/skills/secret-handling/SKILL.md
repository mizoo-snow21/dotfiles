---
name: secret-handling
description: Use when fetching a secret, credential, or API key from a secret store. Reaching for the wrong one first reads as credential-scanning and gets the request denied.
---

# Secret Handling

## Find the canonical name before fetching

Derive the secret ID and its field name from the project's own config, then fetch that single entry:

```bash
rg -n "SECRET_NAME|secretName" scripts/ infrastructure/
```

The CDK / Terraform constructs carry the same answer. Fetch one named entry.

Guessing at names, or listing several secrets to find the right one, reads as credential-scanning and gets denied — so the lookup above is the fast path, not the careful path.

## Move the value without displaying it

Write the value straight to its target (`.env.local` and the like) and validate the format by regex. Keep it out of stdout, out of logs, and out of the transcript — on every path, the failure branch included.

- **Extract before you test.** A secret can be JSON (`{"apiKey":"sk-…"}`). Pull the field out first (`jq -r .apiKey`), then print only its shape and length. A format check that echoes the value on mismatch prints the whole secret the first time the shape surprises you.
- **Keep stderr apart.** Send the CLI's stderr to its own file (`2>err.log`); with `2>&1` into a parser, an error message gets read as the value.
- **Tracing is output.** `bash -x` / `set -x` prints every expansion, so a script holding a token leaks it wherever it is used (`PGPASSWORD="$TOKEN"`) — even with tracing switched on only after the fetch. Debug with `bash -n`, the script's own output file, the failing command run without credentials, or step markers (`echo "step: fetched" >&2`). If a trace already reached a file, delete that file first.
