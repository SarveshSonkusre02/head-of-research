# Task 02 — Transaction CSV Cleaning

## Agent-facing task

Implement `clean_transactions(input_csv, clean_csv, rejects_csv)`.

Input columns, in any order: `transaction_id, account_id, amount, currency, timestamp, status`.

Rules:
1. Trim whitespace from all text fields.
2. `transaction_id` and `account_id` must be non-empty.
3. `amount` must parse as a finite decimal strictly greater than zero. Preserve its numeric value in canonical decimal notation (no unnecessary trailing zeros).
4. `currency` must be exactly three ASCII letters after trimming; normalize to uppercase.
5. `timestamp` must be ISO-8601 with an explicit timezone offset. Normalize to UTC in `YYYY-MM-DDTHH:MM:SSZ` format.
6. `status` must be one of `SETTLED`, `PENDING`, `REVERSED` after uppercasing.
7. For duplicate `transaction_id` values among otherwise valid rows, retain the row with the latest timestamp. If timestamps tie, retain the first occurrence in the input.
8. Invalid rows go to `rejects_csv`, with `source_row` (1-based CSV record number excluding header), `reason`, and original input columns. Use one stable reason string per rejected row; multiple errors may be joined with `; ` in the order of the rules above.
9. Write valid rows to `clean_csv` using the six canonical columns in the order listed above, sorted by `transaction_id` ascending.
10. Both outputs must include headers, even when empty. Do not modify the input file.

## Environment

Python 3.11+, standard library only. CSV is UTF-8 with optional UTF-8 BOM.

## Grading

The grader compares normalized output rows against a known fixture, checks ordering, deduplication, rejection reasons, headers, and input immutability.
