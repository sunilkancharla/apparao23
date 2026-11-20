# T20 — Minimal ownership and conversation storage

Date: 2026-11-20. The user explicitly approved the presented T20 scope after T19 commits `e99630a` / `a51900c`. This task implements the accepted C02/D04 identity/reference subset using existing stdlib SQLite, with no installation, dependency/lock change, HTTP mutation surface, model/OCR execution or historical trial rerun. This task authorization did not include a stage transition or Git commit; the user separately approved the reviewed nine-file closeout and commit on 2026-11-20.

## Implemented behavior

`app/storage/database.py` creates/opens `metadata.sqlite3` within a trusted backend-configured managed root. Root and database/journal sidecar ancestry are checked using the T19 reparse guards. Connections are caller-owned, foreign-key enabled and FULL synchronous; DELETE journaling is required. Schema creation and each metadata write use BEGIN IMMEDIATE, explicit commit and rollback on every uncommitted exit. Application ID `0x44415331` and schema version 1 identify the database. Foreign/future or structurally changed databases are refused, with no automatic migration, schema repair, journal-mode conversion or deletion. SQLite authorizer denies ATTACH, DETACH and SQL load_extension; no native extension is loaded.

Four tables separate content objects, conversations, logical documents and conversation references. A content SHA256 uniquely identifies size/format metadata; mismatching metadata for the same hash is rejected. Documents and references receive server UUIDs. A null document owner means library; a non-null owner is the exclusive conversation. Shared content therefore does not grant shared membership. SQL foreign keys/unique constraints and triggers prevent cross-conversation attachment references, identity reassignment, duplicate membership and more than ten references. Existing same-library membership is returned before attempting another insertion. Separate logical attachments still consume distinct slots. Referenced rows use RESTRICT, not cascading deletion.

`Documents` exposes create_conversation, add_attachment, add_library_document, attach_library, references and resolve. Every read requires a conversation scope; resolving a reference does not offer an unscoped content-hash lookup. SQL values are bound parameters; the sole dynamic read-column choice is a fixed server-controlled Boolean branch. Writes and opening failures use safe StorageError codes without raw paths, hashes or SQLite exception values. The returned connection remains a trusted backend SQL interface; these controls do not authorize exposing arbitrary SQL to users.

Content metadata is assumed to have been verified by a later ingestion boundary. T20 performs no original-byte publication, actual deduplication of stored files, extraction, index creation, message storage, API idempotency ledger, quota reservation or deletion. The 100,000,000-byte metadata check and ten-reference bound reuse settled requirements, without claiming streaming upload/quota enforcement. Product startup/health is unchanged and does not open a product database; only explicit storage callers and tests create databases. Public writes remain gated on later validation/quota/idempotency integration.

## Verification evidence

Tests were written before implementation. Initial collection failed because app.storage did not exist. After implementation, 17 focused tests passed. Review added four checks; the missing-trigger test failed because version alone did not detect a damaged schema. Comparing the actual schema objects with the authored v1 definitions fixed that defect. All 21 focused tests then passed in 1.49 seconds.

Final regression command:

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp=data/t20-final --tb=short
.\.venv\Scripts\ruff.exe check app tests/test_project_setup.py tests/unit tests/integration
.\.venv\Scripts\ruff.exe format --check app tests/test_project_setup.py tests/unit tests/integration
```

Observed: **57 passed, 1 skipped, 1 warning in 7.80 seconds**; Ruff lint passed and all eleven Python files were formatted. The existing symlink test skips because this Windows session cannot create symlinks; the independent reparse-attribute rejection check passes. The warning remains Starlette's HTTPX test-client deprecation, without suppression or dependency changes.

The 21 new tests cover equal-byte attachment isolation, library sharing without implicit membership, duplicate library-reference reuse including at capacity, forbidden exclusive-to-library attachment, closed/reopened persistence and PRAGMAs, conflicting/invalid metadata, uniqueness/FKs, orphan-free failed writes, ten logical references over one content identity, parameterized scope lookups, explicit rollback, read-only failure, refused future/unrelated/damaged schemas and blocked SQL attachment/extension loading.

A separate Python child commits a conversation/reference, begins another transaction, inserts an uncommitted row and terminates with os._exit(23), without connection cleanup. Parent reopen finds the committed reference, no interrupted row, and integrity_check=ok. This exercises actual rollback-journal recovery, not an injected exception standing in for process termination. Fixtures are synthetic and stored only under ignored test roots. The regression suite also retains T19's two short-lived Python launcher checks; no model/native engine starts.

Review mutation inverted the conversation equality predicate in reference resolution. The isolation test failed because another conversation's reference became visible. The source was restored and verified byte-for-byte; no mutation remains. Existing correct-source regression results apply to those restored bytes. No extra successful suite rerun was used as reassurance.

## Review and remaining limits

Correctness/security review traced ownership checks through backend methods and database constraints. No cascade deletes, unscoped lookup, new outbound operation, extension load, user document or private payload log was introduced. Schema DDL is a small fixed tuple in the database module; no unused migrations framework, ORM or speculative lifecycle tables were added. The accepted architecture ADR records this schema mapping.

Filesystem guards do not confine hostile same-account replacement races. Schema refusal does not prove all existing data are uncorrupted, and one process-exit test is not power-loss durability or full recovery acceptance. Multi-process contention/performance and managed byte-growth/quota reservation remain unverified. Direct trusted connections can bypass repository behavior and must not be exposed to the browser. Read queries currently rely on the later API boundary to sanitize operational SQLite errors; opening/writes already use safe storage codes.

The user explicitly approved the reviewed nine-file T20 closeout and commit on 2026-11-20. SPEC, AGENTS, dependency/lock/ignore files, historical evaluation sources and session-checkpoint files remain unchanged. T21 has not started.
