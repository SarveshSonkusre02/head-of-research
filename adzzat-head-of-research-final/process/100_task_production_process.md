# One-page process — producing 100 benchmark tasks at steady quality

## 1. Intake and task brief

Each proposed task starts with a capability label, real-world rationale, agent-facing prompt, explicit success contract, prohibited shortcuts, environment requirements, and known limitations. Reject tasks whose success cannot be judged objectively.

## 2. Authoring template

Every task must include:
- `task.md`: unambiguous instructions, inputs, outputs, constraints, edge cases.
- Environment manifest: pinned runtime/dependencies and deterministic setup.
- Starter state and fixtures: minimal, versioned, no hidden answer leakage.
- Reference solution: readable implementation with rationale.
- Grader: behavior-based assertions, independent from reference internals.
- Tests: happy path, edge cases, regression, adversarial and invalid-input cases.
- Metadata: capability tags, estimated difficulty, source/provenance, owner, review status.

## 3. Validation gates

1. **Contract review:** two reviewers independently restate what success means; resolve disagreement before implementation.
2. **Environment validation:** clean build twice; no network dependency unless explicitly declared; run on supported OS/runtime matrix.
3. **Reference validation:** reference passes grader; baseline starter fails for the intended reason.
4. **Alternative-solution validation:** at least one independently written valid solution passes, preventing overfitting to reference style.
5. **Mutation / leakage validation:** hardcoded output, skipped requirements, fixture detection, hidden-file access, and grader tampering attempts fail.
6. **Human audit:** reviewer checks prompt-test alignment and confirms every tested requirement appears in the prompt or is a standard language/runtime invariant.

## 4. Review and release

Use a two-person author/reviewer model, plus escalation for disagreement. Freeze a versioned task bundle, checksum fixtures, grader, environment image, and reference solution. Do not expose hidden tests to the evaluated agent. Maintain an errata process and retire contaminated or unreliable tasks.

## 5. Metrics and quality dashboard

Track task acceptance rate, reviewer disagreement, environment setup pass rate, reference pass rate, mutation score, agent pass rate by model, confidence intervals, median runtime, tool calls, failure categories, and appeal/regrade rate. Separate task quality metrics from model capability metrics.

## 6. Suggested steady-state capacity

For 100 tasks, pilot 5 tasks first; revise the template; then author in batches of 10. Require 100% clean environment setup and reference pass before release, and a target mutation score threshold set from the pilot. Do not optimize for throughput at the expense of independent review. A realistic staffing and timeline estimate depends on task complexity and is intentionally not asserted here.
