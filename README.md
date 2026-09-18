<p align="center">
  <img src="assets/logo.png" alt="Buzzcut" width="260">
</p>

<h1 align="center">Buzzcut</h1>

<p align="center"><strong>Keep code short back and sides. Nothing fancy on top.</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/Sage-internal-informational" alt="Sage internal">
  <img src="https://img.shields.io/badge/code%20written-28%25%20less-success" alt="28 percent less code written">
  <img src="https://img.shields.io/badge/token%20cost-27%25%20less%20(screen)-success" alt="Token cost 27 percent lower in the latest wrapper screen">
  <img src="https://img.shields.io/badge/works%20with-Copilot%20%2B%20Codex-blue" alt="Works with GitHub Copilot and Codex">
</p>

<p align="center">
  <a href="#install">Install</a> &middot;
  <a href="#how-to-use-it">How to use it</a> &middot;
  <a href="#the-nine-rules">The nine rules</a> &middot;
  <a href="#measured-results">Measured results</a> &middot;
  <a href="#faq">FAQ</a>
</p>

---

Coding agents are rewarded for producing code, so they produce too much of it: a new helper beside the one that already worked, a retry wrapper nobody asked for, a dependency for something the standard library does.

Buzzcut is a drop-in instruction set that makes them stop. It is **nine rules, one agent and three review commands** — a handful of Markdown files. No extension to install, no service to run, no dependency to add.

In a paired evaluation over eight tasks, repeated three times each, Buzzcut produced **27.8% cleaner code diffs** with no loss of correctness, for about a third of a penny more per task. The latest enforced-wrapper screen cut price-weighted cost **26.9%**, output tokens **31.0%**, and wall time **23.9%** across the same eight fixtures; it is one repetition and has one reuse-quality miss, so it is not the headline yet. [See the numbers &rarr;](#measured-results)

### What it costs on a large codebase

The overhead is a **flat 2,491 fresh input tokens per task** — the rules file, loaded once per request. It does not grow with the repository, so its share shrinks as the codebase grows: 21.2% on the ten-file eval fixtures, 5.0% at 50,000 tokens of context, 1.2% at 200,000. The shell wrappers add **zero model-prompt tokens** because they are injected through `PATH`; they cap ordinary `rg` output at 20 lines, `rg --files` at 50 lines, and direct `cat` reads at 100 lines.

If the budget rules also prevent one full repository listing per task, and that listing runs to roughly one line per file at ~10 tokens a line, the modelled change in cost is:

| Repository scale | Baseline context per task | Modelled change | Range |
| :--- | ---: | ---: | ---: |
| Small (~10 files) | ~11,800 tokens | +7.4% *(a cost)* | — |
| Medium (~1,000 files) | ~50,000 tokens | **&minus;10.6%** | &minus;7.8% to &minus;13.5% |
| Enterprise (~10,000 files) | ~200,000 tokens | **&minus;44.2%** | &minus;35.1% to &minus;53.3% |

**A model, not a benchmark** — but reproducible arithmetic, so check it rather than trust it:

```
change = (2,491 - listing_tokens) x $1.25/M / baseline_cost_per_task
baseline_cost_per_task = context_tokens x $1.25/M + $0.0258
```

Both constants are measured in run `20260918T095109Z`. It rests on one assumption — that the agent would otherwise dump the tree once per task. If yours already search narrowly, the saving is not there to collect.

## Works with

| Tool | What you get | How |
| --- | --- | --- |
| **GitHub Copilot** (VS Code, Visual Studio, JetBrains, github.com) | The nine rules on every request, the **Buzzcut** agent in the picker, and the three `/buzzcut-*` commands | `.github/` folder |
| **Codex** (CLI and IDE extension) | The nine rules on every request | `AGENTS.md` |
| Other agents that read `AGENTS.md` | The nine rules on every request | `AGENTS.md` |

Copilot and Codex are both covered by design — the rules are written once and stored in the two places these tools look. The [evaluation](#measured-results) was run against Codex, so the Codex path is the one with measured evidence behind it.

## Install

Pick the line that describes you.

### "Someone already set it up in this repository"

Nothing to install. Skip to [How to use it](#how-to-use-it).

### "I want it in my team's repository" — one-time, ~2 minutes

Copy the Buzzcut files in and commit them. Everyone who works in that repository gets it automatically, with no setup of their own.

```sh
BUZZCUT=$(mktemp -d)
git clone --depth 1 https://github.com/<your-org>/buzzcut.git "$BUZZCUT"

cd /path/to/your-repo
mkdir -p .github/skills
cp -R "$BUZZCUT/.github/agents"                   .github/
cp -R "$BUZZCUT/.github/skills/."                .github/skills/
cp    "$BUZZCUT/.github/copilot-instructions.md" .github/
cp    "$BUZZCUT/AGENTS.md"                       .
```

Not comfortable with a terminal? Download this repository as a ZIP, unzip it, then drag the `.github` folder and the `AGENTS.md` file into your project. That is the same thing.

| What you copied | Gives you |
| --- | --- |
| `AGENTS.md` | The nine rules, for Codex and other agents |
| `.github/copilot-instructions.md` | The same nine rules, for GitHub Copilot |
| `.github/agents/buzzcut.agent.md` | The **Buzzcut** entry in Copilot's agent picker |
| `.github/skills/buzzcut-*/` | The `/buzzcut-review`, `/buzzcut-audit` and `/buzzcut-debt` commands |

> **Already have a `.github/copilot-instructions.md`?** Do not overwrite it. Paste Buzzcut's contents at the end of yours — the rules are written to sit alongside existing repository guidance, not replace it.

### "I just want it for myself, in every project" — one file

Copy the agent file into your VS Code profile. The **Buzzcut** agent then appears in every workspace you open, without changing anyone else's repository.

```sh
mkdir -p ~/Library/Application\ Support/Code/User/prompts          # macOS
cp .github/agents/buzzcut.agent.md ~/Library/Application\ Support/Code/User/prompts/
```

On Windows the folder is `%APPDATA%\Code\User\prompts`; on Linux it is `~/.config/Code/User/prompts`. In VS Code you can also run **Chat: New Agent File** from the Command Palette and paste the contents in.

## How to use it

Once installed there are three ways in, and you do not need all of them.

**1. Do nothing.** The nine rules apply to every Copilot and Codex request in the repository automatically. Ask for a change as you normally would; you should get less code back.

**2. Pick the Buzzcut agent** when a change especially needs to stay small. In Copilot Chat, open the agent dropdown and choose **Buzzcut**, then describe the change. It will implement it, tell you what it deliberately left out, and run the relevant checks.

**3. Run a review command** by typing `/` in Copilot Chat:

| Command | Use it when |
| --- | --- |
| `/buzzcut-review` | You have a change ready and want it checked for over-engineering before raising a PR. |
| `/buzzcut-audit` | You want the biggest simplifications in a folder or a whole service. |
| `/buzzcut-debt` | You want to know which recorded shortcuts are now ready to be replaced. |

All three only read and report. They never edit your code.

### Check it worked

Open Copilot Chat in the repository and type `/buzzcut-review`. You should get either a short list of findings, or `Buzzcut review: no cuts needed.` If the command is missing, reload the window so the editor picks up the new `.github` files.

## What you get

**Nine ordered rules**, applied top to bottom until the request is satisfied. Each one states when it triggers, what to do, when *not* to apply it, and a paired good/bad example — so the agent can tell a real cut from a damaging one.

**One agent**, `Buzzcut`, for when you want the smallest possible implementation of a specific change and a note of what it chose to leave out.

**Three slash commands**, available on demand and never triggered automatically:

| Command | Does |
| --- | --- |
| `/buzzcut-review` | Reviews the current diff for over-engineering and proposes the smallest correct alternative for each finding. |
| `/buzzcut-audit` | Audits a folder or the whole repository for the five highest-value simplifications. |
| `/buzzcut-debt` | Finds recorded `buzzcut:` limits in source and reports whether each is now ready to be replaced. |

**A marker for deliberate limits.** When the agent knowingly leaves a case unhandled, it records why and what would change its mind:

```python
# buzzcut: single region; replace when a second region is configured
```

`/buzzcut-debt` later tells you which of those conditions have come true.

## The nine rules

| # | Rule | In short |
| --: | --- | --- |
| 1 | Fix the shared cause | Change the lowest shared point that owns the behaviour, not each caller. |
| 2 | Reuse before adding | If the repo, language, platform or an installed dependency already does it, call that. |
| 3 | Add no dependency by default | A new package must be named and justified against existing capabilities. |
| 4 | Minimise the change surface | Fewest files, least code; prefer deletion when equivalent. |
| 5 | Require evidence for extra machinery | No unrequested retries, caching, flags, logging or error paths. |
| 6 | Preserve required protections | Never cut validation, security, privacy, accessibility or compliance to be smaller. |
| 7 | Follow the local contract | Match the repository's existing naming, control flow and error handling. |
| 8 | Verify proportionately | Smallest failing check in the existing test mechanism, then run the narrowest checks. |
| 9 | Mark deliberate limits only | Record real omissions as `buzzcut:` with a concrete replacement condition. |

Rule 6 outranks the rest by construction: correctness, security, privacy and explicit requirements always beat brevity. The full text, with triggers, exceptions and examples, is in [.github/copilot-instructions.md](.github/copilot-instructions.md).

## Measured results

Eight synthetic tasks, each written so that an over-engineered solution is the tempting one. Every task ran **three times per condition** — once with no project instructions (`baseline`), once with Buzzcut — in isolated temporary Git repositories, with condition order alternated to cancel ordering effects. Aggregate figures use the 23 matched pairs where both conditions completed and passed their acceptance tests; the acceptance row reports all 24 runs per condition. Per-repetition figures are in [eval/RESULTS.md](eval/RESULTS.md).

| Measure | Baseline | Buzzcut | Change (mean of 3) | Best run of 3 |
| --- | ---: | ---: | ---: | ---: |
| **Added lines** | 37.8 | 27.3 | **&minus;27.8%** | &minus;39.5% |
| Output tokens | 10,559 | 10,798 | +2.3% | &minus;9.4% |
| Fresh input tokens | 96,837 | 111,498 | +15.1% | +3.4% |
| Price-weighted token cost | $0.3278 | $0.3571 | **+8.9%** | &minus;0.1% |
| Wall-clock time | 366.3s | 374.8s | +2.3% | &minus;8.9% |
| New files | 0 | 0 | no change | no change |
| New dependencies | 0 | 0 | no change | no change |
| Acceptance tests | 24/24 pass | 23/24 pass | one stall, see below | — |

**Read the mean column.** Every figure under `Best run of 3` comes from the same repetition — run 2 was the most favourable on all five measures at once, which is what a warm cache looks like, not five separate Buzzcut effects. It is shown so the spread is visible.

**The robust result is the added lines.** A quarter less code, on 6 of the 8 tasks, and the only measure whose worst repetition (&minus;16.1%) still points the same way as its best. It survived three repetitions, a Codex version change and a rewrite of the rules file.

**Tokens and time were flat.** Fresh input rises because the rules load on every request. At list prices a task cost about 9% more — a third of a penny — on ten-file fixtures where the fixed overhead is at its maximum share and there is nothing to explore.

### Later runs

Two smaller runs followed, after the rules gained lookup budgets:

| Run | Shape | Added lines | Cost | Output tokens |
| --- | --- | ---: | ---: | ---: |
| `20260918T132225Z` | 8 tasks, n=1, wrappers on | **&minus;26.5%** | **&minus;26.9%** | **&minus;31.0%** |
| `20260918T124411Z` | 8 tasks, n=1 | &minus;18.2% | +2.5% | &minus;24.2% |
| `20260918T104916Z` | 1 task, n=1 | no change | &minus;8.8% | &minus;10.5% |

All three are **screens, not results** — one repetition each. The repeated run above is the headline until the wrapper configuration is reproduced at `--repeat 3`. The enforced-wrapper screen passed all 16 acceptance tests, but its Buzzcut feature-flag implementation missed one stricter reuse-quality check; the results file records that miss. The single-task screen used `cache`, which the repeated data shows is the most Buzzcut-favourable of the eight on cost (&minus;23.0%, against +54.7% for the worst), and the earlier eight-task screen changed three variables at once, so nothing in it can be attributed to the rules alone.

For context, [Ponytail's agentic benchmark](https://github.com/DietrichGebert/ponytail/blob/main/benchmarks/results/2026-06-18-agentic.md) reports &minus;20% cost on feature tasks over four repetitions with a different agent, model and repository — encouraging, but not comparable.

### Known defect: the AI-label stall

One of the 24 Buzzcut runs made no change and asked a question instead. The agent could not find the Sage label format in the repository, correctly declined to invent one, and stopped. Interactively that is right; unattended it is a silent stall. It happened once in 24 runs and **will happen in any repository that installs Buzzcut without the Sage label guidance present** — so ship that guidance alongside it, or have the policy owner relax the rule to record the gap and proceed.

### Claims we have withdrawn

An earlier README claimed &minus;21.7% output tokens and &minus;37.0% wall-clock time from a single run of each. At three repetitions both went to +2.3% — the wall-time figure was service latency. Added lines went the other way, from &minus;21.2% to &minus;27.8%. One run per condition on these tasks swings further than the effect being measured, so use `--repeat` before believing anything here, including this page.

> [!NOTE]
> A small internal sample, not a statistically powered study. Eight tasks, three repetitions, one model. Per-task cost changes range from &minus;23% to +55%, so the aggregate hides wide swings.

Per-task figures and method: [eval/RESULTS.md](eval/RESULTS.md). Raw metrics: [eval/runs/20260918T095109Z/metrics.json](eval/runs/20260918T095109Z/metrics.json).

### Reproduce it

Requires Python 3 (standard library only) and the Codex CLI on your `PATH`.

```sh
python3 eval/run_eval.py --repeat 3   # all eight tasks, both conditions, three times
python3 eval/run_eval.py --task retry  # one task, once
```

A `--repeat 3` pass is 48 Codex invocations and takes around 40 minutes.

To re-render [eval/RESULTS.md](eval/RESULTS.md) from a run you already have, without spending anything:

```sh
python3 eval/run_eval.py --rewrite-run 20260918T095109Z
```

See [eval/README.md](eval/README.md) for options and what each measurement means.

## Rolling it out across a team

1. **Pilot on one active repository.** Install, then leave it for a sprint. The rules only bite when someone asks an agent for a change, so there is nothing for the team to learn on day one.
2. **Measure on your own code.** The numbers above come from synthetic tasks. Run `/buzzcut-audit` on a real service and judge the findings — that is the evidence your team will actually trust.
3. **Keep the two rule files identical.** `AGENTS.md` and `.github/copilot-instructions.md` are byte-identical on purpose, so Copilot and Codex get the same rules. The [verify workflow](.github/workflows/verify.yml) fails the build if they drift.
4. **Add stack-specific rules separately.** Put them in `.github/instructions/<name>.instructions.md` with an `applyTo` glob, so the always-loaded files stay short. See [CONTRIBUTING.md](CONTRIBUTING.md).
5. **Do not fork the rules per team.** Propose a change upstream instead; nine shared rules are worth more than nine variants.

## FAQ

**Will it make the agent skip tests, validation or security checks?**
No. Rule 6 forbids it explicitly, and the agent and all three commands are instructed never to remove or recommend removing validation, data-loss protection, security, privacy, accessibility, compliance or explicitly requested behaviour. Rule 8 requires a proportionate test for non-trivial logic.

**Does it conflict with our existing Copilot instructions?**
It is written to add to them, not replace them. Append it to your existing file. If a Buzzcut rule genuinely contradicts your repository's guidance, your guidance wins — say so in your own file.

**Does it work with Codex as well as Copilot?**
Yes. The nine rules live in two files with identical contents: `AGENTS.md`, which Codex reads automatically in any repository it is run in, and `.github/copilot-instructions.md`, which Copilot reads. Codex is in fact the tool the [evaluation](#measured-results) was run against. The agent picker entry and the `/buzzcut-*` commands are VS Code Copilot features and are not available in the Codex CLI.

**Do I have to use the agent or the commands?**
No. Installing the files is enough — the rules apply to every request. The agent and the commands are there for when you want to lean on them harder.

**Why are there two copies of the rules?**
Different tools look in different places. `.github/copilot-instructions.md` is Copilot's documented path; `AGENTS.md` is the cross-agent convention Codex follows. Keeping both byte-identical is cheaper than teaching every tool a new path, and CI enforces it.

**Do I need the `eval/` folder in my repository?**
No. It exists so the claims above can be checked and re-run. Copy only `.github/` and `AGENTS.md`.

**Why is the agent still writing too much?**
Check that the instruction file is actually being loaded — in VS Code, Copilot Chat lists the instruction files it used under the response. Then pick the **Buzzcut** agent, or run `/buzzcut-review` on the diff: the rules bias generation, while the agent and commands catch what slips through.

## Contributing

A rule earns its place by changing model behaviour toward a smaller correct change, with evidence. See [CONTRIBUTING.md](CONTRIBUTING.md) for what a proposal needs, and [CHANGELOG.md](CHANGELOG.md) for what has changed.

## Licence and credit

Internal Sage repository. No open-source licence is granted, and no `LICENSE` file is included; distribution and reuse follow Sage internal policy. Confirm with your Open Source Procedure contact before sharing this outside the company.

The name and the review-command shape are inspired by Ponytail. No Ponytail code is included here; the rules, agent, skills and evaluation harness are original.
