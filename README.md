<p align="center">
  <img src="assets/logo.png" alt="Buzzcut" width="260">
</p>

<h1 align="center">Buzzcut</h1>

<p align="center"><strong>Keep code short back and sides. Nothing fancy on top.</strong></p>

<p align="center">
  <img src="https://img.shields.io/badge/licence-MIT-informational" alt="MIT licence">
  <img src="https://img.shields.io/badge/tests-16%2F16%20passing-success" alt="16 of 16 evaluation runs passing">
  <img src="https://img.shields.io/badge/dependencies-none-success" alt="No dependencies">
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

In a paired evaluation over eight tasks, Buzzcut produced **21.2% fewer added lines**, **4.5% fewer tokens** and **37.0% less wall-clock time**, with **all 16 runs passing their acceptance tests**. [See the numbers &rarr;](#measured-results)

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

Eight synthetic tasks, each written so that an over-engineered solution is the tempting one. Every task ran twice — once with no project instructions (`baseline`), once with Buzzcut — in isolated temporary Git repositories, with condition order alternated to cancel ordering effects.

| Measure | Baseline | Buzzcut | Change |
| --- | ---: | ---: | ---: |
| Added lines | 33 | 26 | **&minus;21.2%** |
| Tokens | 992,255 | 947,577 | **&minus;4.5%** |
| Wall-clock time | 617.1s | 388.9s | **&minus;37.0%** |
| New files | 0 | 0 | no change |
| New dependencies | 0 | 0 | no change |
| Acceptance tests | 8/8 pass | 8/8 pass | no regression |

The headline is not just "less code" — it is less code **at no cost to correctness**, and faster, because the agent spends fewer turns building things it then has to justify.

> [!NOTE]
> This is a small internal sample, not a statistically powered study. Each task ran once per condition; model nondeterminism and service latency affect the result. Treat it as directional evidence, and reproduce it before quoting it as a benchmark.

Per-task figures, method and caveats: [eval/RESULTS.md](eval/RESULTS.md). Raw metrics for the published run: [eval/runs/20260918T084536Z/metrics.json](eval/runs/20260918T084536Z/metrics.json).

### Reproduce it

Requires Python 3 (standard library only) and the Codex CLI on your `PATH`.

```sh
python3 eval/run_eval.py              # all eight tasks, both conditions
python3 eval/run_eval.py --task retry # one task
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

Released under the [MIT Licence](LICENSE).

The name and the review-command shape are inspired by Ponytail, which is MIT licensed. No Ponytail code is included in this repository; the rules, skills and evaluation harness are original.
