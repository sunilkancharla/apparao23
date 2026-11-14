# Proposed bounded state-file investigation

**Status: approved for this bounded synthetic investigation and proposal commit.** Static review prepared 2026-11-14 (Asia/Calcutta), after combined-05 results commit `dbe607a`. The user explicitly approved the32-start/ten-active-minute diagnostic package and committing its five proposal documents. Writer-policy repairs, permission changes, new native trials and later investigation source/results commits remain separately gated. All old trial commands stay closed.

## Confirmed failure and static findings

[Combined-05](../benchmarks/combined-ocr-model-fifth-stop.md) stopped on Windows error5/errno13 at `write_json`'s `os.replace(temporary, path)`. This identifies a denied replacement, not a specific locking process or destination from the sanitized receipt. No private exact-path receipt was read. Cleanup was verified; no scored chats ran. The last persisted meter was52/160 with eightAPI attempts, but a failed state write means persisted counters alone cannot prove every attempted transition was saved.

| Path through authored code | Existing coordination | Review finding |
|---|---|---|
| `Ledger.reserve/start/call/observe_native` | Process-local reentrant `_MUTEX` around read/update/replace; shared module alias in CLI/lazy adapter | These ledger callers serialize their own threads. The lock is not an operating-system file lock and does not coordinate unrelated processes or every direct reader |
| `Ledger.observe_native` during every monitor collection | Same `_MUTEX` | Replaces state even when cumulative observed/extra counts and categories are unchanged; unnecessary write frequency is a candidate to evaluate, not an approved optimization |
| Shared `write_json` helper | Fixed sibling `.json.tmp`, closed after writing, then `os.replace` | The helper itself does not serialize all destinations. Same-destination unsynchronized callers could contend; inventory actual callers before asserting that occurs |
| OCR `OwnedRunner.run` deadline polling | Reads global meter with `read_text` outside the combined ledger lock | A coordination gap exists during active OCR polling. Combined-05's failure phase followed completed OCR controls, so this alone does not establish historical causation |
| Other controller summaries/receipts/worker outputs | Several direct writes, generally distinct destinations | Distinguish different-file activity from genuine same-file contention; do not generalize all JSON writes into one proven race |

An external reader or another access restriction remains possible. This static review cannot identify antivirus involvement, an IDE lock, a permission misconfiguration or the exact historical destination. Do not claim one from Windows error5 alone.

## Proposed diagnostic package

Authorize one **32-start/ten-active-minute standard-library synthetic investigation**. Include initialization/inspection, proposal Git work if explicitly approved, all positive/negative/regression tests, tools and reporting in the same shared allocation. Human/host approval waits are excluded. Establish a fresh ignored `data/t11/state-write-investigation-01/` meter or explicit initial reservation before any package commands. Hash-link the closed combined-05 meter and completed cadence-repair budget, never reset or modify them. Stop on allocation/deadline exhaustion, unexpected process/network activity, unsafe path, nontermination or ambiguous cleanup; no automatic retry/reset.

Use only newly authored synthetic scalar JSON under that allocation or its contained temporary directories: at most64KiB per fixture,8MiB added disk,32 write iterations per scenario, two coordinated test threads and no child processes beyond the approved bootstrap/tools. No user samples, raw OCR/answers/evidence, private error receipts, model assets or existing state writes. Test output contains only fixture role, operation phase, scalar counters and error codes.

Allowed runtime is the existing project-local standard-library interpreter/test bootstrap and Ruff; no installs/downloads, inference backends, OCR, model server, API requests or native workload. For one controlled file-sharing scenario, standard-library `ctypes` may open **only a newly generated owned fixture** using Windows `CreateFileW` with an explicitly chosen sharing mode; close that handle in `finally` and test replacement on that fixture. This is a real local synthetic file-handle check, not model/OCR execution or a scan of other processes. Record actual observed Windows codes even if they differ from the historical error5. Do not run system handle scanners, elevate, modify ACLs, disable protections or terminate unrelated processes.

## Ordered tasks and acceptance

Tasks are tracked in root [TODO](../../TODO.md). The package is investigation only; adoption of a changed writer/retry policy or a new native continuation stays separately gated.

| ID | Prerequisite and task | Acceptance/evidence |
|---|---|---|
| T11-SW1 | After package approval, freeze writer/reader inventory and initialize shared meter | All relevant destinations and direct-reader boundaries recorded as safe roles; prior hashes unchanged; every command/test attempt reserved before launch |
| T11-SW2 | After SW1, build deterministic synthetic controls | Real successful atomic replacement; injected write/replace denial preserving last good destination; event-coordinated same-destination/independent-destination cases; explicit open-reader sharing test with handles closed. Record outcomes and codes without claiming historical reproduction |
| T11-SW3 | After SW2, evaluate accounting and diagnostic consequences | Failed reservation/API checkpoint must return failure before simulated work begins; leftover temporary state causes startup refusal. Unchanged/changed descendant observations and overshoot retain exact accounting semantics. Distinguish write versus replace failure using safe roles/codes if additional diagnostics are needed |
| T11-SW4 | After SW3, run focused/full fake regressions and report | Same-budget test/Ruff/diff/privacy checks; bounded threads finish; old hashes unchanged; actual elapsed/start counts and synthetic outcomes documented. Recommend a specific evidence-backed repair or record unresolved cause, then request source/results commit approval |

Source scope: the existing `test_combined_trial.py`, and minimal **diagnostic-only** instrumentation in `combined_trial.py`/`combined_native.py` if needed for operation-stage/known-role reporting. Review `ocr_trial.py` read-only. No change to atomic replacement semantics, locks, write frequency, deadlines, resource ceilings, OCR reader behavior or trial routing in this diagnostic package. Generated fixture files/receipts remain ignored; safe test definitions and factual reports may be versioned after separate Git approval.

The write-denial tests use injected failures as deterministic regression controls. The controlled Windows handle test is separate evidence; it cannot identify who held a historical handle or prove the same code/path caused combined-05. The initial source review also identifies a possible future no-op-write optimization, but this package only measures/asserts current behavior and its consequences.

## Remaining decision

**Subsequent completion:** Proposal documents committed `4a2261e`. [Investigation evidence](../benchmarks/combined-state-write-investigation.md) records40passing tests in3.464s and the observed Windows5/errno13 replacement refusal with controlled Windows and ordinary Python readers. Writer semantics remain unchanged; safe operation/role diagnostics only. Investigation source/results commit and any repair/native continuation remain separately gated. The initial package approval request below is historical.

Approve or amend this exact synthetic investigation, including the fixture-only Windows handle case and32-start/ten-minute ceiling. Its findings would inform a separately reviewed minimal repair. No retry policy, permission change, in-place file rewrite, ledger reset, timing change, model/OCR adoption, product feature or native trial is included. The five proposal documents may be explicitly approved for commit alongside the package; later investigation source/results commits remain a separate gate.
