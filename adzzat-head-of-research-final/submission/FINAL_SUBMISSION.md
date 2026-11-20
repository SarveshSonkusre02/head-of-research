# Take-home submission — Head of Research, Benchmarks

## Summary

This submission contains a compact, reproducible benchmark suite and supporting research note. It covers the three scored sections in the assignment and both optional stretch items.

### Included

- A research note with seven public case studies, a failure taxonomy, evidence limitations, and source register.
- Two scored benchmark tasks, each with a precise task statement, environment assumptions, reference implementation, objective grader, and tests.
- A third optional benchmark task with a runnable reference and grader.
- Leakage / adversarial review for all three tasks.
- Written feedback on the junior-researcher sorting task.
- A one-page process for producing 100 tasks at consistent quality.
- AI-tools and contribution disclosure.

### Local validation

The reference implementations pass the included deterministic graders. The automated test suite is run locally with pytest. These results validate the reference implementations and task harnesses; they are not results from evaluating an external LLM agent.

### Research evidence limitation

The failure review uses public benchmark reports. It includes two explicitly narrated Terminal-Bench agent failures, benchmark task/grader defects from published SWE-bench audits, and one contamination probe. The cases are selected examples, not a random sample, and do not support estimates of failure prevalence across models. No external raw trajectories were independently replayed for this submission.

### Scope boundary

This is a take-home demonstration, not a production evaluation platform. It does not include a hosted agent runner, a 100-task dataset, a model leaderboard, or a production security sandbox. Those require agreed scope, target-agent access, and further resourcing.

### Suggested 30-minute walkthrough

1. Explain why a failed benchmark run may reflect a task or environment defect rather than a model limitation.
2. Run `pytest -q` and `python run_all.py`.
3. Walk through Task 01's tool protocol and backup invariants.
4. Walk through Task 02's validation, deduplication, and reject output.
5. Explain the grader's known limitations and the proposed scale-up quality gates.

See `AI_TOOLS.md` for disclosure of AI assistance and local validation boundaries.
