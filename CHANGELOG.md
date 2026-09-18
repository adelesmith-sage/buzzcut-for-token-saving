# Changelog

All notable changes to Buzzcut are recorded here. This project follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## 1.0.0

First release intended for use across teams.

### Added

- Nine ordered guardrails in `AGENTS.md` and `.github/copilot-instructions.md`, each stating its trigger, required action, exception and a paired good/bad example. The two files are byte-identical so that GitHub Copilot and Codex apply the same rules.
- A selectable **Buzzcut** agent (`.github/agents/buzzcut.agent.md`) for changes that especially need to stay small; it reports what it deliberately left out.
- Three read-only Agent Skills: `/buzzcut-review` for the current diff, `/buzzcut-audit` for a folder or repository, and `/buzzcut-debt` for recorded `buzzcut:` limits.
- A standard-library-only paired Codex eval harness with eight over-engineering-prone tasks, measuring added lines, new files, declared dependencies, tokens, wall time and acceptance-test results.
- `README.md` with installation for repository-wide and personal use, rollout guidance and the measured results; `LICENSE` (MIT); and a `verify` workflow that fails if the two rule files drift or if an agent, skill or task file is malformed.

### Results

First internal sample, recorded in [eval/RESULTS.md](eval/RESULTS.md): all 16 condition runs passed their acceptance tests, and Buzzcut used 21.2% fewer added lines, 4.5% fewer tokens and 37.0% less wall-clock time. Neither condition added files or dependencies. This is a small sample, not a statistically powered result.
