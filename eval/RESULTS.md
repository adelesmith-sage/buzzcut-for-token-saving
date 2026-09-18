# Buzzcut evaluation results

> This is a small internal sample, not a statistically powered study. Each task was run 3 times per condition and the figures below are means; model nondeterminism and service latency still affect results.

Run: `20260918T095109Z`  
Codex CLI: `codex-cli 0.155.0`  
Model: `gpt-5.6-sol` with `high` reasoning  
Repetitions: 3 per condition  
Method: isolated temporary Git repositories; condition order alternated by task; added lines and files measured from the Git diff; token counts read from Codex `turn.completed` usage; wall time measured around `codex exec`; aggregate changes use only matched pairs where both agents completed and passed acceptance tests.

Price-weighted token cost is the primary efficiency measure. Token classes are also reported separately: `Output` is what the agent writes; `Fresh input` is uncached prompt content and can rise because Buzzcut's rules load on every request; `Cached input` is replayed prompt content, billed at roughly a tenth of the fresh rate.

| Task | Condition | Added lines | New files | New deps | Output | Fresh input | Wall time | Tests | Quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Cache template reads | baseline | 3.7 | 0.0 | 0.0 | 1630 | 15747 | 54.03s | 3/3 | n/a |
| Cache template reads | buzzcut | 1.3 | 0.0 | 0.0 | 1067 | 11732 | 35.88s | 2/3 | n/a |
| Add CSV export | baseline | 10.7 | 0.0 | 0.0 | 1166 | 7213 | 43.65s | 3/3 | n/a |
| Add CSV export | buzzcut | 7.3 | 0.0 | 0.0 | 1579 | 16756 | 53.59s | 3/3 | n/a |
| Add suspend endpoint | baseline | 4.0 | 0.0 | 0.0 | 1125 | 8677 | 40.85s | 3/3 | n/a |
| Add suspend endpoint | buzzcut | 4.0 | 0.0 | 0.0 | 1249 | 18323 | 48.55s | 3/3 | n/a |
| Add a refund feature flag | baseline | 5.3 | 0.0 | 0.0 | 1366 | 9775 | 47.75s | 3/3 | n/a |
| Add a refund feature flag | buzzcut | 4.0 | 0.0 | 0.0 | 1264 | 19806 | 43.24s | 3/3 | n/a |
| Log slow requests | baseline | 4.7 | 0.0 | 0.0 | 1373 | 10913 | 46.62s | 3/3 | n/a |
| Log slow requests | buzzcut | 4.0 | 0.0 | 0.0 | 1436 | 8854 | 47.47s | 3/3 | n/a |
| Add invoice retries | baseline | 1.0 | 0.0 | 0.0 | 1429 | 14602 | 48.04s | 3/3 | n/a |
| Add invoice retries | buzzcut | 1.0 | 0.0 | 0.0 | 1355 | 10036 | 48.47s | 3/3 | n/a |
| Apply request timeout | baseline | 3.0 | 0.0 | 0.0 | 1078 | 10526 | 44.88s | 3/3 | n/a |
| Apply request timeout | buzzcut | 1.0 | 0.0 | 0.0 | 1122 | 10757 | 41.35s | 3/3 | n/a |
| Validate user email | baseline | 4.7 | 0.0 | 0.0 | 1309 | 16733 | 41.41s | 3/3 | n/a |
| Validate user email | buzzcut | 4.0 | 0.0 | 0.0 | 1504 | 17845 | 48.78s | 3/3 | n/a |

Aggregate change from baseline to Buzzcut:
- added lines: 37.8 → 27.3 (27.8% reduction)
- new files: 0.0 → 0.0 (no change)
- new dependencies: 0.0 → 0.0 (no change)
- output tokens: 10,559.3 → 10,798.0 (2.3% increase)
- fresh input tokens: 96,836.8 → 111,498.3 (15.1% increase)
- cached input tokens: 809,493.3 → 878,122.7 (8.5% increase)
- price-weighted token cost: 0.3278 → 0.3571 USD (8.9% increase)
- wall-clock time: 366.3 → 374.8 (2.3% increase)
- unsuccessful agent runs: cache/buzzcut#3
- reuse-quality misses: not measured in this run

`Added lines` counts textual additions in the final Git diff, including tests. Price-weighted cost uses indicative gpt-5-class list rates (fresh input $1.25, cached input $0.125, output $10.00 per million tokens) to weight the token classes against each other; it is not a billing statement. `metrics.json` for this run is tracked under `eval/runs/<run id>/`; the raw JSONL, stderr and patches beside it stay local and are ignored.
