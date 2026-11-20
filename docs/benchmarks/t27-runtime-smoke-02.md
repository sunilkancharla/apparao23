# T27-S2 — Successful owned-runtime and embedding smoke

Date: 2026-11-20 (Asia/Calcutta). The operator ran the one approved disconnected [S2 command](../proposals/t27-runtime-smoke-02.md), reconnected and requested inspection. This review reads existing receipts and sealed source only; it starts no service, model, test or trial. The R1 routine allocation and closed S1 allocation are not reopened. Raw receipts remain local and ignored; their worker correlation token is excluded here.

## Result and acceptance trace

**S2 passed.** `data/t27-runtime-smoke-02/result.json` and `worker-output.txt` agree on `status: passed`; the final ledger has `stopped: false`. No `parent-stop.json` exists. All 25 source files still match the S2 seal, including the application, smoke helper, dependency manifest and lockfile. All five historical S1 receipt hashes remain unchanged.

| Required observation | Recorded evidence and sealed control flow |
|---|---|
| Approved runtime/model assets | Successful sessions require the approved Ollama 0.40.16 executable and Nomic v1.5 manifest plus config/layer hash/size/ancestry checks; preflight runs before each session and again before returning success |
| Real document/query embeddings | Result records `documents: 2`, `queries: 1`; the helper requires two complete 768-dimensional finite normalized document vectors and one query vector, with matching embedding space identity |
| Owned process/listener | Real `WindowsJob` membership/liveness and exact loopback root-listener checks precede session yield and guard client exchanges; they were not replaced by test doubles in this command |
| Positive teardown | `positive_port_released: true`; session close requires root reaping and zero active job members before releasing owned handles, followed by a free-port bind check and released work slot |
| Cancellation teardown | `cancellation_checked: true`, `cancel_port_released: true`; the second session deliberately raises cancellation after listener admission and must pass the same cleanup/slot checks |
| Source and allocation | Fresh fixed S2 root, distinct ledger/package and claim-once worker; final charges below approved boundaries, no stop/failure receipt |

Embedding `space_id`: `840d5ba53dc238d6ccb722c4d6f15c9698172204d91b2a0ec652169804dbcc25`. This identifies the approved model/settings/prefix/dimension space; it is not a quality score. Only authored CSV rows `Name,Units / North,42 / South,50` and the query `How many North units?` were supplied. No answer was generated or judged.

The success receipt is a compact result of the sealed checks, not an independent process trace. No raw vectors, document contents, process IDs or numeric memory peaks were retained in these receipts. The absence of `parent-stop.json` is expected on successful supervisor completion, rather than a separate teardown certificate. A read-only listener snapshot during review also found **no listener on port 11435**; it does not reconstruct historical process membership.

## Counters and preserved receipts

| Meter | Final observation | Approved maximum / meaning |
|---|---:|---|
| Charged starts | 34 | 64; two Python starts plus two prepaid 16-start native trees, with no refund |
| Native cumulative starts | Positive 12; cancellation 3 | 16 per tree sampled; includes exited descendants |
| HTTP attempts | 10 | 12 across the package |
| Retained charged bytes | 85,878 | 2,000,000, including reservations and repeated ledger writes |
| Current run-root files/bytes | 10 / 157,356 | 64,000,000 observed byte ceiling; post-run inventory is not a peak measurement |
| Stopped | false | No recorded budget/resource/deadline stop |

The result embeds an earlier ledger snapshot with 84,140 retained charged bytes; the final `ledger.json` is authoritative after result publication and its subsequent ledger write. Starts/calls/native observations agree between the two snapshots. The final total is not reduced to the sum of current file lengths because reservations and repeated writes stay charged. The worker output is 57 bytes, within its 65,536-byte reservation.

| Receipt | Bytes | SHA256 |
|---|---:|---|
| result.json | 484 | `994908cd105cef1008a099d252d03ca73ba9f2ca74f66f10e13f042e8cdad6b5` |
| ledger.json | 230 | `ef8057d25111505429a9824e2c7c6554c2b9d1060435eeb0c68d187f53db0c59` |
| worker-output.txt | 57 | `f9bf5a81a14905e2a493cd4eb3214d1470eb34f7d79de8dcefd2f8d6399946ab` |
| worker.claim | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` |

The S2 root, ledger, source seal and scratch are now preserved as a completed allocation. Do not reset, delete, resume, retry or reseal this run. No additional offline run is needed for this T27 smoke gate.

## Limits and next task

This demonstrates the bounded T27 native Windows ownership/embedding/cancellation path with the selected assets on this machine during the operator-attested disconnected run. **T27 implementation and this integration verification are complete**, with reviewed source/results awaiting the separate Git decision. The earlier [387 passing routine tests, one skip and warning, and Ruff checks](t27-preflight-correction.md) remain the applicable regression evidence; this read-only results review did not rerun them or consume another native allocation.

It does not establish retrieval relevance, answer grounding, in-flight inference cancellation, restart/index persistence, warm-answer latency, broad format/OCR behavior or Stage 1 acceptance. Cancellation here occurs after listener admission, without model input in that session. CPU options are requested controls, not independent GPU-residency proof. Numeric peak memory/available-memory/cadence samples and elapsed-time benchmarks were not persisted; passing sampled guards is not strict aggregate-memory or physical-16-GB proof. The outer supervisor's private memory remains excluded from job accounting. Offline status is operator attestation, not an independent network capture or firewall confinement claim. Same-account/native-trust and exact input-fit limitations remain unchanged.

Next is **T28: persist an idempotent versioned local index**, covering stable chunk/vector identity, duplicate reuse without scope leakage, version changes, interrupted publication and restart recovery. T28 is unstarted; CP10 stays open through T28. This review introduces no new model/dependency, runtime autostart, browser readiness, retention policy or stage transition. The proposed reviewed source/results commit includes the repair/handoff and this report, with no runtime data or unrelated user files. Readable combined diff: `data/reviews/t27-s2-closeout.diff`.
