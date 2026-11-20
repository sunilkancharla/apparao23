# T29-N1 — Successful native cosine bridge check

Date: 2026-11-20 (Asia/Calcutta). The operator completed the approved disconnected [T29-N1 package](../proposals/t29-native-search.md), reconnected and requested inspection. Source/handoff commit: `4a618c2`. This review reads existing receipts, sealed code, public asset hashes and file metadata only. It does not rerun the helper, open the fixture database, load a DLL/model, reset an allocation or start T30. Raw runtime receipts remain local/ignored; their worker token is excluded from this report.

## Outcome and acceptance trace

**T29-N1 passed.** `result.json` reports `package: T29-N1`, `status: passed`, `dimensions: 768`, `ranked: 2`, `evidence: 2`, `expected_cosines: true`, `sql_load_denied: true` and `integrity: ok`. `parent.json` agrees on `status: passed` and records `worker_reaped: true`. Worker output is empty. The final ledger records **two prepaid Python starts and one DLL load attempt**, matching the approved allocation.

| Required check | Receipt and matching sealed control flow |
|---|---|
| Exact selected native artifact | Successful loader verifies the 289,280-byte sqlite-vec 0.1.9 DLL and both companion notice sizes/hashes/ancestry, disables extension loading in `finally` and checks its reported version |
| Real stored-source query bridge | Upload, CSV extraction, T26 chunks and T28 canonical vector publication use the actual application/SQLite path; `Retriever` uses the actual `vec_distance_cosine` kernel on the selected source binding |
| Expected arithmetic/rank | Two ranked records and evidence entries; North/42 first, with native cosine distances checked against 0 and 1 using absolute tolerance `1e-6`; the receipt retains the successful flag, not raw distance samples |
| Pinned vector space | 768 dimensions, complete query/document metadata, finite normalized vectors and source/text identity checks through the implemented index/retrieval boundaries |
| Extension boundary | SQL `load_extension('unapproved')` was denied after the fixed-path loader; no unapproved path was loaded |
| Storage integrity/cleanup | `integrity_check` returned `ok`; the store connection closed in `finally`, worker exited and parent confirmed reaping |

The vectors were authored synthetic unit vectors for `Name,Units / North,42 / South,50` and the query `North units?`. **No Ollama or actual embedding-model inference ran.** This establishes the selected native scalar cosine bridge through the application, not semantic retrieval accuracy or a new combined real-model indexing/search result. The existing scope/mutation/packing tests supply separate mechanical boundary evidence.

All **29 source-seal files** and **three DLL/notice asset identities** were rechecked unchanged after execution. The five S1 and four S2 receipt hashes also remain unchanged. No source seal was regenerated. The compact receipt is evidence of successful sealed checks, not an independent native-call/process/network trace.

## Counters and preserved receipts

| Observation | Result | Approved boundary / interpretation |
|---|---:|---|
| Prepaid Python starts | 2 | Exactly parent plus claim-once worker; no refunds/retry |
| Recorded DLL load attempts | 1 | At most one |
| Ranked / supplied items | 2 / 2 | Authored two-record check |
| Worker output | 0 bytes | Observed cap 65,536 bytes |
| Current run-root files / entries | 8 / 11 | Sampled entry ceiling 128 |
| Current run-root bytes | 250,186 | Sampled byte ceiling 2,000,000; post-run inventory is not a peak measurement |
| Worker reaped | true | Successful supervisor completion |

No numeric elapsed time, memory peaks, packet trace or full descendant accounting was retained. The parent's passed status reflects its deadline/output/root guards, not a new performance or physical-16-GB acceptance result. The approved 45-second shared deadline, sampled resource controls and exceptional cleanup limits remain as documented; this review did not repeat them.

| Receipt | Bytes | SHA256 |
|---|---:|---|
| result.json | 158 | `53a1f950490d6c0f55410bdb57bba081b6682222771929f18e468241cd8c8790` |
| ledger.json | 99 | `d10fa1ae21c0f83a6eacb40ab95adbfc5b0349a054886ba636672ba0dd385d34` |
| parent.json | 43 | `27558fde8c66bfafee73c02e8c47145cd62ddaea8c267ba75c3a060743b0cdc8` |
| worker-output.txt | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |
| worker.claim | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

The root, ledger, claim, seal, fixture originals/database and scratch are preserved as a **completed, closed allocation**. Do not retry, reset, resume, delete or reseal it. No further disconnected run is needed for this bounded T29 native bridge gate.

## Task status and limits

T29 implementation, routine verification and this bounded native bridge verification are complete. Prior [routine evidence](t29-retrieval.md) remains **466 passed, one existing skip/warning; application/test/helper Ruff passed**. No application tests were rerun for this documentation-only receipt review; source/asset/receipt hash, local-link, whitespace and readable-diff checks are its verification.

Offline status is the operator's attestation, not independent network capture/confinement. The helper does not prove strict aggregate memory/CPU residency/native-descendant containment or hostile same-account isolation. Full-scale latency, exact input fit, real model relevance, saved-selection UI, later formats, semantic support/refusal and grounded-answer accuracy remain unverified. Native scalar-query correctness does not carry over the earlier `vec0 MATCH` performance measurements or establish whole-application/Stage 1 acceptance. No dependency/model/retention/readiness or stage change follows from this result.

Next is **T30 — generate and persist grounded chat exchanges**, including bounded current evidence/history, explicit insufficiency behavior, source-version publication checks, safe local-model errors and durable messages. The user subsequently approved this eight-document results/status commit and explicitly instructed proceeding to T30, 2026-11-20. Its new source commit/native trials retain separate gates. No code, checkpoint/session-summary or unrelated user file was changed by this review. Readable reviewed diff including this authored report: `data/reviews/t29-native-results.diff`.
