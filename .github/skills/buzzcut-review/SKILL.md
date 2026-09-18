---
name: buzzcut-review
description: Review the current diff for unnecessary complexity and propose the smallest correct alternatives. Use when asked to review a change for over-engineering, bloat or avoidable code.
argument-hint: "[optional file, commit or diff scope]"
disable-model-invocation: true
---

# Buzzcut review

Review the requested scope, or the staged and unstaged diff when no scope is given. Do not modify files.

1. Read `.github/copilot-instructions.md`.
2. Read enough surrounding code to understand each change.
3. Search for existing helpers, patterns and callers before claiming duplication or a misplaced fix.
4. Check whether the standard library, platform, framework or an installed dependency already covers the change.
5. Flag only actionable over-engineering. Never recommend removing required validation, data-loss protection, security, privacy, accessibility, compliance behaviour or explicitly requested behaviour.

Report each finding as:

`file:line - what is over-built - the smallest correct alternative`

Order findings by impact. If the change is already minimal and correct, say `Buzzcut review: no cuts needed.` and stop.

