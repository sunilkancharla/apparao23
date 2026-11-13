**STOPPED — do not run manual-03 again.** Its first RapidOCR worker failed configuration. See [stop and repair evidence](../benchmarks/manual-ocr-third-stop.md). The instructions below are historical; no fresh native continuation is approved.

# Approved fresh manual-03 OCR handoff

Approved by the user's "yes please" after the explicit proposal of a fresh 160-process-start allowance including preparation. Date: 2026-11-14 (Asia/Calcutta). Git commit and runtime adoption remain separate gates.

## Scope

Retain the [original package](manual-disconnected-ocr-trial.md) and [continuation limits](manual-ocr-continuation.md): exact cached 16 wheels/three English assets, CPU-only execution, synthetic inputs only, no filesystem confinement, disconnection throughout, no external requests/downloads, one worker, 60 comparison roots and 20 negative controls. No user documents, new dependencies, global changes, engine adoption or Windows isolation investigation.

Use fresh `data/t09-manual-ocr/manual-03/` with a new ledger and seal. Link manual-02's meter hash and 77 reservations, preserving both stopped runs. Manual-02 successfully installed the packages before the [reconnection stop](../benchmarks/manual-ocr-second-stop.md). Preparation requires the current project to equal manual-02's sealed proposed configuration and installed metadata to equal its prior baseline plus exact approved OCR versions. Any mismatch stops. Reuse that configuration without duplicate groups; offline lock/sync still validate it before fresh fixtures and the full schedule. No connected native package imports or installation.

Runner changes: explicit manual-03 routing/approval checking, strict reuse of the previously installed configuration, and a stay-disconnected message after READY. Gateway detection and existing stop conditions are unchanged.

## Shared allocation and limits

160 total process starts/attempts cover preparation, fake tests, shells, provisioning, fixtures, comparisons, controls and closeout. Protect 16 closeout slots. Conservative preparation reservations total 36 (initial 24 plus 12 additional test/lint/static-closeout slots from wrapper/reserve allowances). Expected offline shell/controller (3), uv reservations (8), fixture worker (1), and 80 trial/control roots total 92, leaving 32 including the protected 16. No raised ceiling, automatic retry or ledger reset. Unexpected descendants remain charged and fail the existing guard.

Retain 20-minute provisioning, 45-minute evaluation excluding recorded image-review waiting, 30 seconds per OCR worker, 1.5 GiB worker cap, monitored 512 MiB controller stop, at least 4 GiB available RAM, 300 DPI/12 MP per page, 24 fixture files/160 MiB, 128 MiB raw output and 1 GiB added installation/cache/fixture storage. Reconnection, version/hash mismatch, backend errors, resource/time/accounting violations or uncertain cleanup stop the run.

## Preparation evidence

New selection/reuse contracts initially failed. Two test-fixture portability corrections (Windows separators and file-byte hashing) preceded 15 passing tests in 0.071 s. Ruff flagged import order, then passed after correction. PowerShell syntax parsed. Standard-library preparation rehashed cached artifacts/installed metadata and created the seal. No connected OCR/image engine or renderer ran.

Follow [current local instructions](manual-ocr-handoff.md). Stay disconnected after READY until teardown is verified. Source/config changes invalidate the seal. Raw output stays local; review only sanitized status/metrics after reconnection. Completion is not engine adoption.
