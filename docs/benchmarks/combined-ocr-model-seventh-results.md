# Combined-07 completed — local semantic review accepted

## User review acceptance

After being asked to review all 36 answers and citations in the local combined-07 review page, the user confirmed: "i confirm they are good". Record this as qualitative acceptance of that completed evaluation set. No specific factual errors or unsupported citations were reported. This is user review evidence, not an independently graded accuracy score or a guarantee for other documents. T11-C7-6 is complete. Results were committed in `b225d57`; this acceptance note awaits separate commit approval. Runtime model/OCR adoption and remaining Stage 1 acceptance decisions remain separate. Earlier pending-review statements below describe the status before this confirmation.

## Outcome

The user ran the [approved package](../proposals/combined-ocr-model-seventh-run.md) disconnected and supplied its completion console output. Preparation and the approval-frequency rule were committed in `1428cfd`. Sanitized local summary/meter and scalar memory observations confirm `completed_pending_local_semantic_review_no_adoption`, all four deadline/memory controls checked, all36responses completed,44embedding attempts and no supervisor failure. Both chat candidates completed all three conditions. No new native execution was launched during this review.

All36responses passed automated schema/citation-scope checks. All24OCR/chat pairs had positive measured overlap and passed the frozen readable-fixture OCR quality gate; minimum overlap1.704970seconds. These checks do not establish semantic citation support, factual correctness, broader OCR fidelity or an implemented document-chat application. Raw answers/evidence/OCR/images/vectors/logs/private error-path receipts were not inspected by the assistant.

## Recorded chat elapsed time

| Model | Condition | Completed | Mean seconds | Range seconds |
|---|---|---:|---:|---|
| Qwen2.5 1.5B | Baseline | 6 | 8.757 | 2.300–14.883 |
| Qwen2.5 1.5B | Tesserocr | 6 | 7.907 | 3.413–11.074 |
| Qwen2.5 1.5B | RapidOCR | 6 | 8.535 | 2.983–12.589 |
| Qwen3 1.7B | Baseline | 6 | 12.841 | 2.702–23.692 |
| Qwen3 1.7B | Tesserocr | 6 | 11.827 | 2.966–21.471 |
| Qwen3 1.7B | RapidOCR | 6 | 12.718 | 2.956–21.272 |

Models are the exact pinned candidates/settings in the approved proposal. Fixed order, small sample size and uncontrolled caches prevent causal OCR-cost conclusions or controlled cold/warm claims. These are recorded chat durations, not full upload-to-answer latency. Quality remains a separate local review.

## Resources and monitoring

Across3879saved successful observations: minimum available physical RAM9.389GiB, maximum controller private memory44.617MiB, maximum sampled owned private memory2.604GiB and maximum job peak2.609GiB. Reported physical RAM19.911GiB exceeds the approved16-GB target; this successful run does not prove identical results on a physical16-GB machine. CPU-only/no dedicated GPU remains the target and no hardware requirement is amended.

| Timing measurement | Maximum milliseconds |
|---|---:|
| Loop-start gap | 218.225 |
| Completed-reading gap | 296.536 |
| Resource collection | 204.733 |
| TCP inspection | 41.881 |
| Storage scan | 114.771 |
| Full sampled iteration | 218.140 |

The saved completed-reading gap approached the approved300-ms ceiling and exceeded the historical250-ms policy. Completion supports feasibility under this run's policy and hardware; it does not guarantee scheduling or future completion. Observations are sequential software samples, not atomic snapshots or kernel real-time guarantees. No further limit change is proposed.

## Accounting, teardown and next gate

Preserve the final shared meter: **96/160process reservations,125/128API attempts,29native roots,13extra descendants,42observed native processes**. Categories: preparation36,report16,controller3,OCR28,supervisor13,cleanup0. All18prior record hashes were independently rechecked unchanged after completion. Do not mutate the completed meter, reset counters, reseal or rerun this allocation.

Teardown verified true; zero active owned children; process reaped and port released; exit code0. The console explicitly permitted reconnection. The current handoff is closed.

Next, the user should open `data/t11/combined-07/review.html` locally and review all36answers/refusals and their citations against displayed frozen evidence/gold. Report only qualitative factual errors, unsupported citations or acceptance; keep raw content local. Record the user's actual assessment before adoption decisions. Combined-06's separate partial review remains unrecorded. Runtime model/OCR selection, broader OCR/rotation/privacy acceptance, physical16-GB validation and Stage1 product implementation remain gated. Results-document commit approval is pending.
