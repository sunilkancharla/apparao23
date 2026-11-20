# T17-IF-O — synthetic receipt-persistence investigation

## Outcome — 2026-11-16

Approved [IF-O package](../proposals/receipt-persistence-investigation.md), proposal commit `3b43968`. **All four synthetic cases completed as specified.** The128ordinary saves succeeded; the controlled Windows handle prevented target replacement; an independent save succeeded after handle closure; and an existing pending file caused the expected exclusive-open refusal. The worker exited0 and was reaped, with no active descendants found.

This identifies failure stages in controlled cases, not the historical cause of the [IF-N stop](input-fit-tokenizer-static-review.md). No old run was reopened, no writer repaired, and no download/installation/model/candidate execution occurred. Application/G2/runtime adoption remains open.

## Implementation and fake verification

Added `tests/evals/spikes/receipt_persistence_review.py` and `test_receipt_persistence_review.py`. The synthetic writer reproduces exclusive temporary open, JSON write, flush, fsync, close and replace, recording before/success/failure metadata independently. It retains exception class/errno/winerror, excludes arbitrary exception messages/absolute paths and never retries. Its append-only journal and controller receipts do not use the writer under test. The old IF-N aid/test stayed byte-identical and were not imported or executed.

Test-first missing-module red was followed by9passing tests in0.393s. A handle-cleanup test was added and the reporting-after-open boundary corrected before the actual probe. Ten tests passed in4.542s, then the failure-guard mutation caused7expected failing assertions across all six write stages and the stale-pending case. Original bytes were restored; final10tests passed in1.920s. Five focused suite invocations total, within six allowed. Routine tests used synthetic bytes and mocked Windows handles; no real handle API probe ran during them.

Ruff initially fixed2findings and reported one loop-variable capture issue, which was corrected. Formatting, final lint and final format check passed. Four Ruff invocations total, within the original allowance; no extra approval or limit change was needed. Code/guard/source identity was checked before the single actual probe.

## Fixed Windows probe — observed results

| Case | Attempts | Result / retained evidence |
|---|---:|---|
| Ordinary baseline |128 |All open/write/flush/fsync/close/replace stages succeeded; target counter verified after every update; final counter128 |
| Target opened without delete sharing |1 |Failed at `replace_target`: PermissionError, errno13, **winerror5**. Old target counter0 and complete pending counter1 retained |
| Independent post-release positive |1 |Different fresh directory, replacement succeeded and counter1 verified; not a retry of the failed case |
| Pre-existing pending file |1 |Failed at `open_temp`: FileExistsError, errno17, winerror unavailable. Old target and original pending bytes unchanged |

Exactly131transaction attempts and1,695journal packets were recorded. The two failure packets were the expected negative controls. CreateFileW used the approved read handle with read/write sharing and no delete sharing; CloseHandle returned success before the independent positive control. No failed pending file was removed or replaced to make a case pass. The controlled Windows error was5; do not substitute an assumed32.

Owned isolated Python worker PID372, birth2026-11-16T05:22:02.0531785Z, elapsed6.3475043seconds, exit0/reapedtrue, no timeout and zero active descendants found. Console output38bytes/stderr0. Receipts and synthetic cases are ignored under `data/t17/receipt-persistence-01/`: `probe-result.json`, `operations.jsonl`, `controller-start.json`, `teardown.json`, the independent meter/claim and case files. No network or third-party native code was used; the only deliberate handle calls were the two approved Windows APIs.

## Interpretation and historical limits

The controlled case demonstrates that an already-open target can produce PermissionError **at replacement after the pending bytes have been written and closed**. The successful baseline and independent positive show that this sequence worked without that controlled handle during this run. They do not guarantee freedom from intermittent contention or validate a general production persistence mechanism.

The historical IF-N record captured only PermissionError and a pending ninth precharge; it lacks the exact operation/winerror. Therefore the sharing explanation is **consistent with**, not established as, the old cause. These results do not identify antivirus software, another process, ACLs, network filtering or any particular lock owner. No system security setting or permission policy was changed.

Recommended next direction: prepare a fresh, diagnostic-enabled static-acquisition continuation for only the ten remaining data assets, retaining successful artifact identities and fail-closed/no-retry behavior. It would need its own exact package and approval. Per-operation telemetry may help classify a future failure; this investigation does not approve production-writer changes, retries/backoff or another acquisition. Native notices/advisories, dependency closure, remaining asset identities and tokenizer/rendering/runtime parity remain unresolved.

## Accounting, review and handoff

The original96prepaid units(80normal/16protected),1,200seconds/2MiB output, five-of-six focused suites, four-of-four Ruff invocations and one-of-one actual probe remain recorded in the independent meter. All positive/negative/control/journal/cleanup work shared this allocation. No refunds or old-epoch resets. Protected units remain solely for preservation/partial closure.

A post-probe reporting command inadvertently passed PowerShell Get-Content extended string objects through ConvertTo-Json, expanding provider metadata into excessive tool output. The truncation notice alone reports **12,273,370omitted bytes**, exceeding the intended2MiB reporting-output allowance. This is a documented reporting-budget deviation, even though project artifact files remain separately bounded. It was not archived in the project output files; it did not contain candidate file contents or alter the probe. Optional execution stopped; remaining work is preservation/closeout. Subsequent verification uses plain text/scalar JSON fields. Do not treat this as another probe or claim complete output-budget compliance.

Closeout verified312local links,23prior preservation hashes and both new source hashes. At verification elapsed time was471.826seconds and conservative project artifact output upper633,099bytes; these project/time checks passed, separately from the documented stdout deviation. Final closure time/status is in the meter/closeout. The old IF-N source, receipts and three acquired payload hashes remain preserved. No downloaded artifact was parsed or loaded in this investigation. Seven new/updated source/findings/status files require separate commit approval. No host /status or /compact invocation claimed.
