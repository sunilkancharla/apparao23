# Fake-only monitor cadence repair — 2026-11-14

The user approved the [32-start/ten-active-minute package](../proposals/combined-monitor-cadence-repair.md) and committing its five proposal documents, committed as `fd3361b`. Implementation is limited to the three existing combined evaluation scripts and supporting documentation. No OCR/model inference, API call, install, download, rendering or native trial ran.

## Result

The observer now waits only the remainder of its existing 100-ms target interval. Fake-clock integration verified 20-ms check work plus an 80-ms requested wait, and 150-ms check work with zero additional wait. Event-based cancellation is preserved, with no queued catch-up work. Desired cadence remains a software scheduling target, not a real-time guarantee.

Loop-start gaps retain their 250-ms hard stop. Separate checks now enforce the same ceiling for resource collection duration, gaps between completed collections, TCP inspection duration, storage scan duration and complete iteration duration. Exact equality passes; excess, negative/nonfinite intervals and unknown timing fields are refused. The first/direct startup sample has no earlier completed reading, so its reading_gap is zero; its own collection/iteration limits still apply.

Resource collection retains existing disconnection, deadline, descendant accounting and sequential OS memory checks. Its timestamps bracket that collection and associated preconditions, not an atomic memory snapshot. No existing network/storage/accounting check was removed or moved to a slower monitor. A known timing failure stops immediately instead of continuing remaining phases. The kernel memory/worker limits and all sampled memory thresholds are unchanged. No monitor thread, scheduling privilege, dependency or model setting was added.

Successful observations record collection timestamps, named phase/interval durations and the requested wait. Timing failures save whitelisted scalar interval measurements, their unchanged limits and available collection timestamps to the existing resource-failure receipt before owned shutdown. Memory failures retain their existing scalar packet. A receipt-write error still stops work and retains the packet in memory. Clock-invalid errors also fail closed; failed phases do not produce a completed observation. The ordinary summary still includes any retained resource packet after teardown.

Checks execute only when the controller runs; they cannot promise to interrupt a blocked system call precisely at 250 ms. Actual scan costs, CPU scheduling delays and future combined-model feasibility remain unmeasured.

## Verification

Test-first regressions initially failed (33 tests: three failing assertions and seven errors) against the old observer. After the minimum repair and lint corrections, **all 34 combined stdlib/fake contracts passed in 2.164 seconds**. Ruff lint passed and all three source files passed formatting checks.

Six new test methods cover work-aware waiting/cancellation, late collection/TCP/storage/combined iteration/reading gaps, delayed wake-up before another collection, exact/over-limit edges, direct startup, backwards/nonfinite time refusal, unknown-field refusal and receipt-write failure. Integration invokes the real sample/observer control flow with fake collection/TCP/storage/clock boundaries; no real timing sleeps or workload benchmark is used. Existing ownership, disconnection/deadline helpers, memory/quota, receipt privacy, ledger and teardown contracts remain covered by the full suite. These tests do not establish native Windows scheduling behavior under inference load.

```powershell
& 'F:/Python/Python314/python.exe' -I -S -B data/t11/monitor-cadence-repair-01/test_bootstrap.py
& '.venv/Scripts/ruff.exe' check --no-cache tests/evals/spikes/combined_trial.py tests/evals/spikes/combined_native.py tests/evals/spikes/test_combined_trial.py
& '.venv/Scripts/ruff.exe' format --check tests/evals/spikes/combined_trial.py tests/evals/spikes/combined_native.py tests/evals/spikes/test_combined_trial.py
```

The fresh ignored allocation reserved 32 starts up front and closed at **24/32 starts, 335.938 active seconds**, including the proposal Git commit, failing/passing test iterations, lint corrections and final checks. Prior combined-04 and resource-diagnostic closeout hashes verified unchanged. No stopped ledger/seal was modified. Source diff review confirmed unchanged resource caps and preservation of owned cleanup and failure propagation; final whitespace/document-link checks passed. The exact counts/time are also saved in the local allocation receipt.

## Handoff

The repair and results documentation need separate source-commit approval. No new native run identity or allocation exists, and all old commands remain closed. Combined-04 is permanently stopped at its historical 259.0546-ms interval; this repair cannot retrospectively validate it or identify combined-03's lost reading. Any subsequent disconnected combined trial needs a fresh separately approved package and seal. No application feature, runtime model/OCR adoption or Stage 1 acceptance is claimed.
