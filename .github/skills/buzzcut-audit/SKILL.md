---
name: buzzcut-audit
description: Audit first-party repository code for high-value simplifications using the Buzzcut ladder. Use when asked to find unnecessary complexity beyond the current diff.
argument-hint: "[optional folder or subsystem]"
disable-model-invocation: true
---

# Buzzcut audit

Audit the requested area, or the repository when no area is given. Do not modify files.

Skip generated code, vendored code, third-party dependencies, build output, lock files and snapshots. Read enough context to distinguish accidental complexity from necessary domain behaviour. Search for existing helpers and inspect callers before reporting a finding.

Look for:

- code for a problem that no longer exists
- duplicate repository behaviour
- reimplemented language, standard-library, platform, framework or dependency features
- unneeded abstractions, wrappers or extension points
- speculative logging, retries, configuration or error paths
- repeated fixes that belong at one shared root cause

Never suggest cutting required validation, data-loss protection, security, privacy, accessibility, compliance behaviour or explicitly required behaviour.

Report at most the five highest-value findings, grouped by folder:

`file:line - evidence of the issue - the smallest correct fix`

State how many additional candidates were omitted. If there are none, say `Buzzcut audit: no worthwhile cuts found.`

