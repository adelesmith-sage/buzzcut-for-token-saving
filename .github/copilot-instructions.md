# Buzzcut

Make the smallest correct change. Buzzcut adds code-minimisation behaviour to the Aditi harness and repository guidance; do not restate or weaken either. Correctness, security, privacy and explicit requirements take priority over brevity.

Apply these rules in order. Stop when the request is fully satisfied.

## 1. Fix the shared cause

- **Trigger:** The reported symptom can originate in shared code or affect more than one caller.
- **Required action:** Trace the flow and callers; change the lowest shared point that owns the faulty behaviour.
- **Do not apply when:** The behaviour is intentionally caller-specific or changing the shared point would alter unrelated contracts.
- **Example:** Good — correct date parsing in the shared parser. Bad — patch the displayed date separately in every screen.

## 2. Reuse before adding

- **Trigger:** The repository, language, standard library, platform, framework or an installed dependency already performs the required job.
- **Required action:** Call or extend that implementation; if the requested behaviour already exists, report that no code change is needed.
- **Do not apply when:** The existing implementation has a different contract, is unsafe for this use, or extension would break its callers.
- **Example:** Good — pass the existing client's `retries=2` option. Bad — add a second retry helper beside it.

## 3. Add no dependency by default

- **Trigger:** A solution would add a package, service, build tool or runtime dependency.
- **Required action:** Use repository or platform capabilities instead. If a dependency is still necessary, name it and explain why current capabilities cannot solve the problem.
- **Do not apply when:** The user explicitly requests the dependency, or a maintained dependency is necessary for security, standards compliance or a protocol that should not be implemented locally.
- **Example:** Good — use the standard library's CSV writer. Bad — add a CSV package for basic row output.

## 4. Minimise the change surface

- **Trigger:** The task can be completed in existing code without a new abstraction, file or configuration path.
- **Required action:** Edit the fewest files and add the least code that preserves clear behaviour; prefer deletion when equivalent.
- **Do not apply when:** Separation is required by the repository's architecture, generated-file boundary, security boundary, or multiple current implementations already need one shared abstraction.
- **Example:** Good — add one branch to the existing handler. Bad — add an interface, factory and implementation for one branch.

## 5. Require evidence for extra machinery

- **Trigger:** A change introduces retries, logging, caching, feature flags, configuration switches, extension points or extra error paths beyond the stated acceptance criteria.
- **Required action:** Omit it unless current repository evidence or an explicit requirement shows it is needed.
- **Do not apply when:** The user asks for the robustness, or a documented reliability, security or operational requirement demands it.
- **Example:** Good — add the requested timeout using the existing client option. Bad — also add backoff, a circuit breaker and metrics without a requirement.

## 6. Preserve required protections

- **Trigger:** A smaller solution would remove trust-boundary validation, data-loss protection, security, privacy, accessibility, compliance or explicitly requested behaviour.
- **Required action:** Keep the protection and minimise only the surrounding implementation.
- **Do not apply when:** The protection is proven redundant because the same guarantee is enforced at an earlier authoritative boundary.
- **Example:** Good — validate an email at the API boundary with the existing validator. Bad — rely only on browser validation and delete the API check.

## 7. Follow the local contract

- **Trigger:** Several implementations are equally small and correct.
- **Required action:** Choose the repository's existing naming, control flow, error handling, imports and comment style; comment only a non-obvious reason or constraint.
- **Do not apply when:** The local pattern causes the reported defect, violates a requirement or is explicitly being replaced.
- **Example:** Good — return the service's existing `NotFound` error. Bad — introduce a second error hierarchy for one endpoint.

## 8. Verify proportionately

- **Trigger:** The change contains non-trivial logic or fixes a reproducible regression.
- **Required action:** Add the smallest check in the existing test mechanism that fails without the change, then run the narrowest relevant checks.
- **Do not apply when:** The change is documentation, a trivial static value, or already covered by an existing check that you run.
- **Example:** Good — add one regression case to the current test file. Bad — introduce a new test framework for one assertion.

## 9. Mark deliberate limits only

- **Trigger:** The chosen solution knowingly omits a real case until a specific future condition occurs.
- **Required action:** Use the language's normal comment syntax: `buzzcut: <current limit>; replace when <specific condition>`.
- **Do not apply when:** The choice has no known limit or no concrete replacement condition.
- **Example:** Good — `# buzzcut: single region; replace when a second region is configured`. Bad — `# TODO: make this better`.

## Sage requirements

- **AI labels:** When adding or modifying AI-assisted code, use the label format in Sage's GitHub Copilot guidance. If that format is unavailable, ask; do not invent one. Good — use the approved repository label. Bad — invent an `AI-generated` comment.
- **Sensitive data:** When a prompt, example or code would contain customer data, partner credentials, client IDs, tokens, production secrets or confidential repository content, use synthetic placeholders and Sage-approved tooling. There is no prompt-level exception. Good — use `TOKEN_EXAMPLE`. Bad — paste a production token for debugging.
- **Third-party code:** When output resembles third-party or open-source code, complete the Open Source Procedure licence check before accepting it. This does not apply to independently written code with no copied source. Good — record the licence check before reuse. Bad — paste a public snippet without checking its licence.
