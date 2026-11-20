# T30-N1 — Successful Qwen generation and saved-exchange check

Date: 2026-11-20 (Asia/Calcutta). The operator completed the approved disconnected [T30-N1 package](../proposals/t30-model-smoke.md), reconnected and requested inspection. Source/handoff commit: `07a7d27`. This review reads existing receipts, sealed code, public executable/manifest hashes and file metadata only. No helper/model/native call, fixture-database reopen, allocation reset or T31 implementation was performed during review. Raw receipts and fixture data remain local/ignored; the ledger's worker token is excluded from this report.

## Outcome and acceptance trace

**T30-N1 passed.** `result.json` records `package: T30-N1`, `status: passed`, `answer_contains_42: true`, `citations_allowlisted: true`, `restart_persisted: true` and `port_released: true`. The 57-byte worker output agrees on package/status with `code: null`. The ledger records `stopped: false`; no `parent-stop.json` exists, matching the supervisor's success path. This helper does not retain a separate successful parent/reaping receipt.

| Required check | Receipt and matching sealed control flow |
|---|---|
| Selected runtime/model | Ollama 0.40.16 executable and the selected Qwen manifest/blobs pass full identity/size/ancestry checks before launch and after generation; chat client checks version/tags/model identity before and after its request |
| Actual generation boundary | One owned chat-purpose Ollama tree, actual `ChatService`/`ChatModel`, fixed loopback transport and CPU/four-thread/2048-context/64-batch request profile; no unowned service adoption |
| Complete typed result | JSON mode, `stream=false`, `keep_alive=0`, prediction limit 192; valid claims, complete `done/stop` termination and at most 192 observed generated tokens are required before publication |
| Authored answer assertion | Status must be `answered`; at least one claim contains standalone 42, and claims can cite only supplied `ev_native`. The typed validator also requires citations for answered claims. No raw answer or exact token count is retained in the scalar receipts |
| Current source/publication | Actual CSV upload, extraction, indexing metadata and source-original rechecks; selection/reference/current extraction/index identity checks precede complete exchange publication |
| Cleanup | Publication follows owned-runtime teardown; sealed Windows Job close requires verified cleanup. The helper then successfully reserves/releases the private port, reported as `port_released: true` |
| Persistence | The worker closes and reopens `UploadStore`, then requires the scoped saved result to equal the original saved exchange exactly, reported as `restart_persisted: true`. This is a store/connection reopen in one worker, separate from routine process-exit recovery tests |

The only authored document is `Name,Units / North,42 / South,50`, and the question is `How many North units?`. **Index embeddings and retrieval are fixture seams; no Nomic inference or sqlite-vec DLL load occurs in this package.** The fixture retriever delegates source rechecks to the actual retrieval implementation. This establishes the actual Qwen structured-generation/publication/persistence bridge with known supplied evidence, not combined real-model semantic search or general answer accuracy.

All **35 sealed source files** match by membership and SHA256. Seal SHA256: `cc5c99f0a6c63697b64a43f198153b7373768acebfe17e29602375757e8f83f9`. Public asset metadata rechecked during review:

| Asset | Bytes | SHA256 |
|---|---:|---|
| Ollama 0.40.16 executable | 41,268,104 | `4ccefcbfecc50fb6526471adabbc20869dd614e29e351120b15083cb174b0b8a` |
| `qwen2.5:1.5b-instruct-q4_K_M` installed v2 manifest | 857 | `65ec06548149b04c096a120e4a6da9d4017ea809c91734ea5631e89f96ddc57b` |

The successful sealed preflight/postflight covers model blobs; this review did not rehash weights or start inference. All **14 prior S1/S2/T29-N1 receipt hashes** remain unchanged. No source seal was regenerated.

## Counters and preserved receipts

| Observation | Result | Approved boundary / interpretation |
|---|---:|---|
| Charged starts | 18 | Two prepaid Python starts plus 16 prepaid native starts; ceiling 64, no refund/retry |
| Positive-tree cumulative starts | 10 | Sampled job accounting, ceiling 16; no cancellation tree or second question |
| HTTP attempts | 5 | Ceiling 12; normal version/tags checks twice and one chat request |
| Charged retained bytes | 76,825 | Ceiling 2,000,000, including prepaid 65,536-byte worker-output reservation and conservative ledger rewrites |
| Worker output | 57 bytes | Retained cap 65,536 bytes |
| Current run-root files / entries | 9 / 18 | Sampled entry ceiling 10,000 |
| Current run-root bytes | 283,545 | Sampled ceiling 64,000,000; post-run inventory is not a peak |
| Current private-home bytes / entries | 468 / 7 | Sampled ceilings 16,000,000 / 4,096; not peak observations |
| Stopped | false | No failure code or parent-stop receipt |

The allocation retains its original 180-second shared parent deadline, 84-second session boundary, cooperative 90-second answer timeout and exceptional cleanup limits. No numeric elapsed duration, memory peak, token count, per-request timing or packet capture was retained. `deadline` is an absolute monotonic boundary, not elapsed time. A pass means the sealed success path did not reject its sampled controls; it is not a new latency or physical-16-GB resource acceptance result. Ten cumulative native starts does not report the peak active count.

| Receipt | Bytes | SHA256 |
|---|---:|---|
| result.json | 150 | `1d6365054cd5b75d9cd97a46b31fdba6c8d27408a4196078bc8240aa29e95536` |
| ledger.json | 216 | `2200cecb57a42667706dcde705b664a84d9cf9e837dbcd53dadae9f1b3ee8372` |
| worker-output.txt | 57 | `9d10729245b09a969b7be814102950b03c8b550de28108e019f52a54a53b5cd4` |
| worker.claim | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

Preserve `data/t30-model-01/`, its ledger/claim, source seal, original/normalized fixture data, database and staging artifacts as a **completed, closed allocation**. Do not retry, reset, resume, delete or reseal it. No further disconnected run is required for this bounded gate.

## Review, task status and limits

Receipt consistency, source membership/hashes, public executable/manifest hashes, prior-receipt preservation and sealed acceptance/teardown/persistence paths were reviewed; no required finding remains for this bounded result. T30 implementation, routine verification and this native generation/persistence check are complete. Separate [routine evidence](t30-grounded-chat.md) remains **506 passed, one existing skip/warning; scoped Ruff passed**, including a caught/restored publication mutation and two process-exit recovery checks. Those tests were not rerun for this documentation-only receipt review. All 592 local file-link targets across the eight affected documents resolve; whitespace and readable-diff checks accompany the hashes above. The private worker token is absent from all eight documents; the Git index remains empty pending commit approval.

Offline status is the operator's attestation, not independent network capture/confinement. Requested CPU options and sampled guards do not prove strict aggregate RAM, GPU residency or hostile same-account/native-code isolation; outer-parent private memory is outside job accounting. Exact input fit, model prompt-injection resistance, quotation/calculation support, independent meaning verification, general refusal/ambiguity/multi-file quality, full-scale/warm latency, combined real Nomic/sqlite-vec/Qwen retrieval, live historical-source availability, browser readiness and Stage 1 acceptance remain unverified. One correct supplied value and valid citation IDs do not validate every generated claim.

Next is **T31 — validate citations and resolve safe passage previews**: scope saved citation IDs to their supplied evidence, derive filenames/locations/quotations from current stored provenance, and expose bounded escaped previews with honest unavailable/coarse-location behavior. Follow its existing T30/T25 prerequisites and approved lifecycle constraints. The user subsequently approved this **eight-document results/status commit** and explicitly instructed proceeding to T31, 2026-11-20. Its new source commit retains a separate gate. No dependency/model/retention/runtime-adoption/readiness or stage change is made. No code, SPEC, checkpoint/session-summary or unrelated user file was edited by this review. Readable reviewed diff including this report: `data/reviews/t30-native-results.diff`; the approval record is the subsequent closeout update.
