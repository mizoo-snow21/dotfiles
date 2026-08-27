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

Write the value straight to its target (`.env.local` and the like) and validate the format by regex. Keep it out of stdout, out of logs, and out of the transcript.
