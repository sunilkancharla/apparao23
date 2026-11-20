# Session 3 — CSV Session Summary

Updated: **20 November 2026**. Scope: **T23–T25**, from commit **3dd27a1** through **ebbe77b**. Created at the user's explicit request, following the format of the [Session 2 backend summary](SESSION_2_Backend_Session_SUMMARY.md).

## 1. Session Overview

This session extended the backend foundations into a working local CSV path: validated original upload → conversation-scoped reference → durable batch/file status → structured extraction → bounded source preview.

The work added original-file storage, verified upload retries, quota reservations, batch manifests, per-file status, CSV provenance, transactional normalized storage and escaped JSON previews. Failure, interruption and scope checks were exercised with authored fixtures, actual loopback HTTP and deliberately terminated Python processes.

**T23–T25 are implemented and committed.** The user approved their closeouts and the T23–T25 backend checkpoint **CP09**. This is the CSV ingestion/preview portion of Stage 1, not the complete assistant. Chunking, embeddings/indexing, retrieval, grounded answers, saved citations/chat, other-format ingestion and the browser UI remain later work. Health continues to report **HTTP 503 / `ready: false`** until owned-model integration exists.

No dependency was added, no model/OCR engine was run, and no private evaluation original was read. SPEC, dependency/lock files and the prior session summaries were not changed. **T26 has not started; the user reserved it for a new session.**

## 2. Task-wise Work and Files

Each task records its purpose, implementation, evidence and limits. Expand its file list for individual descriptions.

**Created** means the file was added in that task's commit. **Updated** means an existing file changed. Shared source/documentation appears under every task that updated it. Generated source files, databases and review patches are described separately; they were not committed.

#### T23 — Upload a validated CSV conversation attachment

**Summary:** Provide a safe API path from one CSV upload to an immutable stored original and the correct conversation reference.

**Process:** Added Windows-safe display-name validation, complete UTF-8/BOM comma-CSV syntax checks, streamed size enforcement and SHA256 identity. Connected original storage to the existing ownership database. Added durable upload intents, byte reservations, verified request replay, publication and interrupted-upload cleanup. State-changing requests gained an unpredictable per-instance CSRF token alongside the existing exact Host/Origin checks.

**Outcome:** An existing conversation can receive a raw-body CSV attachment. Labels never become filesystem paths. Equal content can share physical original bytes while document/reference UUIDs and conversation visibility remain distinct. A completed retry must consume/hash the actual body before returning the original receipt; changed content conflicts. New same-byte attachments still consume logical reference slots. Success acknowledges `original_stored` with `indexed: false`.

**Limits enforced:** Decimal **100,000,000 bytes per file**, **ten conversation references**, and the approved original/temporary/processed storage classes. Each new upload reserves worst-case original/staging space before writing. Conservative reservation can refuse a smaller request near a cap. Only one application owner holds an upload root.

**Verification:** Added **58 tests**; the full suite reached **181 passed, 1 skipped, 1 warning**; Ruff passed. Checks covered unsafe Windows names/traversal, content mismatches, malformed CSV, streamed boundaries, scope/deduplication, verified replay, count/quota refusal, partial writes, cancellation and cleanup failure. A real local server accepted valid CSV and refused malformed CSV. Actual process exit before/after publication verified that an uncommitted original is cleaned while a committed original/reference survives.

**Review findings:** Metadata failures were initially reported as quota exhaustion; actual SQLITE_FULL is now distinguished from ordinary storage failure. Restart accounting was corrected to avoid charging the main database twice in its reservation; the regression detected a deliberate reintroduction. The fixture setup also now creates its missing ignored parent directory on a clean checkout.

**Limit:** This task stores originals and references; it does not extract/index them. CSV has no definitive magic signature, so valid single-column text cannot always be distinguished from renamed text. Real 100 MB throughput, full storage capacity, power-loss durability and physical-16-GB performance were not proved. Root guards do not confine a hostile process running as the same local account.

**Commit:** `3dd27a1` — Implement T23 validated CSV attachments and recovery.

<details>
<summary>Files associated with T23 (13: 4 created, 9 updated)</summary>

**Application source — Python**

- [app/ingestion/validation.py](../../app/ingestion/validation.py) — **Created.** Defines safe upload errors, Windows display-label checks and complete CSV syntax/content admission.
- [app/storage/files.py](../../app/storage/files.py) — **Created.** Implements one-owner original storage, byte reservations, streaming, verified reuse/replay and owned cleanup.
- [app/storage/database.py](../../app/storage/database.py) — **Updated.** Introduces schema v2 upload intents/reservations, exact v1 migration, optional page limits and safe full-disk error mapping.
- [app/main.py](../../app/main.py) — **Updated.** Connects managed upload storage, exposes the session token/raw-body attachment route and enforces mutation safeguards.

**Tests — Python**

- [tests/integration/test_uploads.py](../../tests/integration/test_uploads.py) — **Created.** Covers validation, actual stored bytes/scoped references, retries, failure cleanup, quotas and real HTTP/process-exit behavior.
- [tests/unit/test_document_storage.py](../../tests/unit/test_document_storage.py) — **Updated.** Checks restart persistence against the current schema version while retaining ownership/integrity assertions.
- [tests/conftest.py](../../tests/conftest.py) — **Updated.** Creates the ignored `data/test-runs` parent before choosing a fresh test root.

**Documentation — Markdown**

- [docs/benchmarks/t23-uploads.md](../benchmarks/t23-uploads.md) — **Created.** Records upload behavior, accounting, recovery, tests, review findings and limits.
- [docs/contracts.md](../contracts.md) — **Updated.** Documents the implemented single-original HTTP/security/storage subset.
- [docs/ADR/0001-stage1-architecture.md](../ADR/0001-stage1-architecture.md) — **Updated.** Records the original-storage/schema mapping and conservative reservation trade-offs.
- [README.md](../../README.md) — **Updated.** Describes verified upload behavior and startup/storage integration.
- [PLAN.md](../../PLAN.md) — **Updated.** Records T23 progress and the next implementation boundary.
- [TODO.md](../../TODO.md) — **Updated.** Records acceptance evidence, closeout and commit approval.

</details>

**Generated/local files:** Synthetic original/staging CSV files, upload lock files, metadata databases/journals and `data/reviews/t23.diff` were kept under ignored local roots. No uploaded original or database binary entered Git.

#### T24 — Expose batch upload and per-file processing status

**Summary:** Coordinate a bounded batch while reporting each file's outcome independently and preserving successful siblings.

**Process:** Added an idempotent JSON filename manifest, stable file-operation IDs, shared conversation-slot reservations and scoped status lookups. File bodies still stream individually through T23 with `X-Batch-File-Id`; no multipart/base64 dependency or worker framework was introduced. Added durable safe failure codes and explicit new-key retry after verified cleanup.

**Outcome:** A batch contains one through ten entries, within **32,768 observed UTF-8 JSON bytes**. Unsafe/unsupported labels fail individually, leaving valid siblings queued. Standalone uploads cannot take slots reserved by a batch. All ten reserved same-byte files can finish as ten distinct references over one physical original. Status remains available during blocked cleanup, while unresolved work prevents new admission.

**State and retry behavior:** Queued entries await body admission. Accepted attempts show processing, failure/interruption or cleanup pending; stored originals await extraction. A completed body replay still verifies its bytes. A known failed attempt can be retried deliberately with a new key after cleanup, but it must reacquire capacity. Unknown outcomes never silently run again. Unsubmitted queued entries retain their slots across restart; no automatic expiry/cancellation endpoint was added.

**Verification:** Added **28 tests**; the full suite reached **209 passed, 1 skipped, 1 warning**; Ruff passed. Tests covered mixed manifests, count/metadata bounds, shared slot accounting, atomic metadata rollback, scoped IDs, CSRF, retries, cleanup locks/restart and all-ten completion. The actual loopback smoke exercised mixed-success upload/status. Two additional abrupt-exit children verified that a receiving file is reconciled and a committed file is preserved, without losing its successful sibling.

**Review findings:** A standalone upload initially bypassed queued batch reservations; shared transactional admission fixed it, and a weakened limit was detected by its test. Specific failure codes replaced an unhelpful generic status. The existing T23 smoke test was corrected to handle connection timeout within its unchanged startup deadline, matching T19; its response assertions were retained.

**Limit:** This task supplies upload coordination/status, not extraction or index readiness. Successful originals remained `awaiting_extraction`; ready/indexed stayed false. Pre-admission quota refusal leaves the unstarted intent queued and reports the refusal in HTTP. General cancellation/deletion, full-size performance and final resource acceptance remained outside this task.

**Commit:** `0e4502f` — Implement T24 batch uploads and durable processing status.

<details>
<summary>Files associated with T24 (12: 3 created, 9 updated)</summary>

**Application source — Python**

- [app/ingestion/processing.py](../../app/ingestion/processing.py) — **Created.** Implements durable manifests, shared slot accounting, scoped file/batch status and truthful readiness fields.
- [app/storage/database.py](../../app/storage/database.py) — **Updated.** Introduces schema v3 batch/file/failure tables and exact migration from v1/v2.
- [app/storage/files.py](../../app/storage/files.py) — **Updated.** Binds attempts to manifest slots, persists safe failure reasons and keeps status readable during pending recovery.
- [app/main.py](../../app/main.py) — **Updated.** Exposes bounded batch creation, file binding and conversation-scoped operation polling.

**Tests — Python**

- [tests/integration/test_processing_status.py](../../tests/integration/test_processing_status.py) — **Created.** Exercises batch state/capacity, partial outcomes, retries, scope and real interruption/restart behavior.
- [tests/integration/test_uploads.py](../../tests/integration/test_uploads.py) — **Updated.** Extends the actual loopback smoke to batches/status and corrects the bounded startup wait.

**Documentation — Markdown**

- [docs/benchmarks/t24-processing.md](../benchmarks/t24-processing.md) — **Created.** Records transport/state/retry rules, reservation behavior, evidence and remaining limits.
- [docs/contracts.md](../contracts.md) — **Updated.** Defines the implemented manifest, operation-status and retry subset.
- [docs/ADR/0001-stage1-architecture.md](../ADR/0001-stage1-architecture.md) — **Updated.** Explains the raw-body/manifest approach and persisted reference reservations.
- [README.md](../../README.md) — **Updated.** Describes batch submission, status polling and recovery behavior.
- [PLAN.md](../../PLAN.md) — **Updated.** Records T24 progress and the next task.
- [TODO.md](../../TODO.md) — **Updated.** Records batch/status evidence and closeout approval.

</details>

**Generated/local files:** Ignored test databases hold manifest/attempt/failure rows, alongside synthetic original/staging files and `data/reviews/t24.diff`. No batch document, database or generated status artifact was committed.

#### T25 — Extract and preview CSV with record/column provenance

**Summary:** Complete the local CSV original → structured extraction → traceable bounded preview path.

**Process:** Split work into **T25-A** parser/provenance, **T25-B** transactional normalized storage/recovery and **T25-C** API/preview/status integration. Reused T21 models and the existing CSV validator. Added schema v4 generations/units/reference-scoped requests, per-unit growth reservation and explicit extraction/preview routes.

**Outcome:** The parser retains decoded values, logical record indices, original column positions and inclusive physical-line spans, including quoted multiline fields. Duplicate/blank/missing headers remain distinguishable; a missing cell is null rather than an invented empty string. Formula-looking strings remain inert. Each normalized unit is a small cell table that repeats its actual header with a separate source anchor. Complete unit models are stored separately from originals and can reconstruct the normalized extraction.

**Precision and text limits:** Present data cells have exact record/column/line anchors. Missing cells and header-only anchors carry explicit coarse limitations; no header data-record number or raw byte/quoting offsets are invented. Previews HTML-escape snippets, retain at most **256 original UTF-8 bytes** per header/value and label truncation, while keeping complete normalized values in storage. Pages default to 20 units, accept at most 50, and stay within **65,536 UTF-8 JSON-body bytes** with a continuation cursor.

**Storage and API behavior:** An extraction intent commits before parsing; all units and complete-generation publication then commit together. Size/hash checks protect both extraction and every preview. Cached normalized text is not served when its original is missing or changed. Reference membership is checked before content access; callers cannot supply a source path or raw hash. Successful extraction reports `awaiting_index`, with ready/indexed false. Status remains pollable during parsing; competing mutations/previews refuse busy.

**Verification:** Added **32 tests**—10 parser and 22 storage/API cases; the full suite reached **241 passed, 1 skipped, 1 warning**; Ruff passed across 29 Python files. Checks covered model reconstruction, large-cell preservation, Unicode-safe truncation, response-size pagination, scope, CSRF, missing/corrupt originals, idempotence, quota refusal and schema migration. Actual failure after a normalized insert rolled back every unit. Two additional abrupt-exit children verified uncommitted rollback/reconciliation and committed-result preservation, both with `integrity_check=ok`.

**Walkthrough and review:** The actual loopback smoke now verifies upload → extraction → preview, including values A/12 at data record 1, physical line 2. Review caught row-width warnings carrying into later valid rows and pending recovery being shown as active extraction; both were fixed. Deliberately inverted conversation scope was detected, then restored with a matching source hash. The user accepted the **CP09 backend evidence** with the T25 closeout.

**Limit:** The supported path remains UTF-8/BOM comma CSV with the first record as headers. This is an escaped JSON preview API, not the browser UI or saved-citation lookup. Conversation-wide selection revisions, broader dialect/encoding robustness, library mutation, chunking/indexing/model work and general lifecycle remain later tasks. Large-file latency/RAM, hard parser deadlines, physical-16-GB capacity and strict disconnected-runtime acceptance were not proved. Older application versions refuse schema v4; no destructive downgrade/repair was added.

**Commit:** `ebbe77b` — Implement T25 CSV provenance extraction and scoped previews.

<details>
<summary>Files associated with T25 (17: 6 created, 11 updated)</summary>

**Application source — Python**

- [app/ingestion/csv.py](../../app/ingestion/csv.py) — **Created.** Streams typed CSV cell tables with stable generation/record/column identities, actual line spans and explicit limitations.
- [app/storage/extractions.py](../../app/storage/extractions.py) — **Created.** Owns versioned/idempotent extraction, complete-generation transactions, recovery and bounded escaped preview material.
- [app/api/sources.py](../../app/api/sources.py) — **Created.** Exposes explicit reference-scoped extraction and numeric, bounded preview pagination.
- [app/ingestion/validation.py](../../app/ingestion/validation.py) — **Updated.** Shares validated row/physical-line iteration and canonical UUID validation with the new routes.
- [app/storage/database.py](../../app/storage/database.py) — **Updated.** Adds schema v4 extraction/unit/request tables and exact v1/v2/v3 migration.
- [app/storage/files.py](../../app/storage/files.py) — **Updated.** Supports reserved growth within streaming transactions and invokes interrupted-extraction recovery.
- [app/ingestion/processing.py](../../app/ingestion/processing.py) — **Updated.** Adds extraction operation/status, correct stored-original counters, derived failures and busy guards.
- [app/main.py](../../app/main.py) — **Updated.** Registers source routes and provides safe extraction/preview/recovery error messages.

**Tests — Python**

- [tests/unit/test_csv_extraction.py](../../tests/unit/test_csv_extraction.py) — **Created.** Checks value fidelity, table relationships, positional headers, record/line anchors, inert formulas and explicit errors.
- [tests/integration/test_source_preview.py](../../tests/integration/test_source_preview.py) — **Created.** Covers normalized storage/reconstruction, growth, rollback/crashes, scoped previews, response bounds, source integrity and API privacy.
- [tests/integration/test_uploads.py](../../tests/integration/test_uploads.py) — **Updated.** Extends the real loopback walkthrough through extraction and anchored preview.

**Documentation — Markdown**

- [docs/benchmarks/t25-csv.md](../benchmarks/t25-csv.md) — **Created.** Records provenance/storage/API rules, evidence, CP09 walkthrough and limitations.
- [docs/contracts.md](../contracts.md) — **Updated.** Describes the implemented CSV normalization, preview and derived-status subset.
- [docs/ADR/0001-stage1-architecture.md](../ADR/0001-stage1-architecture.md) — **Updated.** Records the SQLite generation-publication choice and its transaction/cache trade-offs.
- [README.md](../../README.md) — **Updated.** Documents extraction/preview requests, current schema and verified behavior.
- [PLAN.md](../../PLAN.md) — **Updated.** Records completed T25/CP09 and the new-session boundary for T26.
- [TODO.md](../../TODO.md) — **Updated.** Records T25-A/B/C acceptance, evidence and user approval.

</details>

**Generated/local files:** Authored test CSVs, schema-v4 databases/journals, normalized model/preview rows and `data/reviews/t25.diff` remain local/ignored. The full suite reused the prior synthetic fixture harness; no original document, normalized database, model asset or generated review artifact entered Git.

## 3. Verification Progress

| Task | New ordinary test cases | Full-suite result at closeout | Commit |
|---|---:|---|---|
| T23 | 58 | 181 passed, 1 skipped, 1 warning | `3dd27a1` |
| T24 | 28 | 209 passed, 1 skipped, 1 warning | `0e4502f` |
| T25 | 32 | 241 passed, 1 skipped, 1 warning | `ebbe77b` |

Together these tasks added **118 passing ordinary cases** to T22's 123-pass baseline. The existing Windows symlink-privilege skip and Starlette/HTTPX warning remain; they were not suppressed. Separate reparse/hardlink checks remain active. Ruff lint and format checks passed at each task boundary.

| Task closeout | Shared starts used / cap | Retained factory-artifact/child-output bytes / cap |
|---|---:|---:|
| T23 | 9 / 64 | 263,060 / 2,000,000 |
| T24 | 11 / 64 | 263,224 / 2,000,000 |
| T25 | 13 / 64 | 263,388 / 2,000,000 |

Each listed run used the shared routine-suite meter for supported controls/regression children, within its 120-second admission/owned-child boundary. It is not a general native/model process-tree budget, a meter for every temporary SQLite byte, or a way to terminate a hung pure-Python controller test.

These are recorded implementation checks, not new application test runs performed to write this summary. Documentation closeout uses consistency, Git inventory and link/whitespace checks. Temporary review mutations were restored before final verification. No product throughput, model quality or calibrated correctness result is inferred from test counts.

## 4. Current Status and Next Step

**Implemented and committed:** validated CSV originals/references; safe raw-body upload; durable batch/file operations; reservations and verified retries; structured CSV extraction; interrupted-operation recovery; and bounded, scoped, escaped JSON previews. Across T23–T25, Git records **13 new authored files** and updates to **9 pre-existing files**: **22 distinct task files**, excluding this separately requested summary.

**Still to implement/verify:** chunking, embeddings/indexes, selected-scope retrieval, local generation, grounded citations/evidence indicators, saved chat, the browser UI, additional-format ingestion and general lifecycle. Full-size/resource/offline acceptance remains outstanding. Stage 1 remains active; no Stage 2 transition was approved.

The next task is **T26 — Chunk passages without losing source structure**, using the T25 normalized units and approved T16 chunk/context policy. **T26 is unstarted and reserved for a new session at the user's request.** The next session should inspect current [AGENTS.md](../../AGENTS.md), [SPEC.md](../../SPEC.md), [PLAN.md](../../PLAN.md), [TODO.md](../../TODO.md), [contracts](../contracts.md) and [T25 evidence](../benchmarks/t25-csv.md) before implementation. This summary changes no product requirement or prior historical summary and does not authorize a stage transition.
