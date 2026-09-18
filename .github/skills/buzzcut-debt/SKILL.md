---
name: buzzcut-debt
description: Find and assess deliberate Buzzcut simplifications recorded in source comments. Use when asked to review Buzzcut limits, shortcuts or deferred replacement conditions.
argument-hint: "[optional folder or marker]"
disable-model-invocation: true
---

# Buzzcut debt

Search first-party source in the requested scope for comments containing `buzzcut:`. Do not modify files or create a separate debt ledger unless the user explicitly asks.

For each marker:

1. Read the surrounding implementation.
2. Identify the current limit and its stated replacement condition.
3. Check available repository evidence to see whether that condition is now true.
4. Report one of `keep`, `replace now` or `clarify`.

Use this format:

`file:line - status - current limit - replacement condition - smallest next action`

Flag markers that lack a concrete limit or measurable replacement condition. If no markers exist, say `Buzzcut debt: no deliberate limits recorded.`

