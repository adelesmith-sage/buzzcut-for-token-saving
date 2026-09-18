# Buzzcut evaluation results

> This is a small internal sample, not a statistically powered study. Each task was run once per condition; model nondeterminism and service latency can affect results.

Run: `20260918T130929Z`
Codex CLI: `codex-cli 0.155.0`
Model: `gpt-5.6-sol` with `high` reasoning
Repetitions: 1 per condition
Method: isolated temporary Git repositories; condition order alternated by task; added lines and files measured from the Git diff; token counts read from Codex `turn.completed` usage; wall time measured around `codex exec`; aggregate changes use only matched pairs where both agents completed and passed acceptance tests.

Price-weighted token cost is the primary efficiency measure. Token classes are also reported separately: `Output` is what the agent writes; `Fresh input` is uncached prompt content and can rise because Buzzcut's rules load on every request; `Cached input` is replayed prompt content, billed at roughly a tenth of the fresh rate.

| Task | Condition | Added lines | New files | New deps | Output | Fresh input | Wall time | Tests | Quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Cache template reads | baseline | 2.0 | 0.0 | 0.0 | 2027 | 23242 | 66.38s | 1/1 | 1/1 |
| Cache template reads | buzzcut | 2.0 | 0.0 | 0.0 | 1755 | 17062 | 48.39s | 1/1 | 1/1 |
| Add CSV export | baseline | 10.0 | 0.0 | 0.0 | 1141 | 5891 | 39.09s | 1/1 | 0/1 |
| Add CSV export | buzzcut | 0.0 | 0.0 | 0.0 | 1018 | 9990 | 31.44s | 0/1 | 0/1 |
| Add suspend endpoint | baseline | 4.0 | 0.0 | 0.0 | 1253 | 11980 | 38.25s | 1/1 | 1/1 |
| Add suspend endpoint | buzzcut | 0.0 | 0.0 | 0.0 | 1381 | 5602 | 36.67s | 0/1 | 0/1 |
| Add a refund feature flag | baseline | 4.0 | 0.0 | 0.0 | 1081 | 6396 | 55.67s | 1/1 | 1/1 |
| Add a refund feature flag | buzzcut | 0.0 | 0.0 | 0.0 | 627 | 9644 | 21.56s | 0/1 | 0/1 |
| Log slow requests | baseline | 2.0 | 0.0 | 0.0 | 1178 | 9860 | 42.26s | 1/1 | 0/1 |
| Log slow requests | buzzcut | 0.0 | 0.0 | 0.0 | 1073 | 10722 | 37.37s | 0/1 | 0/1 |
| Add invoice retries | baseline | 1.0 | 0.0 | 0.0 | 1175 | 10962 | 39.67s | 1/1 | 1/1 |
| Add invoice retries | buzzcut | 1.0 | 0.0 | 0.0 | 1353 | 12023 | 46.07s | 1/1 | 1/1 |
| Apply request timeout | baseline | 3.0 | 0.0 | 0.0 | 1375 | 7137 | 44.27s | 1/1 | 1/1 |
| Apply request timeout | buzzcut | 1.0 | 0.0 | 0.0 | 1253 | 6297 | 36.61s | 1/1 | 1/1 |
| Validate user email | baseline | 5.0 | 0.0 | 0.0 | 1678 | 11527 | 52.05s | 1/1 | 1/1 |
| Validate user email | buzzcut | 4.0 | 0.0 | 0.0 | 2145 | 20916 | 60.87s | 1/1 | 1/1 |

Aggregate change from baseline to Buzzcut:
- added lines: 11.0 → 8.0 (27.3% reduction)
- new files: 0.0 → 0.0 (no change)
- new dependencies: 0.0 → 0.0 (no change)
- output tokens: 6,255.0 → 6,506.0 (4.0% increase)
- fresh input tokens: 52,868.0 → 56,298.0 (6.5% increase)
- cached input tokens: 484,096.0 → 351,104.0 (27.5% reduction)
- price-weighted token cost: 0.1891 → 0.1793 USD (5.2% reduction)
- wall-clock time: 202.4 → 191.9 (5.2% reduction)
- unsuccessful agent runs: csv_export/buzzcut#1, endpoint/buzzcut#1, feature_flag/buzzcut#1, logging/buzzcut#1
- reuse-quality misses: csv_export/baseline#1, csv_export/buzzcut#1, endpoint/buzzcut#1, feature_flag/buzzcut#1, logging/buzzcut#1, logging/baseline#1

`Added lines` counts textual additions in the final Git diff, including tests. Price-weighted cost uses indicative gpt-5-class list rates (fresh input $1.25, cached input $0.125, output $10.00 per million tokens) to weight the token classes against each other; it is not a billing statement. `metrics.json` for this run is tracked under `eval/runs/<run id>/`; the raw JSONL, stderr and patches beside it stay local and are ignored.
