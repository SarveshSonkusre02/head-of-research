# Task 03 — Merge Overlapping Intervals (optional stretch)

Implement `merge_intervals(intervals)` where each interval is a pair `[start, end]` of integers or finite floats and `start <= end`.

Return a list of intervals sorted by start, merging overlapping **and touching** intervals. Thus `[1, 3]` and `[3, 5]` merge to `[1, 5]`. Do not mutate the input. Empty input returns `[]`. Invalid shapes, non-numeric/non-finite endpoints, or start greater than end raise `ValueError`.

The grader checks empty, singleton, nested, overlapping, touching, negative, unsorted, and invalid cases, and verifies input immutability.
