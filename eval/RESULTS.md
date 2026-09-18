# Buzzcut evaluation results

> This is a small internal sample, not a statistically powered study. Each task was run once per condition; model nondeterminism and service latency can affect results.

Run: `20260918T124411Z`  
Codex CLI: `codex-cli 0.155.0`  
Model: `gpt-5.6-sol` with `high` reasoning  
Repetitions: 1 per condition  
Method: isolated temporary Git repositories; condition order alternated by task; added lines and files measured from the Git diff; token counts read from Codex `turn.completed` usage; wall time measured around `codex exec`; aggregate changes use only matched pairs where both agents completed and passed acceptance tests.

Price-weighted token cost is the primary efficiency measure. Token classes are also reported separately: `Output` is what the agent writes; `Fresh input` is uncached prompt content and can rise because Buzzcut's rules load on every request; `Cached input` is replayed prompt content, billed at roughly a tenth of the fresh rate.

| Task | Condition | Added lines | New files | New deps | Output | Fresh input | Wall time | Tests | Quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Cache template reads | baseline | 2.0 | 0.0 | 0.0 | 1987 | 7916 | 65.36s | 1/1 | 1/1 |
| Cache template reads | buzzcut | 2.0 | 0.0 | 0.0 | 1148 | 16937 | 38.26s | 1/1 | 1/1 |
| Add CSV export | baseline | 10.0 | 0.0 | 0.0 | 996 | 5702 | 39.25s | 1/1 | 0/1 |
| Add CSV export | buzzcut | 10.0 | 0.0 | 0.0 | 1017 | 16389 | 30.56s | 1/1 | 0/1 |
| Add suspend endpoint | baseline | 4.0 | 0.0 | 0.0 | 1496 | 6650 | 46.72s | 1/1 | 1/1 |
| Add suspend endpoint | buzzcut | 4.0 | 0.0 | 0.0 | 1091 | 11514 | 36.68s | 1/1 | 1/1 |
| Add a refund feature flag | baseline | 4.0 | 0.0 | 0.0 | 1360 | 11151 | 44.90s | 1/1 | 1/1 |
| Add a refund feature flag | buzzcut | 1.0 | 0.0 | 0.0 | 866 | 25499 | 29.24s | 1/1 | 0/1 |
| Log slow requests | baseline | 4.0 | 0.0 | 0.0 | 1392 | 10876 | 52.05s | 1/1 | 1/1 |
| Log slow requests | buzzcut | 4.0 | 0.0 | 0.0 | 1004 | 7029 | 36.36s | 1/1 | 1/1 |
| Add invoice retries | baseline | 1.0 | 0.0 | 0.0 | 1007 | 10985 | 33.16s | 1/1 | 1/1 |
| Add invoice retries | buzzcut | 1.0 | 0.0 | 0.0 | 1021 | 12545 | 36.82s | 1/1 | 1/1 |
| Apply request timeout | baseline | 3.0 | 0.0 | 0.0 | 1042 | 20501 | 36.25s | 1/1 | 1/1 |
| Apply request timeout | buzzcut | 1.0 | 0.0 | 0.0 | 929 | 6370 | 30.36s | 1/1 | 1/1 |
| Validate user email | baseline | 5.0 | 0.0 | 0.0 | 1358 | 6093 | 41.94s | 1/1 | 1/1 |
| Validate user email | buzzcut | 4.0 | 0.0 | 0.0 | 988 | 26648 | 34.48s | 1/1 | 1/1 |

Aggregate change from baseline to Buzzcut:
- added lines: 33.0 → 27.0 (18.2% reduction)
- new files: 0.0 → 0.0 (no change)
- new dependencies: 0.0 → 0.0 (no change)
- output tokens: 10,638.0 → 8,064.0 (24.2% reduction)
- fresh input tokens: 79,874.0 → 122,931.0 (53.9% increase)
- cached input tokens: 824,448.0 → 662,144.0 (19.7% reduction)
- price-weighted token cost: 0.3093 → 0.3171 USD (2.5% increase)
- wall-clock time: 359.6 → 272.8 (24.2% reduction)
- unsuccessful agent runs: none
- reuse-quality misses: csv_export/baseline#1, csv_export/buzzcut#1, feature_flag/buzzcut#1

`Added lines` counts textual additions in the final Git diff, including tests. Price-weighted cost uses indicative gpt-5-class list rates (fresh input $1.25, cached input $0.125, output $10.00 per million tokens) to weight the token classes against each other; it is not a billing statement. `metrics.json` for this run is tracked under `eval/runs/<run id>/`; the raw JSONL, stderr and patches beside it stay local and are ignored.
