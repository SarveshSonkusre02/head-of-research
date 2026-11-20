# Adzzat Labs — Head of Research, Benchmarks | Take-home submission

**Candidate artifact:** compact benchmark research and engineering suite  
**Environment:** Python 3.11+, Windows 10/11, VS Code, pytest  
**Scope:** three runnable benchmark tasks, research review, leakage analysis, junior feedback, and a one-page 100-task production process.

## Executive summary

This submission demonstrates a small, reproducible benchmark workflow:

1. Review publicly documented coding-agent failures and benchmark-quality defects.
2. Define two scored coding tasks with deterministic graders and reference solutions.
3. Add an optional third task as a stretch example.
4. Test graders against deliberately flawed candidate implementations.
5. Document leakage risks, limitations, and a repeatable task-production process.

**Evidence integrity:** no external LLM agent was run for this submission. Public case studies are distinguished from local scripted adversarial candidates. The local tests validate our task packages and graders; they do not establish model capability or general benchmark difficulty.

## Quick start — Windows PowerShell

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
pytest -q
python run_all.py
```

If PowerShell activation is restricted:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe run_all.py
```

## Repository map

```text
research/       failure review, evidence register, taxonomy
benchmarks/
  task01/       constrained filesystem tool-use task
  task02/       transaction CSV cleaning task
  task03/       interval-merging stretch task
quality/        adversarial checks and grader review
process/        one-page 100-task production process
submission/     junior feedback and AI-tools disclosure
run_all.py      run reference implementations and graders
```

## Benchmark overview

| Task | Capability | Core grading signal |
|---|---|---|
| 01 Tool Execution Reliability | Tool selection, order, state handling, path discipline, verification | Correct final files plus observed tool protocol |
| 02 Transaction Data Pipeline | Schema validation, normalization, deduplication, deterministic rejection | Exact accepted/rejected outputs plus invariants |
| 03 Interval Merge (stretch) | Algorithmic reasoning and boundary handling | Exact merged intervals across edge cases |

## Important design choices

- The grader checks requested behavior, not source-code similarity to the reference.
- Tasks specify inputs, outputs, edge cases, and environment assumptions.
- Reference implementations are included and tested against the graders.
- Adversarial fixtures target hardcoding, omitted steps, corrupted backups, malformed rows, and boundary errors.
- Task 01's virtual tool API is a benchmark harness, **not a production security sandbox**. A real agent runner must isolate the process/container and must not expose host filesystem access.
- Task 02 uses Python's standard library; no network or paid model is required.

## What is deliberately not included

This is not a production benchmark platform, hosted evaluation service, model leaderboard, 100-task dataset, or security-certified sandbox. Those would require a paid engagement, access to target agents, and agreed evaluation requirements. The 100-task section is a process sketch only.

## Reproducibility and expected outputs

- `pytest -q` runs the unit and adversarial test suite.
- `python run_all.py` runs each reference solution and prints its grader report.
- The benchmark runner reports local reference correctness only. It does not run an AI model.

## Suggested reviewer walkthrough

1. Read `research/failure_analysis.md` and inspect the source register.
2. Run `pytest -q`.
3. Run `python run_all.py`.
4. Inspect Task 01's trajectory checks and Task 02's accepted/rejected rows.
5. Review `quality/leakage_and_grader_review.md` for known limitations.

## License / reuse

The code and task specifications in this repository are original candidate-created material for this take-home exercise. External benchmark examples are summarized and linked to their public sources; their underlying datasets and repositories retain their respective licenses and terms.
