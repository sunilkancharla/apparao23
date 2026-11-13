# Manual offline OCR trial: manual-04 instructions

Only manual-04 is current, under the [approved fresh package](manual-ocr-fourth-run.md). Do not rerun/reset/reseal manual-01, manual-02 or manual-03. Existing approved project packages are verified and reused; no downloads or global installations.

## Before starting

Save these instructions locally. Keep project files unchanged so the source/config seal stays valid. Use ordinary PowerShell; do not elevate, change execution policy or bypass checks. Close heavy applications; at least 4 GiB free RAM is required. Only synthetic files are used. This trial has no filesystem confinement: native packages have your Windows account's file access.

Disconnect Wi-Fi, unplug Ethernet, and disconnect tethering and all other external links. Keep them disconnected throughout. Codex may be unavailable offline; the runner is standalone. Adapter checks supplement your attestation and cannot prove every possible path is absent.

## Run after disconnecting

```powershell
& 'F:\document_assistant\data\t09-manual-ocr\manual-04\run.ps1'
```

1. Type `OFFLINE` at the disconnection prompt.
2. Wait for offline package verification and fixture creation.
3. At the review prompt, open `F:\document_assistant\data\t09-manual-ocr\manual-04\fixtures\contact-sheet.html` locally. Compare images with expected text. M08 (rotation) and M09 (low contrast) are deliberately degraded; decline readiness if ordinary readable cases or page mappings are wrong. Do not edit gold text.
4. Type `READY` in PowerShell after review. **Testing starts now and may be quiet. Keep all external links disconnected.** There are 60 comparisons and 20 negative controls, one worker at a time, with a 45-minute evaluation limit. Do not reconnect to ask for progress.
5. Wait for final status, `TEARDOWN VERIFIED: True`, and the message saying reconnection is safe. This is the safe reconnection point even if the status says stopped.
6. Reconnect and report the final status. Do not paste raw OCR text/images. The sanitized report is `F:\document_assistant\data\t09-manual-ocr\manual-04\summary.json`.

`completed_pending_quality_review_no_adoption` means the schedule finished, not that an engine passed or is adopted. `stopped_no_automatic_retry` means preserve the run and report it; do not restart.

## If cleanup is uncertain

If no report exists, teardown is false/uncertain or the terminal hangs, remain disconnected. Use Ctrl+C to request cleanup. Verify that the controller and owned workers have stopped before reconnecting. If needed, use Task Manager to stop only those processes, not unrelated Python/Ollama applications. Do not reconnect for remote help while trial workers may remain alive.

The report must show `teardown_verified: true` and an empty `active_owned_children` list. Missing confirmation is not permission to reconnect. Missing assets, changed versions or installation failures stop without downloads or automatic retries.
