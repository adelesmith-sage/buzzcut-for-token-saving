# Buzzcut eval harness

This pilot compares the same synthetic coding tasks with no project instructions (`baseline`) and with the repository's `AGENTS.md` (`buzzcut`). It uses only Python's standard library plus the installed Codex CLI.

Requirements: Python 3.9 or later, Git, and `codex` on your `PATH`.

Run all tasks from the repository root:

```sh
python3 eval/run_eval.py
```

Use `--task retry` to run one fixture (repeat the flag for several), or `--model` and `--reasoning` to pin another Codex configuration. `--timeout` caps each run, in seconds.

Each condition runs in a disposable temporary Git repository, and condition order alternates by task so that ordering effects cancel. The comparable summary is written to [RESULTS.md](RESULTS.md). Per-run output goes to `runs/<run id>/`, where `metrics.json` is tracked as evidence and the raw JSONL, stderr and patches beside it stay local.

The harness measures textual lines added, new files, declared dependencies, Codex input/output tokens, wall-clock time and whether the fixture's acceptance tests pass. These measurements describe this small sample only; they are not a statistically powered benchmark.

## Adding a task

Add a JSON file to `tasks/` with `title`, `prompt`, `test_command` and `files` (a path-to-contents map that seeds the temporary repository). A good task is one where the over-engineered solution is the tempting one, and where the acceptance tests pass for both a minimal and a bloated implementation — otherwise you are measuring correctness, not restraint.
