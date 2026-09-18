# Buzzcut eval harness

This pilot compares the same synthetic coding tasks with no project instructions (`baseline`) and with the repository's `AGENTS.md` (`buzzcut`). It uses only Python's standard library plus the installed Codex CLI.

Requirements: Python 3.9 or later, Git, and `codex` on your `PATH`.

Run all tasks from the repository root:

```sh
python3 eval/run_eval.py
```

Use `--task retry` to run one fixture (repeat the flag for several), or `--model` and `--reasoning` to pin another Codex configuration. `--timeout` caps each run, in seconds. `--repeat N` runs every task N times per condition and reports means, which is the main defence against model nondeterminism. `--rewrite-run <run id>` re-renders `RESULTS.md` from a stored `metrics.json` without calling Codex, which is how to pick up a reporting change without paying for the runs again.

A full pass is `tasks x 2 conditions x repeats` Codex invocations, so `--repeat 3` over eight tasks is 48 runs and takes roughly an hour.

Each condition runs in a disposable temporary Git repository, and condition order alternates by task so that ordering effects cancel. The comparable summary is written to [RESULTS.md](RESULTS.md). Per-run output goes to `runs/<run id>/`, where `metrics.json` is tracked as evidence and the raw JSONL, stderr and patches beside it stay local.

The harness measures textual lines added, new files, declared dependencies, wall-clock time, whether the fixture's acceptance tests pass, whether it reuses the intended repository capability, and tokens split into three classes.

## Why tokens are split

Reporting one combined token figure is misleading here, because the three classes move in opposite directions and are not priced alike:

- **Output** is what the agent writes. This is what Buzzcut is designed to reduce, and it is the figure comparable to other instruction sets that quote a token saving.
- **Fresh input** is uncached prompt content. Buzzcut *increases* it, because its rules are loaded on every request — currently about 1,600 tokens each time.
- **Cached input** is replayed prompt content, billed at roughly a tenth of the fresh rate. In practice it is over 90% of all input tokens, so any combined total is mostly a measure of conversation length rather than of the instructions.

`RESULTS.md` therefore reports all three, plus a price-weighted total that applies indicative gpt-5-class list rates so the classes can be compared on one line. Those rates are set in `PRICE_PER_MILLION` in `run_eval.py`; change them to match your own contract if you need a realistic figure.

These measurements describe this small sample only; they are not a statistically powered benchmark.

## Adding a task

Add a JSON file to `tasks/` with `title`, `prompt`, `test_command`, `quality_checks` and `files` (a path-to-contents map that seeds the temporary repository). Each quality check names a file and required or forbidden text so the harness can distinguish a passing duplicate implementation from reuse of the repository's intended capability.

A good task is one where the over-engineered solution is tempting and the acceptance tests can pass for both a minimal and a bloated implementation. Define the reuse expectation separately in `quality_checks`; otherwise you are measuring only correctness, not restraint.
