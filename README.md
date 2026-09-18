<p align="center">
  <img src="assets/logo.png" alt="Buzzcut" width="260">
</p>

<h1 align="center">Buzzcut</h1>

<p align="center"><strong>Keep code short back and sides. Nothing fancy on top.</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/Sage-internal-informational" alt="Sage internal">
  <img src="https://img.shields.io/badge/code%20written-28%25%20less-success" alt="28 percent less code written">
  <img src="https://img.shields.io/badge/token%20cost-9%25%20more-orange" alt="9 percent higher token cost">
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

In a paired evaluation over eight tasks, repeated three times each, Buzzcut produced **27.8% fewer added lines** across matched successful runs. It did **not** reduce tokens or wall-clock time in that run — it cost about **9% more** per task. [See the numbers, including what did not work &rarr;](#measured-results)

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

Eight synthetic tasks, each written so that an over-engineered solution is the tempting one. Every task ran **three times per condition** — once with no project instructions (`baseline`), once with Buzzcut — in isolated temporary Git repositories, with condition order alternated to cancel ordering effects. Aggregate figures use the 23 matched pairs where both conditions completed and passed their acceptance tests; the acceptance row reports all 24 runs per condition.

| Measure | Baseline | Buzzcut | Change |
| --- | ---: | ---: | ---: |
| **Added lines** | 37.8 | 27.3 | **&minus;27.8%** |
| Output tokens | 10,559 | 10,798 | +2.3% |
| Fresh input tokens | 96,837 | 111,498 | +15.1% |
| Price-weighted token cost | $0.3278 | $0.3571 | **+8.9%** |
| Wall-clock time | 366.3s | 374.8s | +2.3% |
| New files | 0 | 0 | no change |
| New dependencies | 0 | 0 | no change |
| Acceptance tests | 24/24 pass | 23/24 pass | one stall, see below |

**What Buzzcut does:** it writes about a quarter less code, on 6 of the 8 tasks. That effect is the most robust thing in the data — it survived three repetitions, a Codex version change and a rewrite of the rules file.

**What Buzzcut did not do in this run:** save tokens or time. Output and wall-clock time each rose 2.3%; fresh input rose 15.1% because the rules load on every request. On the indicative prices used by the harness, a task cost roughly **9% more** with Buzzcut than without.

### The one failure, and why it matters

One of the 24 Buzzcut runs made **no change at all** and asked a question instead. It was not a minimisation problem — it was the AI-label rule:

> **AI labels:** label AI-assisted code using the format in Sage's GitHub Copilot guidance. If it is unavailable, ask; do not invent one.

The agent could not find the label format in the repository, correctly declined to invent one, and stopped to ask:

> "I'm blocked from editing only by the repository's mandatory AI-label rule … no format or guidance is present in this repository."

In an interactive session that is reasonable behaviour. In an automated or non-interactive run it is a silent stall: the agent exits cleanly, having done nothing. It happened once in 24 runs (~4%), and it will happen in any repository that installs Buzzcut without the Sage label guidance present.

**If you are rolling this out, make sure your repositories carry the label guidance, or change that rule to record the gap and proceed rather than block.** It is a compliance rule, so the wording is deliberately left as-is here pending a decision from whoever owns that policy.

### Claims we have withdrawn

An earlier version of this README claimed 21.7% fewer output tokens and 37.0% less wall-clock time, from a single run of each condition. Neither survived repetition:

| Claim | Single run | Three runs | Verdict |
| --- | ---: | ---: | --- |
| Output tokens | &minus;21.7% | +2.3% | withdrawn |
| Wall-clock time | &minus;37.0% | +2.3% | withdrawn — it was service latency |
| Added lines | &minus;21.2% | &minus;27.8% | holds, and strengthened |

### Cost-first optimization screen

After the repeated run, the always-loaded rules were cut from 5.48 KB to 3.99 KB and repository discovery was made explicit: search the requested capability across filenames and symbols once before adding code. A one-task cache screen then recorded:

| Measure | Baseline | Buzzcut | Change |
| --- | ---: | ---: | ---: |
| Added lines | 2 | 2 | no change |
| Output tokens | 1,233 | 1,104 | **&minus;10.5%** |
| Price-weighted token cost | $0.0391 | $0.0356 | **&minus;8.8%** |
| Acceptance and reuse checks | pass | pass | no quality loss detected |

This is an **optimization screen: one task, one repetition**, not a replacement for the repeated result above. Its cost reduction is in the same range as [Caveman's instruction-only external result](https://github.com/JuliusBrussee/caveman#what-the-skill-saves-writing-less), but the harnesses differ. [Ponytail's agentic benchmark](https://github.com/DietrichGebert/ponytail/blob/main/benchmarks/results/2026-06-18-agentic.md) reports &minus;20% cost on feature tasks and &minus;7% on safety tasks using a different agent, model, repository and four repetitions; direct parity cannot be claimed. A full repeated Buzzcut rerun is required before promoting the screen to the headline.

Screen metrics: [eval/runs/20260918T104916Z/metrics.json](eval/runs/20260918T104916Z/metrics.json).

The lesson is worth more than the numbers: with one run per condition, normal variance on these tasks is larger than the effect being measured. Use `--repeat` before believing anything here.

> [!NOTE]
> Still a small internal sample, not a statistically powered study. Eight tasks, three repetitions, one model. Per-task output-token changes range from &minus;35% to +35%, so the flat aggregate hides wide swings. Reproduce it before quoting it.

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
