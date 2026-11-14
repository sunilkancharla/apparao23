**STOPPED — DO NOT RUN COMBINED-05 AGAIN.** Windows denied atomic state-file replacement during corpus embedding. [Stop evidence](../benchmarks/combined-ocr-model-fifth-stop.md) records verified teardown, four passed controls and zero scored chats. Preserve all partial/temporary state and do not reset/reseal/retry. Combined-01/02/03/04/05 remain closed. No new investigation, repair or native allocation is approved. Instructions below are historical.

# Approved combined OCR/model trial: local offline instructions

**Fresh run:** `combined-05`, under the [approved fresh continuation](combined-ocr-model-fifth-run.md). This is a synthetic/frozen-evidence feasibility test, not an application or engine adoption. Do not run combined-01, combined-02, combined-03, combined-04 or any old OCR/T10/T11A command; their ledgers may not be restarted. Existing models/packages are reused; missing/drifted assets stop without downloads.

## Before starting

Save these instructions locally. Keep project source/configuration/assets unchanged: the runner verifies its seal. Close heavy applications; at least 4 GiB available RAM is required. Use ordinary local PowerShell, without elevation, policy changes or edits to bypass stops.

This trial has **no filesystem confinement**: native packages have your Windows account's file access. It uses only the prior synthetic M02/M03/M04 images and the frozen T10/T11A benchmark packets, not additional samples/private documents. Their earlier local review remains applicable. It does not change image orientation or resolve the rotated-output discrepancy.

Disconnect Wi-Fi, unplug Ethernet, and disconnect tethering and every external link. Keep disconnected throughout. Codex may become unavailable; the command is standalone. If you want to inspect the reused images before running, the existing local contact sheet is `F:\document_assistant\data\t09-manual-ocr\manual-04\fixtures\contact-sheet.html` (only M02/M03/M04 enter this combined trial).

## One command after disconnecting

```powershell
& 'F:\document_assistant\data\t11\combined-05\run.ps1'
```

Type `OFFLINE` at the attestation prompt. **There is no new READY prompt**: sealed-asset verification, owned-server startup, controls and the fixed schedule proceed automatically. Large cached weights are rehashed first; this can be quiet for a while. Do not reconnect to ask for progress.

The schedule has 36 chat attempts, 44 embedding attempts, 24 overlapping OCR workers and four timeout/memory sentinels. It is bounded to 75 minutes of active execution, one chat request/one OCR worker, CPU only, with shared process/API/resource limits. A failed or non-overlapping pair stops without retry. Model loading/residency and actual combined Windows behavior remain unvalidated until this user-run phase.

Wait for final status, **`TEARDOWN VERIFIED: True`**, and the message saying you may reconnect. Keep external links disconnected even when the console is quiet, the initial controls end, or an error is printed. A return from the image viewer is not a completion signal.

After verified cleanup, reconnect and report the final status. The local sanitized report is:

```text
F:\document_assistant\data\t11\combined-05\summary.json
```

`completed_pending_local_semantic_review_no_adoption` means the fixed schedule finished; it is not proof of factual/citation correctness or adoption. `stopped_no_automatic_retry` means preserve all receipts and report the stop, without rerunning/resetting/resealing.

## If cleanup is uncertain

If there is no summary, teardown is false/uncertain, or the terminal hangs, remain disconnected. Use Ctrl+C to request owned cleanup. Verify that the trial controller, its direct OCR workers and its project-owned Ollama server/runners stopped. In Task Manager, use executable path/command line to distinguish the controller (`combined_trial.py`) and project Ollama (`F:\document_assistant\.venv\tools\ollama\0.40.16\ollama.exe`) from unrelated Python/Ollama programs. Never terminate another service merely because it uses port 11434.

Do not reconnect for remote help while owned trial work may still be active. Missing confirmation is not permission to reconnect; partial startup/cleanup failures are deliberately reported conservatively.

## Local answer review after completion

Open `F:\document_assistant\data\t11\combined-05\review.html` locally. Compare answers/refusals and each citation against the frozen case evidence and gold. Raw answers, prompts, OCR text/images and vectors remain local; do not paste them into Codex. Only sanitized status/metrics and your qualitative assessment should be shared. No cloud evaluator is used.

## Resource diagnostic repair — 2026-11-14

The original [diagnostic repair](../benchmarks/combined-resource-diagnostic.md) preserves failing scalar readings. The committed [cadence repair](../benchmarks/combined-monitor-cadence-repair.md) accounts for check work in the desired 100-ms cadence and enforces the same 250-ms ceiling for start/reading/collection/TCP/storage/iteration intervals. The combined-05 package has separate approval. A timing violation still stops execution; do not change the limit or retry if that occurs. Share only the sanitized summary after verified teardown and reconnection.
