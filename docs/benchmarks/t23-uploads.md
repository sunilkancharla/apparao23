# T23 — Validated CSV conversation attachments

Date: 2026-11-20 (Asia/Calcutta). The user explicitly requested T23 using the repository incremental-implementation and test-driven-development skills, after T22 implementation commit `57973a6` and session-summary commit `beed4c5`. This implements the accepted G2 upload/security/storage contracts using the existing Python/FastAPI/SQLite environment. No installation, model/OCR execution, private sample reading or historical evaluation rerun occurred. The user explicitly approved the reviewed T23 closeout and thirteen-file commit on 2026-11-20.

## Implemented path

`GET /api/session` supplies an unpredictable token held only by the running app instance. `POST /api/conversations/{conversation_id}/attachments` requires the configured Host, exact Origin and `X-CSRF-Token`, a client `Idempotency-Key` (16–128 ASCII letters/digits/underscore/hyphen), and a percent-encoded UTF-8 `X-Filename`. Content is a raw CSV body with `Content-Type: text/csv` or `application/octet-stream`; an optional UTF-8 charset is accepted. Content encodings, duplicate required metadata, malformed lengths and invalid UUIDs are refused before body processing. There is no multipart dependency or upload-from-URL path.

The conversation must already exist through the T20 trusted backend interface. There is no public conversation-creation UI/API in this task. Display names never become paths. Validation rejects traversal, Windows separators/device names/alternate streams/invalid characters, control characters and unsafe trailing characters. The complete file is checked as UTF-8, with an optional BOM and comma-separated strict CSV syntax. Common PDF/ZIP/OLE/HTML mismatches, invalid encoding/control bytes, malformed quoted records and empty text are refused. CSV has no authoritative signature: plain single-column text can be valid CSV. This is syntax admission, not normalized extraction or semantic table validation; broader dialects/encodings and source previews remain T25/T39.

Body bytes are hashed incrementally and written in at most 65,536-byte slices. A chunk that would exceed 100,000,000 total bytes is refused before writing that chunk; declared length alone never admits a file. Supplied lengths must also match the observed total. Formula-like cells, filenames and document instructions remain inert data.

The upload root is held by one OS file lock per app instance; a busy stream refuses concurrent admission. SQLite schema v2 adds durable upload intents, key digests, metadata, publication IDs, ownership flags and reservations, with a unique conversation/key constraint and at most one unresolved active upload. Exact v1 schema migration preserves existing identity/reference rows; foreign/damaged schemas remain refused. The separate display label persists on its upload record. No ORM, vector extension or general lifecycle schema is introduced.

The server persists an intent before staging. It validates and flushes the staged file, records the verified hash/size and promotion ownership, then publishes an immutable SHA256-named original. Windows rename refuses overwrite of an existing target. Reuse requires matching content metadata and an actual original-file size/hash check. Content identity can share physical bytes across conversations, while document/reference UUIDs and visibility remain separate. Final reference creation and `original_stored` publication commit together. The 202 receipt has `indexed: false`; it does not claim queued/ready ingestion, extraction, embeddings or answers.

Completed retries consume/hash the incoming body before comparing both filename and actual content identity. Matching retries return the same receipt without another reference; different payloads return 409. Pending/failed keys cannot recreate effects. A missing/corrupt committed original is unavailable, not silently restored. Ten logical references include new same-byte attachments; verified replay consumes none.

## Reservation and recovery implementation

Each new intent reserves the full 100,000,000-byte original allowance and the same temporary allowance before any body file is created. Admission counts actual managed logical file lengths, with unique SHA256 originals charged to the library class if required by a library identity, otherwise to conversation originals. The existing 1 GB library, 10 GB conversation-original and 1 GB temporary caps are unchanged. Worst-case reservation can refuse a smaller or duplicate upload near a class cap before its hash is known; the implementation does not promise that every smaller request will fit.

For each short metadata transaction, processed accounting includes all remaining managed files, database lengths, retained free pages and journals. The connection limits growth to at most sixteen extra SQLite pages and further reduces that ceiling so `other_processed + 4 * maximum_main_database_bytes + 1,048,576 <= 5,000,000,000`. This conservatively reserves the main database and rollback-journal envelope, including ledger growth. DELETE/FULL remains required; ATTACH is denied, upload writes use no savepoints, cache spilling is disabled and temporary SQLite work stays in memory. Initial database creation/migration is bounded before its transaction as well. This is an implementation reservation, not a new processed-data cap, journal-mode adoption or permission for unbounded future SQL. New writers/batch/vector work must preserve or revalidate this envelope. No automatic vacuum, pruning or eviction occurs.

[SQLite documents the page-growth refusal mechanism](https://www.sqlite.org/pragma.html#pragma_max_page_count) and [rollback-journal recovery](https://www.sqlite.org/lockingv3.html#the_rollback_journal). Tests exercise actual SQLITE_FULL/rollback with a deliberately oversized metadata insert. They validate this small upload write path, not general 5 GB capacity or every possible SQLite statement/VFS.

On controlled failure/cancellation, cleanup first records `cleanup_pending`, removes only paths owned by the durable intent, and preserves originals required by surviving documents. A new promoted original is removed only after hash/size verification and a live-reference recheck. Reservations are released only after cleanup succeeds. Failure leaves the record/charges and blocks admission. Startup performs one pass over the single unresolved upload after acquiring exclusive root ownership; it cleans an interrupted staging/promotion or leaves storage unavailable if cleanup cannot be verified. Unknown files are counted and preserved, never swept. Successful committed uploads remain intact. This does not implement conversation/library deletion or secure erasure.

The root must remain private and stable under the same-account operator. Reparse/hardlink checks and OS ownership do not confine a hostile process running as that operator. POSIX compatibility branches are present but only Windows was exercised. Streamed byte limits and serialized admission are implemented; no full-size latency/RAM proof, general ingestion worker timeout or physical 16 GB acceptance follows.

## Verification

Tests first failed on the absent validation module, then on the absent session/upload path, durable admission and restart cleanup. The validation slice passed 22 cases before storage/API integration. Later failure injection exposed incorrect mapping of all metadata errors to quota exhaustion; actual SQLITE_FULL is now 507 while ordinary metadata failure is 503. Restart accounting was corrected to avoid counting the main database twice in its reservation. A temporary reintroduction of that defect made the new reopen test fail; the correct source was restored before final verification.

The 58 new tests cover filename/content/header controls, BOM/quoted multiline/inert formulas, stored original/reference trace, isolation/deduplication, verified replay/conflict, logical count limits, quota refusal, exact/over-bound streamed size using a reduced test constant, mismatched lengths, partial disk-write failure, metadata failure after promotion, cancellation, retained cleanup charges, hardlinked storage refusal, root ownership, v1 migration, actual SQLite growth refusal, missing originals and concurrent admission.

Two Python children exit with `os._exit(23)` at publication boundaries. The first exits after inserting content within the uncommitted publication transaction; reopen rolls that insert back, removes its uncommitted promoted original and leaves no reference. The second exits after the publication commit and before returning its receipt; reopen preserves the original/reference. Both reopen with `integrity_check=ok`. A separate actual Python launcher accepts a valid upload and rejects a malformed upload over loopback HTTP using missing model paths. Captured output contains neither the synthetic private marker nor its CSRF token. These are actual process/socket checks, not mocks standing in for crashes or HTTP.

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe -m pytest -q -rP -p no:cacheprovider
.\.venv\Scripts\ruff.exe check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration
.\.venv\Scripts\ruff.exe format --check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration
git diff --check
```

Final suite: **181 passed, 1 skipped, 1 warning in 13.95 seconds**. The skip is the existing Windows symlink-permission test; independent attribute and hardlink checks remain active. The warning is the existing Starlette/HTTPX test-client deprecation. Ruff lint/format passed. The shared routine meter reports **9/64 starts, 263,060/2,000,000 retained factory-artifact/child-output bytes**, inside its 120-second admission/child boundary. All regression/negative-control children share that session meter; it is not a native/model trial allocation or a meter for every temporary SQLite byte. Generated test databases and tiny uploads remain ignored. The pytest setup now creates its missing ignored `data/test-runs` parent before selecting a fresh child directory; initial runs exposed that pre-existing clean-checkout issue.

No real 100 MB file was generated within this routine artifact allocation. The production decimal bound is checked at the header boundary and the same streaming comparison is tested at exact/over limits with an eight-byte allocation. Large-file throughput, disk-full hardware behavior, power-loss durability, broad CSV encodings/dialects, library mutation, batch/status operations, extraction/previews and model/offline acceptance remain later work. T24 has not started.

## Reviewable change map

| Before | After | Files |
|---|---|---|
| Read-only diagnostics; all mutations denied | Same-origin/token-checked single CSV POST and safe 202 receipt | `app/main.py` |
| Content metadata only; no uploaded bytes | Server-owned originals, stream validation, durable retry/reservation/cleanup | `app/storage/files.py`, `app/ingestion/validation.py` |
| Exact schema v1 only | Exact v1→v2 migration, upload intent constraints and optional page bound | `app/storage/database.py` |
| No upload boundary regression coverage | 58 upload tests, schema-version-aware existing test, clean-parent fixture setup | `tests/integration/test_uploads.py`, `tests/unit/test_document_storage.py`, `tests/conftest.py` |
| T22 current status; upload contracts only proposed as behavior | Verified T23 API, constraints/evidence and approved closeout | README, PLAN, TODO, contracts, architecture ADR, this report |

The user approved this thirteen-file closeout and commit on 2026-11-20. Its scope excludes unrelated untracked files, generated documents/databases, runtime roots, secrets and model assets. Correctness, readability, architecture, security and resource review found no unresolved issue within this single-original task; the limits above remain explicit. SPEC, AGENTS, dependency/lock files, historical evidence and session-checkpoint/session-summary files are unchanged.

Local Markdown link targets and tracked/new-file whitespace checks passed. A complete readable unstaged patch is retained outside Git at `data/reviews/t23.diff`. No host `/status` or `/compact` tool is exposed; neither was run. Durable task/evidence status is in TODO/PLAN and this report.
