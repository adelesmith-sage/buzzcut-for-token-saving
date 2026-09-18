#!/usr/bin/env python3
"""Run paired Codex evaluations with and without Buzzcut instructions."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
import time
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
TASKS_DIR = ROOT / "eval" / "tasks"
RESULTS_PATH = ROOT / "eval" / "RESULTS.md"
DEFAULT_MODEL = "gpt-5.6-sol"
DEFAULT_REASONING = "high"

# Indicative gpt-5-class list rates in USD per million tokens, used only to weight
# the three token classes against each other. Not a billing statement.
PRICE_PER_MILLION = {"fresh_input": 1.25, "cached_input": 0.125, "output": 10.0}


def token_split(usage: dict[str, int]) -> dict[str, int]:
    """Separate the token classes, which differ in both price and meaning."""
    cached = usage.get("cached_input_tokens", 0)
    return {
        "fresh_input": usage.get("input_tokens", 0) - cached,
        "cached_input": cached,
        "output": usage.get("output_tokens", 0),
    }


def weighted_cost(usage: dict[str, int]) -> float:
    split = token_split(usage)
    return sum(split[key] * PRICE_PER_MILLION[key] for key in split) / 1_000_000


def codex_version() -> str:
    if not shutil.which("codex"):
        # Fall back to the version already published, so a rewrite keeps its provenance.
        if RESULTS_PATH.exists():
            recorded = re.search(r"^Codex CLI: `(.+?)`", RESULTS_PATH.read_text(encoding="utf-8"), re.MULTILINE)
            if recorded:
                return recorded.group(1)
        return "unknown"
    return run(["codex", "--version"], ROOT).stdout.strip() or "unknown"


def run(command: list[str], cwd: Path, *, timeout: int = 60) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=cwd,
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )


def materialise(task: dict[str, Any], destination: Path, with_buzzcut: bool) -> str:
    for relative, content in task["files"].items():
        target = destination / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(content, encoding="utf-8")

    (destination / ".gitignore").write_text("__pycache__/\n*.py[cod]\n", encoding="utf-8")
    (destination / "SAGE_AI_GUIDANCE.md").write_text(
        "# Synthetic evaluation fixture\n\n"
        "These disposable fixtures are exempt from in-source AI labels.\n",
        encoding="utf-8",
    )
    if with_buzzcut:
        shutil.copy2(ROOT / "AGENTS.md", destination / "AGENTS.md")

    commands = [
        ["git", "init", "-q", "-b", "main"],
        ["git", "config", "user.name", "Buzzcut Eval"],
        ["git", "config", "user.email", "buzzcut-eval@example.invalid"],
        ["git", "add", "-A"],
        ["git", "commit", "-q", "-m", "Initial fixture"],
    ]
    for command in commands:
        completed = run(command, destination)
        if completed.returncode:
            raise RuntimeError(completed.stderr.strip() or "Failed to initialise fixture")
    return run(["git", "rev-parse", "HEAD"], destination).stdout.strip()


def dependency_snapshot(root: Path) -> set[str]:
    dependencies: set[str] = set()

    package_json = root / "package.json"
    if package_json.exists():
        package = json.loads(package_json.read_text(encoding="utf-8"))
        for group in ("dependencies", "devDependencies", "peerDependencies", "optionalDependencies"):
            dependencies.update(f"npm:{name}" for name in package.get(group, {}))

    pyproject = root / "pyproject.toml"
    if pyproject.exists():
        section = ""
        in_dependency_array = False
        for raw_line in pyproject.read_text(encoding="utf-8").splitlines():
            line = raw_line.split("#", 1)[0].strip()
            if line.startswith("[") and line.endswith("]"):
                section = line.strip("[]")
                in_dependency_array = False
            if line.startswith(("dependencies = [", "optional-dependencies = [")):
                in_dependency_array = True
            if in_dependency_array and line not in ("dependencies = [", "optional-dependencies = [", "]"):
                dependencies.add(f"pyproject:{line.rstrip(',')}")
            if in_dependency_array and line.endswith("]"):
                in_dependency_array = False
            if "dependencies" in section and "=" in line:
                name = line.split("=", 1)[0].strip().strip('"')
                if name and name != "python":
                    dependencies.add(f"pyproject:{section}:{name}")

    for requirements in root.glob("requirements*.txt"):
        for line in requirements.read_text(encoding="utf-8").splitlines():
            value = line.strip()
            if value and not value.startswith(("#", "-")):
                dependencies.add(f"python:{value}")

    cargo = root / "Cargo.toml"
    if cargo.exists():
        section = ""
        for raw_line in cargo.read_text(encoding="utf-8").splitlines():
            line = raw_line.split("#", 1)[0].strip()
            if line.startswith("[") and line.endswith("]"):
                section = line.strip("[]")
            elif section in ("dependencies", "dev-dependencies", "build-dependencies") and "=" in line:
                dependencies.add(f"cargo:{line.split('=', 1)[0].strip()}")

    go_mod = root / "go.mod"
    if go_mod.exists():
        in_block = False
        for raw_line in go_mod.read_text(encoding="utf-8").splitlines():
            line = raw_line.strip()
            if line == "require (":
                in_block = True
            elif in_block and line == ")":
                in_block = False
            elif line.startswith("require "):
                dependencies.add(f"go:{line.split()[1]}")
            elif in_block and line and not line.startswith("//"):
                dependencies.add(f"go:{line.split()[0]}")

    return dependencies


def parse_usage(jsonl: str) -> dict[str, int]:
    usage: dict[str, int] = {}
    for line in jsonl.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if event.get("type") == "turn.completed":
            usage = event.get("usage", {})
    return {key: int(value) for key, value in usage.items() if isinstance(value, (int, float))}


def diff_metrics(root: Path, base: str) -> tuple[int, list[str], str]:
    run(["git", "add", "-A"], root)
    patch = run(["git", "diff", "--binary", base], root).stdout
    numstat = run(["git", "diff", "--numstat", base], root).stdout
    added_lines = 0
    for line in numstat.splitlines():
        added, _, _ = line.split("\t", 2)
        if added.isdigit():
            added_lines += int(added)
    new_files = [
        line
        for line in run(["git", "diff", "--diff-filter=A", "--name-only", base], root).stdout.splitlines()
        if line
    ]
    return added_lines, new_files, patch


def run_condition(
    task_path: Path,
    condition: str,
    artifact_dir: Path,
    model: str,
    reasoning: str,
    timeout: int,
) -> dict[str, Any]:
    task = json.loads(task_path.read_text(encoding="utf-8"))
    with tempfile.TemporaryDirectory(prefix=f"buzzcut-{task_path.stem}-{condition}-") as temp:
        worktree = Path(temp)
        base = materialise(task, worktree, condition == "buzzcut")
        dependencies_before = dependency_snapshot(worktree)
        command = [
            "codex",
            "exec",
            "--ephemeral",
            "--json",
            "--ignore-user-config",
            "--ignore-rules",
            "--approve-for-me",
            "--model",
            model,
            "--config",
            f'model_reasoning_effort="{reasoning}"',
            "--cd",
            str(worktree),
            task["prompt"],
        ]
        started = time.monotonic()
        try:
            completed = run(command, worktree, timeout=timeout)
            timed_out = False
        except subprocess.TimeoutExpired as error:
            completed = subprocess.CompletedProcess(
                command,
                124,
                stdout=error.stdout or "",
                stderr=error.stderr or "Timed out",
            )
            timed_out = True
        elapsed = time.monotonic() - started
        added_lines, new_files, patch = diff_metrics(worktree, base)
        new_dependencies = sorted(dependency_snapshot(worktree) - dependencies_before)
        test_result = run(task["test_command"], worktree, timeout=60)
        usage = parse_usage(completed.stdout)

        artifact_dir.mkdir(parents=True, exist_ok=True)
        (artifact_dir / "events.jsonl").write_text(completed.stdout, encoding="utf-8")
        (artifact_dir / "stderr.txt").write_text(completed.stderr, encoding="utf-8")
        (artifact_dir / "changes.patch").write_text(patch, encoding="utf-8")

        return {
            "task": task_path.stem,
            "title": task["title"],
            "condition": condition,
            "model": model,
            "reasoning": reasoning,
            "exit_code": completed.returncode,
            "timed_out": timed_out,
            "tests_passed": test_result.returncode == 0,
            "added_lines": added_lines,
            "new_files": new_files,
            "new_dependencies": new_dependencies,
            "wall_seconds": round(elapsed, 2),
            "usage": usage,
        }


def change_label(baseline: float, buzzcut: float) -> str:
    if baseline == 0:
        return "no change" if buzzcut == 0 else "increase from zero"
    change = ((buzzcut - baseline) / baseline) * 100
    if change < 0:
        return f"{-change:.1f}% reduction"
    if change > 0:
        return f"{change:.1f}% increase"
    return "no change"


def write_results(results: list[dict[str, Any]], run_id: str, cli_version: str) -> None:
    repeats = max((row.get("repeat", 1) for row in results), default=1)
    task_order = {task: index for index, task in enumerate(dict.fromkeys(row["task"] for row in results))}
    pairs = sorted(
        {(row["task"], row["condition"]) for row in results},
        key=lambda pair: (task_order[pair[0]], pair[1] != "baseline"),
    )

    def rows_for(task: str, condition: str) -> list[dict[str, Any]]:
        return [row for row in results if row["task"] == task and row["condition"] == condition]

    def mean(rows: list[dict[str, Any]], value: Any) -> float:
        return sum(value(row) for row in rows) / len(rows)

    sample = (
        f"Each task was run once per condition; model nondeterminism and service latency can affect results."
        if repeats == 1
        else f"Each task was run {repeats} times per condition and the figures below are means; model nondeterminism and service latency still affect results."
    )
    lines = [
        "# Buzzcut evaluation results",
        "",
        f"> This is a small internal sample, not a statistically powered study. {sample}",
        "",
        f"Run: `{run_id}`  ",
        f"Codex CLI: `{cli_version}`  ",
        f"Model: `{results[0]['model']}` with `{results[0]['reasoning']}` reasoning  ",
        f"Repetitions: {repeats} per condition  ",
        "Method: isolated temporary Git repositories; condition order alternated by task; added lines and files measured from the Git diff; token counts read from Codex `turn.completed` usage; wall time measured around `codex exec`.",
        "",
        "Token classes are reported separately because they behave differently. `Output` is what the agent writes, and is the figure Buzzcut is designed to move. `Fresh input` is uncached prompt content, which Buzzcut *increases* because its rules are loaded on every request. `Cached input` is replayed prompt content, billed at roughly a tenth of the fresh rate.",
        "",
        "| Task | Condition | Added lines | New files | New deps | Output | Fresh input | Wall time | Tests |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for task, condition in pairs:
        rows = rows_for(task, condition)
        passed = sum(1 for row in rows if row["tests_passed"] and not row["exit_code"])
        lines.append(
            f"| {rows[0]['title']} | {condition} | {mean(rows, lambda r: r['added_lines']):.1f} | "
            f"{mean(rows, lambda r: len(r['new_files'])):.1f} | {mean(rows, lambda r: len(r['new_dependencies'])):.1f} | "
            f"{mean(rows, lambda r: token_split(r['usage'])['output']):.0f} | "
            f"{mean(rows, lambda r: token_split(r['usage'])['fresh_input']):.0f} | "
            f"{mean(rows, lambda r: r['wall_seconds']):.2f}s | {passed}/{len(rows)} |"
        )

    totals: dict[str, dict[str, float]] = {}
    for condition in ("baseline", "buzzcut"):
        per_task = [rows_for(task, condition) for task, cond in pairs if cond == condition]
        totals[condition] = {
            "added_lines": sum(mean(rows, lambda r: r["added_lines"]) for rows in per_task),
            "new_files": sum(mean(rows, lambda r: len(r["new_files"])) for rows in per_task),
            "new_dependencies": sum(mean(rows, lambda r: len(r["new_dependencies"])) for rows in per_task),
            "output": sum(mean(rows, lambda r: token_split(r["usage"])["output"]) for rows in per_task),
            "fresh_input": sum(mean(rows, lambda r: token_split(r["usage"])["fresh_input"]) for rows in per_task),
            "cached_input": sum(mean(rows, lambda r: token_split(r["usage"])["cached_input"]) for rows in per_task),
            "cost": sum(mean(rows, lambda r: weighted_cost(r["usage"])) for rows in per_task),
            "wall_seconds": sum(mean(rows, lambda r: r["wall_seconds"]) for rows in per_task),
        }

    lines.extend(["", "Aggregate change from baseline to Buzzcut:"])
    for label, key in (
        ("added lines", "added_lines"),
        ("new files", "new_files"),
        ("new dependencies", "new_dependencies"),
        ("output tokens", "output"),
        ("fresh input tokens", "fresh_input"),
        ("cached input tokens", "cached_input"),
        ("price-weighted token cost", "cost"),
        ("wall-clock time", "wall_seconds"),
    ):
        base = totals["baseline"][key]
        buzz = totals["buzzcut"][key]
        formatted = f"{base:.4f} → {buzz:.4f} USD" if key == "cost" else f"{base:g} → {buzz:g}"
        lines.append(f"- {label}: {formatted} ({change_label(base, buzz)})")

    failures = [
        f"{row['task']}/{row['condition']}#{row.get('repeat', 1)}"
        for row in results
        if not row["tests_passed"] or row["exit_code"]
    ]
    lines.append(f"- unsuccessful runs: {', '.join(failures) if failures else 'none'}")
    lines.extend([
        "",
        "`Added lines` counts textual additions in the final Git diff, including tests. Price-weighted cost uses indicative gpt-5-class list rates (fresh input $1.25, cached input $0.125, output $10.00 per million tokens) to weight the token classes against each other; it is not a billing statement. `metrics.json` for this run is tracked under `eval/runs/<run id>/`; the raw JSONL, stderr and patches beside it stay local and are ignored.",
        "",
    ])
    RESULTS_PATH.write_text("\n".join(lines), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", action="append", help="Task stem to run; repeat to select multiple")
    parser.add_argument("--model", default=os.environ.get("CODEX_MODEL", DEFAULT_MODEL))
    parser.add_argument("--reasoning", default=os.environ.get("CODEX_REASONING", DEFAULT_REASONING))
    parser.add_argument("--timeout", type=int, default=600, help="Seconds allowed per Codex run")
    parser.add_argument("--repeat", type=int, default=1, help="Repetitions per condition; results are reported as means")
    parser.add_argument("--rewrite-run", help="Regenerate RESULTS.md from a stored run's metrics.json instead of calling Codex")
    args = parser.parse_args()

    if args.rewrite_run:
        metrics_path = ROOT / "eval" / "runs" / args.rewrite_run / "metrics.json"
        if not metrics_path.exists():
            parser.error(f"no metrics.json for run {args.rewrite_run}")
        stored = json.loads(metrics_path.read_text(encoding="utf-8"))
        write_results(stored, args.rewrite_run, codex_version())
        print(f"Rewrote {RESULTS_PATH.relative_to(ROOT)} from {args.rewrite_run}", flush=True)
        return 0

    if not shutil.which("codex"):
        parser.error("codex CLI is not on PATH")

    task_paths = sorted(TASKS_DIR.glob("*.json"))
    if args.task:
        selected = set(args.task)
        task_paths = [path for path in task_paths if path.stem in selected]
        missing = selected - {path.stem for path in task_paths}
        if missing:
            parser.error(f"unknown task(s): {', '.join(sorted(missing))}")
    if not task_paths:
        parser.error("no tasks selected")
    if args.repeat < 1:
        parser.error("--repeat must be at least 1")

    run_id = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    run_dir = ROOT / "eval" / "runs" / run_id
    results: list[dict[str, Any]] = []
    total = len(task_paths) * 2 * args.repeat
    for repeat in range(1, args.repeat + 1):
        for index, task_path in enumerate(task_paths):
            # Alternate which condition goes first so ordering effects cancel.
            conditions = ("baseline", "buzzcut") if (index + repeat) % 2 == 0 else ("buzzcut", "baseline")
            for condition in conditions:
                print(f"[{len(results) + 1}/{total}] {task_path.stem}: {condition} (repeat {repeat})", flush=True)
                result = run_condition(
                    task_path,
                    condition,
                    run_dir / task_path.stem / condition / f"r{repeat}",
                    args.model,
                    args.reasoning,
                    args.timeout,
                )
                result["repeat"] = repeat
                results.append(result)
                (run_dir / "metrics.json").write_text(json.dumps(results, indent=2) + "\n", encoding="utf-8")

    write_results(results, run_id, codex_version())
    print(f"Wrote {RESULTS_PATH.relative_to(ROOT)}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
