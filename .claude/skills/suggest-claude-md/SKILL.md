---
name: suggest-claude-md
description: >
  Analyze conversation history and propose new rules or patterns to add to CLAUDE.md.
  Use when the user runs /suggest-claude-md or asks to review the session for CLAUDE.md updates.
---

# Suggest CLAUDE.md Updates

Analyze the current conversation history and propose concrete additions to CLAUDE.md — not summaries or explanations, but actionable rules and patterns worth persisting.

## Usage

```
/suggest-claude-md
```

## Analysis Criteria

Scan the conversation for content matching these three trigger conditions:

### 1. Project-Specific Rules

**Detection patterns**:
- "Use X instead of Y"
- "In this project we do it like this"
- Standard code was generated, then the user corrected it to follow a project-specific convention

**Examples**:
- "Use the project's Config module instead of reading env vars directly"
- "Controllers in this project never pass params directly"
- "Use the existing finder methods instead of the ORM's built-in query methods"

### 2. Repeated Correction Patterns

**Detection patterns**:
- The same kind of correction appears 2+ times
- Similar code fixes are applied across multiple files
- The same advice is given more than once

**Examples**:
- The same setup boilerplate was requested in multiple test files
- The same controller pattern was corrected across several controllers
- The same finder method usage was enforced across multiple models

### 3. Cross-Cutting Consistency Rules

**Detection patterns**:
- "Keep these two implementations in sync"
- "Web and API sides should be consistent"
- "The regular version and the WebView version must match"
- Instructions to unify related code in multiple locations

**Examples**:
- "If the Web route is `/brands/:brand_id/series`, the API route should be `/api/brands/:brand_id/series`"
- "When you update `/xxx`, also update `/webview/xxx` the same way"
- "Use this same image upload pattern for all models"

## Output Format

**Required**: Always use the format below. Do not output summaries, reports, or explanations.

When triggers are found:

```
Analyzed the conversation history. Consider adding the following to CLAUDE.md:

If this looks right, tell me "Add this to CLAUDE.md" and I'll apply it.

[Proposed content — ready to paste into CLAUDE.md]

Reason: [Project-specific rule / Repeated correction (N times) / Cross-cutting consistency rule]
```

When no triggers are found:

```
Analyzed the conversation history. No new content to add to CLAUDE.md was found.
```

**Prohibited**:
- Do not write completion reports like "Fixed X" or "Implemented Y"
- Do not summarize the conversation
- Do not omit the opening "Analyzed the conversation history." line

## Proposal Criteria

### Propose (yes)
- Universal rules that should apply across the project
- Technically accurate content
- Clearly expressible as a rule
- New patterns that emerged from the current code changes

### Do not propose (no)
- One-off judgments or case-specific workarounds
- Content already present in CLAUDE.md
- Personal preferences or temporary experiments
- Vague or ambiguous instructions

## Post-Execution Actions

1. Review the proposed content
2. If appropriate, instruct Claude to add it to CLAUDE.md
3. Include the CLAUDE.md change in the same PR as the code changes
4. Have team members review the update during PR review
