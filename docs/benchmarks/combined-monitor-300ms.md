# Combined monitor: 300-ms policy implementation

## Scope and approval

The user approved the [32-start/ten-minute fake-only package](../proposals/combined-monitor-300ms.md) and its five proposal documents' commit, `7586f68`. This report records evaluation-harness behavior, not product functionality or native feasibility. Windows 11/16 GB/CPU-only remains the target.

Only `combined_trial.py` and `test_combined_trial.py` changed. A named `MONITOR_LIMIT_SECONDS = 0.300` now supplies the six named monitor timing checks, resource sampling-gap guard and sanitized failure-limit packets. The desired100-ms work-aware cadence, all memory limits and every network/storage/accounting/ownership/teardown check remain unchanged. The native adapter and standalone OCR sources were not modified.

## Test-first evidence

Commands used the dedicated project environment and the copied, reviewed standard-library bootstrap in ignored `data/t11/monitor-300ms-01/`. The bootstrap sets a Windows512MiB/single-process Job boundary, places temporary fixtures in that allocation, and explicitly loads the combined and standalone OCR fake suites. It does not load native OCR/model backends or call inference APIs.

1. `.venv/Scripts/python.exe data/t11/monitor-300ms-01/test_bootstrap.py`: red,61tests in2.145s, one failure/two errors. New acceptance cases raised the old250-ms boundary, and the saved resource packet still reported0.25s rather than0.3s.
2. The same command after the minimum implementation: **61tests passed in1.901s** (45combined/16OCR).
3. `.venv/Scripts/ruff.exe check tests/evals/spikes/combined_trial.py tests/evals/spikes/test_combined_trial.py`: passed.
4. Focused Ruff format check initially found one comprehension layout; Ruff formatted that line, then both files passed the format check and lint. This was a whitespace-only change after the green tests; no unnecessary test rerun was performed.

For every named interval, guards accept250ms,251ms, the recorded287.7155-ms gap and exact300ms;300.001ms is refused. The resource guard has the same acceptance/refusal contract. Negative, Boolean, nonnumeric and nonfinite inputs remain refused. The exact-boundary direct-sample fake clock starts at zero to avoid subtraction-rounding artifacts; production comparisons retain strict `>` without a grace tolerance.

Existing fake observer/sample cases still cover long collection, TCP/storage duration, cumulative full iteration, late wake-up, completed-reading gaps, backwards clocks, failure-receipt durability, write denial and cancellation. Stop fixtures now exceed300ms rather than relying on the obsolete250-ms ceiling. One-byte memory-boundary controls, failed accounting persistence, ownership, restart refusal and standalone OCR contracts remain intact. Work-aware waiting also accepts the287.7155-ms workload without adding idle wait.

## Review, accounting and limits

Correctness/readability/architecture review found one shared constant and no new dependencies or control-flow changes. Security review confirmed the approved50-ms relaxation affects sampled observation timing only; kernel memory caps and all other boundaries remain intact. No raw documents, answers, images, evidence, vectors, model logs or private error-path receipts were read. Controlled file-sharing tests used owned scalar fixtures and closed their own handles.

The fresh shared allocation conservatively reserved16initial starts and eight verification starts; eight further starts are reserved for final documentation/hash/diff closeout, for **32/32 reservations**. Reservations cover failed red/format checks, PowerShell, Python, Ruff and proposal Git processes. Actual active elapsed time and the closed combined-06 meter/seal identity verification are recorded in ignored `data/t11/monitor-300ms-01/budget.json`. This is a conservative reservation count, not a claim that32native workers ran. Native OCR/model execution, API attempts, installations, downloads and rendering were zero.

Combined-06 and all older native runs remain closed. Its meter and seal must remain byte-identical; the old seal deliberately no longer matches edited source and must never be replaced. Its15answers still require local semantic review; no factual/citation acceptance is inferred. This package does not demonstrate completion at300ms, fix an identified scheduling cause, or authorize another native trial. A separate fresh sealed/disconnected native package and later runtime adoption remain gated. The allocation closed at32/32reservations and267.056active seconds, with prior hashes, documentation links and whitespace checks passing. The user subsequently approved the eight implementation/results files' commit; no new native execution was authorized.
