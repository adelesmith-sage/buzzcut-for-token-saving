# Contributing to Buzzcut

Buzzcut rules should earn their place by changing model behaviour toward a smaller correct change.

## Propose a guardrail

Open a pull request that includes:

- the failure mode, with a concrete example;
- evidence that existing guidance does not already cover it;
- the shortest rule that prevents the failure without blocking valid work;
- any interaction with correctness, security, privacy, accessibility, compliance or the Aditi harness; and
- before-and-after results from representative prompts or repository tasks.

Put general rules in `AGENTS.md` and mirror them in `.github/copilot-instructions.md`. The two files must stay byte-identical; the `verify` workflow fails the build if they drift. Put language- or stack-specific rules in `.github/instructions/<name>.instructions.md` with an `applyTo` glob in YAML frontmatter, so the always-loaded files stay short.

## Review criteria

A rule is ready when it is actionable, testable, broadly useful in its stated scope and not a duplicate or rewording of an existing rule. Prefer tightening an existing rule over adding another one.

Keep pull requests focused. Do not combine a guardrail proposal with unrelated wording or formatting changes.

## Evidence

To produce before-and-after numbers, run the paired harness described in [eval/README.md](eval/README.md). Add a task under `eval/tasks/` if your failure mode is not already represented; a good task is one where the over-engineered solution is the tempting one.
