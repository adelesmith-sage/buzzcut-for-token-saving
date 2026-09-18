<p align="center">
  <img src="assets/logo.png" alt="Buzzcut" width="180">
</p>

<h1 align="center">Buzzcut</h1>

<p align="center"><em>Keep code short back and sides. Nothing fancy on top.</em></p>

<p align="center">
  <a href="#install">Install</a> &middot;
  <a href="#what-you-get">What you get</a> &middot;
  <a href="#the-nine-rules">The nine rules</a> &middot;
  <a href="#measured-results">Measured results</a> &middot;
  <a href="#faq">FAQ</a>
</p>

---

Coding agents are rewarded for producing code, so they produce too much of it: a new helper beside the one that already worked, a retry wrapper nobody asked for, a dependency for something the standard library does.

Buzzcut is a drop-in instruction set that makes them stop. It is **nine ordered rules and three review commands** — two Markdown files and a folder. No extension to install, no service to run, no dependency to add.

In a paired evaluation over eight tasks, Buzzcut produced **21.2% fewer added lines**, **4.5% fewer tokens** and **37.0% less wall-clock time**, with **all 16 runs passing their acceptance tests**. [See the numbers &rarr;](#measured-results)

## Install

Buzzcut is files, not software. Copy three things into the repository you want it to apply to.

```sh
BUZZCUT=$(mktemp -d)
git clone --depth 1 https://github.com/<your-org>/buzzcut.git "$BUZZCUT"

cd /path/to/your-repo
mkdir -p .github/skills
cp -R "$BUZZCUT/.github/skills/."                .github/skills/
cp    "$BUZZCUT/.github/copilot-instructions.md" .github/
cp    "$BUZZCUT/AGENTS.md"                       .
```

Commit the result. That is the whole installation.

| What you copied | Purpose | Read by |
| --- | --- | --- |
| `.github/copilot-instructions.md` | The nine rules | GitHub Copilot in VS Code, Visual Studio, JetBrains and on github.com |
| `AGENTS.md` | The same nine rules | Codex CLI, and other agents that read `AGENTS.md` |
| `.github/skills/buzzcut-*/SKILL.md` | Three on-demand review commands | Copilot Agent Skills |

> **Already have a `.github/copilot-instructions.md`?** Do not overwrite it. Append Buzzcut's contents to the end of yours — the rules are written to sit alongside existing repository guidance rather than replace it.

### Check it worked

Open Copilot Chat in the repository and run:

```text
/buzzcut-review
```

You should get either a list of `file:line - what is over-built - the smallest correct alternative` findings, or `Buzzcut review: no cuts needed.` If the command does not appear, reload the window so the editor picks up the new `.github/skills` folder.

## What you get

**Nine ordered rules**, applied top to bottom until the request is satisfied. Each one states when it triggers, what to do, when *not* to apply it, and a paired good/bad example — so the agent can tell a real cut from a damaging one.

**Three slash commands**, available on demand and never auto-invoked:

| Command | Does |
| --- | --- |
| `/buzzcut-review` | Reviews the current diff for over-engineering and proposes the smallest correct alternative for each finding. |
| `/buzzcut-audit` | Audits a folder or the whole repository for the five highest-value simplifications. |
| `/buzzcut-debt` | Finds recorded `buzzcut:` limits in source and reports whether each is now ready to be replaced. |

All three are read-only. They report; they do not edit.

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

1. **Pilot on one active repository.** Install, then leave it for a sprint. The rules only bite when someone asks an agent for a change.
2. **Measure on your own code.** The numbers above come from synthetic tasks. Run `/buzzcut-audit` on a real service and judge the findings — that is the evidence your team will actually trust.
3. **Keep the two rule files identical.** `AGENTS.md` and `.github/copilot-instructions.md` are byte-identical on purpose, so every agent gets the same rules. The [verify workflow](.github/workflows/verify.yml) fails the build if they drift.
4. **Add stack-specific rules separately.** Put them in `.github/instructions/<name>.instructions.md` with an `applyTo` glob, so the always-loaded files stay short. See [CONTRIBUTING.md](CONTRIBUTING.md).
5. **Do not fork the rules per team.** Propose a change upstream instead; nine shared rules are worth more than nine variants.

## FAQ

**Will it make the agent skip tests, validation or security checks?**
No. Rule 6 forbids it explicitly, and all three skills are instructed never to recommend removing validation, data-loss protection, security, privacy, accessibility, compliance or explicitly requested behaviour. Rule 8 requires a proportionate test for non-trivial logic.

**Does it conflict with our existing Copilot instructions?**
It is written to add to them, not replace them. Append it to your existing file. If a Buzzcut rule genuinely contradicts your repository's guidance, your guidance wins — say so in your own file.

**Does it work outside GitHub Copilot?**
Yes, via `AGENTS.md`, which Codex CLI and several other agents read. The slash commands are Copilot Agent Skills and are Copilot-specific.

**Why are there two copies of the rules?**
Different tools look in different places. `.github/copilot-instructions.md` is Copilot's documented path; `AGENTS.md` is the cross-agent convention. Keeping both byte-identical is cheaper than teaching every tool a new path, and CI enforces it.

**Do I need the `eval/` folder in my repository?**
No. It exists so the claims above can be checked and re-run. Copy only `.github/` and `AGENTS.md`.

**Why is the agent still writing too much?**
Check that the instruction file is actually being loaded — in VS Code, Copilot Chat lists the instruction files it used under the response. Then try `/buzzcut-review` on the diff; the rules bias generation, while the skills catch what slips through.

## Contributing

A rule earns its place by changing model behaviour toward a smaller correct change, with evidence. See [CONTRIBUTING.md](CONTRIBUTING.md) for what a proposal needs, and [CHANGELOG.md](CHANGELOG.md) for what has changed.

## Licence and credit

Released under the [MIT Licence](LICENSE).

The name and the review-command shape are inspired by Ponytail, which is MIT licensed. No Ponytail code is included in this repository; the rules, skills and evaluation harness are original.
