# Research note — coding-agent failures and benchmark defects

## Scope and evidence standard

This review uses publicly documented examples from Terminal-Bench and OpenAI's published audits of SWE-bench / SWE-bench Pro. It does **not** claim that the author independently replayed the external model trajectories. Some cases are direct agent-attempt observations; others are task/grader defects that can create false negatives or false positives. Evidence type is identified per case.

The purpose of the review is to distinguish:

- **Capability gap:** the agent's decisions or implementation are inadequate against a clear, feasible task.
- **Task/grader defect:** instructions, tests, or environment do not define or measure the intended behavior fairly.
- **Contamination/leakage:** success may be inflated because task-specific information was available during training or elicitation.
- **Environment/interface failure:** the runtime or interaction model contributes to failure.

## Seven public case studies

### Case 1 — Terminal-Bench: Linux kernel build with QEMU

- **Observed behavior:** Terminus with GPT-4.1 chose to install/use `nano`, mishandled the interactive session, and gave up instead of switching to another tool or recovering.
- **Likely category:** tool-use / interactive-session recovery.
- **Capability vs defect:** primarily an agent capability gap as described by the benchmark authors; the task itself is presented as an example of interactive terminal difficulty.
- **Caveat:** the public announcement is a concise case description, not a full raw trajectory.

### Case 2 — Terminal-Bench: Raman fitting

- **Observed behavior:** the input values were wavelengths (nm), but the agent attempted to fit peaks at expected wavenumber positions. It obtained a numerical fit with nonsensical parameters, including negative amplitudes or extremely large widths, and did not detect the problem despite claiming a sanity check.
- **Likely category:** domain/unit reasoning plus failed result verification.
- **Capability vs defect:** primarily capability / verification failure; the unit distinction is part of the task context.
- **Caveat:** a single example does not establish a general weakness in scientific reasoning.

### Case 3 — SWE-bench Verified: `pylint-dev__pylint-4551`

- **Observed defect:** the issue asks for Python type hints to appear in UML output. The PR test imports a helper named `get_annotation`, although that helper name is not specified by the task. A functionally valid alternative can therefore fail at test collection with an import error.
- **Likely category:** overly strict / implementation-specific grader.
- **Capability vs defect:** task/grader defect; a failed test here is not reliable evidence of an agent capability gap.

### Case 4 — SWE-bench Verified: `sympy__sympy-18199`

- **Observed defect:** the task description covers one `nthroot_mod` issue, while the PR-derived tests cover three related issues. Models that correctly implement the described issue can fail tests for the other two.
- **Likely category:** underspecified / overly broad task contract (wide tests).
- **Capability vs defect:** task/grader defect.

### Case 5 — SWE-bench Verified: `scikit-learn__scikit-learn-14520`

- **Observed defect:** the task context does not make the expected deprecation behavior and exact warning message sufficiently clear, but the test requires a specific `DeprecationWarning` message when a parameter is used.
- **Likely category:** prompt underspecification and over-specific assertion.
- **Capability vs defect:** task/grader defect; exact wording is not a fair hidden requirement if it is absent from the task contract.

### Case 6 — SWE-Bench Pro audit: `OpenLibrary-77c16d5`

- **Observed defect:** the prompt's examples specify one leading space in a Markdown table-of-contents row, while hidden assertions expect two leading spaces. An agent following the visible instruction can be rejected.
- **Likely category:** prompt/test contradiction.
- **Capability vs defect:** task/grader defect.

### Case 7 — SWE-bench Verified contamination example: `django__django-11451`

- **Observed behavior:** during a deliberate memory/contamination probe, GPT-5.2 reconstructed the relevant function, file path, and early-return code change from a short task hint, closely matching the gold patch.
- **Likely category:** benchmark contamination / memorization risk.
- **Capability vs defect:** not a failure; this is included as a leakage case because it illustrates why a passing score may not reflect fresh problem-solving.
- **Caveat:** the elicitation was a deliberate contamination probe, not an ordinary benchmark run.

## Failure taxonomy

| Category | Operational definition | Evidence in this review | What to measure |
|---|---|---|---|
| Tool-use / interaction recovery | Agent chooses or operates tools poorly, or fails to recover from interactive state | Terminal-Bench kernel case | Invalid calls, failed commands, recovery attempts, completion |
| Reasoning / unit interpretation | Agent applies the wrong conceptual model or units | Terminal-Bench Raman case | Domain constraints checked, dimensional consistency, output plausibility |
| Verification failure | Agent declares success without checking whether output is plausible/correct | Raman case | Independent postcondition checks, invariant violations |
| Prompt/test misalignment | Tests require behavior not specified or contradict instructions | Pylint, SymPy, scikit-learn, OpenLibrary | Human prompt-test consistency review; false-negative rate |
| Contamination / leakage | Task-specific solution knowledge is available before evaluation | Django contamination probe | Memorized patch reproduction, exposure analysis, private task variants |
| Environment/interface defect | Setup or tool session creates failures unrelated to task capability | Terminal interaction context; general SWE-bench setup concerns | Clean setup pass, dependency reproducibility, OS/Python matrix |

## What the evidence supports — and does not support

The cases demonstrate that terminal interaction, unit interpretation, verification, prompt/test alignment, and contamination are meaningful failure or evaluation-risk categories. They do **not** support estimating their prevalence across current models. The cases are selected public examples, drawn from different benchmarks and methods, and are not a random sample.

OpenAI's 2026 audit of SWE-bench Pro reported 200/731 tasks flagged by an automated pipeline (27.4%) and 249/731 by human annotation (34.1%). The reported categories included overly strict tests, underspecified prompts, low-coverage tests, and misleading prompts. These figures describe that audited dataset and methodology; they should not be generalized to all coding benchmarks.

OpenAI's earlier SWE-bench Verified audit reported that 59.4% of 138 repeatedly difficult tasks had material test/prompt issues. This is a selected subset, not an estimate for the entire dataset.

## Research conclusion

A benchmark failure is not automatically a model failure. Before attributing a miss to model capability, validate task clarity, grader scope, environment reproducibility, and contamination exposure. This is the central research principle used in the three tasks in this repository.
