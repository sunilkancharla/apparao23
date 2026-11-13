**COMPLETED — do not run again.** Manual-04 finished with verified teardown. See [results and limitations](../benchmarks/manual-ocr-results.md). Instructions below describe the historical approved run.

# Approved manual-04 offline OCR continuation

2026-11-14 (Asia/Calcutta). The user explicitly approved committing the reviewed changes and preparing a fresh offline run with the same tests and a new 160-start allowance, after the [manual-03 enum failure and repair](../benchmarks/manual-ocr-third-stop.md).

Retain the [original package](manual-disconnected-ocr-trial.md) and [manual-03 limits](manual-ocr-third-run.md): 16 exact cached wheels/three English assets, English/CPU only, synthetic fixtures, 60 comparison and 20 negative-control roots, one worker, no filesystem confinement, disconnection throughout, no downloads/external requests, user documents, global changes or adoption. Manual-04 starts the full fixed schedule; prior partial results are not merged into a successful run.

Use fresh `data/t09-manual-ocr/manual-04/`. Its ledger links stopped manual-03's meter SHA/count (79/160). Preserve manual-01 (104/240), manual-02 (77/160), manual-03 (79/160) and the separate fake-only enum-repair evidence. Do not reset/reseal/rerun old ledgers. Routing adds only manual-04; strict configuration reuse still compares with manual-02's sealed proposed project and exact installed baseline plus approved OCR pins. Offline lock/sync verify existing packages; no installation/import of native OCR while connected.

The previously reviewed fix supplies RapidOCR's enum instances for language, OCR version, model type and CPU ONNX engine selection. No model/settings values, asset paths, thresholds, thread/GPU/download policies, gateway guards or schedule change. Fake tests verify enum identities; actual RapidOCR initialization/inference remains unvalidated until this offline run. Further compatibility failures remain possible.

## Shared budget and stops

160 total starts/attempts include all preparation, shells, tests, provisioning, fixtures, OCR/controls and closeout; protect 16 cleanup slots. Reserve 24 for preparation and 16 for source/docs/hash/Git closeout, conservatively 40 before handoff. Expected offline shell/controller (3), uv (8), fixtures (1) and comparisons/controls (80) consume 92, leaving 28 including the protected 16. Unexpected descendants are charged and fail the existing strict guard. No retries or budget reset.

Retain 20-minute provisioning, 45-minute evaluation excluding logged image-review waiting, 30-second OCR worker, 1.5 GiB worker Job cap, 512 MiB monitored controller stop, at least 4 GiB available RAM, 300 DPI/12 MP per page, 24 fixture files/160 MiB, 128 MiB raw output, and 1 GiB added install/cache/fixture storage. Reconnection, asset/version/hash/config mismatch, backend errors, resource/time/accounting violation or uncertain cleanup stops without automatic retry.

## Verification and handoff

Manual-04 selection contract failed before routing changes; all 15 stdlib/fake tests then passed in 0.052 s. Ruff passed; PowerShell syntax parsed. Static artifact/baseline verification generated a fresh source/config seal, without importing OCR/image engines or rendering. The source commit includes the already approved offline-generated evaluation group/lockfile and reviewed runner/docs only; runtime outputs/packages are excluded.

Use the [current instructions](manual-ocr-handoff.md). Stay disconnected after READY until teardown is verified and the runner says reconnection is safe. No automated native execution by Codex. Raw OCR text/images stay local; only sanitized status/metrics are reviewed after reconnection. Completion does not adopt an engine or approve later stages.
