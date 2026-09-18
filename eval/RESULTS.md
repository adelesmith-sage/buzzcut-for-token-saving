# Buzzcut evaluation results

> This is a small internal sample, not a statistically powered study. Each task was run once per condition; model nondeterminism and service latency can affect results.

Run: `20260918T132225Z`
Codex CLI: `codex-cli 0.155.0`
Model: `gpt-5.6-sol` with `high` reasoning
Repetitions: 1 per condition
Shell output wrappers: on
Method: isolated temporary Git repositories; condition order alternated by task; added lines and files measured from the Git diff; token counts read from Codex `turn.completed` usage; wall time measured around `codex exec`; aggregate changes use only matched pairs where both agents completed and passed acceptance tests.

Price-weighted token cost is the primary efficiency measure. Token classes are also reported separately: `Output` is what the agent writes; `Fresh input` is uncached prompt content and can rise because Buzzcut's rules load on every request; `Cached input` is replayed prompt content, billed at roughly a tenth of the fresh rate.

| Task | Condition | Added lines | New files | New deps | Output | Fresh input | Wall time | Tests | Quality |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Cache template reads | baseline | 2.0 | 0.0 | 0.0 | 1724 | 11391 | 50.17s | 1/1 | 1/1 |
| Cache template reads | buzzcut | 2.0 | 0.0 | 0.0 | 1057 | 6614 | 37.56s | 1/1 | 1/1 |
| Add CSV export | baseline | 10.0 | 0.0 | 0.0 | 1221 | 16750 | 39.68s | 1/1 | 0/1 |
| Add CSV export | buzzcut | 6.0 | 0.0 | 0.0 | 819 | 16830 | 28.10s | 1/1 | 1/1 |
| Add suspend endpoint | baseline | 4.0 | 0.0 | 0.0 | 1122 | 5871 | 45.27s | 1/1 | 1/1 |
| Add suspend endpoint | buzzcut | 4.0 | 0.0 | 0.0 | 1037 | 10645 | 31.17s | 1/1 | 1/1 |
| Add a refund feature flag | baseline | 5.0 | 0.0 | 0.0 | 1103 | 21839 | 54.16s | 1/1 | 1/1 |
| Add a refund feature flag | buzzcut | 1.0 | 0.0 | 0.0 | 1059 | 10771 | 54.67s | 1/1 | 0/1 |
| Log slow requests | baseline | 4.0 | 0.0 | 0.0 | 1973 | 12529 | 65.82s | 1/1 | 1/1 |
| Log slow requests | buzzcut | 4.0 | 0.0 | 0.0 | 1013 | 7063 | 38.44s | 1/1 | 1/1 |
| Add invoice retries | baseline | 1.0 | 0.0 | 0.0 | 1258 | 10219 | 45.87s | 1/1 | 1/1 |
| Add invoice retries | buzzcut | 1.0 | 0.0 | 0.0 | 860 | 10027 | 32.14s | 1/1 | 1/1 |
| Apply request timeout | baseline | 3.0 | 0.0 | 0.0 | 1177 | 21239 | 36.09s | 1/1 | 1/1 |
| Apply request timeout | buzzcut | 3.0 | 0.0 | 0.0 | 943 | 6541 | 41.02s | 1/1 | 1/1 |
| Validate user email | baseline | 5.0 | 0.0 | 0.0 | 2128 | 8487 | 60.60s | 1/1 | 1/1 |
| Validate user email | buzzcut | 4.0 | 0.0 | 0.0 | 1290 | 7128 | 39.67s | 1/1 | 1/1 |

Aggregate change from baseline to Buzzcut:
- added lines: 34.0 → 25.0 (26.5% reduction)
- new files: 0.0 → 0.0 (no change)
- new dependencies: 0.0 → 0.0 (no change)
- output tokens: 11,706.0 → 8,078.0 (31.0% reduction)
- fresh input tokens: 108,325.0 → 75,619.0 (30.2% reduction)
- cached input tokens: 832,128.0 → 682,240.0 (18.0% reduction)
- price-weighted token cost: 0.3565 → 0.2606 USD (26.9% reduction)
- wall-clock time: 397.7 → 302.8 (23.9% reduction)
- unsuccessful agent runs: none
- reuse-quality misses: csv_export/baseline#1, feature_flag/buzzcut#1

`Added lines` counts textual additions in the final Git diff, including tests. Price-weighted cost uses indicative gpt-5-class list rates (fresh input $1.25, cached input $0.125, output $10.00 per million tokens) to weight the token classes against each other; it is not a billing statement. `metrics.json` for this run is tracked under `eval/runs/<run id>/`; the raw JSONL, stderr and patches beside it stay local and are ignored.
