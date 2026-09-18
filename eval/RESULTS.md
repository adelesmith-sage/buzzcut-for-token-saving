# Buzzcut evaluation results

> This is a small internal sample, not a statistically powered study. Each task was run 3 times per condition and the figures below are means; model nondeterminism and service latency still affect results.

Run: `20260918T095109Z`  
Codex CLI: `codex-cli 0.155.0`  
Model: `gpt-5.6-sol` with `high` reasoning  
Repetitions: 3 per condition  
Method: isolated temporary Git repositories; condition order alternated by task; added lines and files measured from the Git diff; token counts read from Codex `turn.completed` usage; wall time measured around `codex exec`.

Token classes are reported separately because they behave differently. `Output` is what the agent writes, and is the figure Buzzcut is designed to move. `Fresh input` is uncached prompt content, which Buzzcut *increases* because its rules are loaded on every request. `Cached input` is replayed prompt content, billed at roughly a tenth of the fresh rate.

| Task | Condition | Added lines | New files | New deps | Output | Fresh input | Wall time | Tests |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Cache template reads | baseline | 3.7 | 0.0 | 0.0 | 1630 | 15747 | 54.03s | 3/3 |
| Cache template reads | buzzcut | 1.3 | 0.0 | 0.0 | 1067 | 11732 | 35.88s | 2/3 |
| Add CSV export | baseline | 10.7 | 0.0 | 0.0 | 1166 | 7213 | 43.65s | 3/3 |
| Add CSV export | buzzcut | 7.3 | 0.0 | 0.0 | 1579 | 16756 | 53.59s | 3/3 |
| Add suspend endpoint | baseline | 4.0 | 0.0 | 0.0 | 1125 | 8677 | 40.85s | 3/3 |
| Add suspend endpoint | buzzcut | 4.0 | 0.0 | 0.0 | 1249 | 18323 | 48.55s | 3/3 |
| Add a refund feature flag | baseline | 5.3 | 0.0 | 0.0 | 1366 | 9775 | 47.75s | 3/3 |
| Add a refund feature flag | buzzcut | 4.0 | 0.0 | 0.0 | 1264 | 19806 | 43.24s | 3/3 |
| Log slow requests | baseline | 4.7 | 0.0 | 0.0 | 1373 | 10913 | 46.62s | 3/3 |
| Log slow requests | buzzcut | 4.0 | 0.0 | 0.0 | 1436 | 8854 | 47.47s | 3/3 |
| Add invoice retries | baseline | 1.0 | 0.0 | 0.0 | 1429 | 14602 | 48.04s | 3/3 |
| Add invoice retries | buzzcut | 1.0 | 0.0 | 0.0 | 1355 | 10036 | 48.47s | 3/3 |
| Apply request timeout | baseline | 3.0 | 0.0 | 0.0 | 1078 | 10526 | 44.88s | 3/3 |
| Apply request timeout | buzzcut | 1.0 | 0.0 | 0.0 | 1122 | 10757 | 41.35s | 3/3 |
| Validate user email | baseline | 4.7 | 0.0 | 0.0 | 1309 | 16733 | 41.41s | 3/3 |
| Validate user email | buzzcut | 4.0 | 0.0 | 0.0 | 1504 | 17845 | 48.78s | 3/3 |

Aggregate change from baseline to Buzzcut:
- added lines: 37.0 → 26.7 (27.9% reduction)
- new files: 0.0 → 0.0 (no change)
- new dependencies: 0.0 → 0.0 (no change)
- output tokens: 10,476.7 → 10,577.3 (1.0% increase)
- fresh input tokens: 94,186.3 → 114,109.0 (21.2% increase)
- cached input tokens: 814,506.7 → 845,738.7 (3.8% increase)
- price-weighted token cost: 0.3243 → 0.3541 USD (9.2% increase)
- wall-clock time: 367.2 → 367.3 (0.0% increase)
- unsuccessful runs: cache/buzzcut#3

`Added lines` counts textual additions in the final Git diff, including tests. Price-weighted cost uses indicative gpt-5-class list rates (fresh input $1.25, cached input $0.125, output $10.00 per million tokens) to weight the token classes against each other; it is not a billing statement. `metrics.json` for this run is tracked under `eval/runs/<run id>/`; the raw JSONL, stderr and patches beside it stay local and are ignored.
