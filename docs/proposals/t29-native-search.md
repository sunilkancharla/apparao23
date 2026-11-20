# T29-N1 — One disconnected native cosine bridge check

**Status: approved, prepared and source-sealed; not executed.** The user explicitly approved this exact T29-N1 package and the reviewed 14-file T29 source/status/handoff commit on 2026-11-20. No further project approval is needed for its one operator-disconnected run. Routine retrieval tests inject a cosine function and models; this package checks the exact selected DLL against the real application database/query path, with synthetic embeddings only. Its limits and stop conditions below remain unchanged; execution alone does not establish native acceptance or authorize T30.

## Fixed inputs and work

Use existing project `.venv` Python/SQLite, application/helper/configuration files in the [29-file source seal](t29-native-search-seal.json), and only the existing reviewed `.venv/.cache/sqlite-vec-review/part-d-01/` assets:

| Artifact | Bytes | SHA256 |
|---|---:|---|
| vec0.dll, sqlite-vec 0.1.9 Windows x64 | 289,280 | `fcf98662a7ad9dce394b96a88f91032047823831b951c76636787c312a6476e6` |
| LICENSE-MIT | 1,068 | `6ce72bbe12d975bd5286e5ab0a064c069693300c47bccbc57bec18485f1621ea` |
| LICENSE-APACHE | 10,931 | `a38070a94d4afd9cd710e3ce67bd1de78097cfe1784c1f0109ac95d3c196bfdc` |

Pinned companion notices and the earlier binary/source-provenance limitations remain unchanged. No installation, download, wrapper import, source build, model weights, Ollama process, OCR, private corpus or runtime adoption is included. Neither S1/S2 nor historical sqlite-vec trial allocations are reopened or resealed.

1. Parent creates fresh ignored `data/t29-native-01/`, prepays itself and one hidden project-Python worker and checks the source seal. Existing roots are refused; no reset/resume/retry is permitted.
2. A token-checked claim-once worker repeats source checks, creates a small real `UploadStore`, uploads/extracts/indexes only inline `Name,Units / North,42 / South,50`, and uses synthetic unit vectors for document/query embeddings.
3. Real `Retriever` loads the exact verified DLL once, verifies its version, and uses `vec_distance_cosine` over the selected binding. Assert two expected ranked records, distances approximately 0 and 1 (float32 comparison tolerance `1e-6`), two supplied evidence items and 768 dimensions. These checks establish arithmetic/bridge behavior, not semantic quality.
4. Confirm SQL `load_extension` remains denied and SQLite `integrity_check` returns `ok`. Close storage, exit/reap the worker and retain bounded scalar result, parent status, ledger and fixture scratch. No original/vector/engine dump is written to receipts.

## Separate finite allocation and stop conditions

Exactly **two allowed/prepaid Python starts**, no additional application-requested child processes, at most **one DLL load attempt**, two authored document vectors, one synthetic query and two native cosine evaluations in the positive query. Worker audit hooks refuse Python subprocess launches; they are not OS process-tree confinement. No HTTP/model request is made. Failed starts/loads keep their reservation.

The parent uses one **45-second shared deadline** from ledger creation, including source checks. It samples its owned worker's output/run-root growth every 50 ms, killing its worker on deadline, observed output above **65,536 bytes**, run-root sum above **2,000,000 bytes**, unsafe ancestry or more than **128 entries**. Allow at most two 5-second kill/wait attempts on exceptional cleanup. Individual JSON receipts are at most 16,384 bytes. Root/output limits are sampled and can observe an overshoot after it occurs. Code creation/DLL internals and filesystem check/use races are not isolated by this helper; preserve any failure rather than calling it a pass.

This small correctness check does not instrument strict aggregate RAM, CPU residency, network packets or all possible native descendants, and it does not validate the physical-16-GB/8-GiB application target. Native scratch is preserved and charged. The audited artifact and authored two-record scope limit the intended work; the explicit native-trust/resource limitations remain. This is not a performance benchmark or permission for a larger data set.

Stop on any asset/source/version drift, occupied/existing run root, unexpected launch/load, resource/output/deadline guard, malformed vector/distance, wrong rank/count, SQL load allowance, integrity failure, worker error or uncertain reaping. Preserve the root/receipts; do not weaken guards, retry, change assets or allocate another root without a new decision. Source and fake supervisor/gate checks passed during T29 routine verification; actual native execution remains unverified.

## Approved operator handoff — run once while disconnected

Read/save these instructions while connected. The package is approved. Disconnect external networking and run **once** locally:

```powershell
cd F:\document_assistant
.\.venv\Scripts\python.exe -m tests.evals.spikes.t29_native_search --execute-approved --offline-attested
```

The flags attest to approval and actual disconnection; they do not change network settings. No chat reply is needed while offline. The terminal reports completion. Inspect local `data/t29-native-01/result.json`, `ledger.json`, `parent.json` and `worker-output.txt`; a pre-worker failure can leave no result file. Do not publish the ledger's worker token. A failure/stop is not acceptance and must not be retried.

Once the command returns, reconnect and say **“T29-N1 finished; please inspect the results.”** I can read those local files directly. Review determines whether the T29 native bridge gate can close before T30; this command does not start chat implementation, approve an unreviewed Git commit or transition stages.
