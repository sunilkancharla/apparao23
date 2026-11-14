# Proposed minimal state reader/writer repair

**Status: approved for bounded synthetic implementation and proposal commit.** Prepared 2026-11-14 (Asia/Calcutta), after investigation commit `612378a`. The user explicitly approved the40-start/15-active-minute package and committing its five proposal documents. Later repair source/results commits, runtime adoption and any native continuation remain separately gated. All stopped trial commands remain closed.

## Evidence and decision

The [synthetic investigation](../benchmarks/combined-state-write-investigation.md) passed40tests and reproduced Windows5/errno13 while an ordinary Python reader held a synthetic destination open. Replacement succeeded after closing it. Deliberately unsynchronized same-destination writers also collided on the fixed temporary filename, producing a different error. The exact reader/destination behind combined-05 remains unknown.

Current ledger operations use a process-local reentrant lock, but the shared writer itself does not acquire it and OCR deadline polling reads directly outside it. Descendant observations rewrite the meter even when persisted values do not change. Recommend addressing these owned coordination gaps before another native trial, without retries or permission changes.

| Option | Consequence |
|---|---|
| Unique temporary names alone | Can avoid temporary-name collisions, but does not coordinate read/modify/write accounting or prevent a held destination reader from blocking replacement |
| Retry denied replacements | Adds persistence/timing policy and can conceal a failed reservation; outside this minimal proposal |
| Shared short lock, coordinated OCR reads, unchanged-counter write suppression | Addresses owned thread overlap and unnecessary replacement work while preserving atomic writes, exact accounting and immediate refusal on actual failure; recommended |

## Exact proposed behavior

1. Acquire the existing reentrant `_MUTEX` around the entire core `write_json` operation, including its existing temporary write and single atomic replacement. Ledger read/modify/write already holds this same lock and remains reentrant. Direct core writers share it too. Preserve existing temporary naming, safe error operation/role tags, leftover-state startup refusal and exception propagation. No retry, in-place fallback or relaxed failure handling.
2. Introduce a small overridable meter-reading method on the reused OCR `OwnedRunner`; its default performs the same legacy JSON read/parse as today. The polling loop calls that method. The combined controller's existing OCR runner overrides it to use the active combined `Ledger.read`, closing the owned file handle under the same lock. Do not import the combined controller into the legacy OCR module, bypass its shared deadline fields, or change standalone OCR behavior. Never hold the lock across worker launch, OCR execution, sleeps, event waits, HTTP requests or inference. Lock only each short state access/update.
3. In `Ledger.observe_native`, compute the same cumulative maximum/extra/category/process values as today. If **every value that would be persisted is unchanged**, skip the replacement. Any increased observed-total/high-water mark must still persist, even if extra-descendant count stays the same. Never skip changed reservation/API/start updates. Evaluate category/total overshoot on every observation, including unchanged already-over-limit state; preserve write-before-raise for newly observed overshoot. Failed persistence still prevents simulated work/forward progress.

This coordinates owned threads sharing the combined module/lock only, not unrelated processes or arbitrary external readers. It cannot prove the historical cause or guarantee replacement never fails. An external sharing denial must continue to stop safely. The stricter250ms monitor checks may still stop on slow state access; this proposal does not weaken them. It does not attempt cross-process state sharing, new databases, file-lock services, OS scheduling changes or permission modifications.

## Proposed bounded synthetic implementation package

**40 shared process starts/attempts,15 active minutes**: a larger fake-only allowance than the investigation because this repair touches the reused OCR reader hook and requires both combined and standalone OCR regression suites. Include inspection/initialization, proposal Git only if explicitly approved, red/green runs, negative controls, tool/lint/format checks and reporting. Human/host approval waits excluded. Initialize a fresh ignored `data/t11/state-coordination-repair-01/` allocation or explicit initial reservation before launching package commands. Hash-link closed combined-05 and completed state-write investigation budgets; never reset/mutate them. Stop on the shared count/time boundary, unsafe paths, unexpected native workload/network activity, nontermination or uncertain cleanup.

Use only existing project-local standard-library Python, bounded fake-test bootstrap and Ruff. Generated scalar fixtures/temporary files stay under the new allocation, at most8MiB added disk; each new fixture at most64KiB and each new concurrency case at most32iterations/two test threads, all joined. Full existing fake regressions retain their own established control counts. Existing owned-fixture Windows sharing tests remain part of the combined suite and may call standard-library kernel APIs on those fixtures only. No model/OCR backend import/inference, API request, downloads, installation, rendering, real documents/answers/private error receipts, elevation, protection exclusions or ACL changes.

At most five existing source/test files:

- `tests/evals/spikes/combined_trial.py`: shared writer lock and no-op descendant observation logic.
- `tests/evals/spikes/combined_native.py`: combined OCR meter-read override/binding.
- `tests/evals/spikes/ocr_trial.py`: small polling read hook with unchanged default behavior.
- `tests/evals/spikes/test_combined_trial.py`: coordination/accounting/negative regressions.
- `tests/evals/spikes/test_ocr_trial.py`: standalone default-reader/hook contract regressions as needed.

Keep legacy-file edits focused. Run Ruff/format on the maintained combined scripts; check changed OCR code against its existing style/lint baseline and do not reformat unrelated legacy code to disguise the repair. Existing OCR and combined stdlib/fake contracts must pass within this package. Update factual reports/README/TODO/checkpoint and proposal status; all generated receipts/assets remain ignored. No run routing or new native handoff is included.

## Ordered tasks and acceptance

Tasks are tracked in root [TODO](../../TODO.md); all are pending package approval.

| ID | Prerequisite and objective | Acceptance/evidence |
|---|---|---|
| T11-SR1 | After approval, freeze scope and establish shared allocation | Active baseline/old hashes verified; counted initialization; exact reader/writer hook and legacy fallback reviewed before edits |
| T11-SR2 | After SR1, add meaningful failing coordination/accounting tests | Event-coordinated owned reader/writer and same-destination writer tests fail before repair, without deadlocking the test coordinator; unchanged observation performs no replacement; changed high-water/overshoot/failed persistence remain strict |
| T11-SR3 | After SR2, implement the minimal lock/hook/no-op repair | Owned access serialized with the same reentrant lock; real polling loop uses the hook, combined binding calls Ledger.read, standalone fallback preserved; no lock held across a worker wait/request; existing failure/privacy/timing controls preserved |
| T11-SR4 | After SR3, verify both suites and close out | Full combined/OCR fake suites and applicable lint/format pass; deterministic concurrency cases finish, external-reader denial remains fail-closed; old hashes unchanged and actual count/time reported; review diff/privacy and request separate source/results commit approval |

Required checks include: reader-open versus writer-replace ordering under the shared lock; nested/reentrant ledger writes; two owned same-destination writers retaining valid JSON without a fixed-temp collision; no-op observations with replacement deliberately denied succeeding without writing; changed observations still persisting/failing as appropriate; observed-total increase without extra-count increase; newly observed overshoot saved before failure; unchanged overshoot still refused; failed API/process reservation starts no simulated work; leftover temporary state still blocks startup; safe diagnostic roles never echo paths/messages; real polling invokes its hook and reads the same deadline; default standalone read behavior unchanged. Preserve the external-reader denial test, closing all fixture handles. Do not infer thread safety merely from a mocked lock call count.

Update the earlier characterization test that expected unchanged observations to write, explicitly because this package changes that behavior. Preserve the investigation report as historical evidence and retain its failure scenarios as appropriate external/uncoordinated controls; replace tests that deliberately interleave core-owned writers with tests proving the new serialization. Do not weaken quotas, counters or failures to obtain a pass.

## Approval and next gate

Approve or amend the exact40-start/15-active-minute synthetic implementation package, including its small legacy OCR hook/default compatibility review. That authorizes its necessary test-first changes and verification, not a native trial, retry policy, timing/permission change, dependency/runtime adoption or product feature. The five proposal documents can be explicitly approved for commit in the same reply; later repair source/results commits retain their own gate. A subsequent native trial would need a new reviewed allocation/identity/seal and disconnected handoff. Combined-05 must never be rerun.
