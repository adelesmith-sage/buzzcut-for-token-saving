# Buzzcut evaluation results

> This is a small internal sample, not a statistically powered study. Each task was run once per condition; model nondeterminism and service latency can affect results.

Run: `20260918T084536Z`  
Codex CLI: `codex-cli 0.154.0-alpha.6.2`  
Model: `gpt-5.6-sol` with `high` reasoning  
Method: isolated temporary Git repositories; condition order alternated by task; added lines and files measured from the Git diff; token counts read from Codex `turn.completed` usage; wall time measured around `codex exec`.

| Task | Condition | Added lines | New files | New deps | Tokens | Wall time | Tests |
|---|---:|---:|---:|---:|---:|---:|---:|
| Cache template reads | baseline | 2 | 0 | 0 | 119944 | 91.20s | pass |
| Cache template reads | buzzcut | 2 | 0 | 0 | 95386 | 39.75s | pass |
| Add CSV export | baseline | 12 | 0 | 0 | 86674 | 66.62s | pass |
| Add CSV export | buzzcut | 6 | 0 | 0 | 95541 | 56.07s | pass |
| Add suspend endpoint | baseline | 4 | 0 | 0 | 158864 | 63.45s | pass |
| Add suspend endpoint | buzzcut | 4 | 0 | 0 | 130709 | 43.81s | pass |
| Add a refund feature flag | baseline | 3 | 0 | 0 | 118338 | 48.30s | pass |
| Add a refund feature flag | buzzcut | 4 | 0 | 0 | 129161 | 38.18s | pass |
| Log slow requests | baseline | 4 | 0 | 0 | 152656 | 69.48s | pass |
| Log slow requests | buzzcut | 4 | 0 | 0 | 134886 | 73.78s | pass |
| Add invoice retries | baseline | 1 | 0 | 0 | 102477 | 85.59s | pass |
| Add invoice retries | buzzcut | 1 | 0 | 0 | 119371 | 40.06s | pass |
| Apply request timeout | baseline | 3 | 0 | 0 | 118184 | 85.77s | pass |
| Apply request timeout | buzzcut | 1 | 0 | 0 | 129418 | 46.95s | pass |
| Validate user email | baseline | 4 | 0 | 0 | 135118 | 106.70s | pass |
| Validate user email | buzzcut | 4 | 0 | 0 | 113105 | 50.28s | pass |

Aggregate change from baseline to Buzzcut:
- added lines: 33 → 26 (21.2% reduction)
- new files: 0 → 0 (no change)
- new dependencies: 0 → 0 (no change)
- tokens: 992255 → 947577 (4.5% reduction)
- wall-clock time: 617.11 → 388.88 (37.0% reduction)
- unsuccessful runs: none

`Added lines` counts textual additions in the final Git diff, including tests. `Tokens` is input plus output tokens; cached input remains part of the reported input count. `metrics.json` for this run is tracked under `eval/runs/<run id>/`; the raw JSONL, stderr and patches beside it stay local and are ignored.
