# Synthetic state-file investigation — 2026-11-14

The user approved the [32-start/ten-active-minute package](../proposals/combined-state-write-investigation.md) and committing five proposal documents, committed as `4a2261e`. Tests use owned synthetic scalar JSON only. No OCR/model inference, API call, download, install, permission change, old trial execution or private-path receipt access occurred.

## Observed outcomes

| Scenario | Actual result |
|---|---|
| Successful atomic state replacement | Destination contained the complete new JSON |
| Injected temporary-write or replacement denial | Last good destination bytes remained unchanged; errors propagated |
| Failed process/API reservation persistence | Simulated work did not start; leftover meter temporary file caused new Ledger construction to refuse startup |
| Two deliberately unsynchronized writers to the same destination/fixed temporary filename | Coordinated interleaving reproduced FileNotFoundError after one writer consumed the shared temporary file; retained destination contained the second writer's valid JSON |
| Same coordinated interleaving with distinct destinations | Both writes succeeded with separate contents |
| Repeated unchanged descendant observation | State values remained equal but both observations still invoked the writer; a later increased count persisted correctly |
| Owned Windows reader with read/write sharing but no delete sharing | Replacement failed with Windows5/errno13; last good JSON retained; closing the handle restored replacement |
| Ordinary held Python text reader on the synthetic destination | Replacement also failed with Windows5/errno13; closing the reader restored replacement |

The ordinary-reader experiment uses the same open/read/close style as the polling code, but deliberately holds the handle across the replacement. This establishes that such an overlap can produce the exact historical error class/codes on this machine. It does **not** establish which reader, destination or process overlapped during combined-05. The failed native phase followed completed OCR controls; blaming that particular reader remains unsupported. The separate same-destination test produced FileNotFoundError, not the historical permission failure, and should not be conflated with it.

The project-owned ledger callers already use a shared process-local lock; OCR polling reads the global meter directly outside that lock. External readers are not coordinated by it. The observer also rewrites unchanged state every collection, creating unnecessary opportunities for replacement contention. These are concrete design considerations, not proof that a particular external program or antivirus caused the stop.

## Diagnostic changes and verification

Two authored source files changed: `combined_trial.py` adds only `state_operation` (write/replace) and known `state_role` enum metadata to filesystem errors; `test_combined_trial.py` adds six synthetic test methods. Arbitrary error attributes/paths/messages are not echoed. The helper still writes the same temporary sibling, closes it and performs one replacement; there is no retry, new lock, changed write frequency or in-place fallback. Native adapter/OCR polling implementation, timing/resource guards and old routing are unchanged.

The new diagnostic expectations first failed with three errors across40 tests. After minimal instrumentation and lint corrections, the final full suite passed **40 tests in3.464seconds**, Ruff lint and source formatting passed. The standard Python reader case was added after the first green run to directly characterize the existing read style. All test invocations, negative controls, the fixture-only Windows handle case, proposal Git and tools share the same allocation. All synthetic worker threads finished, all opened handles closed in finally blocks and temporary cases cleaned up. Existing accounting, overshoot, ownership, timing, privacy, quota and teardown regressions remained in the suite.

```powershell
& 'F:/Python/Python314/python.exe' -I -S -B data/t11/state-write-investigation-01/test_bootstrap.py
& '.venv/Scripts/ruff.exe' check --no-cache tests/evals/spikes/combined_trial.py tests/evals/spikes/combined_native.py tests/evals/spikes/test_combined_trial.py
& '.venv/Scripts/ruff.exe' format --check tests/evals/spikes/combined_trial.py tests/evals/spikes/combined_native.py tests/evals/spikes/test_combined_trial.py
```

The local bootstrap directs temporary fixtures into the investigation allocation; no user documents/runtime outputs are reused. The allocation reserved32 launches up front and closed at **29/32 starts,466.578 active seconds**. Old combined-05/cadence-repair hashes verified unchanged. Final whitespace/link/source/privacy checks passed. The local budget receipt records the same results. No full-load Windows/model feasibility follows from these synthetic tests.

## Recommended next repair, not yet approved

Propose a minimal repair that coordinates all **owned** state reads/writes, including OCR polling, with the same serialization boundary, and avoids writing descendant state when no persisted value changes. Preserve atomic replacement, reservation-before-work, exact changed/overshoot counters, failure propagation, temporary-state startup refusal and all resource/timing controls. Same-destination direct writers must also be coordinated if present; unique temporary names alone would not establish serialized read/modify/write accounting. Do not add retries, alter permissions or waive failures.

This would reduce a proven owned-reader/writer overlap opportunity and redundant replacement work. It cannot guarantee protection from external readers or identify the historical locking handle. The exact source scope, regression tests and bounded execution allowance for that repair require a separate proposal/approval; no further native run is authorized. Investigation diagnostics/test/report commit also needs explicit approval. All old ledgers, seals, receipts and stopped commands remain closed and unchanged.
