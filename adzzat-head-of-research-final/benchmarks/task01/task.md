# Task 01 — Tool Execution Reliability

## Agent-facing task

The workspace contains `config/app.json`. Update only its `api_endpoint` field to `https://api.example.com/v2`.

Before modifying the original file, create an exact byte-for-byte backup at `config/app.json.bak`. Preserve every other JSON field and value. Read the updated file back and verify that it is valid JSON and contains the requested endpoint. Use only the documented workspace tools. Do not access paths outside the workspace.

## Environment and interface

Python 3.11+. The agent receives a `WorkspaceTools` object exposing `list_files`, `read_file`, `copy_file`, `write_file`, and `validate_json`. The agent is not given a workspace root path as part of the task contract.

## Grading

The grader verifies the backup, final JSON, preservation of unrelated fields, tool-call order, read-back verification, and call budget. See `grader.py`.

## Limitations

This virtual API validates tool-use logic but is not an operating-system security boundary. A production runner must isolate the agent process and prevent direct host filesystem access.
