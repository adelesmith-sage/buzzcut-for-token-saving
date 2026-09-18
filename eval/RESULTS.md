# Buzzcut evaluation results

> This is a small internal sample, not a statistically powered study. Each task was run once per condition; model nondeterminism and service latency can affect results.

Run: `20260918T084536Z`  
Codex CLI: `codex-cli 0.154.0-alpha.6.2`  
Model: `gpt-5.6-sol` with `high` reasoning  
Method: isolated temporary Git repositories; condition order alternated by task; added lines and files measured from the Git diff; token counts read from Codex `turn.completed` usage; wall time measured around `codex exec`.

Token classes are reported separately because they behave differently. `Output` is what the agent writes, and is the figure Buzzcut is designed to move. `Fresh input` is uncached prompt content, which Buzzcut *increases* because its rules are loaded on every request. `Cached input` is replayed prompt content, billed at roughly a tenth of the fresh rate.

| Task | Condition | Added lines | New files | New deps | Output | Fresh input | Wall time | Tests |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Cache template reads | baseline | 2 | 0 | 0 | 1659 | 6669 | 91.20s | pass |
| Cache template reads | buzzcut | 2 | 0 | 0 | 1118 | 12220 | 39.75s | pass |
| Add CSV export | baseline | 12 | 0 | 0 | 928 | 5362 | 66.62s | pass |
| Add CSV export | buzzcut | 6 | 0 | 0 | 1058 | 11283 | 56.07s | pass |
| Add suspend endpoint | baseline | 4 | 0 | 0 | 2093 | 14307 | 63.45s | pass |
| Add suspend endpoint | buzzcut | 4 | 0 | 0 | 1243 | 12218 | 43.81s | pass |
| Add a refund feature flag | baseline | 3 | 0 | 0 | 1362 | 9584 | 48.30s | pass |
| Add a refund feature flag | buzzcut | 4 | 0 | 0 | 1131 | 7582 | 38.18s | pass |
| Log slow requests | baseline | 4 | 0 | 0 | 2057 | 17095 | 69.48s | pass |
| Log slow requests | buzzcut | 4 | 0 | 0 | 1152 | 17894 | 73.78s | pass |
| Add invoice retries | baseline | 1 | 0 | 0 | 1167 | 6078 | 85.59s | pass |
| Add invoice retries | buzzcut | 1 | 0 | 0 | 1170 | 15289 | 40.06s | pass |
| Apply request timeout | baseline | 3 | 0 | 0 | 1256 | 6208 | 85.77s | pass |
| Apply request timeout | buzzcut | 1 | 0 | 0 | 1301 | 13557 | 46.95s | pass |
| Validate user email | baseline | 4 | 0 | 0 | 1501 | 6641 | 106.70s | pass |
| Validate user email | buzzcut | 4 | 0 | 0 | 1235 | 7294 | 50.28s | pass |

Aggregate change from baseline to Buzzcut:
- added lines: 33 → 26 (21.2% reduction)
- new files: 0 → 0 (no change)
- new dependencies: 0 → 0 (no change)
- output tokens: 12023 → 9408 (21.7% reduction)
- fresh input tokens: 71944 → 97337 (35.3% increase)
- cached input tokens: 908288 → 840832 (7.4% reduction)
- price-weighted token cost: 0.3237 → 0.3209 USD (0.9% reduction)
- wall-clock time: 617.11 → 388.88 (37.0% reduction)
- unsuccessful runs: none

`Added lines` counts textual additions in the final Git diff, including tests. Price-weighted cost uses indicative gpt-5-class list rates (fresh input $1.25, cached input $0.125, output $10.00 per million tokens) to weight the token classes against each other; it is not a billing statement. `metrics.json` for this run is tracked under `eval/runs/<run id>/`; the raw JSONL, stderr and patches beside it stay local and are ignored.
