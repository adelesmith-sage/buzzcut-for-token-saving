# Changelog

All notable changes to Buzzcut are recorded here. This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.0.0

First release intended for use across teams.

### Added

- Nine ordered guardrails in `AGENTS.md` and `.github/copilot-instructions.md`, each stating its trigger, required action, exception and a paired good/bad example. The two files are byte-identical so that GitHub Copilot and Codex apply the same rules.
- A selectable **Buzzcut** agent (`.github/agents/buzzcut.agent.md`) for changes that especially need to stay small; it reports what it deliberately left out.
- Three read-only Agent Skills: `/buzzcut-review` for the current diff, `/buzzcut-audit` for a folder or repository, and `/buzzcut-debt` for recorded `buzzcut:` limits.
- A standard-library-only paired Codex eval harness with eight over-engineering-prone tasks, measuring added lines, new files, declared dependencies, tokens, wall time and acceptance-test results.
- `README.md` with installation for repository-wide and personal use, rollout guidance and the measured results, and a `verify` workflow that fails if the two rule files drift or if an agent, skill or task file is malformed. The repository is Sage-internal and carries no open-source licence.

### Results

Measured over eight tasks with three repetitions per condition (48 runs), recorded in [eval/RESULTS.md](eval/RESULTS.md): Buzzcut produced **27.9% fewer added lines**, on 6 of 8 tasks, and added no files or dependencies.

It did not reduce tokens or time. Output tokens were flat (+1.0%), fresh input rose 21.2% because the rules load on every request, and wall-clock time was unchanged (0.0%). Price-weighted token cost rose 9.2%.

One of 24 Buzzcut runs stalled without making a change, blocked by the AI-label rule when the Sage label format was absent from the repository.

### Fixed

- Token reporting previously combined cached input, fresh input and output into one figure. Cached input is over 90% of that total and is billed at roughly a tenth of the fresh rate, so the combined number tracked conversation length rather than the instructions. The three classes are now reported separately, alongside a price-weighted total.
- Added `--repeat` to the harness. The previous single-run-per-condition results claimed 21.7% fewer output tokens and 37.0% less wall-clock time; neither survived three repetitions, and both claims have been withdrawn. Normal variance on these tasks exceeds the effect being measured at n=1.
