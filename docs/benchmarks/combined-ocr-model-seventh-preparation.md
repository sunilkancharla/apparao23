# Combined-07 static preparation — 2026-11-14

The user approved the [exact combined-07 package](../proposals/combined-ocr-model-seventh-run.md) and its five proposal documents, committed as `1dddbcb`. This connected preparation performed no native OCR/model inference, API request, installation, download, rendering or new document processing. The Stage 1 Windows 11/16-GB/CPU-only target remains unchanged.

## Source and test-first evidence

Only `combined_trial.py` and `test_combined_trial.py` changed. The default, explicit CLI and lazy worker routing now permit `combined-07` only and refuse combined-01 through combined-06, missing/invalid IDs and traversal. The first full fake run failed with the expected two routing errors. After the minimal source change, the full combined and standalone OCR suites passed **61 tests in 1.589 seconds**. Five relevant files passed Ruff lint and the three maintained combined files passed formatting. The 300-ms constant/guards, native adapter, OCR code, sealed-source inventory, models, fixtures and dependencies did not change.

The fake bootstrap is stored only in ignored runtime data. It uses the reviewed standard-library Windows Job boundary: one process,512MiB, and temporary fixtures inside combined-07. Its tests include controlled owned file-sharing behavior; they do not import native OCR/model backends or prove native feasibility.

## Static seal and readiness

Cached preparation verified **158 sealed identities**: exact sources/contracts, standalone OCR tests, environment/lock files, Python interpreter/DLL, Ollama executable/runtime files, three pinned model manifests/layers, evaluated OCR wheels/assets, synthetic M02/M03/M04 fixtures and frozen T10/T11A inputs. PowerShell launcher syntax parsed successfully. No drift was accepted.

Eighteen prior records were linked and independently rehashed: combined-06's fifteen inherited records, its closed meter and seal, and the closed 300-ms policy budget. All matched their initial preparation hashes. Old meters, seals and receipts remain unchanged; combined-06's source mismatch after the committed policy change is historical and was not repaired or resealed.

Independent readiness verification rehashed the full seal, explicitly confirmed both combined and standalone OCR test files in it, checked `MONITOR_LIMIT_SECONDS == 0.300`, verified all prior hashes, and confirmed zero API attempts/native roots/native descendants with the offline epoch unset. `data/t11/combined-07/readiness.json` records **389.808 active preparation seconds and 44/160 reservations**:28 preparation and16 reporting. The 16 cleanup reservations remain protected.

## Handoff and remaining gates

The [combined-07 handoff](../proposals/combined-ocr-model-handoff.md) is ready for the already approved user-operated disconnected step. Save it locally, close new state-file watchers, disconnect every external link, run the exact combined-07 command once and remain disconnected through verified teardown and the explicit safe-to-reconnect message. The synthetic/frozen trial has no filesystem confinement. Never rerun/reset/reseal on a stop.

Preparation source/results commit approval remains separate. This readiness does not establish native completion at300ms, factual/citation correctness, physical16-GB performance, broader OCR/rotation acceptance, runtime model/OCR adoption, application functionality or Stage 1 completion. Combined-06's local S01–S15 semantic review remains pending independently.
