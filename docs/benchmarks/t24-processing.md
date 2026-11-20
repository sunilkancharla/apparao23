# T24 — Batch upload and durable per-file status

Date: 2026-11-20 (Asia/Calcutta). The user instructed continuation after T23 commit `3dd27a1`, authorizing T24 in the approved sequence. Implementation used the repository incremental-implementation, test-driven-development, API/interface, quality/security and documentation workflows. No dependencies, downloads, model/OCR runs, private originals, historical evaluations or stage changes are included. The user explicitly approved the reviewed T24 closeout and twelve-file commit on 2026-11-20. T25 has not started.

## HTTP and state contract

The existing CSRF/Host/Origin boundary protects batch mutations. `POST /api/conversations/{id}/attachment-batches` accepts `Content-Type: application/json`, an `Idempotency-Key`, and `{ "files": ["a.csv", "b.csv"] }`. The UTF-8 JSON body is limited to 32,768 observed bytes, with declared-length checks too. This accommodates ten maximally escaped 255-character labels. Duplicate object keys, malformed/deeply invalid JSON, extra fields, non-string entries, content encodings and invalid IDs/keys are refused. A manifest contains one through ten entries; duplicate names remain distinct file intents.

Creation returns 202 with `data.operation_id` for the batch and ordered `data.files`, each with its own stable `operation_id`. Stream each file separately through the existing raw-body attachment route, adding `X-Batch-File-Id: <file operation_id>` and its own upload idempotency key. The display filename must match the manifest. No multipart/base64/archive transport or new parser dependency is introduced. Batch creation does not claim that document bytes have arrived or enqueue automatic heavy processing.

`GET /api/operations/{id}?conversation_id=<conversation UUID>` returns a no-store status snapshot for a batch, a batch file, or an actual T23 upload operation. Matching conversation scope is mandatory; unrelated/unknown operations return 404. Polling performs no cleanup, extraction, model work or file rehashing, and returns no private paths, hashes, document text, prompts or raw exception output. A stored-original status is historical upload progress, not a current physical-integrity certificate.

| File state | Meaning |
|---|---|
| `queued` | Valid manifest entry awaits admission/body transfer; no original/temporary bytes have been allocated |
| `processing` | A durable upload attempt is receiving, validating or promoting its original; `bytes_stored` remains null while unknown |
| `awaiting_extraction` | Original/reference publication committed; document/reference IDs and actual stored length are available |
| `failed` | Invalid manifest metadata, or a failed admitted attempt whose cleanup finished; a safe error code explains the failure |
| `interrupted` | Startup/cancellation cleanup finished for an interrupted attempt; it was not silently replayed |
| `cleanup_pending` | Cleanup remains unresolved; charges and the active-upload guard remain in place |

All current responses have `ready: false` and `indexed: false`. Successful files carry `EXTRACTION_PENDING`. A ready/indexed transition requires later actual extraction/index work; T24 does not invent readiness or a completion percentage. Batch snapshots include `total_files`, `originals_stored`, `failed_files` and each file result. They report active/queued states while work remains and `partial_failure` for a finished upload group with both stored and failed/interrupted files. A stored sibling is never rolled back because another file fails.

Unsafe display labels are omitted (`display_name: null`) with `INVALID_FILENAME`; safe unsupported names receive `UNSUPPORTED_FORMAT`. These are individual manifest failures, so valid siblings remain queued. A malformed manifest shape/count is rejected as a request. Pre-admission body-request refusals, such as unavailable temporary quota, leave the original file intent queued and report the refusal in HTTP; they do not fabricate a started/failed processing attempt. A bound over-limit declared file size is recorded as a failed attempt without reading its body.

## Persistence, capacity and retries

Schema v3 adds `upload_batches`, ordered `upload_batch_files` and safe `upload_failures`; exact v1/v2 schemas migrate transactionally while preserving earlier identities. Batch metadata, file rows and reference-slot reservations commit together. A deliberate duplicate-ID insert confirms that failure rolls back every manifest row.

Valid queued/in-flight file entries reserve conversation-reference slots. Admission counts actual references plus outstanding batch slots inside the same serialized SQLite write used by T23. Standalone uploads cannot take those slots. A claimed entry consumes its own reservation rather than counting twice; all ten same-byte files can finish as ten references over one physical original. Failed cleanup retains its slot; verified failure releases it. A retry after verified cleanup must reacquire capacity and cannot overrun another batch's reservations. Future library/public reference mutations must also respect these reservations; the T20 trusted metadata primitives are not public quota-admission interfaces.

Only one body/expensive upload is admitted at a time. Original and temporary byte reservations remain T23's per-attempt maximum, not ten concurrently allocated bodies. New batch creation is refused during active/unresolved upload work. The existing processed-data page ceiling and conservative rollback-journal envelope also cover these bounded metadata writes. All approved byte/count caps remain unchanged; no unbounded in-memory work queue, automatic pruning, eviction or model startup is added.

Batch idempotency compares a canonical ordered-name fingerprint and preserves operation IDs; replay returns current progress for those same intents. File attempts still compare actual bytes on completed replay. Changing payload, filename, scope or manifest binding conflicts/refuses before creating another reference. A successful or unresolved file cannot be attached again with a fresh key. After an attempt is known failed and cleanup verified, a deliberate new upload key may retry that same file ID; previous attempt records remain readable. Retrying an old failed key does not recreate its effect.

One startup pass reconciles the single active T23 attempt. If cleanup is locked or storage cannot complete it, safe metadata reads remain available, health reports `STORAGE_CLEANUP_PENDING`, and admission remains blocked by the durable active intent. Restoring access and restarting retries cleanup once. Successfully committed siblings and their scoped references survive. Unsubmitted queued entries retain their slots across restart; there is no automatic expiry or cancellation endpoint. General lifecycle/cancellation, retention maintenance and secure erasure are not selected by this task.

## Test evidence

Tests first failed on missing schema-v2 migration support, the absent operation/batch implementation and the absent HTTP routes. An initial capacity test showed a standalone upload taking a queued batch's reserved slot; shared transactional admission corrected it. A mixed-result test initially saw only `UPLOAD_FAILED`; durable safe failure codes now retain the actual `INVALID_CSV` reason. These failures preceded their implementation fixes.

The 28 new tests cover schema migration/reference preservation, queued/idempotent manifests, mixed unsafe/unsupported metadata, one/ten/eleven-entry boundaries, shared capacity, unrelated scope, original-stored status, processing observation with null progress, verified replay, failures/retries, invalid file binding, cleanup locks/restart, all-ten success, failed retry at capacity, oversized declared bodies, bounded/ambiguous JSON, CSRF and full metadata rollback. Pre-admission quota refusal is explicitly distinguished from a started attempt.

Two new Python children call `os._exit(23)`: one during a second file's receiving phase, the other after its publication commit and before response delivery. Reopen preserves the first committed sibling in both cases; it cleans/labels the interrupted second file or preserves its already committed original/reference. Both databases reopen with `integrity_check=ok`. Existing T23 publication-crash tests remain active.

The existing actual loopback smoke now creates a batch, submits valid/invalid siblings and polls `partial_failure`. Initial runs exposed a pre-existing T23 test startup-wait defect: it handled `ConnectError` but not `ConnectTimeout`. A host-permission retry reproduced the timeout, so it was not assumed to be sandbox-only. The test now handles both inside the same existing ten-second startup boundary, matching T19; response assertions are unchanged and the real API check passes. No test was skipped to hide the failure.

Review temporarily weakened shared slot refusal from `> 10` to `> 11`. The reserved-slot test failed as expected. The source was restored before final checks. Correctness, readability, architecture, security and resource review traced request bounds, parameterized scoped SQL, durable publication/cleanup, failure privacy and reference/byte accounting. No additional dependency or external document transport was adopted.

```powershell
$env:PYTEST_DISABLE_PLUGIN_AUTOLOAD = '1'
.\.venv\Scripts\python.exe -m pytest -q -rP -p no:cacheprovider
.\.venv\Scripts\ruff.exe check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration
.\.venv\Scripts\ruff.exe format --check app tests/test_project_setup.py tests/conftest.py tests/fixtures tests/unit tests/integration
git diff --check
```

Final suite: **209 passed, 1 skipped, 1 warning in 33.95 seconds**. The existing Windows symlink-permission skip and Starlette/HTTPX warning remain. Ruff lint/format passed (24 Python files). Shared final meter: **11/64 starts; 263,224/2,000,000 retained factory-artifact/child-output bytes**, within the 120-second admission/owned-child boundary. This includes the new crash children and existing controls/regressions; it is not a general native/model allocation or a meter for every temporary database byte. Fixtures remain small, authored and ignored; no real 100 MB or full-class-cap capacity benchmark was run.

## Reviewable change map and limits

| Before | After | Files |
|---|---|---|
| Single raw upload only | Bounded batch manifest, existing raw upload binding and scoped status endpoint | `app/main.py` |
| Schema v2 upload intents | Exact v1/v2→v3 migration, manifest/file/failure records | `app/storage/database.py` |
| No shared batch-slot accounting or durable status projection | Transactional reservations, idempotent manifests and safe per-file snapshots | `app/ingestion/processing.py`, `app/storage/files.py` |
| Only standalone API smoke | 28 batch/status tests, two real exit cases, expanded loopback smoke/startup wait fix | `tests/integration/test_processing_status.py`, `tests/integration/test_uploads.py` |
| T23 closeout current | T24 behavior, API details, review/evidence and approved closeout | README, PLAN, TODO, contracts, architecture ADR, this report |

T24 is the API/status layer for CSV originals, not normalized extraction, preview, embedding/index readiness, UI or complete Stage 1 acceptance. T25 and later pipeline work remain separately gated. No physical-16-GB, full-size throughput, general worker timeout, power-loss, strict disconnected-runtime or cancellation/lifecycle claim follows. Same-account hostile filesystem replacement and direct trusted-SQL bypass remain outside the supported browser boundary.

The user approved this twelve-file closeout and commit on 2026-11-20. Its scope excludes unrelated untracked files, generated uploads/databases, the ignored review patch, model assets, secrets and historical/session-summary/checkpoint files. A readable full diff is retained at `data/reviews/t24.diff`. Host `/status` and `/compact` commands are not exposed; neither was run. Durable progress is recorded in TODO/PLAN and this report.

Local Markdown link targets and tracked/new-file whitespace checks passed. All initial unrelated untracked files remain unchanged. Only closeout documentation changed after the final passing suite; no unchanged-code test rerun was used as reassurance.
