# T17-IF-O — synthetic receipt-persistence investigation

## Status and objective

Proposed; execution awaits approval. The user approved committing IF-N findings and preparing this investigation. Nine reviewed files were committed as `1770d69`. [The stopped static review](../benchmarks/input-fit-tokenizer-static-review.md) retains eight observed HTTP events and a ninth pending precharge. Its sanitized exception was PermissionError; the exact failed I/O operation and Windows error number were not captured.

Identify where the same atomic-write sequence fails in controlled synthetic cases, and establish useful per-operation diagnostics. This cannot retrospectively prove the cause of the historical failure. No download, installation, artifact parsing/loading, acquisition retry, application work or runtime adoption is included. The IF-N run stays closed.

## Scope and intended files

Create only `tests/evals/spikes/receipt_persistence_review.py` and `test_receipt_persistence_review.py`, plus findings/status documentation. Use stdlib Python and, solely for the controlled Windows handle case, stdlib ctypes calls to Windows `kernel32.CreateFileW` and `CloseHandle`. No third-party DLL/model/library import or execution. Use the existing isolated interpreter; do not install dependencies or change PATH, global configuration or execution policy.

Read the committed IF-N `Budget.save` sequence as evidence: exclusive temporary-file open, JSON write, flush, fsync, close, then os.replace. Keep the old aid/test byte-identical; do not import its controller or call any of its acquisition/budget functions. A small instrumented synthetic equivalent may reproduce that sequence in the new case directories. It is an experiment, not a replacement writer or a repair of the closed ledger. Do not create a general persistence framework or change download code in this package.

## Ordered tasks and acceptance

| ID | Objective / prerequisite | Acceptance and evidence | Status |
|---|---|---|---|
| IF-O1 |After approval, persist shared accounting and preservation manifest |Fresh clock/reservations, fixed case schedule and old-evidence hashes recorded before optional work |Pending approval |
| IF-O2 |After O1, implement the diagnostic aid test-first |Failing tests then passing focused suite/lint/format checks and a caught guard mutation; injected errors classified without retry |Pending O1 |
| IF-O3 |After O2, one bounded synthetic Windows probe |Per-operation evidence for the fixed cases, correct expected failures and verified owned worker/handle teardown; unexpected failures stop without retry |Pending O2 |
| IF-O4 |After O3 or bounded stop, review and close |Findings separate observations from hypotheses, old evidence preserved, budgets/link/diff/checkpoint checked and separate source/results commit requested |Pending O3 |

## Diagnostic contract and fake controls

Record operation stages `open_temp`, `write_json`, `flush`, `fsync`, `close_temp` and `replace_target`, with before/success/failure status, exception class, errno, winerror when available and a synthetic case ID. Record only approved synthetic basenames and scalar metadata, never absolute error paths, document content, tokenizer vocabulary or arbitrary exception strings. Retain both failed temporary bytes and the old target on refusal. A diagnostic cannot imply the replacement succeeded merely because bytes reached a pending file.

The investigation's independent accounting/reporting must not use the writer under test. Keep a bounded append-only operation journal and a separate controller/teardown receipt; reporting failure stops the probe. A missing error number remains unknown. Do not introduce automatic retries, sleeps intended to hide sharing failures, permission escalation inside the worker, forced overwrites, deletion of failed pending files or reset of counters.

Fake tests must inject each write-stage failure and diagnostic-reporting failure; assert precise stage/status, preservation of pre-existing target/pending content, fail-closed accounting and no transport/candidate calls. Also cover malformed/outside/reparse paths, an already-closed epoch, case/count/time/output bounds, and mutation of a failure/replacement-success guard. Use representative synthetic bytes, not copies of old ledgers or downloaded assets. At most **six focused suite invocations** including red/green/mutation/regression and **four Ruff invocations** including final lint and format checks, all in the same shared budget. Reserve the final checks before optional refinements.

## One explicit synthetic Windows schedule

After fake checks pass, run exactly one isolated stdlib worker against fresh subdirectories under `data/t17/receipt-persistence-01/cases/`:

1. **Baseline:** at most128sequential updates of a small synthetic JSON target, using the same exclusive-pending/flush/fsync/close/replace sequence. Verify the published counter/content after each success. Stop at the first unexpected failure; no retry.
2. **Controlled sharing failure:** in a separate case directory, hold a read handle to the synthetic target with `CreateFileW`, sharing read/write but excluding delete sharing. Make one replacement attempt; record the actual stage/exception/errno/winerror. Expected refusal must preserve the old target and pending content. Always close the owned handle and verify CloseHandle success. Failure to obtain/close the intended handle stops the probe.
3. **Independent post-release positive control:** after verified handle closure, use a different fresh directory and make one successful replacement. This is a fixed positive control, not a retry of the failed case; the failed case remains untouched.
4. **Existing-pending negative control:** in another fresh directory, pre-create a synthetic pending file and make one exclusive-open attempt. Expect refusal at open_temp, unchanged old target/pending bytes and no replacement.

Maximum **131 transaction attempts**, with controlled negative cases, journal writes, verification and teardown included in the same execution/resource budget. Each target/pending JSON body is at most8KiB. The journal is bounded by the global2MiB output cap. No extra probe, rerun, reset, broad stress test or timing benchmark is authorized. If the expected sharing refusal is not reproduced, report that negative-control failure rather than claiming the historical error was explained.

Retain the owned Process handle/birth identity, supervise the worker for at most120seconds, and allow30seconds for verified teardown. Record controller/worker/console descendants; no candidate/service subprocess. Do not reuse saved PowerShell scripts or bypass execution policy. This is a synthetic-only execution boundary with no network and **no filesystem confinement or kernel RAM-cap claim**. Ordinary file APIs and the two named Windows handle APIs are the only intended native OS interactions beyond the interpreter/stdlib itself.

## Shared limits and stop conditions

After approval only, create ignored `data/t17/receipt-persistence-01/`. **96prepaid conservative units:80normal/16protected**: initialization8, helper/tests40, probe12, review12, close8, protected16. Count all wrappers, shells/interpreters, test/lint/mutation/positive/negative/control/report/cleanup operations in these blocks. Separately approved Git actions are outside this epoch. These are conservative allocations, not measured kernel process counters.

**1,200active seconds /2MiB new local outputs**, including synthetic fixtures, journals, partial receipts and reports. One actual probe worker only. Persist the complete reservations before optional preparation; no refunds. Protected units are solely for preservation/partial closure, never more tests or experiments. Stop on the first applicable cap, unapproved path/API, host denial, unexpected I/O error, failed control, deadline or uncertain handle/process teardown. Never silently extend a trial or replace its reporting transport.

Preserve AGENTS/SPEC/pyproject/lock, both committed IF-N aids, IF-N findings and prior parity design; also the final IF-N meter, original stopped meter, pending receipt, research ledger, manifest, closeout, controller/teardown/worker-result receipts, two wheel-inspection reports and Qwen identity report. Hash-check the three acquired payload files only to verify preservation; do not parse/load them or copy them into synthetic cases. Preserve linked earlier evidence through the existing manifests. No old file, receipt, budget, seal or source is changed by the investigation.

## Findings and next decision

Deliver `docs/benchmarks/receipt-persistence-investigation.md`, local operation/handle/process/budget receipts, the two tested aids and affected PLAN/TODO/README/checkpoint references. State which new synthetic operation failed or succeeded, and whether the sharing hypothesis is merely consistent with the old stop. Do not infer antivirus, network filtering, global permissions or an exact historical cause from a reproduced error class alone.

Any production-writer change, retry/backoff policy, fresh acquisition run or further diagnosis requires a separately reviewed decision/package. No runtime fix/adoption is promised by this investigation. Original 16GB CPU-only target, provisional context/output limits and all Stage1 scope/privacy requirements remain unchanged; G2 stays open.

Requested now: approve IF-O1–O4 as one exact synthetic-only package, including the named Windows handle APIs and limits, and separately commit the five proposal/status documents. One approval covers routine ordered work; later source/results commits, repair/acquisition/runtime adoption and stage transitions retain their gates.
