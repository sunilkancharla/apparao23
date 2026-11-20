# T29 — Scoped retrieval, native bridge preparation and routine evidence

Date: 2026-11-20 (Asia/Calcutta). The user approved the T28 commit, accepted CP10 and explicitly instructed proceeding to T29; T28 is committed as `e9d5580`. T29 implementation followed the repository's incremental/TDD/security/review/documentation workflows. No model, sqlite-vec DLL, OCR, download or install was executed during the routine implementation below. Source/handoff was committed as `4a618c2`; the operator subsequently completed the separately approved [T29-N1 package](../proposals/t29-native-search.md), and [native bridge verification passed](t29-native-search.md). T30 remains unstarted.

## Implemented boundary and behavior

`Retriever(store).retrieve(conversation, references, question, session_factory=runtime.session)` is a trusted internal API over the same store's owned runtime. It accepts an explicit list/tuple of at most ten distinct selected references and a nonblank question of at most 512 UTF-8 bytes. Empty selection returns `no_evidence` without model/native calls. `None` returns `SELECTION_REQUIRED`: saved selection is not implemented here, so omission cannot broaden scope. Conversation and reference membership are resolved server-side; an unknown/foreign reference rejects the request before embedding or native evaluation.

Known unavailable, unextracted/unindexed or unsupported selected sources are excluded with fixed blocked-source codes. Current complete extraction/index identities and original bytes are checked before retrieval. Source snapshots retain reference, document, content, extraction, generation and binding identity. A source/reference/version change during query generation or ranking returns `SOURCE_CHANGED` with no retrieval result. Final answer publication still needs T30's coordinated current-version check; these snapshots are observations, not authorization tokens or an atomic saved-answer transaction.

The owned runtime creates the local query embedding in the pinned Nomic space. Query batches must match model/digest/runtime/dimensions/normalization/space, query ID/text hash, count and finite normalized components. They are frozen once as little-endian float32 bytes. Selected persisted vector lengths, finite values and float32 unit-norm tolerance are checked before native distance execution. Uncertain runtime teardown cannot return evidence. The operation uses the existing 90-second cooperative boundary and SQLite progress checks; threaded file reads/native functions are not a hard process deadline or full memory confinement.

`app/retrieval/vector_search.py` verifies the exact selected sqlite-vec 0.1.9 DLL and both pinned companion notices, including size/hash/local ancestry and single-link files. It enables Python extension loading only for the fixed absolute DLL path, disables it in `finally`, then checks the reported version. There is no wrapper import, arbitrary caller path, registry lookup, install/download or alternative similarity fallback. Loader/version/SQLite failures expose safe codes without private paths/upstream text. The app does not load it at startup; current routine tests inject a native-function seam.

## Native query choice and evidence packing

The query joins only the selected, current source bindings to canonical T28 vectors **before** invoking `vec_distance_cosine`. It streams scoped cosine results and retains at most five winners with stable `(distance, chunk_id, reference_id)` ordering, validating result counts and finite/range-bounded distances. Ranked source payloads must match chunk/text/source identities. Identical content in different conversations cannot grant membership, and same-content selected sources retain distinct source-specific provenance. No history parameter or all-library search is introduced.

This uses the approved sqlite-vec backend's scalar cosine function over existing canonical BLOBs. It does not create a second persisted vector copy or a virtual-table schema/migration. The earlier native `vec0 MATCH` comparison remains benchmark evidence for that different query path; its timings do **not** apply here. The streaming implementation performs two scoped passes and O(n) native distance calls, retaining O(5) candidate rows in the ranking heap. Full-scale latency/memory, source hashing costs and target-machine performance are unvalidated. A future native index optimization must preserve scope, exact-tie behavior and source/version checks.

`RetrievalResult` separates ranked hits, actually supplied evidence, omitted candidates, blocked sources, source snapshots, warnings and rendered evidence bytes. Only supplied complete chunks receive response-local opaque evidence IDs. JSON filename/reference labels, T26's complete text/location labels and two-byte separators count toward the approved provisional **2,000-byte** evidence budget; values/quotations/rows are never sliced to fit. Source metadata remains typed and separate. T30 must enforce the whole 3,000-byte policy/question/history/evidence/serialization budget and model-input-fit behavior; this is not a token-fit proof.

Distances order candidates; they do not assess answerability or correctness. Exact ties emit `DISTANCE_TIE`, blocked sources and budget omissions are disclosed, and index omissions remain visible. `ANSWERABILITY_UNASSESSED` and `TOKEN_FIT_UNVERIFIED` prevent treating candidates as a supported answer. A question about an absent fact can still retrieve nearest passages; semantic insufficiency/contradiction/refusal belongs to grounded generation/evaluation rather than an invented distance threshold. No calibrated confidence score is returned.

## Verification and small deterministic evaluation

**42 added cases**: 18 query/loader unit cases, 18 stored-source retrieval integration cases and six data-only native-handoff gate/supervisor cases. Real upload/extraction/chunk/index/SQLite joins are used; document/query vectors and the SQLite cosine kernel are injected. The test cosine oracle computes an independent normalized dot product from frozen float32 bytes. Production contains no Python cosine fallback.

| Authored evaluation/control | Observed result |
|---|---|
| `Name,Units / North,42 / South,50`, question `North units?` | North/42 is first at synthetic distance 0; both typed table records retain header/data anchors |
| Same conversation contains unselected `North,999` | Only two selected vectors reach the distance function; the unselected value/reference is absent |
| Identical bytes in another conversation | Foreign reference rejected before model/native calls |
| Selected second file `North,70` | Both selected file identities retained; exact-distance tie uses stable chunk IDs and warns, without choosing a factual winner |
| Six selected large-row files | Five ranked candidates retained; only whole rendered chunks fitting 2,000 bytes supplied; IDs/omissions/byte count agree |
| Unindexed or missing selected original | Affected source is explicitly blocked; all-blocked/empty selection returns no evidence without query/native calls |
| Absent-fact question about company ownership | Candidate passages retained with answerability/fit limitations; no semantic pass or answer fabricated |
| Source bytes, generation identity or reference changes while embedding | No result published; `SOURCE_CHANGED` |

These are deterministic mechanical relevance/scope fixtures, not actual embedding-model relevance scores or the Stage 1 acceptance corpus. No private sample, new quality threshold, benchmark denominator or calibrated probability is introduced.

| Check | Actual result |
|---|---|
| Initial red unit seam | Missing module import, 1.30 s |
| First unit green | 18 passed, 0.91 s |
| Scope red / first integration green | Missing retriever module, 1.28 s; then 6 passed, 3.59 s |
| Added corrupt-vector control | Passed before further changes, confirming existing pre-native rejection; not presented as a failing reproduction |
| Concurrent-reference-removal red | 1 failed, 1.27 s: returned `SOURCE_NOT_FOUND` instead of the concurrent-change code; fixed with source recheck translation |
| Expanded scope/query checks | 36 passed, 6.18 s |
| Prepared handoff gates/supervisor | 42 passed, 5.80 s; fake owned process only, no DLL/native worker |
| Scope-join mutation | Replacing binding membership with `ON 1=1` failed the selected-scope control before native scoring; original restored exactly |
| Final full suite after restoration | **466 passed, 1 skipped, 1 warning, 64.22 s**; shared meter **16/64 starts, 675,529/2,000,000 retained metered bytes** |
| Established application/test/helper Ruff scope | Lint passed; **57 files already formatted** |

The existing skip is Windows symlink permission; warning is Starlette/HTTPX deprecation. Mutation-restored `app/retrieval/search.py` SHA256 is `c159506e2f7c427726a53127ca6df88af1b782827c4b7169840318f6f3ef5237`. No assertions were weakened or old tests removed. Commands used project Python, disabled third-party pytest plugin autoload/cache writes and included both T27/T29 helpers in the established quality scope, excluding unchanged historical evaluation scripts:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe -m pytest -q -rP -p no:cacheprovider
.\.venv\Scripts\python.exe -m ruff check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration tests/evals/spikes/t27_runtime_smoke.py tests/evals/spikes/t29_native_search.py
.\.venv\Scripts\python.exe -m ruff format --check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration tests/evals/spikes/t27_runtime_smoke.py tests/evals/spikes/t29_native_search.py
```

`data/t29-01/budget.json` records the explicit 42-start prepayment under the 64-start ceiling. Final conservative phase charges are red 4/4, green 4/6, regression 17/22, mutation 2/2 and quality/review 8/8: **35 charged starts**, **34 observed owned test/quality starts** because the final suite used 16 of 17 reserved starts, with no refund. Test-meter artifact/child-output charges sum to **1,040,856 bytes**; final accounting also charges actual logs, review diff/seal, ledger reserve and the first fake supervisor fixture's 65,537 bytes before its explicit artifact-meter addition. The combined retained charge stays under 2,000,000 bytes. No allocation is reset or reused for native work.

## Review and next gate

Manual review traced pre-ranking scope joins, source rechecks, selected-only vector validation, fixed loader assets and safe enable/disable boundaries, finite/stable ranking, complete-byte packing, response-local citation eligibility, cancellation and no-fallback errors. At preparation closeout, the [native package](../proposals/t29-native-search.md) was source-sealed before any native root/run: one authored two-record SQLite pipeline, one exact DLL load, two arithmetic distance checks, disabled SQL extension load and integrity/reaping checks. Its source/asset identities were checked read-only. The operator subsequently executed that package once; [reviewed native results](t29-native-search.md) passed, with all pins and receipts preserved. No additional native execution is needed for this bounded gate.

T29 implementation/routine verification is delivered. The user approved its 14-file commit and exact N1 package; committed as `4a618c2`. The operator then completed the one disconnected run and [native receipt review passed](t29-native-search.md), closing this bounded T29 verification gate. Full grounded-answer quality, real query/index model integration, memory/latency acceptance, saved-selection UI, later formats and atomic answer publication remain later gates. T30 is next and unstarted. S1/S2/N1 receipts/seals and prior allocations are preserved unchanged; no checkpoint/session-summary file or unrelated user change was edited. Original implementation diff: `data/reviews/t29-retrieval.diff`; subsequent eight-document native results/status diff: `data/reviews/t29-native-results.diff`, awaiting its separate Git decision.
