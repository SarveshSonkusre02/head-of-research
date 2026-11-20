# Leakage, grader robustness, and quality review

## Task 01 — Tool Execution Reliability

| Attack / shortcut | Risk | Mitigation in this package | Residual risk |
|---|---|---|---|
| Hardcode final endpoint only | Superficial output passes | Backup, unrelated-field preservation, and tool protocol checks | Fixed fixture can still be memorized; randomize fields per run |
| Skip backup | Final config looks correct | Exact byte comparison of backup | Agent could copy known fixture if leaked |
| Modify wrong file | Tool call succeeds but requested target untouched | Grader inspects exact target path | Need randomized workspace names in larger suite |
| Write then never read back | No evidence of verification | Trajectory must contain read after write | A read call alone does not prove semantic inspection |
| Path traversal | Agent accesses outside task scope | Workspace-relative resolution rejects escapes | Not a security sandbox against Python introspection/process escape |
| Forge tool-call trace | Protocol score could be falsified | In a real harness, capture calls outside agent process | Current local Python object is a demonstrator, not tamper-proof |

## Task 02 — Transaction CSV Pipeline

| Attack / shortcut | Risk | Mitigation | Residual risk |
|---|---|---|---|
| Hardcode three fixture IDs | Passes fixed fixture only | Validate amounts, currencies, statuses, sorting, uniqueness and input immutability | Need hidden randomized fixtures and property-based tests |
| Drop every row | Could pass weak empty-output checks | Expected accepted IDs and reject source rows | Fixture-specific; randomized hidden set recommended |
| Keep first duplicate | Wrong winner | Assert latest timestamp wins | Add randomized duplicate timestamps/ties |
| Ignore malformed rows | Invalid data contaminates output | Reject-row and schema checks | Expand malformed-value combinations |
| Mutate input | Destroys source evidence | Byte-for-byte input immutability check | File permissions/read-only mount in production |

## Task 03 — Interval merge

| Attack / shortcut | Mitigation | Residual risk |
|---|---|---|
| Return fixed expected list | Multiple structurally different cases | Hidden randomized interval sets |
| Merge overlap but not touching | Explicit touching-boundary case | Randomized boundary generation |
| Mutate caller's list | Input snapshot comparison | Nested custom mutable objects not in task contract |
| Accept NaN / infinity | Explicit invalid endpoint cases | Broader numeric type policy may be required |

## Mutation-test plan

The current suite includes deliberate bad candidates / corrupted states for the main benchmark requirements. A production-grade mutation suite should also mutate each grader predicate one at a time and confirm that the suite fails. This package does not claim exhaustive mutation coverage.

## Security boundary

A benchmark grader should run outside the agent's writable namespace. The evaluated process should receive only a narrow task workspace, with no grader source, hidden fixtures, host mounts, credentials, or network access unless the task explicitly requires them. Tool traces should be recorded by the harness, not self-reported by the agent.

## Difficulty calibration

For a sufficiently large run set, use multiple agent/model configurations and repeated independent seeds. Report task pass rate with Wilson confidence intervals, per-check failure rates, tool calls, retries, time-to-completion, and infrastructure failure rate. Manually inspect a stratified sample of passes and failures. A low pass rate is not evidence of high difficulty until task validity and environment reliability are established.
