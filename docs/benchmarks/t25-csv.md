# T25 — CSV normalization and scoped source previews

Date: 2026-11-20 (Asia/Calcutta). The user instructed continuation after T24 commit `0e4502f`, authorizing T25. Work was split into sequential parser/provenance (T25-A), transactional storage/recovery (T25-B) and API/preview/status (T25-C) increments. Implementation used the repository incremental-implementation, TDD, API, quality/security and documentation workflows. No dependency/download, model/OCR execution, private sample reading, historical evaluation rerun, stage transition or T26 work occurred. The user explicitly approved the reviewed T25/CP09 closeout and seventeen-file commit on 2026-11-20. T26 is reserved for a new session.

## Extraction and provenance

The existing standard-library UTF-8/optional-BOM, comma-delimited strict CSV path remains the supported dialect. The first logical record is the header; there is no delimiter/encoding/header sniffing or numerical/formula evaluation. Original bytes remain immutable. Shared validation now yields decoded records and inclusive physical-line spans to both admission and extraction. Quoted delimiters and CR/LF sequences remain decoded cell text, rather than creating additional data records.

`CsvExtractor` emits one T21 `SourceUnit` per data-column position. Each is a two-row, one-column table containing the actual header and data cell, with its original positional column/record identity. Grouping units by data record and original column reconstructs relationships without flattening them into an ambiguous sentence. Values remain verbatim strings; missing cells are `None`, distinct from explicit empty strings. Duplicate/blank headers are preserved by position. Extra data columns have no invented header. Blank data records retain their record number/physical span and missing-cell warnings. A header-only file or a file with no nonblank data values fails as `EMPTY_CSV`; invalid syntax/encoding/control bytes remain `INVALID_CSV`.

For the authored multiline fixture:

| Data record | Original column | Decoded value | Physical lines |
|---|---|---|---|
| 1 | 1 / Name | Apex, West | 2–2 |
| 1 | 2 / Units | 10 | 2–2 |
| 2 | 1 / Name | Line + newline + Break | 3–4 |
| 2 | 2 / Units | 20 | 3–4 |

Present data cells retain exact record/column/line anchors. A missing cell is coarse, with an explicit absence limitation. Header cells retain their own physical span and column position with coarse precision: the T21 model reserves positive record numbers for data, so no fabricated header data-record number is introduced. Decoded text has an explicit mapping limitation because raw CSV byte/quoting offsets are not retained. Formula-looking text and hostile instructions are inert strings; `formula` remains null for CSV.

Unit IDs are deterministic within an extraction generation, using record/column coordinates. The normalized envelope records logical document ID, original SHA256, display label, CSV format, extraction/normalization versions and warnings. Units record the actual Python/CSV parser identity/version and native method. Header warnings apply to the document; row-width warnings apply only to affected units. A regression exposed and fixed warnings incorrectly carrying over to later valid rows.

## Transactional normalized storage

Schema v4 adds `csv_extractions`, `csv_units` and `csv_requests`; exact v1/v2/v3 schemas migrate while preserving earlier identity/reference data. The envelope is stored without its units array; separate ordered unit rows hold complete serialized T21 models. Tests reconstruct and validate a complete `NormalizedExtraction` from these rows. Complete source values remain stored even when previews are truncated. This is CSV-derived storage in the existing local SQLite database, separate from original-file bytes; it does not select a storage layout for later format-specific image/render artifacts.

An idempotent request, scoped to the chosen reference, commits a generation intent before parsing. All normalized units and the complete-generation marker then commit in one transaction. A failed/crashed transaction cannot expose a partial extraction. A unique complete-version key prevents duplicate successful work for one logical document/version/parser; additional keys bind to that completed generation. A recorded failed key never silently starts again; after recovery, a deliberate new key can create another attempt. Equal-byte exclusive documents keep separate logical generations and access scope; existing library-reference ownership is preserved without claiming a library-upload feature now.

SQLite storage avoids another filesystem publication/reconciliation boundary for CSV cells. The trade-off is a longer write transaction and potentially substantial cache/CPU use; full-size/target-machine latency and memory remain unverified. Work streams units rather than building a full-document tuple. At most one heavy operation holds the existing store lease. Hash reads run on a local worker thread without SQLite access; the event-loop thread owns all database writes. Every 64 units the parser yields so status can be polled. Other mutations/previews refuse busy rather than entering a nested transaction.

Before each unit insert, `reserve_growth` uses the actual serialized unit/preview lengths to allow conservative row/index growth (four payload lengths plus sixteen pages), subject to the existing `other_processed + 4 * maximum_database_bytes + 1,048,576 <= 5,000,000,000` main/journal envelope. SQLite enforces the page ceiling. Tests expand that ceiling twice inside a real transaction and verify rollback, and retain the original small-metadata SQLITE_FULL control. Retained journals/free pages remain charged; no automatic vacuum, eviction or pruning occurs. This is not a full-cap capacity or native-memory proof.

Original size/hash are checked before extraction, before publication and before every preview. Missing/changed originals block cached previews instead of recreating a source or silently trusting old derived text. One startup pass resolves the single interrupted extraction intent after SQLite journal rollback. If a failure/recovery record cannot be written, the root reports pending recovery, blocks admission and retains readable safe status; restoring capacity and restarting resolves it. No committed original or previous complete generation is deleted by extraction failure.

## API and preview contract

After obtaining the existing Origin/CSRF safeguards, send an empty-body `POST /api/conversations/{conversation_id}/references/{reference_id}/extractions` with `Idempotency-Key`. The reference must belong to that conversation and identify a validated CSV original. Success is 202 with extraction/operation/document IDs, actual record/unit counts, warnings, `state: awaiting_index`, `ready: false` and `indexed: false`. Unexpected bodies, content encodings, options/query parameters and invalid IDs/keys are refused without echoing their values.

`GET` on the same reference's `/preview` route accepts only numeric `after` (default 0, maximum signed 64-bit) and `limit` (default 20, maximum 50). Results contain at most 65,536 UTF-8 JSON-body bytes, including the `data` envelope, and a numeric `next_after` cursor when more units remain. Each header/value snippet retains at most 256 original UTF-8 bytes before HTML escaping; truncation flags are explicit and Unicode boundaries remain valid. Complete normalized values are not shortened. Preview records include unit ID, logical record, original column, physical/header spans, precision/limitations, warnings and escaped header/value strings. Pagination never splits a unit or fabricates a continuous quotation.

Access resolves the explicitly requested reference and conversation before reading any source. There is no path, filename, raw hash or caller-supplied source URL lookup. This route does not implement saved-citation IDs or a conversation-wide selection/revision UI; the single requested eligible reference is the preview scope. Unrelated/unknown references return 404, missing/corrupt originals 410 and not-yet-extracted sources 409. Responses remain no-store, nosniff and CSP protected. This is an escaped JSON source-preview API, not a completed browser UI.

The operation endpoint now accepts scoped extraction IDs as well as upload/batch IDs. Status shows `extracting`, then `awaiting_index`; failed extraction is disclosed alongside the retained original. Batch original-storage counters remain accurate after extraction, with a separate extraction-failure count. Pending recovery is not misrepresented as an actively running parser. No source is marked indexed/ready before later chunking/embedding/index work.

## Verification and review

Tests first failed for the absent parser, growth reservation, schema-v3 migration support, extraction/preview implementation and routes. Actual failure after an uncommitted unit insert rolls back all units and preserves the original. Two Python children use `os._exit(23)`: one after an uncommitted normalized insert, the other after complete-generation commit but before acknowledgement. Reopen finds zero partial units and an interrupted intent, or preserves all committed units, respectively. Both pass `integrity_check=ok`; old failed keys stay failed, and deliberate new-key recovery produces exactly one complete result.

The 32 new tests (10 parser, 22 storage/API) cover quoted/multiline/BOM/CRLF values, duplicate/absent headers, missing versus empty cells, inert formulas, empty/invalid data, exact/coarse anchors, full model reconstruction, idempotence, migration, growth/rollback/crash recovery, scoped access, missing/corrupt source refusal, escaped/bounded pagination, complete large-cell storage, status during a transaction, mutation/busy guards, CSRF and payload privacy. A real quota/failure-record control verifies pending recovery rather than falsely reporting active extraction.

The existing actual loopback smoke now demonstrates upload → extraction → preview with actual record-1/physical-line-2 anchors and values A/12, alongside valid/bad/batch upload/status checks. This uses authored fixtures and missing model paths. No user sample or actual model/OCR engine is involved. The UI/browser frontend and physical-16-GB/full-size proof remain later gates.

Review temporarily inverted conversation equality in source resolution. The unrelated-reference test failed as expected; the original source was restored and its Git blob hash matched the pre-mutation value. Correctness/security review traced original verification, parameterized scope queries, immutable source identity, structured provenance, atomic publication, growth bounds, escaped previews and safe errors. No new third-party code or outbound document transport was adopted.

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe -m pytest -q -rP -p no:cacheprovider
.\.venv\Scripts\ruff.exe check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration
.\.venv\Scripts\ruff.exe format --check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration
git diff --check
```

Final suite: **241 passed, 1 skipped, 1 warning in 44.49 seconds**. The retained skip is the Windows symlink-permission test; the warning is the existing Starlette/HTTPX test-client deprecation. Ruff lint/format passed across 29 Python files. Final shared routine meter: **13/64 starts; 263,388/2,000,000 retained factory-artifact/child-output bytes**, within its 120-second admission/child boundary. New crash children share the same session meter as controls/regressions. This is not a native/model allocation or a meter for all temporary SQLite bytes. All generated source/database artifacts remain ignored. No real 100 MB or full-class-cap benchmark was run.

## Reviewable change map and remaining limits

| Before | After | Files |
|---|---|---|
| CSV syntax admission only | Shared validated rows and streaming typed cell/provenance extraction | `app/ingestion/validation.py`, `app/ingestion/csv.py` |
| Schema v3 and small metadata growth only | Exact migration to v4, versioned atomic CSV generations/requests/units and per-unit growth reservation | `app/storage/database.py`, `app/storage/files.py`, `app/storage/extractions.py` |
| Upload/batch status awaiting extraction | Explicit extraction trigger, reference-scoped bounded preview and honest derived status | `app/api/sources.py`, `app/main.py`, `app/ingestion/processing.py` |
| No real extraction/preview checks | 32 new tests, expanded actual loopback walkthrough and two additional exit cases | `tests/unit/test_csv_extraction.py`, `tests/integration/test_source_preview.py`, `tests/integration/test_uploads.py` |
| T24 current | T25/CP09 evidence, API/storage trace and approved closeout | README, PLAN, TODO, contracts, architecture ADR, this report |

UTF-8/comma/header conventions remain explicit; broader dialect/encoding robustness belongs to T39. Raw byte offsets, saved-citation resolution, conversation-selection revisions, library mutation, frontend UI, retrieval/model quality, chart semantics, general deletion/cancellation, full-size performance, hard parser deadlines and physical-16-GB/disconnected-runtime acceptance are not claimed. Hash checks/reparse guards do not confine hostile same-account replacement races. Pending metadata or a growth refusal is visible, not permission to delete originals or reduce the approved upload limit.

The user approved this seventeen-file closeout and commit on 2026-11-20. Its scope preserves unrelated untracked files and excludes runtime data, generated documents/databases, review artifacts, model assets, secrets and historical session/checkpoint files. Readable full diff: `data/reviews/t25.diff`. Host `/status` and `/compact` tools are not exposed; neither was run. Durable progress/evidence belongs in TODO/PLAN and this report. A separate session summary was explicitly requested; T26 remains for a new session.

Local Markdown targets and tracked/new-file whitespace checks passed. Only closeout documentation changed after the final passing suite. Schema downgrade/automatic repair is not implemented; older application versions refuse a newer schema rather than deleting derived data to make it fit.
