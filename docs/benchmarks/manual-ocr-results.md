# Manual-04: completed offline synthetic OCR comparison

**Recorded:** 2026-11-14 (Asia/Calcutta). **Source commit:** `0797fe5`. **Package:** [approved manual-04 continuation](../proposals/manual-ocr-fourth-run.md). Only sanitized local summary/receipts and the user's terminal output were reviewed; raw OCR text/images stayed local. No native job was rerun for this report.

## Execution and cleanup

The user disconnected, attested OFFLINE, reviewed the generated synthetic contact sheet and typed READY. The schedule completed with status `completed_pending_quality_review_no_adoption`: 60 unique comparison tuples (30 per engine), all 20 controls checked (10 per engine), verified teardown and no active owned children. Offline resolution checked the existing 52 installed packages; no new installation/download is shown by the run. RapidOCR's repaired enum configuration initialized and ran successfully with the approved cached detection/recognition models; the adapter's provider checks required CPUExecutionProvider.

The shared ledger reserved 132/160 on native completion, including the conservative preparation/closeout reservations. Four initial sanitized-result/documentation slots and eight subsequent approved result-recheck/Git closeout slots bring reservations to 144/160, preserving the 16 cleanup slots. This is a completed schedule, not permission to rerun its ledger. Prior stopped epochs remain separate and unchanged; their partial results are not counted here.

## Measurements

| Measure | Tesserocr 2.13.0 | RapidOCR 3.10.0 |
|---|---:|---:|
| Comparisons | 30 | 30 |
| Readable-case gate passes | 24/24 | 24/24 |
| Mean readable-case character / word error | 0 / 0 | 0 / 0 |
| Mean comparison worker time | 1.02 s | 5.21 s |
| Maximum comparison worker time | 1.86 s | 5.71 s |
| Maximum sampled worker private memory | 193.82 MiB | 543.92 MiB |
| Checked negative controls | 10/10 | 10/10 |

Readable cases are eight synthetic case definitions repeated three times, not 24 independent documents. Several reuse the same short passages across native, scanned, mixed and cropped pages. The readable gate requires character error <=0.05, word error <=0.10 and exact selected numeric facts. Zero observed errors on this narrow set is not general document accuracy.

The deliberately 90-degree-rotated case M08 did not meet text-matching expectations: mean character error 0.9524 for Tesserocr and 1.0 for RapidOCR; word error 1.0 for both. The low-contrast case M09 had zero character/word error for both. These degraded cases are exploratory and excluded from the readable gate; readable pass counts must not hide the rotation failure.

Timing covers a fresh worker per comparison, including startup/import/model initialization. OS caches may be warm. Sampled process-private memory is not combined system peak, application latency or proof of fitting all future workloads in 16 GB. Native Tesseract/Leptonica versions are checked in the adapter (5.5.4/1.87.0). Exact wheel/asset identities remain in the approved inventory and local prepared-state/seal.

## Controls and limitations

Checked cases cover missing/wrong assets, truncated/empty images, unreadable input, pixel limits, timeout, memory, backend refusal and remote-input refusal. Timeout/memory controls use dedicated sentinels; backend failure is injected. These are not comprehensive native fault/fuzz tests. The empty-detection warning near the end of the user's log is consistent with the unreadable-input control, which was checked successfully; it is not a failed overall run.

The run used manual disconnection plus repeated local adapter checks, without filesystem confinement or an independently enforced network boundary. It demonstrates this disconnected synthetic trial, not end-to-end offline application acceptance. Real scanned PDFs, varied layouts/fonts/noise, tables, reliable regions/confidence, automatic rotation, chart understanding and combined OCR/Ollama/application pressure remain unproven. No user document or cloud evaluation was used.

## Recommendation and next gate

Tesserocr is the leading candidate from this narrow comparison because readable results matched while worker time and sampled memory were lower. Do not adopt it automatically: rotation handling and representative quality coverage need an explicit reviewed decision. T09 retains open acceptance items; the next combined-pressure work must use a separately approved T11 package, with fixed models/fixtures/budgets and no silent runtime adoption. No new model downloads or native runs are authorized by this report. The user explicitly approved committing this results closeout on 2026-11-14. This does not approve executing the next evaluation.

## Rotated-case review follow-up

The user commented that the rotated text results looked good. Preserve that qualitative assessment separately from automated measurements. Rechecking all six M08 tuples confirms Tesserocr CER 0.95238/WER 1.0 and RapidOCR CER 1.0/WER 1.0, with numeric-fact matching false throughout. Source inspection confirms M08 rotates M03 by 90 degrees and retains its original gold; the scoring code compares recognized text against that gold with whitespace normalization only. The contact sheet displays input images and expected text, not recognized outputs. No raw OCR text/image was inspected by Codex. The visual-versus-scoring discrepancy remains open for local output review; do not change gold, scores, orientation settings or acceptance requirements based on either observation alone.
