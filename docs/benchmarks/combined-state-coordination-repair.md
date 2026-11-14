# Synthetic state coordination repair — 2026-11-14

The user approved the [40-start/15-active-minute package](../proposals/combined-state-coordination-repair.md) and committing five proposal documents, committed as `2a65871`. No inference backend, model server, API request, installation, download, rendering, permission change or stopped trial ran.

## Implemented behavior

Core `write_json` acquires the existing reentrant state lock around the unchanged temporary-file write and single atomic replacement. Nested ledger writes remain reentrant. Temporary naming, safe diagnostics, exception propagation and unfinished-state startup refusal remain intact. No retries or in-place fallback were added.

The reused OCR runner has a small `read_global_meter` hook whose standalone default retains the previous JSON read/parse and error behavior. The actual polling loop calls it. The combined runner factory overrides the hook with the active `Ledger.read`, so owned meter reads close their handles under the same lock as replacement. Existing storage/failure callbacks remain. The lock covers short file access/update, not worker launch/execution, sleeps, HTTP or inference. The OCR module does not import the combined controller.

`observe_native` skips replacement only when cumulative observed/extra counts and corresponding persisted counters remain unchanged. Increased observed high-water counts still persist even when no extra descendant is charged. Newly observed overshoot persists before refusal; unchanged already-over-limit state is refused without rewriting. Failed changed updates preserve the last good destination and propagate; failed reservations/API writes still start no simulated work.

This coordinates owned threads, not unrelated processes. Existing uncoordinated held-reader controls still report Windows5/errno13 and closing the fixture handle restores replacement. The historical locking handle remains unidentified. All timing, memory/disk/process/API, disconnection, ownership and cleanup controls remain unchanged.

## Verification

Test-first execution initially failed59tests with3failures/4errors against old behavior. Final combined and standalone OCR suites passed **60 tests in2.534seconds** (44combined,16OCR). All five changed source/test files passed Ruff lint. The maintained combined scripts passed formatting; legacy OCR files received only the narrow hook/default test edits, without unrelated formatting. Their pre-edit lint baseline was0 and remains clean.

Event-coordinated tests hold a real synthetic file read or first writer while a second writer attempts the same actual lock. They assert the second has not completed until release, then verify complete valid final JSON and terminated threads. Same- and distinct-destination writers are covered. This exercises actual file-operation ordering rather than only lock-call counts. Existing external-reader denial controls remain separate negative cases.

Tests also cover no-op observations with replacement deliberately denied; changed/high-water-only updates; newly observed and unchanged overshoot; changed-update denial preserving old state and refusing restart; existing reservation/API refusal; actual reused OCR polling invoking the hook and retaining shared deadline expiry; combined factory binding to ledger reads; and standalone valid/invalid/missing-file reads. The old no-op characterization expectation changed under explicit approved scope; its investigation report remains historical evidence. Worker execution is faked; no native OCR backend is imported or run.

```powershell
& 'F:/Python/Python314/python.exe' -I -S -B data/t11/state-coordination-repair-01/test_bootstrap.py
& '.venv/Scripts/ruff.exe' check --no-cache tests/evals/spikes/combined_trial.py tests/evals/spikes/combined_native.py tests/evals/spikes/test_combined_trial.py tests/evals/spikes/ocr_trial.py tests/evals/spikes/test_ocr_trial.py
& '.venv/Scripts/ruff.exe' format --check tests/evals/spikes/combined_trial.py tests/evals/spikes/combined_native.py tests/evals/spikes/test_combined_trial.py
```

Source review confirms five changed source/test files with the declared lock/hook/no-op behavior. Fixtures stay in the ignored allocation; handles close and test threads join. One shared budget covered inspection, approved proposal Git, red/green/negative runs, regression additions, lint and reporting. It closed at **32/40 starts,604.971 active seconds**. Old combined-05/investigation hashes verified unchanged; final links/whitespace passed. Exact results are saved in the local allocation receipt. No old ledger was mutated or trial resealed.

## Remaining gate

Repair source/results commit needs explicit approval. A native trial would need a fresh reviewed package, allocation, source/asset seal and disconnected handoff; none was prepared. This repair does not retrospectively validate old runs, eliminate external locking risks or prove native model feasibility, semantic accuracy, runtime adoption or Stage1 completion. Never rerun combined-05 or earlier commands.
