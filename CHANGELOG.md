# Changelog

All notable changes to Buzzcut are recorded here. This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## Unreleased

### Changed

- Reduced the always-loaded guardrails from 5.48 KB to 3.99 KB while retaining all nine triggers, exceptions and examples. The execution guidance now requires one capability search across filenames and symbols before new code is added. The selectable agent prompt fell from 2.75 KB to 0.85 KB by referencing the canonical rules instead of repeating them.
- Made price-weighted token cost the primary efficiency measure and added deterministic reuse-quality checks to every eval task.
- Excluded failed or unpaired runs from aggregate comparisons so a stalled zero-line run cannot improve the code-reduction headline. The corrected three-repeat result is 27.8% fewer added lines and 8.9% higher price-weighted cost.

### Optimization screen

- A one-task, one-repeat cache screen of the compact rules measured 8.8% lower price-weighted token cost and 10.5% fewer output tokens, with identical two-line implementations and both acceptance and reuse checks passing. This is directional evidence only; the repeated eight-task result remains the headline until the compact rules receive a full rerun.

## 1.0.0

First release intended for use across teams.

### Added

- Nine ordered guardrails in `AGENTS.md` and `.github/copilot-instructions.md`, each stating its trigger, required action, exception and a paired good/bad example. The two files are byte-identical so that GitHub Copilot and Codex apply the same rules.
- A selectable **Buzzcut** agent (`.github/agents/buzzcut.agent.md`) for changes that especially need to stay small; it reports what it deliberately left out.
- Three read-only Agent Skills: `/buzzcut-review` for the current diff, `/buzzcut-audit` for a folder or repository, and `/buzzcut-debt` for recorded `buzzcut:` limits.
- A standard-library-only paired Codex eval harness with eight over-engineering-prone tasks, measuring added lines, new files, declared dependencies, tokens, wall time and acceptance-test results.
- `README.md` with installation for repository-wide and personal use, rollout guidance and the measured results, and a `verify` workflow that fails if the two rule files drift or if an agent, skill or task file is malformed. The repository is Sage-internal and carries no open-source licence.

### Results

Measured over eight tasks with three repetitions per condition (48 runs), recorded in [eval/RESULTS.md](eval/RESULTS.md): Buzzcut produced **27.8% fewer added lines** across matched successful runs, on 6 of 8 tasks, and added no files or dependencies.

It did not reduce tokens or time. Output tokens and wall-clock time each rose 2.3%; fresh input rose 15.1% because the rules load on every request. Price-weighted token cost rose 8.9%.

One of 24 Buzzcut runs stalled without making a change, blocked by the AI-label rule when the Sage label format was absent from the repository.

### Fixed

- Token reporting previously combined cached input, fresh input and output into one figure. Cached input is over 90% of that total and is billed at roughly a tenth of the fresh rate, so the combined number tracked conversation length rather than the instructions. The three classes are now reported separately, alongside a price-weighted total.
- Added `--repeat` to the harness. The previous single-run-per-condition results claimed 21.7% fewer output tokens and 37.0% less wall-clock time; neither survived three repetitions, and both claims have been withdrawn. Normal variance on these tasks exceeds the effect being measured at n=1.
