# Combined-06 partial results and completed-reading gap stop

Recorded 2026-11-14 (Asia/Calcutta), after the user's disconnected run and verified teardown report. Only sanitized summary/meter fields, scalar aggregates and authored source were inspected. Raw answers, prompts, evidence, OCR, images, vectors, model logs and private-path receipts were not opened. Proposal documents are committed `a7732ab`; the sealed preparation source changes remain uncommitted, since their separate Git approval has not been received.

## Stop and cleanup

Four OCR deadline/memory controls passed. The run completed S01–S15 and began S16 before stopping in `S16-query-and-chat`. The supervisor reported `ResourceBoundary: Resource boundary: reading_gap`. The final summary contains the retained scalar timing packet:

| Timing measurement | Value | Hard limit |
|---|---|---|
| Loop-start gap | 109.3241 ms | 250 ms |
| Current collection duration | 204.7855 ms | 250 ms |
| Gap between completed resource collections | 287.7155 ms | 250 ms |

Only the completed-reading gap violated its guard, by37.7155ms. Individually acceptable loop-start/collection intervals do not guarantee a completed-reading gap below250ms when collection costs vary. This is the stricter repaired measurement, not a recurrence of the same historical loop-start metric. It does not identify the source of collection delay, justify changing the limit automatically or prove that the entire workload fits the16GB target.

No filesystem/state-write error was reported in this run. This does not prove such errors cannot recur, or identify the historical combined-05 reader. The timing packet contains no failed-reading memory values; do not invent them or substitute earlier samples as the failing measurement.

Cleanup verified true: zero active owned children, owned process reaped and port released, server exit125. Preserve the ledger at **64/160 reservations,62 API attempts,15 explicit native roots,11 extra native descendants,26 observed native processes**. Categories: preparation28,report8,controller3,OCR14,supervisor11,cleanup0. Embedding attempts24; response attempts16, completed15. Preserve S16 as attempted/incomplete and the remaining20 schedule slots as unattempted, not passes. Never retry/reset/reseal this allocation or old ones.

## Partial native evidence

All fifteen completed cases used `qwen2.5:1.5b-instruct-q4_K_M`; the Qwen3 candidate was not reached. All completed responses passed the automated schema/citation-scope check. Their factual and semantic citation support remain unreviewed.

| Completed condition | Cases | Mean recorded chat elapsed | Range |
|---|---|---|---|
| Baseline, no OCR | 6 | 10.253 s | 3.101–17.416 s |
| Tesserocr overlap | 6 | 9.285 s | 3.185–13.531 s |
| RapidOCR overlap | 3 | 11.733 s | 9.334–14.018 s |

All nine completed OCR/chat pairs had positive measured overlap and passed the frozen readable-fixture OCR gate. The smallest completed overlap was2.36596seconds. This is evidence of bounded native overlap for those completed pairs, not full matrix acceptance, broader scanned-PDF/table quality, rotated-text resolution, application integration or runtime adoption. The small/unbalanced completed subset and uncontrolled cache/order mean these elapsed times must not be treated as a causal performance comparison or complete cold/warm benchmark. No scores are assigned to missing attempts.

## Local semantic review and next decision

`data/t11/combined-06/review.html` exists. The user can open it locally to review the completed S01–S15 answers, refusals and citations against displayed frozen evidence/gold. Keep raw contents local; share only qualitative factual/citation findings or acceptance. S16 is incomplete and must not be scored as completed. No remote grader or automatic semantic-accuracy claim is used.

Before another native trial, review these partial answers and revisit the sampling contract using the measured completed-reading gap. Repeating unchanged settings can stop again. Any cadence/maximum-gap or monitor-architecture change needs a concrete separately approved package with its observation-latency tradeoff and unchanged kernel/resource/privacy/cleanup controls. No new policy, diagnostic workload, repair or native allocation is authorized here.

The user subsequently explicitly approved committing the nine combined-06 preparation/source/result files. No new code or limits changed during result review, and no trial was rerun. This Git approval does not approve another trial or timing change. Local semantic review, Stage1 acceptance, strict physical16GB feasibility and model/OCR adoption remain open.
