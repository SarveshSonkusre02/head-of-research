# Public sources consulted

1. **Terminal-Bench announcement and examples** — https://www.tbench.ai/news/announcement  
   Includes the Linux kernel/QEMU interactive-session failure and Raman-fitting unit/verification failure, plus benchmark task/harness design.
2. **OpenAI, “Why we no longer evaluate SWE-bench Verified” (23 February 2026)** — https://openai.com/index/why-we-no-longer-evaluate-swe-bench-verified/  
   Includes the Pylint narrow-test example, SymPy wide-test example, and Django contamination probe.
3. **OpenAI, “Separating signal from noise in coding evaluations” (8 July 2026)** — https://openai.com/index/separating-signal-from-noise-coding-evaluations/  
   Includes SWE-Bench Pro audit methodology, task defect categories, aggregate audit results, and the OpenLibrary-77c16d5 prompt/hidden-test mismatch.
4. **OpenAI, “Introducing SWE-bench Verified” (13 August 2024; subsequently updated)** — https://openai.com/index/introducing-swe-bench-verified/  
   Includes the scikit-learn example of a test requiring an exact deprecation warning not adequately specified by the task.
5. **SWE-agent trajectories dataset card** — https://huggingface.co/datasets/ElenaFu/SWE-agent-trajectories  
   Describes a public collection of 80,036 SWE-agent trajectories and aggregate statistics. It is a potential source for future trajectory-level analysis; this submission did not download or reanalyze the full dataset.
6. **Terminal-Bench GitHub repository** — https://github.com/harbor-framework/terminal-bench  
   Task definitions and harness implementation reference.

All case summaries in `failure_analysis.md` are paraphrased. The submission does not redistribute external benchmark data or raw trajectories.
