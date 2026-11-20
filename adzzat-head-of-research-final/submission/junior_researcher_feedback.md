# Written feedback to a junior researcher

**Submitted task:** “Write a function that sorts a list. The grader checks that the output contains the word `sorted`.”

This is not yet a valid benchmark task because the specification and grader do not measure the requested behavior. A candidate could return the literal string `sorted`, print that word, or include it in a comment without sorting anything.

Please revise it by specifying:

1. The input and output types.
2. Whether sorting is ascending or descending.
3. Whether the function may mutate the input.
4. The required behavior for empty lists, duplicates, negative values, and invalid/mixed types.
5. An executable grader that compares the returned sequence with independently computed expected outputs across multiple cases.
6. Adversarial tests that reject a constant return value, a single hardcoded example, and mutation when mutation is prohibited.

The key principle is to grade the behavior requested by the task, not the presence of a token associated with the task. A reference implementation should pass, and at least one independently authored valid implementation should also pass so the grader does not enforce a single coding style.
