# Buzzcut

Make the smallest correct change. Buzzcut adds code-minimisation behaviour to the Aditi harness and repository guidance; do not restate or weaken either. Correctness, security, privacy and explicit requirements beat brevity.

Apply these rules in order. Stop when the request is fully satisfied.

## 1. Fix the shared cause

- **When:** the symptom can originate in shared code, or affects more than one caller.
- **Do:** trace the flow and callers; change the lowest shared point that owns the faulty behaviour.
- **Unless:** the behaviour is intentionally caller-specific, or the shared point carries unrelated contracts.
- **Good / bad:** correct the shared date parser / patch the displayed date in every screen.

## 2. Reuse before adding

- **When:** the repository, language, standard library, platform, framework or an installed dependency already does the job.
- **Do:** call or extend it. If the behaviour already exists, say so and change nothing.
- **Unless:** its contract differs, it is unsafe here, or extending it would break callers.
- **Good / bad:** pass the client's existing `retries=2` / add a second retry helper beside it.

## 3. Add no dependency by default

- **When:** a solution would add a package, service, build tool or runtime dependency.
- **Do:** use repository or platform capabilities. If a dependency is still needed, name it and explain why existing capabilities cannot do it.
- **Unless:** the user asked for it, or it is needed for security, standards compliance or a protocol you should not implement locally.
- **Good / bad:** the standard library's CSV writer / a CSV package for basic rows.

## 4. Minimise the change surface

- **When:** the task fits in existing code without a new abstraction, file or configuration path.
- **Do:** edit the fewest files and add the least code that keeps behaviour clear; prefer deletion when equivalent.
- **Unless:** architecture, a generated-file or security boundary requires separation, or several current implementations already need one shared abstraction.
- **Good / bad:** one branch in the existing handler / an interface, factory and implementation for one branch.

## 5. Require evidence for extra machinery

- **When:** a change would add retries, logging, caching, feature flags, configuration switches, extension points or extra error paths beyond the acceptance criteria.
- **Do:** omit it unless repository evidence or an explicit requirement shows it is needed.
- **Unless:** the user asked for the robustness, or a documented reliability, security or operational requirement demands it.
- **Good / bad:** the requested timeout via the existing client option / also backoff, a circuit breaker and metrics.

## 6. Preserve required protections

- **When:** a smaller solution would drop trust-boundary validation, data-loss protection, security, privacy, accessibility, compliance or explicitly requested behaviour.
- **Do:** keep the protection; minimise only the code around it.
- **Unless:** the same guarantee is already enforced at an earlier authoritative boundary.
- **Good / bad:** validate email at the API boundary with the existing validator / rely on browser validation and delete the API check.

## 7. Follow the local contract

- **When:** several implementations are equally small and correct.
- **Do:** match existing naming, control flow, error handling, imports and comment style; comment only a non-obvious reason or constraint.
- **Unless:** the local pattern causes the defect, breaks a requirement, or is being replaced.
- **Good / bad:** return the service's existing `NotFound` / add a second error hierarchy for one endpoint.

## 8. Verify proportionately

- **When:** the change has non-trivial logic or fixes a reproducible regression.
- **Do:** add the smallest check in the existing test mechanism that fails without the change, then run the narrowest relevant checks.
- **Unless:** it is documentation, a trivial static value, or already covered by a check you run.
- **Good / bad:** one regression case in the current test file / a new test framework for one assertion.

## 9. Mark deliberate limits only

- **When:** the solution knowingly omits a real case until a specific future condition occurs.
- **Do:** record it in a normal comment: `buzzcut: <current limit>; replace when <specific condition>`.
- **Unless:** there is no known limit or no concrete replacement condition.
- **Good / bad:** `# buzzcut: single region; replace when a second region is configured` / `# TODO: make this better`.

## Sage requirements

- **AI labels:** label AI-assisted code using the format in Sage's GitHub Copilot guidance. If it is unavailable, ask; do not invent one.
- **Sensitive data:** never put customer data, partner credentials, client IDs, tokens, production secrets or confidential repository content in a prompt, example or code. Use synthetic placeholders and Sage-approved tooling. There is no exception.
- **Third-party code:** when output resembles third-party or open-source code, complete the Open Source Procedure licence check before accepting it.
