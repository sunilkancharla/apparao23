# Session 4 — AI Session Summary

Updated: **20 November 2026**. Scope: **T26–T32**, from commit **f7f0a90** through **c3c6e61**, including separately reviewed native smoke results and corrections. Created at the user's explicit request, following the format of the [Session 3 CSV summary](SESSION_3_CSV_Session_SUMMARY.md). The separately committed summary/status handoff is outside the task inventories below.

## 1. Session Overview

This session extended the CSV storage/extraction foundations into the AI backend path: source-preserving chunks → pinned local embeddings → versioned vector persistence → selected-source retrieval → grounded generation and saved exchanges → checked citations/previews → observable evidence-support signals.

**T26–T32 are implemented and committed.** The user accepted **CP10** and **CP11**. Routine tests use injected models/native kernels, actual SQLite/source storage and controlled process/HTTP boundaries. Separately approved operator-disconnected runs proved bounded real embedding ownership/cleanup, the selected native cosine bridge, and one real Qwen generation/persistence case. Those separate checks are not a combined real-model retrieval-quality benchmark.

The ordinary suite progressed from T25's **241 passes** to **579 passed, 1 skipped, 1 warning**. No dependency/model was installed or downloaded in this implementation session. Existing local Ollama, selected model assets and sqlite-vec artifacts were reused only within their approved packages. No private evaluation document was processed or sent externally. Native run roots, claim/ledger receipts and historical seals remain preserved and closed.

The backend does not automatically configure/start inference for browser users; trusted owned factories are still required. Health/browser readiness and final Stage 1 acceptance remain unchanged. The browser flow, saved-chat list/reopen/rename, additional-format ingestion and general lifecycle are later tasks.

**Session-end decisions:** the user skipped **T15/UI UX Pro Max** entirely, including source review/use; retained manual design/accessibility review with local HTML/CSS/JavaScript; approved **T34A** initial CSV input-boundary/real-pipeline validation after T34 and before format expansion; and reserved **T33 for a new session**. T48 remains the final all-format quality/resource baseline. Exact input fit and independent per-answer semantic support are not claimed verified. This requested summary is a one-file exception to the default no-summary rule; earlier summaries/checkpoints remain unchanged.

## 2. Task-wise Work and Files

Each task records purpose, implementation, evidence and limits. Expand its file list for individual descriptions.

**Created** means introduced in that task's source/results commits; **Updated** means already present before that task. A file created then modified within one task is listed once as created. Shared files appear under each task that changed them. Counts come from actual Git inventories, not proposed file lists. Authored helpers/seals/reports are versioned; runtime originals, vectors, databases, model assets, receipts and review patches remain local/ignored.

#### T26 — Chunk passages without losing source structure

**Summary:** Transform normalized units into bounded retrieval evidence while preserving actual source spans, table relationships and explicit omissions.

**Process:** Implemented sequential prose, structured table/CSV and stored-source integration increments. Added immutable chunk/part/omission models and a pure deterministic iterator; source extraction stays unchanged.

**Outcome:** The provisional T16 policy uses a 600-byte prose target, 800-byte maximum including generated labels and up to 120 bytes of complete-boundary prose overlap. Tables retain whole values, headers and declared row keys. CSV columns reunite by actual logical record/physical-line span. Oversized unsplittable passages/rows, missing structure and images needing interpretation receive omissions rather than fabricated evidence. Repeated context is distinguished from fresh evidence.

**Verification:** Added **32 ordinary cases**; full suite **273 passed, 1 skipped, 1 warning**; Ruff passed across 34 Python files. Actual stored CSV units trace through chunking without changing original bytes. Exact-boundary controls caught an inverted maximum-byte predicate; original source was restored before regression.

**Limit:** Synthetic PDF/XLSX provenance tests do not implement those ingestion formats. This task adds no persisted index, API route, model inference or token-fit proof. Source IDs/filenames are not access permissions, and structured metadata is outside the chunk-text byte cap.

**Commit:** `f7f0a90` — Implement T26 source-preserving bounded chunks. [Evidence](../benchmarks/t26-chunking.md).

<details>
<summary>Files associated with T26 (10: 6 created, 4 updated)</summary>

**Application source — Python**

- [app/retrieval/__init__.py](../../app/retrieval/__init__.py) — **Created.** Introduces the retrieval package namespace; it does not start processing or inference.
- [app/retrieval/chunking.py](../../app/retrieval/chunking.py) — **Created.** Builds deterministic bounded prose/table/CSV chunks with complete values, repeated context and explicit omissions.
- [app/retrieval/models.py](../../app/retrieval/models.py) — **Created.** Defines immutable chunk/source-part/omission values, identities, text hashes, Unicode spans and provenance.

**Tests — Python**

- [tests/integration/test_stored_chunking.py](../../tests/integration/test_stored_chunking.py) — **Created.** Traces chunks to actual stored CSV extraction while preserving original bytes and metadata.
- [tests/unit/test_chunking.py](../../tests/unit/test_chunking.py) — **Created.** Tests deterministic boundaries, complete table values, overlap, omissions and source spans across synthetic provenance formats.

**Documentation — Markdown**

- [PLAN.md](../../PLAN.md) — **Updated.** Records task order, evidence, approval boundaries and the next implementation/validation step.
- [README.md](../../README.md) — **Updated.** Describes verified backend behavior, actual commands, prerequisites and remaining limits.
- [TODO.md](../../TODO.md) — **Updated.** Tracks atomic work, acceptance evidence, explicit decisions and the session stopping point.
- [docs/benchmarks/t26-chunking.md](../benchmarks/t26-chunking.md) — **Created.** Records chunking behavior, source tracing, boundary mutation, tests and provisional limits.
- [docs/contracts.md](../contracts.md) — **Updated.** Documents the implemented source, runtime, storage, answer and HTTP boundary contracts.

</details>

**Generated/local files:** Authored CSV originals, extraction databases and test/review artifacts remain in ignored roots. No generated document, original or database entered Git.

#### T27 — Embed chunks through a pinned, owned local runtime

**Summary:** Add the bounded local embedding client, then bind it to an exclusively owned model process/session and verify one separately approved native package.

**Process:** First implemented fixed loopback HTTP and pinned document/query embeddings. Then added the one-store work slot, private runtime home, Windows Job ownership, exact root-listener checks, watchdog/resource guards, cancellation/cleanup and a sealed one-worker smoke handoff. Model/runtime/digest/prefix/dimension identities remain fixed; no unowned service is adopted or downloaded automatically.

**Outcome:** The client requires complete ordered finite nonzero 768-dimensional vectors with source/text/profile linkage, distinct Nomic document/query prefixes and stable normalization. Bounded requests/responses reject malformed output, changed identity, redirects/proxies, unsupported endpoints and partial batches without retries. The owner verifies selected assets and retains ownership until cleanup is verified.

**Native sequence and review findings:**

- **S1** stopped during model preflight before a native model launch: diagnostics expected the legacy manifest directory while the installed selected Ollama runtime used the v2 layout. The failed allocation and receipts were preserved; no reset/retry was performed.
- **R1 correction** selected the exact installed v2 path, retained identity/size/hash/ancestry checks, improved component-specific errors and corrected separate-package/root/stop reporting. No fallback scan, model replacement or dependency change was introduced.
- **S2** then ran once under its own approved seal/root. Actual authored CSV evidence produced **two document embeddings and one query embedding**. Positive cleanup and cancellation **after listener admission** released the private port/work slot. That cancellation case does not prove interruption during active inference.

**Verification:** Client closeout **329 passes** (+56), owner **365** (+36), correction **387** (+22), each with the existing skip/warning and passing Ruff. Digest, listener-address and asset-size mutations were caught and restored. The separate S2 receipt records passed status, 34 charged starts and ten HTTP attempts; it does not retain raw vectors, peak memory or a packet trace.

**Limit:** Requested CPU settings and sampled controls do not establish strict aggregate memory/GPU residency or hostile same-account isolation. Native success is a bounded ownership/embedding bridge result, not final 16-GB feasibility, semantic relevance, answer accuracy or general application readiness. The smoke uses operator offline attestation rather than independent network capture.

**Commits:** `ae1f611` client; `67bdd7f` owned runtime/handoff; `8fabbfa` S1 review/correction approval; `73cb659` preflight correction and successful S2 review. [Client](../benchmarks/t27-embeddings.md), [owner](../benchmarks/t27-runtime-owner.md), [S1](../benchmarks/t27-runtime-first-stop.md), [correction](../benchmarks/t27-preflight-correction.md), [S2](../benchmarks/t27-runtime-smoke-02.md).

<details>
<summary>Files associated with T27 (30: 23 created, 7 updated)</summary>

**Application source — Python**

- [app/diagnostics.py](../../app/diagnostics.py) — **Updated.** Checks selected local assets and exact model manifest/blob identities; the correction uses the installed Ollama v2 manifest layout.
- [app/ollama.py](../../app/ollama.py) — **Created.** Implements fixed loopback, purpose-restricted, bounded HTTP transport with safe failures and no proxy/redirect/retry fallback.
- [app/retrieval/embeddings.py](../../app/retrieval/embeddings.py) — **Created.** Validates pinned document/query embeddings, prefixes, dimensions, source linkage and complete bounded batches.
- [app/runtime.py](../../app/runtime.py) — **Created.** Owns the exclusive local model session, selected assets, private home, process/listener checks, watchdog and cleanup.
- [app/windows_job.py](../../app/windows_job.py) — **Created.** Implements Windows Job/process/listener/resource controls and verified owned-tree teardown.

**Tests — Python**

- [tests/integration/test_local_embeddings.py](../../tests/integration/test_local_embeddings.py) — **Created.** Exercises the embedding client with a controlled local HTTP server, without actual model inference.
- [tests/integration/test_startup.py](../../tests/integration/test_startup.py) — **Updated.** Checks safe startup/diagnostics against the current pinned asset behavior.
- [tests/unit/test_embeddings.py](../../tests/unit/test_embeddings.py) — **Created.** Tests embedding profiles/prefixes, source hashes/order, dimension/normalization checks and complete batches.
- [tests/unit/test_model_assets.py](../../tests/unit/test_model_assets.py) — **Created.** Tests real-layout manifest/blob identity checks and component-specific preflight errors on authored fixtures.
- [tests/unit/test_ollama.py](../../tests/unit/test_ollama.py) — **Created.** Tests fixed-endpoint HTTP bounds, identity/purpose restrictions, malformed responses, timeouts and cancellation seams.
- [tests/unit/test_runtime_owner.py](../../tests/unit/test_runtime_owner.py) — **Created.** Tests exclusive runtime admission, private homes, watchdog failures, lease cleanup and cancellation using fake owned processes.
- [tests/unit/test_runtime_smoke_budget.py](../../tests/unit/test_runtime_smoke_budget.py) — **Created.** Tests native handoff gates, shared finite accounting, worker claims, root selection and conservative stop reporting.
- [tests/unit/test_windows_job.py](../../tests/unit/test_windows_job.py) — **Created.** Tests Win32 ownership, listener and resource checks with controlled native-call seams.
- [tests/unit/test_windows_launch.py](../../tests/unit/test_windows_launch.py) — **Created.** Tests atomic process/job startup and safe handle cleanup without launching a real model.

**Separately gated native handoff — Python**

- [tests/evals/spikes/t27_runtime_smoke.py](../../tests/evals/spikes/t27_runtime_smoke.py) — **Created.** Defines the separately gated embedding smoke, shared meter, one-worker supervision and preserved closed-package behavior.

**Authored source seals — JSON**

- [docs/proposals/t27-runtime-smoke-02-seal.json](../proposals/t27-runtime-smoke-02-seal.json) — **Created.** Pins the corrected S2 source set separately from S1.
- [docs/proposals/t27-runtime-smoke-seal.json](../proposals/t27-runtime-smoke-seal.json) — **Created.** Pins the historical S1 executed source set; it is preserved rather than resealed for newer code.

**Documentation — Markdown**

- [PLAN.md](../../PLAN.md) — **Updated.** Records task order, evidence, approval boundaries and the next implementation/validation step.
- [README.md](../../README.md) — **Updated.** Describes verified backend behavior, actual commands, prerequisites and remaining limits.
- [TODO.md](../../TODO.md) — **Updated.** Tracks atomic work, acceptance evidence, explicit decisions and the session stopping point.
- [docs/ADR/0001-stage1-architecture.md](../ADR/0001-stage1-architecture.md) — **Updated.** Explains architecture and publication/ownership trade-offs without silently adopting new dependencies or retention rules.
- [docs/benchmarks/t27-embeddings.md](../benchmarks/t27-embeddings.md) — **Created.** Records embedding-client validation, local HTTP tests, identity mutation and owner/native prerequisites.
- [docs/benchmarks/t27-preflight-correction.md](../benchmarks/t27-preflight-correction.md) — **Created.** Records the v2 manifest/error/gate correction, regression, budgets and preserved S1 evidence.
- [docs/benchmarks/t27-runtime-first-stop.md](../benchmarks/t27-runtime-first-stop.md) — **Created.** Records S1's pre-native preflight stop and preserved failure/cleanup evidence.
- [docs/benchmarks/t27-runtime-owner.md](../benchmarks/t27-runtime-owner.md) — **Created.** Records fake-verified process ownership, resource/cleanup controls and native smoke preparation.
- [docs/benchmarks/t27-runtime-smoke-02.md](../benchmarks/t27-runtime-smoke-02.md) — **Created.** Records passing real embeddings, owned teardown and cancellation-after-admission in the separate S2 run.
- [docs/contracts.md](../contracts.md) — **Updated.** Documents the implemented source, runtime, storage, answer and HTTP boundary contracts.
- [docs/proposals/t27-preflight-correction.md](../proposals/t27-preflight-correction.md) — **Created.** Defines the approved bounded preflight correction and separately prepared S2 handoff.
- [docs/proposals/t27-runtime-smoke-02.md](../proposals/t27-runtime-smoke-02.md) — **Created.** Records the exact distinct S2 package and offline operator handoff; its completed allocation remains closed.
- [docs/proposals/t27-runtime-smoke.md](../proposals/t27-runtime-smoke.md) — **Created.** Records the exact historical S1 package, allocation, source/model pins and operator handoff; S1 remains closed.

</details>

**Generated/local files:** `data/t27-runtime-smoke-01/`, `data/t27-runtime-smoke-02/`, `data/t27-repair-01/`, private staging homes, test stores and review diffs remain ignored. Both native allocations are closed; do not rerun/reset/delete/reseal them. Worker tokens and raw receipt internals are excluded from this summary.

#### T28 — Persist versioned vectors without losing scope or recovery

**Summary:** Publish canonical embeddings and source-specific chunk/provenance bindings atomically in the managed SQLite store.

**Process:** Added schema v5, exact migrations, version/profile identity, canonical float32 validation, durable indexing intents and content reuse. Kept document/reference/display ownership distinct from shared content/vector identity.

**Outcome:** Indexing uses bounded embedding batches and one publication transaction through verified teardown. Complete generation identity includes transformation/model/storage versions. Same content can reuse canonical vector work without borrowing another reference's labels/scope. Stale/incompatible/failed work cannot advertise current readiness. Quota/source/model/space failures roll back publication; interrupted intents recover without silently retrying inference.

**Verification:** Added **37 cases**; full suite **424 passed, 1 skipped, 1 warning**; Ruff passed across 51 files. Three actual metered Python exit controls checked recovery/publication boundaries. A mismatched-space mutation was caught and source restored. **CP10** reviewed T26 chunks, T27 client/ownership/native evidence and T28 atomic persistence and was accepted by the user.

**Limit:** T28 embeddings are injected; actual model-to-index persistence is not inferred from those tests. Native search, full-scale hashing/transactions, physical-16-GB capacity and application quality remained later validation. The SQLite backend/profile is retained; no new database/vector dependency or retention policy is selected.

**Commit:** `e9d5580` — Persist versioned scoped vector generations and complete CP10. [Evidence](../benchmarks/t28-indexing.md).

<details>
<summary>Files associated with T28 (13: 5 created, 8 updated)</summary>

**Application source — Python**

- [app/ingestion/processing.py](../../app/ingestion/processing.py) — **Updated.** Reports current indexing operation/state through the existing scoped processing-status interface.
- [app/retrieval/index.py](../../app/retrieval/index.py) — **Created.** Orchestrates versioned CSV indexing, embedding batches, canonical-vector publication, reuse and failure rollback.
- [app/storage/database.py](../../app/storage/database.py) — **Updated.** Adds and migrates exact SQLite schema versions for index generations and saved selections/exchanges.
- [app/storage/files.py](../../app/storage/files.py) — **Updated.** Integrates index/message recovery and quota/accounting within the existing one-owner managed store.
- [app/storage/index_state.py](../../app/storage/index_state.py) — **Created.** Maintains current index profiles, durable intents/bindings, checked chunk reads, status and restart recovery.

**Tests — Python**

- [tests/integration/test_indexing.py](../../tests/integration/test_indexing.py) — **Created.** Tests actual index storage/reuse/scope/rollback/restart with injected embeddings and exact schema migration assertions.
- [tests/unit/test_index_vectors.py](../../tests/unit/test_index_vectors.py) — **Created.** Tests canonical float32 vectors, model/profile identities, serialization and invalid-space refusals.

**Documentation — Markdown**

- [PLAN.md](../../PLAN.md) — **Updated.** Records task order, evidence, approval boundaries and the next implementation/validation step.
- [README.md](../../README.md) — **Updated.** Describes verified backend behavior, actual commands, prerequisites and remaining limits.
- [TODO.md](../../TODO.md) — **Updated.** Tracks atomic work, acceptance evidence, explicit decisions and the session stopping point.
- [docs/ADR/0001-stage1-architecture.md](../ADR/0001-stage1-architecture.md) — **Updated.** Explains architecture and publication/ownership trade-offs without silently adopting new dependencies or retention rules.
- [docs/benchmarks/t28-indexing.md](../benchmarks/t28-indexing.md) — **Created.** Records schema-v5 indexing/reuse/recovery tests, source-space mutation and CP10 review.
- [docs/contracts.md](../contracts.md) — **Updated.** Documents the implemented source, runtime, storage, answer and HTTP boundary contracts.

</details>

**Generated/local files:** Synthetic stores hold canonical vectors, chunk bindings and recovery intents; restart-control logs and review patches remain ignored. No vector database, uploaded original or model weight entered Git.

#### T29 — Retrieve complete evidence from explicitly selected sources

**Summary:** Resolve eligible current references, rank selected vectors and supply bounded complete provenance-bearing evidence for generation.

**Process:** Added explicit selected-reference eligibility, current source snapshots, pinned query-vector checks, stable top-five cosine ranking and whole-chunk packing within the 2,000-byte rendered evidence guard. Separated ranked candidates from supplied evidence, omissions and blocked sources; rechecked sources after embedding/ranking.

**Outcome:** Unknown/foreign references fail rather than broaden search. Known unavailable/unindexed sources are blocked visibly. SQL constrains eligible source bindings before native scoring. The fixed-path sqlite-vec loader verifies the selected DLL/notices, checks version and disables extension loading after admission. Scalar `vec_distance_cosine` uses canonical stored BLOBs; earlier virtual-table MATCH timings are not performance evidence for this path. Similarity is not semantic support or a correctness threshold.

**Verification:** Added **42 cases**; full suite **466 passed, 1 skipped, 1 warning**; Ruff passed. Scope mutation was caught/restored. Separately approved **T29-N1** loaded the real selected sqlite-vec 0.1.9 bridge against actual stored CSV data with synthetic vectors: North/42 ranked first, expected cosine arithmetic/rank and two evidence items passed, SQL extension loading was denied, SQLite integrity was `ok` and the parent confirmed worker reaping.

**Limit:** N1 runs no actual embedding/chat model. It establishes native arithmetic/application plumbing, not semantic relevance, a new combined real-model result, full-scale latency/memory or Stage 1 acceptance.

**Commits:** `4a618c2` retrieval/native handoff; `b301d1d` passing N1 review. [Routine evidence](../benchmarks/t29-retrieval.md), [native evidence](../benchmarks/t29-native-search.md).

<details>
<summary>Files associated with T29 (15: 10 created, 5 updated)</summary>

**Application source — Python**

- [app/retrieval/search.py](../../app/retrieval/search.py) — **Created.** Resolves selected current sources, ranks eligible vectors, packs complete evidence and rechecks source versions.
- [app/retrieval/vector_search.py](../../app/retrieval/vector_search.py) — **Created.** Validates query/stored vectors and loads only the pinned sqlite-vec DLL for scoped native cosine evaluation.

**Tests — Python**

- [tests/integration/test_retrieval_scope.py](../../tests/integration/test_retrieval_scope.py) — **Created.** Exercises actual selected-source SQLite retrieval and changed-reference/original/index boundaries with synthetic vectors.
- [tests/unit/test_retrieval.py](../../tests/unit/test_retrieval.py) — **Created.** Tests native-loader/query guards, stable ranking, evidence packing and provenance using controlled kernel/model seams.
- [tests/unit/test_retrieval_handoff.py](../../tests/unit/test_retrieval_handoff.py) — **Created.** Tests the distinct T29 native-package/source-seal/root/worker gates without loading its real DLL.

**Separately gated native handoff — Python**

- [tests/evals/spikes/t29_native_search.py](../../tests/evals/spikes/t29_native_search.py) — **Created.** Defines the one-run native cosine bridge against authored stored CSV data and synthetic embeddings.

**Authored source seals — JSON**

- [docs/proposals/t29-native-search-seal.json](../proposals/t29-native-search-seal.json) — **Created.** Pins the T29-N1 application/helper/lock source identities without including runtime data.

**Documentation — Markdown**

- [PLAN.md](../../PLAN.md) — **Updated.** Records task order, evidence, approval boundaries and the next implementation/validation step.
- [README.md](../../README.md) — **Updated.** Describes verified backend behavior, actual commands, prerequisites and remaining limits.
- [TODO.md](../../TODO.md) — **Updated.** Tracks atomic work, acceptance evidence, explicit decisions and the session stopping point.
- [docs/ADR/0001-stage1-architecture.md](../ADR/0001-stage1-architecture.md) — **Updated.** Explains architecture and publication/ownership trade-offs without silently adopting new dependencies or retention rules.
- [docs/benchmarks/t29-native-search.md](../benchmarks/t29-native-search.md) — **Created.** Records the passing real sqlite-vec bridge, expected arithmetic/rank, load restrictions, integrity and reaping.
- [docs/benchmarks/t29-retrieval.md](../benchmarks/t29-retrieval.md) — **Created.** Records scoped retrieval/ranking/evidence tests, source-scope mutation and distinct scalar-query performance limits.
- [docs/contracts.md](../contracts.md) — **Updated.** Documents the implemented source, runtime, storage, answer and HTTP boundary contracts.
- [docs/proposals/t29-native-search.md](../proposals/t29-native-search.md) — **Created.** Records the bounded T29-N1 DLL-bridge package and completed one-run conditions.

</details>

**Generated/local files:** The closed `data/t29-native-01/` holds authored fixture storage, its ledger/claim/result/parent receipts and scratch. Preserve it without retry/reset/reseal. DLL/model assets and generated data are not versioned.

#### T30 — Generate and persist evidence-bound chat exchanges

**Summary:** Add typed local generation, bounded evidence/history packing and durable selection/revision-protected answer publication.

**Process:** Implemented ordered generation/prompt, schema-v6 message/selection storage, service/API and native handoff increments. Reused the owned runtime with a separate chat purpose and fixed Qwen identity/settings. No caller-provided model/history/evidence or unowned service is accepted.

**Outcome:** Questions stay within 512 UTF-8 bytes; whole rendered evidence within 2,000; eligible history within two complete pairs/500 bytes; the complete serialized chat request within 3,000 bytes. Typed status/claim/citation output must finish with valid model identity and complete termination, at most 192 observed generated tokens and supplied-only citations. Those byte/post-response controls do not prove exact input fit.

Schema v6 stores selections/revisions, idempotent intents and complete exchanges. Selection changes can invalidate in-flight work. Publication checks current selection/reference/extraction/index state in the same transaction that saves the exchange, after native teardown and original checks. Cancelled/invalid/stale/interrupted work saves no partial assistant text. History is untrusted and excluded when source scope/version no longer qualifies. Full source text/prompts are not newly retained as quotation snapshots. Default inference remains disabled without trusted owned factories.

**Verification:** Added **40 cases**; full suite **506 passed, 1 skipped, 1 warning**; Ruff passed across 66 files. Two process-exit controls checked intent/publication recovery. Concurrent-selection mutation was caught/restored. Separately approved **T30-N1** used actual pinned Qwen generation with authored retrieval/index vectors: an answered claim contained standalone **42**, citations stayed within supplied `ev_native`, the saved exchange matched exactly after store/connection reopen and the private port was released.

**Limit:** N1 does not combine real Nomic inference, native retrieval and Qwen into a quality evaluation. Reopen in the native worker is distinct from routine abrupt-process-exit tests. One correct value/supplied citation does not independently verify every claim, quotation, calculation or prompt-injection behavior. Browser chat and transcript listing/renaming remained later work.

**Commits:** `07a7d27` generation/persistence/handoff; `aff116e` successful native review. [Implementation](../benchmarks/t30-grounded-chat.md), [native result](../benchmarks/t30-model-smoke.md).

<details>
<summary>Files associated with T30 (24: 13 created, 11 updated)</summary>

**Application source — Python**

- [app/api/chat.py](../../app/api/chat.py) — **Created.** Exposes bounded same-origin selection, answer and historical-read routes with current citation/support annotations.
- [app/chat/__init__.py](../../app/chat/__init__.py) — **Created.** Introduces the chat package namespace without configuring or starting a model service.
- [app/chat/generation.py](../../app/chat/generation.py) — **Created.** Builds bounded evidence/history prompts and validates pinned Qwen requests, typed claims, supplied IDs and complete output.
- [app/chat/service.py](../../app/chat/service.py) — **Created.** Coordinates grounded generation, current-source checks, atomic saved exchanges and explicit insufficiency/failure behavior.
- [app/main.py](../../app/main.py) — **Updated.** Connects chat/storage routes and the trusted service injection point while retaining existing Host/Origin/CSRF/readiness rules.
- [app/ollama.py](../../app/ollama.py) — **Updated.** Implements fixed loopback, purpose-restricted, bounded HTTP transport with safe failures and no proxy/redirect/retry fallback.
- [app/runtime.py](../../app/runtime.py) — **Updated.** Owns the exclusive local model session, selected assets, private home, process/listener checks, watchdog and cleanup.
- [app/storage/database.py](../../app/storage/database.py) — **Updated.** Adds and migrates exact SQLite schema versions for index generations and saved selections/exchanges.
- [app/storage/files.py](../../app/storage/files.py) — **Updated.** Integrates index/message recovery and quota/accounting within the existing one-owner managed store.
- [app/storage/messages.py](../../app/storage/messages.py) — **Created.** Stores selection revisions, idempotent answer intents and complete exchanges, with scoped history and interrupted-intent recovery.

**Tests — Python**

- [tests/integration/test_chat.py](../../tests/integration/test_chat.py) — **Created.** Tests scoped grounded/abstention orchestration, API/security failures, source changes and historical context with injected generation.
- [tests/integration/test_indexing.py](../../tests/integration/test_indexing.py) — **Updated.** Tests actual index storage/reuse/scope/rollback/restart with injected embeddings and exact schema migration assertions.
- [tests/integration/test_messages.py](../../tests/integration/test_messages.py) — **Created.** Tests durable selections/intents/exchanges, idempotency, migrations and process-exit recovery.
- [tests/unit/test_generation.py](../../tests/unit/test_generation.py) — **Created.** Tests pinned chat transport/output, prompt/history/evidence bounds, citation IDs and the guarded native chat handoff.

**Separately gated native handoff — Python**

- [tests/evals/spikes/t30_model_smoke.py](../../tests/evals/spikes/t30_model_smoke.py) — **Created.** Defines the one-run actual Qwen generation/publication/reopen check with authored retrieval seams and its distinct allocation.

**Authored source seals — JSON**

- [docs/proposals/t30-model-smoke-seal.json](../proposals/t30-model-smoke-seal.json) — **Created.** Pins all 35 T30-N1 application/helper/dependency-manifest source identities.

**Documentation — Markdown**

- [PLAN.md](../../PLAN.md) — **Updated.** Records task order, evidence, approval boundaries and the next implementation/validation step.
- [README.md](../../README.md) — **Updated.** Describes verified backend behavior, actual commands, prerequisites and remaining limits.
- [TODO.md](../../TODO.md) — **Updated.** Tracks atomic work, acceptance evidence, explicit decisions and the session stopping point.
- [docs/ADR/0001-stage1-architecture.md](../ADR/0001-stage1-architecture.md) — **Updated.** Explains architecture and publication/ownership trade-offs without silently adopting new dependencies or retention rules.
- [docs/benchmarks/t30-grounded-chat.md](../benchmarks/t30-grounded-chat.md) — **Created.** Records prompt/generation/storage/API behavior, revision publication, process-exit tests and remaining limits.
- [docs/benchmarks/t30-model-smoke.md](../benchmarks/t30-model-smoke.md) — **Created.** Records the passing actual Qwen case, supplied-only citations, exact saved exchange after reopen and private-port cleanup.
- [docs/contracts.md](../contracts.md) — **Updated.** Documents the implemented source, runtime, storage, answer and HTTP boundary contracts.
- [docs/proposals/t30-model-smoke.md](../proposals/t30-model-smoke.md) — **Created.** Records the approved T30-N1 Qwen generation/persistence package and its completed, withdrawn handoff.

</details>

**Generated/local files:** The closed `data/t30-model-01/` holds the authored CSV store, private home and bounded scalar receipts. Routine intent/exit logs and review diffs remain ignored. No prompts, complete retrieved-source snapshots, model assets or database binary entered Git.

#### T31 — Validate citations and expose safe passage previews

**Summary:** Bind previews to citations actually used by the saved answer and verify their current source text/locations.

**Process:** Added checked normalized passage/cell spans, saved-answer/conversation citation resolution, escaped previews and historical availability labels. Rechecked membership/version after asynchronous original hashing. The response-local citation ID requires its saved answer identity; there is no global source lookup or arbitrary filesystem path input.

**Outcome:** Preview quotations match genuine normalized text/cells at Unicode code-point spans; generated labels are not quotes. Missing/null versus empty cells, coarse headers and parser/method/confidence metadata remain honest. Every preview string is escaped once and the complete JSON envelope stays within 65,536 bytes. Missing/changed/detached/unsafe/unreadable sources block live preview; historical answer text remains readable with availability labels. Busy/recovery state keeps history readable and explicitly unrevalidated. No new quotation snapshot or retention change is introduced.

**Verification:** Added **35 cases**; full suite **541 passed, 1 skipped, 1 warning**; Ruff passed across 69 files. Source traces resolve North/42 to actual CSV record/column/line anchors. Tests cover foreign/uncited IDs, altered quotes/locations, response bounds, escaping, source changes and safe filesystem errors. A mutation returning supplied-but-uncited evidence failed its control; source was restored. **CP11** was accepted with mechanical versus semantic evidence distinguished.

**Review finding/accounting:** Explicit permission/unsafe-path tests exposed uncaught failures; those now become safe unavailable-source responses. A closeout audit also found Windows Ruff wrapper children were undercharged; quality charges were corrected to ten, making 54 conservative task starts under the unchanged 64 ceiling. That retroactive correction is retained as a procedural limitation; T32 precharged wrapper and child before each command.

**Limit:** Quote/location resolution does not independently verify model prose meaning or free-prose quotation/location assertions. Cooperative file/SQLite checks do not hard-confine threads/native code or hostile same-account edits. Actual CSV is supported; synthetic PDF/XLSX values do not adopt those ingestion paths. No browser preview UI or runtime semantic verifier is implemented.

**Commit:** `fd830e5` — Validate scoped citations and resolve checked source previews. [Evidence and CP11 review](../benchmarks/t31-citations.md).

<details>
<summary>Files associated with T31 (12: 4 created, 8 updated)</summary>

**Application source — Python**

- [app/api/chat.py](../../app/api/chat.py) — **Updated.** Exposes bounded same-origin selection, answer and historical-read routes with current citation/support annotations.
- [app/api/sources.py](../../app/api/sources.py) — **Updated.** Adds the saved-answer-scoped citation-preview route alongside the existing extraction/reference preview interface.
- [app/chat/citations.py](../../app/chat/citations.py) — **Created.** Checks normalized source quotations/locations and resolves escaped live previews only within the saved answer and conversation.
- [app/chat/service.py](../../app/chat/service.py) — **Updated.** Coordinates grounded generation, current-source checks, atomic saved exchanges and explicit insufficiency/failure behavior.

**Tests — Python**

- [tests/integration/test_saved_citations.py](../../tests/integration/test_saved_citations.py) — **Created.** Tests actual CSV citation/preview storage and HTTP scope, source availability, escaping, bounds and safe filesystem failures.
- [tests/unit/test_citations.py](../../tests/unit/test_citations.py) — **Created.** Tests genuine normalized quotation spans/coordinates and rejection of fabricated source metadata or invalid IDs.

**Documentation — Markdown**

- [PLAN.md](../../PLAN.md) — **Updated.** Records task order, evidence, approval boundaries and the next implementation/validation step.
- [README.md](../../README.md) — **Updated.** Describes verified backend behavior, actual commands, prerequisites and remaining limits.
- [TODO.md](../../TODO.md) — **Updated.** Tracks atomic work, acceptance evidence, explicit decisions and the session stopping point.
- [docs/ADR/0001-stage1-architecture.md](../ADR/0001-stage1-architecture.md) — **Updated.** Explains architecture and publication/ownership trade-offs without silently adopting new dependencies or retention rules.
- [docs/benchmarks/t31-citations.md](../benchmarks/t31-citations.md) — **Created.** Records checked preview behavior, current-source failures, cited-only mutation, CP11 review and the explicit accounting correction.
- [docs/contracts.md](../contracts.md) — **Updated.** Documents the implemented source, runtime, storage, answer and HTTP boundary contracts.

</details>

**Generated/local files:** Authored source stores, local response/control logs and `data/reviews/t31-citations.diff` remain ignored. The routine allocation is closed; no new native/model smoke occurred for this task.

#### T32 — Expose observable evidence-support signals

**Summary:** Explain observable checks, structural coverage, abstention and limitations without presenting an accuracy probability.

**Process:** Added a pure classifier, fixed labels/messages, declared-block counts and independent warnings; connected it to answer POST/replay and saved-answer GET. GET reuses current checked provenance to expose method/precision/OCR-confidence-availability flags. POST adds no extra hash/model pass. Signals are computed per response rather than persisted as scores.

**Outcome:** Source/request failures, invalid citations and incomplete checks take precedence over successful empty/resolved states. Successful pre-generation no-evidence and applicable clarification/refusal use N/A coverage. Partial/OCR/coarse/omission/conflict/missing-cache warnings remain separate. Declared text-block counts do not identify hidden facts or establish semantic support. The label is **“Citations checked; meaning not independently verified”**, never a calibrated correctness score.

Current generated answers keep incomplete support because exact input fit remains unknown, even when current quote/location checks pass. A stored operation's complete state means its exchange was saved, not that all support checks passed. The verified-fit argument is an authored-test/future trusted-backend seam; ordinary HTTP callers cannot set it. Model self-assessment/caller confidence fields do not control the signal. All-blocked selected sources now retain the unavailable-source warning instead of only the generic no-evidence warning.

**Verification:** Added **38 cases** (30 pure and eight actual-storage/HTTP); full suite **579 passed, 1 skipped, 1 warning**; Ruff passed across 72 files. Five reported hard-warning cases failed before correction. The mutation allowing unavailable sources to receive successful no-evidence status failed its HTTP control; exact source was restored before regression. OCR bridge/positive verified-fit cases are synthetic observations, not actual OCR/tokenizer proof.

**User-approved closeout:** Commit the implementation; skip T15 source review/use; add T34A after T34/before T35; keep T48's final baseline; create this summary and reserve T33 for the next session. The T32 commit includes its 13 implementation/report files plus the three explicit policy/decision records in AGENTS, SPEC and the decision register. No product format, model, dependency, retention or quality threshold changes.

**Commit:** `c3c6e61` — Implement T32 support signals and schedule early CSV validation. [Evidence](../benchmarks/t32-evidence-support.md), [explicit decisions](../decisions.md#2026-11-20--t32-commit-approved-ui-aid-skipped-csv-validation-scheduled).

<details>
<summary>Files associated with T32 (16: 4 created, 12 updated)</summary>

**Application source — Python**

- [app/api/chat.py](../../app/api/chat.py) — **Updated.** Exposes bounded same-origin selection, answer and historical-read routes with current citation/support annotations.
- [app/chat/citations.py](../../app/chat/citations.py) — **Updated.** Checks normalized source quotations/locations and resolves escaped live previews only within the saved answer and conversation.
- [app/chat/evidence.py](../../app/chat/evidence.py) — **Created.** Computes observable support states, declared-block counts and independent warnings without a semantic correctness score.
- [app/chat/service.py](../../app/chat/service.py) — **Updated.** Coordinates grounded generation, current-source checks, atomic saved exchanges and explicit insufficiency/failure behavior.

**Tests — Python**

- [tests/integration/test_evidence_support.py](../../tests/integration/test_evidence_support.py) — **Created.** Tests HTTP indicators, changed-source labels, no saved badge, blocked-source warnings and rejected caller grading fields.
- [tests/unit/test_evidence_indicator.py](../../tests/unit/test_evidence_indicator.py) — **Created.** Tests the approved support truth table, failure precedence, N/A coverage and semantic/correctness counterexamples.

**Documentation — Markdown**

- [AGENTS.md](../../AGENTS.md) — **Updated.** Records the user's durable UI UX Pro Max skip and the continued manual frontend review requirement.
- [PLAN.md](../../PLAN.md) — **Updated.** Records task order, evidence, approval boundaries and the next implementation/validation step.
- [README.md](../../README.md) — **Updated.** Describes verified backend behavior, actual commands, prerequisites and remaining limits.
- [SPEC.md](../../SPEC.md) — **Updated.** Records the narrow approved workflow amendment: skip the UI aid and schedule early CSV validation without changing product scope or quality targets.
- [TODO.md](../../TODO.md) — **Updated.** Tracks atomic work, acceptance evidence, explicit decisions and the session stopping point.
- [docs/ADR/0001-stage1-architecture.md](../ADR/0001-stage1-architecture.md) — **Updated.** Explains architecture and publication/ownership trade-offs without silently adopting new dependencies or retention rules.
- [docs/benchmarks/t32-evidence-support.md](../benchmarks/t32-evidence-support.md) — **Created.** Records support-state semantics, truth-table/API tests, precedence mutation and approved closeout decisions.
- [docs/contracts.md](../contracts.md) — **Updated.** Documents the implemented source, runtime, storage, answer and HTTP boundary contracts.
- [docs/decisions.md](../decisions.md) — **Updated.** Records approval of the T32 commit, the UI aid skip, T34A scheduling and the explicit summary/new-session instructions.
- [docs/evaluation.md](../evaluation.md) — **Updated.** Links implemented support signals to the approved observable-state design while preserving internal quality metrics and denominators.

</details>

**Generated/local files:** `data/t32-01/` contains closed routine accounting/logs; reviewed/approved closeout diffs and this summary's Git inventory remain under ignored `data/reviews/`. No badge database, evaluation original or model output dump is committed.

## 3. Verification Progress

| Task | New ordinary cases / increase | Full-suite closeout | Implementation/result commits |
|---|---:|---|---|
| T26 | 32 | 273 passed, 1 skipped, 1 warning | `f7f0a90` |
| T27 | 114 (56 client + 36 owner + 22 correction) | 387 passed, 1 skipped, 1 warning | `ae1f611`, `67bdd7f`, `8fabbfa`, `73cb659` |
| T28 | 37 | 424 passed, 1 skipped, 1 warning | `e9d5580` |
| T29 | 42 | 466 passed, 1 skipped, 1 warning | `4a618c2`, `b301d1d` |
| T30 | 40 | 506 passed, 1 skipped, 1 warning | `07a7d27`, `aff116e` |
| T31 | 35 | 541 passed, 1 skipped, 1 warning | `fd830e5` |
| T32 | 38 | 579 passed, 1 skipped, 1 warning | `c3c6e61` |

Together these tasks increased the passing ordinary suite by **338** from T25's 241-pass baseline. The Windows symlink-permission skip and Starlette/HTTPX warning were retained, not suppressed. Ruff passed at each boundary; mutation controls were restored before final regression. Test counts measure mechanical coverage, not product correctness or model quality.

| Latest task full-suite run | Shared starts used / cap | Retained metered artifact/child-output bytes / cap |
|---|---:|---:|
| T26 | 13 / 64 | 263,388 / 2,000,000 |
| T27 correction | 13 / 64 | 337,196 / 2,000,000 |
| T28 | 16 / 64 | 470,244 / 2,000,000 |
| T29 | 16 / 64 | 675,529 / 2,000,000 |
| T30 | 18 / 64 | 739,284 / 2,000,000 |
| T31 | 18 / 64 | 894,737 / 2,000,000 |
| T32 | 18 / 64 | 913,767 / 2,000,000 |

These are each run's shared routine-suite controller/child/artifact figures, under the existing 120-second admission/owned-child boundary. Separate task ledgers include earlier red/green/mutation/quality attempts and review overhead. T31's documented Ruff-child correction remains explicit; T32 finished at **42 conservative charges / 48 prepaid / 64 ceiling**, with **1,163,397 conservative retained bytes / 2,000,000** in its closed ledger. These meters do not count every temporary database byte or provide general native-code confinement.

| Separately approved native run | Outcome and scope | Limits retained |
|---|---|---|
| T27-S1 | Preflight stopped before native inference; preserved failed allocation | Not a model/cleanup success; corrected via a new package |
| T27-S2 | Real two-document/one-query embeddings; owned teardown/free port; cancellation after listener admission | 34 charged starts, ten HTTP attempts; no answer-quality or active-inference cancellation result |
| T29-N1 | One real pinned DLL load, expected rank/arithmetic, SQL-load denial, integrity `ok`, worker reaped | Two prepaid Python starts; synthetic embeddings, no Ollama inference |
| T30-N1 | Actual pinned Qwen answer contains 42, supplied-only IDs, exact saved exchange after reopen, port released | 18 charged starts/five HTTP attempts; fixture retrieval/index vectors, no combined real-model search |

All four native allocations remain closed. Preserve their ledgers/claims/receipts and original source seals rather than resealing them for current code. Offline status is the operator's attestation; no independent packet trace, full memory peak or broad quality score is inferred. Eighteen retained native receipt hashes and the T30 seal were verified unchanged at T32 closeout. Worker tokens are never copied into committed documentation.

These are recorded implementation/native checks, not new application/model tests run to create this summary. The summary closeout uses actual Git inventories, report cross-checks, local-link/whitespace and readable-diff review. No source regression suite or consumed native trial was rerun merely for this documentation request.

## 4. Current Status and Next Step

**Implemented and committed:** source-preserving chunks; pinned embedding/owned runtime boundaries; schema-v5 canonical vector storage/recovery; selected-source retrieval; schema-v6 selections/intents/exchanges; typed grounded generation and bounded history; safe current-source citation previews; historical-source availability; and observable support signals. Actual native embedding, DLL and chat bridges have separately bounded evidence. Current storage schema is v6; no new runtime dependency or global installation was added.

Across the listed T26–T32 source/result/decision commits, Git records **65 new authored files** and updates to **16 pre-existing files**: **81 distinct task files**, excluding the separately requested summary/status handoff. Native model assets, user originals, local databases, run receipts and generated review artifacts remain outside Git.

**Still to implement/verify:** the browser interface, complete saved-chat list/reopen/rename flow, combined real-model CSV relevance/grounding evaluation, exact input fit, required PDF/XLSX/scanned-PDF ingestion, library/lifecycle and final resource/offline/acceptance evidence. Valid IDs/quotes and one correct smoke answer do not independently establish per-answer meaning. Byte limits and response token counts do not prove exact input fit. Stage 1 remains active; no Stage 2 transition was approved.

The user explicitly **skipped T15/UI UX Pro Max review and use**. Do not research or install it in the next session. The approved minimal local HTML/CSS/JavaScript stack and Design 1/2 references remain, with manual keyboard/focus/labels/contrast/loading/error/source-preview review under T33.

The next implementation task is **T33 — Deliver the local browser CSV chat flow**. **It is unstarted and reserved for a new session at the user's request.** The next session should inspect current [AGENTS](../../AGENTS.md), [SPEC](../../SPEC.md), [PLAN](../../PLAN.md), [TODO](../../TODO.md), [contracts](../contracts.md) and [T32 evidence](../benchmarks/t32-evidence-support.md) before implementation. This summary does not start T33 or approve another source commit/native trial.

After T34 completes saved-chat restart/reopen and CP12, perform **T34A — initial CSV validation before format expansion**. Its approved placement/scope covers selected-Ollama input boundaries and the actual local embedding/retrieval/generation/citation/saved-chat path against fixed authored CSV ground truth. Prepare exact pins/fixtures/settings/shared budgets/controls/offline conditions and obtain the separate bounded-execution decision before a native run. Preserve failure denominators and report any unsupported exact-fit guarantee honestly. No standalone tokenizer/private bridge/custom build, new model or runtime semantic verifier is implicitly selected. T48 still provides the final all-format quality/resource evaluation; benchmark success will not independently verify every future answer.

**Stopping point:** the approved implementation/decision commit and explicitly requested summary/status commit complete this session. Earlier summaries and historical checkpoint files are unchanged. T33, T34 and T34A have not been executed, and no new research, installation, inference or stage transition is authorized by this handoff.
