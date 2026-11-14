# T12 — Proposed local storage and search evaluation

**Status: PartA package and five proposal documents' commit approved.** The user explicitly said "i approve the package and commit". The approved model/OCR shortlist is committed in `48f0333`. This authorizes only the bounded evaluation described below, not runtime index selection, optional-extension installation or application coding. Stage1 remains PDF/XLSX/CSV, Windows11,16GB, CPU-only, local processing. The requested-decision paragraph below is historical; later source/results commits retain a separate approval gate.

## Question and alternatives

Keep SQLite for document metadata and saved chats, as approved. Determine the simplest adequate way to persist/search vectors alongside document/conversation references and recover safely after interruption.

| Option | Proposed representation | Benefit | What must be demonstrated |
|---|---|---|---|
| A — baseline | SQLite tables with validated768-dimensional float32 vector BLOBs; bounded Python exact cosine search over eligible rows | Existing standard library, one transaction boundary for rows/references/vectors, no new search dependency | Query time at scale, memory use, scoped search, version checks, recovery and original-file reconciliation |
| B — optional candidate | SQLite metadata plus `sqlite-vec`0.1.9 native extension and its vector tables | Potentially moves vector search into the database | Exact artifact/source/notice review, Windows/Python loading, correct scoped ranking/transactions/deletion, time/RAM/disk measurements |

OptionB is a candidate for review, not an assumed performance improvement or an approved extension load. Do not introduce a standalone server, graph search, cloud service or framework database. A separate sidecar vector file is a design alternative to discuss if evidence justifies its added coordination/recovery cost, not an additional implementation in the first package.

Public primary-source checks for this proposal: [Python sqlite3 documentation](https://docs.python.org/3.14/library/sqlite3.html) describes disk-backed SQLite without a separate server; actual interpreter/SQLite version and build flags must be recorded locally. [sqlite-vec upstream v0.1.9](https://github.com/asg017/sqlite-vec/tree/v0.1.9) and [its registry release](https://pypi.org/project/sqlite-vec/0.1.9/) identify the candidate. The registry lists a WindowsAMD64 wheel and MIT/Apache license metadata, but its description/homepage are placeholders and the wheel is marked without provenance. This is insufficient for trust, compatibility or redistribution acceptance. Do not substitute a fork, alpha, newer version or source build without review.

## First proposed package: baseline experiment and optional-dependency review

Approve **64 shared process starts/attempts and45active minutes**, excluding human/host approval waits, in a fresh ignored `data/t12/storage-baseline-01/`. Preallocate initial inspection/initialization starts before the first command. Category ceilings: preparation16, tests/negative controls16, measured workers16, reporting8, protected cleanup8. No borrowing, resets, automatic continuation or uncounted subprocesses. Stop on exhaustion/failure and retain partial evidence. Link unchanged completed combined-07 meter/seal and approved shortlist source identities; never modify those records.

Use the existing project Python3.14.6 and its `sqlite3`, `struct`, `math`, hashing and file utilities. Record actual SQLite version/compile options; no optional SQLite extension loading in this package. No lock/dependency/global/PATH change, package installation, native OCR/model execution, API call, new embeddings, real user samples or old raw corpus/vector access. Public optional-dependency source/metadata review is limited to40requests/8MiB, without document content, installation or execution; keep any source receipts in this allocation. If additional artifact inspection/download is needed, propose its exact hash/size/permissions first.

For baseline workers: serial execution, at most one owned worker plus its controller,2GiB aggregate owned job cap,512MiB controller-private limit, at least4GiB available system RAM,120-second per-worker timeout and512MiB total generated artifacts including database/journal/synthetic originals. Sample memory/headroom at100-ms target cadence with300-ms hard observation gap; report software sampling versus independent job enforcement. Supervisor, crash-control and teardown failures stop without retry. No sockets or external service are needed for these workers; keep document processing absent and imports restricted to reviewed standard-library code. This does not certify arbitrary native dependency containment.

### Frozen synthetic workload and measurements

- Generate deterministic seeded768-dimensional float32 vectors at32,1000and10000rows and12queries per size, with one first pass and three repeated passes. Record seed/generator version, byte hashes, vector validation/normalization and tie rule. These are Nomic-shaped synthetic numbers, not Nomic-generated embeddings or semantic-quality evidence. Raw10000-row vectors occupy30,720,000bytes before metadata/database overhead; this is not a library-capacity prediction.
- Create two conversations, a reusable library document referenced by both, an exclusive attachment per conversation, duplicate-byte uploads with different ownership, and distinct extraction/model versions. All fixture bytes are newly authored synthetic placeholders within the run root. Use nominal PDF page/XLSX sheet-cell/CSV record-column-line anchors as metadata; do not claim ingestion/parsing was tested.
- Compare eligible top5IDs and distances to a separately implemented exhaustive reference over the same frozen float32 values. Require exact scope membership and deterministic tie IDs, and distance agreement within1e-6. Invalid dimensions/nonfinite/zero-norm vectors and incompatible model/prefix/extraction versions must fail explicitly. Use a deliberately closer excluded-document vector as a scope-leak control. Rank within authorized scope before taking topK.
- Measure first/repeated query latency (median/max and all12sample values), insertion/transaction/rebuild/restart time, peak owned/controller memory and database/journal/disk bytes. Freeze timing boundaries before measurement. Accept a result as measured, not as proof of product latency targets. A120-second timeout leaves that scale incomplete; do not shrink data or increase limits silently.

### Integrity, ownership and recovery checks

Test-first: repeat insertion is idempotent; content deduplication does not merge ownership or expose another conversation's attachment; deleting a synthetic conversation removes only its exclusive references/content according to the fixture's declared test operation; shared library bytes remain. Warn/block referenced library removal, preserving the approved rule. Reject corrupt vector bytes, unsafe paths and missing originals with explicit non-ready state; never retrieve orphaned/incompatible rows.

Exercise successful commit, explicit rollback and **actual owned worker termination** before commit and after commit, then reopen using a separate counted worker and check exact row/reference/vector invariants and SQLite integrity. Distinguish injected exceptions from process-crash evidence; do not claim power-loss durability. For synthetic original-file/database boundaries, test interruption after file creation/before database commit, and after database commit/before cleanup. Design explicit pending/ready states and owner-tagged reconciliation; never scan/delete outside the synthetic root or auto-delete unknown files. Derive/rebuild disposable vectors from frozen fixture inputs, preserving stable source references and version separation. Journal/WAL settings and checkpoints must be recorded, not silently tuned between passes.

These are scoped test operations, not an approved product retention policy. Keep historical messages/quotes/citations as opaque synthetic records; report their unresolved lifecycle rather than inventing deletion/secure-erasure behavior. Any later retention-dependent implementation waits for the user's decision.

## Ordered atomic tasks

| ID | Prerequisites / objective | Acceptance and verification |
|---|---|---|
| T12-A1 | Exact package approval; establish allocation and fixture contract | Initial commands reserved, old identities unchanged, hardware/SQLite recorded, frozen workload and reference rules saved; source scope/worker caps reviewed before execution |
| T12-A2 | A1; write meaningful baseline correctness controls | Failing tests for vector validation, eligible ranking, duplicate/reference/version semantics and crash outcomes; no external services/dependencies |
| T12-A3 | A2; minimum evaluation-only adapter | At most three authored evaluation files (`storage_trial.py`, `test_storage_trial.py`, fixture manifest); passing scope/integrity tests and independently checked rankings, real counted termination/restart controls |
| T12-A4 | A3; bounded performance measurements | All three frozen scales measured or explicit partial/timeout outcome; complete counters/time/resource/disk observations; no automatic limit or fixture changes |
| T12-A5 | A1; inspect optional candidate without executing it | Exact upstream/version/source/license/maintenance/security/native requirements, outbound/startup paths, Windows wheel/build/load constraints and footprint reviewed; unavailable information remains explicit; propose artifact identities for later approval |
| T12-A6 | A4/A5; review and report | Full focused regressions/Ruff, privacy/security/diff review, owned teardown, prior hashes unchanged; factual `docs/benchmarks/storage-index.md`, README/TODO/checkpoint updates; separate commit request |

A5 may be done sequentially when earlier steps leave time; it does not authorize importing an extension. Document test/benchmark commands after verifying them. No app modules or product schema migrations. Package scope includes the three evaluation files, ignored fixtures/receipts and affected documentation only. PartA completion alone must not mark T12 complete or adopt OptionA.

## Later comparison and decisions

After PartA, present an exact optional-extension trial package only if the review supports it. It must pin wheel/source hashes, project-local installation/lock changes if any, local loading/permissions, shared budgets and the same frozen data/reference checks. Compare identical scope/precision/settings and cache limitations; never compare scoped exact search against unfiltered or approximate results as equivalent. Optional candidate rejection/unavailability is a documented outcome requiring review of how T12 closes, not an invented measured comparison. Final index/model adoption remains T17/G2.

Decisions still needed before product storage/lifecycle implementation:

1. Original-size byte conversion, counting/dedup enforcement and derived/temporary storage budgets under the settled100MB/file,10files and1GB library-original limits. The benchmark scales/caps above are experiment-only and require approval with this package.
2. Historical messages/quotes/citations, detached references, temporary outputs and derived-vector retention. Preserve approved exclusive-chat deletion/shared-library preservation and block referenced-library deletion; do not invent TTLs or secure erasure.
3. Representative product chunk volume and acceptable query/index/recovery time/memory targets after exploratory measurements. Synthetic10000vectors do not prove support for the approved maximum file/library sizes or physical16GB end-to-end acceptance.

**Requested decision:** approve or amend this64-start/45-minute PartA package and its experimental scales/resource caps. This covers baseline evaluation code/tests and bounded public optional-dependency review, with zero installation or native model/OCR execution. OptionB installation/comparison, product retention, runtime adoption and product coding remain separately gated. The five proposal documents' commit may be explicitly approved together with the package.

## Actual PartA outcome

Package approved and proposal committed `976455c`. [Evidence](../benchmarks/storage-index.md) records11passing focused tests and mutation detection, four real termination/reopen cases,32/1000-row measurements and a10000-row120-second worker timeout. Teardown verified; allocation closed, never retry/reset. Public optional review remained incomplete for binary/provenance and exact browser transport-byte accounting; no wheel was downloaded/loaded. T12 and G2 remain open. Later source/results commit and any exact-wheel review/PartB execution require separate approval.
