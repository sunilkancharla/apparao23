# Manual offline OCR trial - local instructions

**STOP NOTICE:** The first run stopped before installation because of a package-name comparison defect. [Diagnosis and tested repair](../benchmarks/manual-ocr-first-stop.md). Its ledger is not reusable, and its source seal no longer matches the corrected helper. The command below is historical until an explicitly approved fresh handoff is prepared; do not rerun/reset/reseal `manual-01`.

**Prepared 2026-11-14 (Asia/Calcutta).** This is the user-operated portion of the approved [synthetic-only package](manual-disconnected-ocr-trial.md). Nothing has been installed/rendered/OCR-tested during connected preparation. The end-to-end offline path is unrun; contract tests, hashes and script syntax have been checked. A missing cache entry, Windows restriction or backend incompatibility stops the run, without downloads or retries.

## Before starting

Save/open these instructions locally. Keep the project files unchanged: the runner checks a source/config hash seal before installation. Use an ordinary local PowerShell terminal. Do not elevate it, change execution policy, edit the script to bypass a stop, or use a previously stopped ledger.

Close other heavy applications. This targets the approved CPU-only/16-GB machine and requires at least 4 GiB available RAM. Only authored synthetic files will be used; no `sample_files` or private documents. Native packages have the Windows account's file access: this trial has no filesystem confinement.

Disconnect Wi-Fi, unplug Ethernet and disconnect tethering/other external links. Codex may become unavailable while disconnected; the following command is standalone. It records local adapter/route metadata and asks for an `OFFLINE` attestation. An active gateway or uncertain disconnection is a stop. This is not proof against every possible network path; physically disconnect and keep it disconnected throughout.

## One command after disconnecting

```powershell
& 'F:\document_assistant\data\t09-manual-ocr\manual-01\run.ps1'
```

The runner uses the existing project environment and only verified cached wheels/assets. It performs offline resolution/install, preserves existing version pins, creates synthetic PDF/image fixtures, then pauses for your review. No pip fallback, package/model/font download, global install or network-setting change is permitted.

When prompted, open this **local** file in your browser or Explorer:

```text
F:\document_assistant\data\t09-manual-ocr\manual-01\fixtures\contact-sheet.html
```

Check each image against its displayed expected text. M08 (rotated) and M09 (low contrast) deliberately test degraded input. If the ordinary readable cases are wrong/unreadable or page mappings look incorrect, decline readiness; do not change the expected text. Type `READY` in the terminal only after review. That pause is recorded separately from timed execution.

The fixed schedule then compares two English OCR engines, at most 60 comparison workers and 20 negative controls. It prints status/paths rather than raw OCR text. There is no automatic retry. Initialization/render/OCR timings and memory samples are exploratory, not product guarantees. Direct base Python workers load only the project package directory under isolated/no-site startup; this avoids virtual-environment launcher descendants and does not install anything globally. Each direct trial worker consumes one actual root slot; the original allocation's additional wrapper slots are not silently charged twice.

## Completion or stop

Read the terminal and this local sanitized report:

```text
F:\document_assistant\data\t09-manual-ocr\manual-01\summary.json
```

Reconnect only after `teardown_verified` is `true` and `active_owned_children` is empty. `completed_pending_quality_review_no_adoption` means the schedule finished, not that an OCR engine passed all quality gates or is adopted. A stopped run is also valid evidence; keep its files/ledger and do not run again.

If there is no report, teardown is false/uncertain, or the terminal stops responding, **remain disconnected**. Use Ctrl+C to request cleanup, then verify the controller and its reported owned worker PIDs have ended before reconnecting. If necessary, use Windows Task Manager to end only those owned trial processes; do not terminate unrelated Python/Ollama/application processes. No safe teardown is claimed until you verify it. Do not reconnect just to obtain remote help while a worker might remain alive.

If offline installation fails, the runner restores only its own matching project/config edits when possible and reports incomplete provisioning; partial installed files may remain. Do not reconnect and import OCR packages, reinstall, reset the ledger or fetch missing dependencies as a repair. Report the sanitized stop status after workers are confirmed stopped.

After reconnecting, tell Codex that the run finished/stopped and whether teardown was verified. Codex can read sanitized status/counts/hashes locally; do not paste raw OCR text, image files or private documents into the conversation. Raw synthetic outputs remain in the ignored `raw` directory for your local review. Code/results commits and engine adoption retain their separate approval gates.
