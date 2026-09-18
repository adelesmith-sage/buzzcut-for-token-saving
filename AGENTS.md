# Buzzcut

Make the smallest correct change. Buzzcut supplements Aditi and repository rules; do not repeat or weaken them. Correctness, security, privacy and explicit requirements outrank brevity.

Before adding code, search file names and symbols once using the request's capability terms, then trace only the touched flow, callers and matches. Batch focused reads; edit once the owner, reusable capability and check are clear. Do not reread files, dump broad output or explore hypothetical designs. Run the narrowest check once; retry only after a real failure.

Use terse technical prose. Omit acknowledgements, task restatement, routine progress, unrequested options and recap. In the final response give only changed files, verification, and material assumptions or blockers. Keep code, commands, paths, exact errors, security warnings and approval questions complete.

## Nine rules

1. **Fix the shared cause.** If shared code owns the symptom or several callers are affected, fix the lowest shared owner and inspect its callers. Exception: caller-specific behaviour or incompatible contracts. Example: fix the shared parser; do not patch every screen.
2. **Reuse before adding.** If the repository, language, standard library, platform, framework or an installed dependency does the job, call or extend it; if behaviour is already correct, change nothing. Exception: unsafe or incompatible contracts. Example: pass existing `retries=2`; do not add a retry wrapper.
3. **Add no dependency by default.** If a solution adds a package, service or build tool, use existing capabilities or state why none works. Exception: an explicit request or required security, standard or protocol implementation. Example: use the standard CSV writer; do not add a CSV package for basic rows.
4. **Minimise the surface.** If the change fits existing code, touch the fewest files and add the least clear code; prefer deletion when equivalent. Exception: required generation, security boundaries or several current implementations. Example: add one branch; do not add an interface and factory for it.
5. **Demand evidence for machinery.** Omit unrequested retries, logging, caching, flags, configuration, extension points and extra error paths. Exception: acceptance criteria or documented reliability, security or operations evidence requires them. Example: add the requested timeout; do not also add backoff, a breaker and metrics.
6. **Preserve protections.** Never remove boundary validation, data-loss protection, security, privacy, accessibility, compliance or requested behaviour to save code. Exception: the same guarantee exists at an earlier authoritative boundary. Example: keep the API validator; browser validation alone is insufficient.
7. **Follow the local contract.** Among equally small correct options, match local naming, flow, errors, imports and comment style. Exception: that pattern caused the defect or violates the request. Example: reuse `NotFound`; do not create a second error hierarchy.
8. **Verify proportionately.** For non-trivial logic or a regression, add the smallest check in the existing test mechanism and run the narrowest relevant checks. Exception: trivial static or documentation changes, or existing coverage. Example: add one current-suite case; do not introduce a test framework.
9. **Mark real limits only.** If the solution deliberately omits a known case, comment `buzzcut: <current limit>; replace when <specific condition>`. Exception: no known limit or trigger. Example: `# buzzcut: single region; replace when a second is configured`; not `# TODO: improve`.

## Sage requirements

- Label AI-assisted code using Sage's GitHub Copilot format. If unavailable, ask; do not invent it.
- Never put customer data, credentials, IDs, tokens, production secrets or confidential source in prompts or examples; use synthetic data and approved tooling.
- Licence-check third-party or open-source-like output through the Open Source Procedure before accepting it.
