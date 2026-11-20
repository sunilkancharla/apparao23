# T09 - First offline run: package-name comparison defect

**Report date:** 2026-11-14 (Asia/Calcutta). The user ran the approved manual handoff while disconnected and reported `stopped_no_automatic_retry` with verified teardown. This report uses sanitized status/version metadata only; no OCR text/images were read or generated.

## Actual stop

The sole native trial command reached was offline `uv lock`, which completed successfully: 53 packages resolved, including the 16 exact OCR additions. Its receipt reports exit 0, one Job process, no remaining worker, and no timeout. No `uv sync` receipt exists. Resolution's printed "Added" lines describe the proposed lock additions, **not installed packages**.

The controller then raised `Baseline lock version changed`. Inspection identified a defect in its own name comparison: installed metadata called the existing distribution `pdfminer.six`, while lock entries use `pdfminer-six`. Both identify the baseline version `20260107`; the check handled underscores but not dots. That name alias incorrectly looked like a missing/changed pin. This is a runner defect, not an OCR engine failure or demonstrated dependency upgrade.

The runner restored its own project/lock edits; Git inspection before the repair showed no tracked dependency/config changes. Installation, fixture generation, scoring and all OCR/control workers were never reached. This is why the contact sheet does not exist. Summary: empty comparison/control lists, no active owned children, `teardown_verified=true`. Reconnection after that verified stop was permitted.

Ignored evidence remains under `data/t09-manual-ocr/manual-01/`: `summary.json`, `receipts/uv-lock.json`, original meter/events and prepared inputs. The meter recorded 104/240 reservations at the stopped native run. Subsequent read-only diagnosis/repair checks are separate closeout activity; do not treat that number as a newly available allocation or reset/reuse the stopped ledger.

## Repair and verification

Use one canonical comparison for lowercase names with any runs of dot/underscore/hyphen mapped to hyphen, consistently for installed metadata, reused packages, lock entries and expected OCR pins. Exact version checks are unchanged; canonicalization does not authorize a version substitution. Mismatch errors now identify the distribution and expected/observed version.

A new regression first failed for the missing helper, then **13 contract tests passed in 0.080 s** and Ruff passed for all OCR Python files. The regression covers the observed dot/hyphen alias and mixed case/repeated separators. No offline resolution, installation, rendering or OCR was rerun to test this fix. Unit-only repair receipts are `data/t09-manual-ocr/name-repair-01/`; the original run/summary was not overwritten.

**The old handoff is stopped and its sealed source no longer matches the corrected helper. Do not rerun it or replace its seal.** A fresh explicitly approved continuation must preserve the stopped run and carry forward prior resource accounting, create a new verified handoff and retain the original cached artifacts/versions/settings. No reset, extra download or automatic native retry. Source/result commit remains separately gated.
